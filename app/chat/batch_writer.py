import asyncio
from typing import List
from app.db.database import chat_collection


class ChatBatchWriter:
    def __init__(self, batch_size: int = 1, flush_interval: int = 2):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.buffer: List[dict] = []
        self._lock = asyncio.Lock()
        self._task: asyncio.Task | None = None
        self._running = False

    async def start(self):
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._flush_loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        await self.flush()

    async def add(self, message: dict):
        async with self._lock:
            self.buffer.append(message)
            if len(self.buffer) >= self.batch_size:
                await self.flush()

    async def flush(self):
        async with self._lock:
            if not self.buffer:
                return

            batch = self.buffer
            self.buffer = []
            
        # TODO: Bulk insert
        await chat_collection.insert_many(batch)
        print(f"💾 Inserted {len(batch)} chat messages")

    async def _flush_loop(self):
        while self._running:
            await asyncio.sleep(self.flush_interval)
            await self.flush()


batch_writer = ChatBatchWriter()
