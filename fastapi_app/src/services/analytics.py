from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from kafka import KafkaProducer

from db.kafka_client import get_kafka


class KafkaService:
    def __init__(self, kafka: KafkaProducer):
        self.kafka = kafka

    def put_film_progress(self, user_id: int, film_id: UUID, film_position_ms: int) -> None:
        self.kafka.send(
            topic="views",
            value={"film_position_ms": film_position_ms},
            key=f"{user_id}+{film_id}",
        )


@lru_cache
def get_kafka_service(
    kafka: KafkaProducer = Depends(get_kafka),
) -> KafkaService:
    return KafkaService(kafka)
