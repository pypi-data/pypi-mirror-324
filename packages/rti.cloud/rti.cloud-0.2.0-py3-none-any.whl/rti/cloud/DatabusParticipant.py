import time
import rti.connextdds as dds
import asyncio
from typing import Optional, Tuple, List, Union, Callable


class DiscoveryService:
    def __init__(self, participant, verbose=False):
        self._types = {}
        self._verbose = verbose
        self._participant = participant
        self._start()

    def _start(self):
        types = self._types
        verbose = self._verbose

        class Listener(dds.SubscriptionBuiltinTopicData.NoOpDataReaderListener):
            def __init__(self, participant: dds.DomainParticipant):
                super().__init__()

                self._participant = participant

            def on_data_available(
                self, reader: dds.SubscriptionBuiltinTopicData.DataReader
            ):
                samples = reader.select().state(dds.DataState.new_instance).take()
                for sample in filter(lambda s: s.info.valid, samples):
                    data: dds.SubscriptionBuiltinTopicData = sample.data
                    types[data.topic_name] = (data.type_name, data.type)
                    if verbose:
                        ps = (
                            participant_data
                            for disc_part in self._participant.discovered_participants()
                            if (
                                participant_data := self._participant.discovered_participant_data(
                                    disc_part
                                )
                            ).key
                            == data.participant_key
                        )

                        pdata: dds.ParticipantBuiltinTopicData = next(ps)
                        hostname = pdata.property["dds.sys_info.hostname"]
                        print(
                            f"* [{time.strftime('%H:%M:%S')}] Discovered topic ({hostname}): {data.topic_name}"
                        )

        self._participant.subscription_reader.set_listener(
            Listener(self._participant), dds.StatusMask.DATA_AVAILABLE
        )

    def get_type(self, topic_name: str) -> Optional[Tuple[str, dds.DynamicType]]:
        return self._types.get(topic_name)

    def get_topics(self) -> List[str]:
        return list(self._types.keys())

    def wait_for_topic(
        self, topic_name: str, timeout: float = 10
    ) -> Optional[Tuple[str, dds.DynamicType]]:
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            if topic_name in self._types:
                return self._types[topic_name]
            time.sleep(0.1)

        if self._verbose:
            print(
                f"* [{time.strftime('%H:%M:%S')}] Timeout waiting for topic {topic_name}"
            )
            print(
                f"  - discovered participants: {len(self._participant.discovered_participants())}"
            )

            for disc_part in self._participant.discovered_participants():
                pdata = self._participant.discovered_participant_data(disc_part)
                hostname = pdata.property["dds.sys_info.hostname"]
                print(f"    - {hostname}")

            print(f"  - discovered topics: {len(self.get_topics())}")
        return None

    def wait_for_subscriber(self, writer: dds.DataWriter, timeout: float = 10) -> bool:
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            if len(writer.matched_subscriptions) > 0:
                return True
            time.sleep(0.1)

        if self._verbose:
            print(f"* [{time.strftime('%H:%M:%S')}] Timeout waiting for participant")
        return False


class DatabusParticipant:
    def __init__(self, qos_file: Optional[str] = None, verbose: bool = False) -> None:
        self._verbose = verbose
        self._waitset = dds.WaitSet()
        self._subscriptions = []
        self._qos_provider = (
            dds.QosProvider(qos_file) if qos_file else dds.QosProvider.default
        )

        self._create_participant()
        self._discovery_service = DiscoveryService(self.participant, verbose)
        self._start()

    def subscribe(
        self,
        topic_name: str,
        callback: Optional[Callable[[dds.DynamicData], None]] = None,
    ) -> dds.DynamicData.DataReader:
        type_info = self._discovery_service.wait_for_topic(topic_name, 1000)
        if not type_info:
            return None

        topic = dds.DynamicData.Topic(self.participant, topic_name, type_info[1])
        reader = dds.DynamicData.DataReader(
            topic, qos=self._qos_provider.datareader_qos
        )
        if self._verbose:
            print(f"* [{time.strftime('%H:%M:%S')}] Subscribing to topic", topic_name)

        if callback:
            self._subscriptions.append((reader, callback))

        return reader

    def publish(
        self, topic_name: str, type: Optional[type] = None
    ) -> Union[dds.DataWriter, dds.DynamicData.DataWriter, None]:
        """Creates a DataWriter to publish the given topic.

        If the type is specified, a `dds.DataWriter` for that topic and type is
        immediately created and returned. Otherwise, this function waits until
        the topic and its type are discovered. If the topic is discovered
        before the timeout, it returns a `dds.DynamicData.DataWriter` for the
        discovered topic and its type.

        The `type` argument must be a class decorated with `rti.types.struct`
        or `rti.types.union` or `None`.
        """

        if type is None:
            type_info = self._discovery_service.wait_for_topic(topic_name, 10)
            if not type_info:
                return None
            type = type_info[1]

            topic = dds.DynamicData.Topic(self.participant, topic_name, type)
            writer = dds.DynamicData.DataWriter(
                topic, qos=self._qos_provider.datawriter_qos
            )

        else:
            topic = dds.Topic(self.participant, topic_name, type)
            writer = dds.DataWriter(topic, qos=self._qos_provider.datawriter_qos)
            if not self._discovery_service.wait_for_subscriber(writer, 10):
                return None

        if self._verbose:
            print(f"* [{time.strftime('%H:%M:%S')}] Publishing to topic", topic_name)

        return writer

    async def run(self):
        async def process_data(reader, callback):
            async for data in reader.take_data_async():
                callback(data)

        async def process_data_and_info(reader, callback):
            async for data, info in reader.take_async():
                callback(data, info)

        await asyncio.gather(
            *[
                (
                    process_data(reader, callback)
                    if self._num_args_in_callback(callback) == 1
                    else process_data_and_info(reader, callback)
                )
                for reader, callback in self._subscriptions
            ]
        )

    def _num_args_in_callback(self, callback) -> int:
        """Gets the number of input arguments in a function"""

        import inspect

        return len(inspect.signature(callback).parameters)

    def _create_participant(self) -> None:
        fqos = dds.DomainParticipantFactoryQos()
        fqos.entity_factory.autoenable_created_entities = False
        dds.DomainParticipant.participant_factory_qos = fqos
        self.participant = dds.DomainParticipant(
            domain_id=100, qos=self._qos_provider.participant_qos
        )
        initial_peers = ", ".join(self.participant.qos.discovery.initial_peers)
        if "udpv4_wan" not in initial_peers:
            print(
                "WARNING: initial_peers does not contain udpv4_wan, did you specify the correct QoS file?"
            )

        if self._verbose:
            print(f"* [{time.strftime('%H:%M:%S')}] Connecting to: ", initial_peers)

    def _start(self) -> None:
        self.participant.enable()
