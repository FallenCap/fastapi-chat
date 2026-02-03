from aiokafka import AIOKafkaProducer
import json
from app.core.config import Settings


async def get_producer() -> AIOKafkaProducer:
    if not Settings.KAFKA_BROKER_URL: 
        raise RuntimeError("Kafka producer settings are not properly configured.")

    producer = AIOKafkaProducer(
        bootstrap_servers=Settings.KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    await producer.start()
    return producer