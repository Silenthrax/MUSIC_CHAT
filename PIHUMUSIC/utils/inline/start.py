from pyrogram.types import InlineKeyboardButton
import config
from PIHUMUSIC import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT
            ),
        ],
    ]
    return buttons


def private_panel(_):
    # Fallback to tg://user if OWNER_USERNAME not available
    if hasattr(config, "OWNER_USERNAME") and config.OWNER_USERNAME:
        owner_url = f"https://t.me/{config.OWNER_USERNAME}"
    else:
        owner_url = f"tg://user?id={config.OWNER_ID}"

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_10"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_11"],
                url=owner_url
            ),
            InlineKeyboardButton(
                text=_["S_B_12"],
                callback_data="abot_cb"
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="ubot_cb"
            ),
        ],
    ]
    return buttons
