from discord_components import DiscordComponents
from dotenv import load_dotenv
from discord.ext import commands
import locale
from datetime import datetime
import discord
from discord.ext import commands
from itertools import compress
import gettext
import json
import logging
import os
import re
import testapi


# load_dotenv()


bot = discord.ext.commands.Bot("!")


# DiscordComponents(client)

class Bot(commands.Bot):
    def __init__(self):
        self.Bot = Bot
        self.token = None
        self.launch_time = datetime.utcnow()

        super().__init__(command_prefix=self.prefix_manager)

    def prefix_manager(self, bot, message):
        return commands.when_mentioned_or("!")(bot, message)

    @bot.event
    async def on_ready(self):
        print("The botbot is online")
        self.load_extension('PurgeClear')
        self.load_extension('PlainRaid')
        self.token = os.getenv('TOKEN2')


        #self.load_extension('dummy')



    # await

#  dumb = dummy.dumb()

# PurgeClear.client()


#  await client.load_extension('dummy')


# bot.run(os.getenv('TOKEN'))
# self.token = read_config_key(config, 'BOT_TOKEN', True)