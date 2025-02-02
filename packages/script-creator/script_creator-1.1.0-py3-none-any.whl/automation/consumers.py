
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

import asyncio
import subprocess

class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        logger.debug(f"WebSocket connection initiated for session_id: {self.session_id}")

        self.script_path = "C:/Temp/test.py"
        self.process = subprocess.Popen(
            ["python", "-u", self.script_path, self.session_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        await self.accept()
        asyncio.create_task(self.send_real_time_data())

    async def disconnect(self, close_code):
        logger.debug(f"WebSocket disconnected for session_id: {self.session_id}")
        if self.process and self.process.poll() is None:
            self.process.terminate()

    async def send_real_time_data(self):
        loop = asyncio.get_event_loop()
        try:
            while True:
                output = await loop.run_in_executor(None, self.process.stdout.readline)
                if not output:
                    break
                message = {"data": output.strip()}
                logger.debug(f"Sending WebSocket message: {message}")
                await self.send(text_data=json.dumps(message))
        except asyncio.CancelledError:
            logger.debug("WebSocket connection closed.")
        finally:
            if self.process.poll() is None:  #
                self.process.terminate()