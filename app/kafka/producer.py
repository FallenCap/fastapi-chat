from aiokafka import AIOKafkaProducer
import json
from typing import Optional
from app.core.config import settings

producer: Optional[AIOKafkaProducer] = None


async def start_producer() -> None:
    global producer

    if not settings.KAFKA_BROKER_URL or not settings.KAFKA_TOPIC:
        raise RuntimeError("Kafka producer settings are not properly configured.")

    if producer is not None:
        return  # already started

    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    await producer.start()
    print("✅ Kafka producer started")


async def stop_producer() -> None:
    global producer

    if producer is not None:
        await producer.stop()
        producer = None
        print("🛑 Kafka producer stopped")


async def publish_chat_message(payload: dict) -> None:
    if producer is None:
        raise RuntimeError("Kafka producer not started")

    await producer.send_and_wait(
        settings.KAFKA_TOPIC,
        payload,
    )
