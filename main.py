# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from pyrogram import Client, filters


Bot = Client(
    "YouTube-Thumbnail-Downloader",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

Bot.run()
