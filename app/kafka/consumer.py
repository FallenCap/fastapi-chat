from aiokafka import AIOKafkaConsumer
import asyncio
import json
import contextlib
from app.core.config import settings


class KafkaConsumerService:
    def __init__(self):
        self._task: asyncio.Task | None = None
        self._consumer: AIOKafkaConsumer | None = None
        self._lock = asyncio.Lock()

    async def start(self, broadcast) -> None:
        async with self._lock:
            if (
                not settings.KAFKA_BROKER_URL
                or not settings.KAFKA_TOPIC
                or not settings.KAFKA_CONSUMER_ID
            ):
                raise RuntimeError(
                    "Kafka consumer settings are not properly configured."
                )

            # 🛑 Already running
            if self._task and not self._task.done():
                return

            # 🔁 Retry until Kafka is ready
            for attempt in range(10):
                try:
                    self._consumer = AIOKafkaConsumer(
                        settings.KAFKA_TOPIC,
                        bootstrap_servers=settings.KAFKA_BROKER_URL,
                        group_id=settings.KAFKA_CONSUMER_ID,
                        auto_offset_reset="latest",
                        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                    )

                    await self._consumer.start()
                    print("✅ Kafka consumer started")
                    break

                except Exception:
                    self._consumer = None
                    print(f"⏳ Kafka not ready (attempt {attempt + 1}/10)")
                    await asyncio.sleep(3)
            else:
                print("❌ Kafka unavailable, consumer not started")
                return

            async def consume_loop():
                try:
                    while True:
                        # 🛡️ Absolute guard
                        if not self._consumer:
                            break

                        async for msg in self._consumer:
                            await broadcast(msg.value)

                except asyncio.CancelledError:
                    pass

                finally:
                    if self._consumer:
                        await self._consumer.stop()
                        print("🛑 Kafka consumer stopped")

            self._task = asyncio.create_task(consume_loop())

    async def stop(self):
        async with self._lock:
            if not self._task:
                return

            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

            self._task = None
            self._consumer = None
