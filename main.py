__author__ = 'smailzhu'
import asyncio
import logging
from configparser import ConfigParser

import coloredlogs
from telepot import Bot

from telepot.aio import DelegatorBot
from telepot.aio.delegate import create_open
from telepot.aio.loop import MessageLoop
from telepot.delegate import pave_event_space, per_inline_from_id

from inlineHandler import InlineHandler


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)

config = ConfigParser()
config.read('config.ini')
TOKEN = config.get('bot', 'token')

bot = DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=10),
])

me = Bot(TOKEN).getMe()
logger.info(me["first_name"]+' is Listening...')

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
loop.run_forever()

