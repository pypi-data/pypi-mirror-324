import asyncio
import code
import json
import logging
from dataclasses import asdict, dataclass
from time import time
from typing import IO, Optional, Union
from unittest.mock import patch

import fakeredis

logging.basicConfig(level=logging.INFO)
import onchebot
from onchebot.bot import Bot
from onchebot.models import Message

bot_type_id = "tetris"
posted_msgs = []
topic_id = -1
username = "Connard"


@dataclass
class PostedMessage:
    content: str
    answer_to: Optional[int]


redis_client = fakeredis.FakeRedis(decode_responses=True)


class OncheConsole(code.InteractiveConsole):
    def __init__(self, environment=None):
        # Initialize with a custom environment (defaults to an empty dictionary)
        self.environment = environment or {}
        super().__init__(locals=self.environment)
        self.autoloop: Optional[str] = None

    async def init(self):
        self.bot = await Bot.create("__console", bot_type_id, topic_id, username)

    async def process_msg(self, msg: Message):
        await onchebot.redis_client.r.xadd(
            name="topics:" + str(topic_id), fields={"msg": json.dumps(asdict(msg))}
        )
        await onchebot.consumer.consume_once()
        if self.autoloop:
            await self.bot.run_task_once(self.autoloop)

    def push(self, line):
        global bot_type_id, username
        """Override to customize input handling."""
        if line.strip().startswith("SETBOTTYPE"):
            bot_type_id = line.strip().split(" ")[1]
            print(bot_type_id)
            return

        if line.strip().startswith("AUTOTASK"):
            loop_id = line.strip().split(" ")[1]
            self.autoloop = loop_id
            return

        if line.strip().startswith("TASK"):
            loop_id = line.strip().split(" ")[1]
            asyncio.run(self.bot.run_loop_once(loop_id))
            return

        if line.strip().startswith("STATE"):
            print(json.dumps(self.bot.state, indent=2))
            return

        if line.strip().startswith("SETUSER"):
            username = line.strip().split(" ")[1]
            return

        try:
            content = line
            msg = Message(
                id=-1,
                answer_to=None,
                stickers=[],
                mentions=[],
                content_html=content,
                content_without_stickers=content,
                content=content,
                username=username,
                timestamp=int(time()),
                topic_id=-1,
            )
            asyncio.run(self.process_msg(msg))
        except Exception as e:
            print(f"Error: {e}")

    def showtraceback(self):
        """Override to customize the traceback display."""
        print("Oops! Something went wrong.")
        super().showtraceback()

    def write(self, data):
        """Override to customize output handling."""
        print(f"Output: {data.strip()}")


def post_msg(content: str, answer_to: Optional[int] = None):
    posted_msgs.append(PostedMessage(content=content, answer_to=answer_to))
    print(content)


def upload_img(data: Union[IO, bytes, str], filename: str, content_type: str):
    print(f"{filename} uploaded")
    return f"mock-image-id-{filename}"


@patch("onchebot.redis_client.r", redis_client)
@patch("onchebot.redis_client.setup", side_effect=lambda: None)
@patch("onchebot.bot.Bot.post_message", side_effect=post_msg)
@patch("onchebot.bot.Bot.upload_image", side_effect=upload_img)
async def start(type_id: str, A, B, C):
    global bot_type_id
    bot_type_id = type_id
    onchebot.setup(
        bot_username="Bot",
        bot_password="",
        admin_username="Admin",
    )
    console = OncheConsole()
    await console.init()
    console.interact(
        "Ceci est un environement de test pour un bot, qui ne poste pas sur onche.org.\nChaque message est interpréter comme un message onche et est envoyé au bot.\n\n"
        + f"BOT TYPE: {bot_type_id}\n\n"
        + 'Change de bot avec SETBOTTYPE le_bot_type_id (exemple: "SETBOTTYPE tetris")'
    )
    return console


if __name__ == "__main__":
    asyncio.run(start("pingpong"))
