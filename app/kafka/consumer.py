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
        self._running = False

    async def start(self, broadcast) -> None:
        async with self._lock:
            if self._running:
                return
            self._running = True
            self._task = asyncio.create_task(self._run(broadcast))

    async def _run(self, broadcast):
        print("🟡 Kafka consumer runner started")

        while self._running:
            try:
                if (
                    not settings.KAFKA_BROKER_URL
                    or not settings.KAFKA_TOPIC
                    or not settings.KAFKA_CONSUMER_ID
                ):
                    raise RuntimeError(
                        "Kafka consumer settings are not properly configured."
                    )
                print("🟡 Trying to start Kafka consumer...")

                self._consumer = AIOKafkaConsumer(
                    settings.KAFKA_TOPIC,
                    bootstrap_servers=settings.KAFKA_BROKER_URL,
                    group_id=settings.KAFKA_CONSUMER_ID,
                    auto_offset_reset="earliest",
                    enable_auto_commit=False,
                    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                )

                await self._consumer.start()
                print("🟢 Kafka consumer started")
                print("🟢 Consumer loop started")

                async for msg in self._consumer:
                    print("🟢 Message received from Kafka:", msg.value)

                    await broadcast(msg.value)

                    # ✅ commit only after successful processing
                    await self._consumer.commit()

            except asyncio.CancelledError:
                break

            except Exception as e:
                print("🔴 Kafka consumer error:", e)

                if self._consumer:
                    with contextlib.suppress(Exception):
                        await self._consumer.stop()
                    self._consumer = None

                print("🟡 Retrying Kafka consumer in 3 seconds...")
                await asyncio.sleep(3)

        print("🛑 Kafka consumer runner stopped")

    async def stop(self) -> None:
        async with self._lock:
            self._running = False

            if self._task:
                self._task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await self._task

            if self._consumer:
                await self._consumer.stop()

            self._task = None
            self._consumer = None
