from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Sequence

from buz.kafka.domain.models.create_kafka_topic import CreateKafkaTopic

DEFAULT_NUMBER_OF_MESSAGES_TO_POLLING = 999


class KafkaAdminClient(ABC):
    @abstractmethod
    def create_topics(
        self,
        *,
        topics: Sequence[CreateKafkaTopic],
    ) -> None:
        pass

    @abstractmethod
    def is_topic_created(
        self,
        topic: str,
    ) -> bool:
        pass

    @abstractmethod
    def delete_topics(
        self,
        *,
        topics: set[str],
    ) -> None:
        pass

    @abstractmethod
    def get_topics(
        self,
    ) -> set[str]:
        pass
