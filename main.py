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


@client.command(name="ping")
async def test_ping(ctx):
    correct_response = 'Pong!'
    channel = await client.fetch_channel(channel_id)
    await channel.send(correct_response)
    guild = client.get_guild(server_id)
    for member in guild.members:
        print(member.name)

    def check(m):
        return m.content == correct_response and m.author.id == target_id

    response = await client.wait_for('message', check=check)
    assert (response.content == correct_response)


@client.command(name='hello', aliases=['hi'], pass_context=True)
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}")


@client.command(name='Eldo')
@commands.has_permissions(administrator=True)
async def Eldo(ctx):
    eld = "142962988523978752"
    await ctx.send(f"Hi <@{eld}>")


# manual help command
@client.command()
async def helpcarla(ctx):
    embeds = discord.Embed(title="Commands",
                           description="Carlas commands",
                           color=discord.Color.blue())
    embeds.add_field(name="!hello", value="Answers back with your discord name")
    embeds.add_field(name="!purge x", value="Delete bulk of messages. Only officers can use it/have admin rights")
    embeds.add_field(name="!hru", value="Random answers back from bot", inline=False)
    embeds.add_field(name="!timestamp or !raid <yyyy-mm-dd hh:mm>",
                     value="Registers date, time and gives choice of raid and tier")
    embeds.add_field(name="!8ball <question>", value="You ask preferably a yes or no question. Carla answer back")

    await ctx.send(embed=embeds)


client.run(os.getenv('TOKEN2'))
