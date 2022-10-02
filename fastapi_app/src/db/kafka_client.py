from kafka import KafkaProducer

kafka: KafkaProducer | None = None


async def get_kafka() -> KafkaProducer:
    return kafka
