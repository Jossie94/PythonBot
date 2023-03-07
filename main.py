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
    url = "http://localhost:3862/api/Raids"
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


@client.command()
async def hru(ctx):
    ra = ["I am good, thank you for asking",
          "I am well. You, however, look unwell. Go outside.", "I was okay until I saw your outfit. Nasty.",
          "I might be a bot, but I am not interested.",
          "I was good until you asked. But you are not important enough to hate. Sit down.",
          "Why on earth would you ask a bot how's it doing?",
          "How am I? Who are you?"]
    await ctx.send(random.choice(ra))


# rude arraylist of 8ball
@client.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    resp = ["Definitely",
            "No.",
            "Yes.",
            "What kind of question is that?",
            "Are you sure you want the answer to that?",
            "Thats not a pretty face enough for me to make me answer your question",
            "Maybe.",
            "Absolutely not",
            "Obviously",
            "There is this lousy bot called Carl. Ask him.",
            "Yes queen"]
    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(resp)}')


# delete bulk of messages (requires administrator)
@client.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, amount: int):
    if amount > 50:
        amount = 50
    await ctx.channel.purge(limit=amount + 1)


# create a raid sign up
@client.command(aliases=['raid'])
# @commands.has_permissions(administrator=True)
async def timestamp(ctx, *, strinput):
    # url1 = "http://localhost:2386/api/Raids"

    # url2 = "http://localhost:2386/api/Raidusers"
    print(strinput)
    user = str(member)

    # utc = datetime.now(tzutc())
    # print('UTC TIME: ' + str(utc))

    # local = utc.astimezone(tzlocal())
    # print('Local TIME: ' + str(local))
    fmt = "%Y-%m-%d %H:%M %Z%z"

    # print(datetime.strptime(strinput, "%Y-%m-%dT%H:%M"))
    # stringformat = '{:%Y-%m-%d %H:%M:%S}'.format(strinput)

    botdate = datetime.strptime(strinput, "%Y-%m-%d %H:%M")

    # local = pytz.timezone("America/Los_Angeles")
    # local_dt = local.localize(botdate, is_dst=None)
    # utc_dt = local_dt.astimezone(pytz.utc)

    # print(utc_dt)

    select1 = Select(min_values=1, max_values=1, placeholder='Select raid', options=[
        discord.SelectOption(label="The Hiddenhoard of Abnankâra", value="Hiddenhoard of Abnankâra"),
        discord.SelectOption(label="Amdân Dammul", value="Amdân Dammul"),
        discord.SelectOption(label="The Fall of Khazadûm", value="Fall of Khazadûm"),
        discord.SelectOption(label="Remmorchant", value="Remmorchant")
    ],
                     custom_id="select1")
    select2 = Select(placeholder='Select tier', options=[
        discord.SelectOption(label="T1", value="t1"),
        discord.SelectOption(label="T2", value="t2"),
        discord.SelectOption(label="T3", value="t3"),
        discord.SelectOption(label="T4", value="t4"),
        discord.SelectOption(label="T5", value="t5")
    ],
                     custom_id="select2")

    button = Button(label="Submit", style=discord.ButtonStyle.green, custom_id="button1")

    async def my_callback1(interaction):  # callback method to select1

        if select1.custom_id == "select1":
            raid = select1.values[0]
            print(raid)
            await interaction.response.send_message(content=f"{select1.values[0]}")
            return raid

    async def my_callback2(interaction):  # callback method to select2

        if select2.custom_id == "select2":
            tiers = select2.values[0]
            print(tiers)
            await interaction.response.send_message(content=f"{select2.values[0]}")
            return tiers

    async def button_callback(interaction):
        if button.custom_id == "button1":
            raidselect = select1.values[0]
            tier = select2.values[0]

            # interaction.disabled = True

            url = "http://localhost:3862/api/Raids"

            post_data = {'raidname': raidselect,
                         'tier': tier,
                         'raiddate': strinput.replace(" ", "T"),
                         "raidusers": [
                             {
                                 "userDId": 0,
                                 "userDName": ctx.author.name

                             }
                         ]
                         },
            print(type(post_data))
            json_ob_tiba = json.dumps(post_data, indent=4, sort_keys=True, default=str)

            print(json_ob_tiba)

            response = requests.post(url, json=post_data[0])
            pass
            print(response.status_code)
            print(response.text)
            if response.status_code == 201:
                client.dispatch("custom_event", ctx, raidselect, tier, botdate)
            else:
                await ctx.send("Something went wrong. Contact Celladis")

    select1.callback = my_callback1
    select2.callback = my_callback2
    button.callback = button_callback

    view = View()
    view.add_item(select1)
    view.add_item(select2)
    view.add_item(button)

    await ctx.send(view=view)

    # await interaction.send(content=f"{raidselect}, {tier}, {botdate} submitted")

    # make a try catch with no API connection if possible


# result of raid sign up and users can sign up with emojis
@client.event
async def on_custom_event(ctx, raidselect, tier, botdate):
    # userstr = str(payload.member)
    embeds = discord.Embed(title=f"{raidselect}",
                           # timestamp=botdate.datetime.utcnow(),
                           color=discord.Color.dark_green())
    # embeds.add_field(name="Raid", value=f"{raidselect}")
    embeds.add_field(name="Date", value=f"{botdate}")
    embeds.add_field(name="Tier", value=f"{tier}")
    embeds.add_field(name="Leader", value=f"{ctx.author.name}")

    embededit = discord.Embed(title=f"Signup",
                              color=discord.Color.dark_green())
    embededit.add_field(name="Player:", value=f"")
    msg = await ctx.send(embed=embeds)
    while True:
        reaction, user = await client.wait_for("reaction_add",
                                               check=lambda reaction, user: reaction.message.id == msg.id)
        # embededit #finish your line Josefine.....


# if on_raw_reaction_add:
# print(f"reacted")
@client.event
async def on_reaction_add(reaction, user):
    print(f"You reacted with {reaction.emoji} {user}")
    url = "http://localhost:3862/api/Raidusers"

    userD = str(user)

    get_response = requests.get(url)
    print(get_response.text)

    post_data = {

        "userDName": userD

    }

    print(type(post_data))
    json_ob_tiba = json.dumps(post_data, indent=4, sort_keys=True, default=str)

    print(json_ob_tiba)  # random json name. It prints json objects in the console

    response = requests.post(url, json=post_data)

    # client.dispatch("custom_event", userD)
    print(response.status_code)
    print(response.text)

client.run(os.getenv('TOKEN2'))
