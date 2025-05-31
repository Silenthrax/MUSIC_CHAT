import asyncio
import importlib
import logging

from pyrogram.sync import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from PIHUMUSIC import LOGGER, app, userbot
from PIHUMUSIC.core.call import PIHU
from PIHUMUSIC.misc import sudo
from PIHUMUSIC.plugins import ALL_MODULES
from PIHUMUSIC.utils.database import get_banned_users, get_gbanned
from PIHUMUSIC.utils.ssl_helper import set_exception_handler
from config import BANNED_USERS

# Set up exception handler for unhandled futures
set_exception_handler()

# Configure logging to suppress SSL warnings
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("aiohttp.client").setLevel(logging.ERROR)


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String Season Not Filled Fill Pyrogram season " \
        "string")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("PIHUMUSIC.plugins" + all_module)
    LOGGER("PIHUMUSIC.plugins").info("All Features Loaded Successfully 🥳...")
    await userbot.start()
    await PIHU.start()
    try:
        await PIHU.stream_call("https://envs.sh/7aQ.mp4")
    except NoActiveGroupCall:
        LOGGER("PIHUMUSIC").error(
            "Plz Start Your Log group Voicechat\\Channel\\n\\nMusic Bot Stop........"
        )
        exit()
    except:
        pass
    await PIHU.decorators()
    LOGGER("PIHUMUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎Made By Pihu☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("PIHUMUSIC").info("Stop Pihu Music 🎻 Bot..")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
