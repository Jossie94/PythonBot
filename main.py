import json
import os
import random
from datetime import datetime, time, timedelta

import discord
import discord.utils
import pytz
import requests
from discord import member
from discord.ext import commands

from discord.ui import Button, View, Select
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default().all()
client = commands.Bot(command_prefix="!", intents=intents)
server_id = 936515208573227032  # discord server id
channel_id = 936540455238254622  # test channel id
target_id = 936518781717598218  # test bot ID


@client.event
async def on_ready():
    print("The command bot is online")
    url = "http://localhost:2386/api/Raids"
    response = requests.get(url)

    if response.status_code == 200:
        print(response.status_code)
    else:
        print("Something is wrong with api")


client.run(os.getenv('TOKEN2'))