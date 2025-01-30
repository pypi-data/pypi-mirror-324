from __future__ import annotations

import re
from typing import Any, Callable, Sequence

from cachetools import TTLCache
from kafka import KafkaClient
from kafka.admin import KafkaAdminClient as KafkaPythonLibraryAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

from buz.kafka.domain.exceptions.topic_already_created_exception import KafkaTopicsAlreadyCreatedException
from buz.kafka.domain.models.create_kafka_topic import CreateKafkaTopic
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.services.kafka_admin_client import KafkaAdminClient

INTERNAL_KAFKA_TOPICS = {"__consumer_offsets", "_schema"}


class KafkaPythonAdminClient(KafkaAdminClient):
    __PYTHON_KAFKA_DUPLICATED_TOPIC_ERROR_CODE = 36

    def __init__(
        self,
        *,
        config: KafkaConnectionConfig,
        cache_ttl_seconds: int = 0,
    ):
        self._config = config
        self._config_in_library_format = self.__get_kafka_config_in_library_format(config)
        self._kafka_admin = KafkaPythonLibraryAdminClient(**self._config_in_library_format)
        self._kafka_client = KafkaClient(**self._config_in_library_format)
        self.__ttl_cache: TTLCache[str, Any] = TTLCache(maxsize=1, ttl=cache_ttl_seconds)

    def __get_kafka_config_in_library_format(self, config: KafkaConnectionConfig) -> dict:
        return {
            "client_id": config.client_id,
            "bootstrap_servers": config.bootstrap_servers,
            "security_protocol": config.credentials.security_protocol.value,
            "sasl_mechanism": config.credentials.sasl_mechanism.value if config.credentials.sasl_mechanism else None,
            "sasl_plain_username": config.credentials.user,
            "sasl_plain_password": config.credentials.password,
        }

    def create_topics(
        self,
        *,
        topics: Sequence[CreateKafkaTopic],
    ) -> None:
        new_topics = [
            NewTopic(
                name=topic.name,
                num_partitions=topic.partitions,
                replication_factor=topic.replication_factor,
                topic_configs=topic.configs,
            )
            for topic in topics
        ]

        try:
            self._kafka_admin.create_topics(new_topics=new_topics)
        except TopicAlreadyExistsError as error:
            topic_names = self.__get_list_of_kafka_topics_from_topic_already_exists_error(error)
            raise KafkaTopicsAlreadyCreatedException(topic_names=topic_names)

    def __get_list_of_kafka_topics_from_topic_already_exists_error(self, error: TopicAlreadyExistsError) -> list[str]:
        message = str(error)
        response_message = re.search(r"topic_errors=\[.*?]", message)
        topic_messages = re.findall(
            r"topic='[^']*', error_code=" + str(self.__PYTHON_KAFKA_DUPLICATED_TOPIC_ERROR_CODE), response_message[0]  # type: ignore
        )

        return [re.search("'.*'", topic_message)[0].strip("'") for topic_message in topic_messages]  # type: ignore

    def is_topic_created(
        self,
        topic: str,
    ) -> bool:
        topics = self.get_topics()
        return topic in topics

    def get_topics(
        self,
    ) -> set[str]:
        return self.__resolve_cached_property(
            "topics", lambda: set(self._kafka_admin.list_topics()) - INTERNAL_KAFKA_TOPICS
        )

    def __resolve_cached_property(self, property_key: str, callback: Callable) -> Any:
        value = self.__ttl_cache.get(property_key)
        if value is not None:
            return value
        value = callback()
        self.__ttl_cache[property_key] = value
        return value

    def delete_topics(
        self,
        *,
        topics: set[str],
    ) -> None:
        self._kafka_admin.delete_topics(
            topics=topics,
        )

    def delete_subscription_groups(
        self,
        *,
        subscription_groups: set[str],
    ) -> None:
        self._kafka_admin.delete_consumer_groups(
            group_ids=subscription_groups,
        )

    def get_subscription_groups(
        self,
    ) -> set[str]:
        return set(self._kafka_admin.list_consumer_groups())

    def _wait_for_cluster_update(self) -> None:
        future = self._kafka_client.cluster.request_update()
        self._kafka_client.poll(future=future)
