# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import ytthumb
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

load_dotenv()

Bot = Client(
    "YouTube-Thumbnail-Downloader",
    bot_token = os.environ.get("BOT_TOKEN"),
    api_id = int(os.environ.get("API_ID")),
    api_hash = os.environ.get("API_HASH")
)

START_TEXT = """Hello {},
I am a simple youtube thumbnail downloader telegram bot.

- Send a youtube video link or video ID.
- I will send the thumbnail.
- You can also send youtube video link or video id with quality. ( like :- `rokGy0huYEA | sd`
  - sd - Standard Quality
  - mq - Medium Quality
  - hq - High Quality
  - maxres - Maximum Resolution
"""

BUTTON = [InlineKeyboardButton("Feedback", url='https://telegram.me/FayasNoushad')]

photo_buttons = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Other Qualities', callback_data='qualities')], BUTTON]
)

@Bot.on_callback_query()
async def cb_data(_, message):
    data = message.data.lower()
    if data == "qualities":
        await message.answer('Select a quality')
        buttons = []
        for quality in ytthumb.qualities():
            buttons.append(
                InlineKeyboardButton(
                    text=ytthumb.qualities()[quality],
                    callback_data=quality
                )
            )
        await message.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [[buttons[0], buttons[1]], [buttons[2], buttons[3]], BUTTON]
            )
        )
    if data == "back":
        await message.edit_message_reply_markup(photo_buttons)
    if data in ytthumb.qualities():
        thumbnail = ytthumb.thumbnail(
            video=message.message.reply_to_message.text,
            quality=message.data
        )
        await message.answer('Updating')
        await message.edit_message_media(
            media=InputMediaPhoto(media=thumbnail),
            reply_markup=photo_buttons
        )
        await message.answer('Updated Successfully')


@Bot.on_message(filters.private & filters.command(["start", "help"]))
async def start(_, message):
    await message.reply_text(
        text=START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([BUTTON]),
        quote=True
    )


@Bot.on_message(filters.private & filters.text)
async def send_thumbnail(bot, update):
    message = await update.reply_text(
        text="`Analysing...`",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        if " | " in update.text:
            video = update.text.split(" | ", -1)[0]
            quality = update.text.split(" | ", -1)[1]
        else:
            video = update.text
            quality = "sd"
        thumbnail = ytthumb.thumbnail(
            video=video,
            quality=quality
        )
        await update.reply_photo(
            photo=thumbnail,
            reply_markup=photo_buttons,
            quote=True
        )
        await message.delete()
    except Exception as error:
        await message.edit_text(
            text=error,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([BUTTON])
        )


Bot.run()
