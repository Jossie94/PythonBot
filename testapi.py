import os

from datetime import datetime
import discord
import requests
from dateutil.tz import tzutc, tzlocal
from requests.adapters import HTTPAdapter
from discord_components import SelectOption, Select, Button, DiscordComponents
from dotenv import load_dotenv
from discord.ext import commands
import json
import pytz

bot = discord.ext.commands.Bot("!")
load_dotenv()
DiscordComponents(bot)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    response = requests.get("http://localhost:2386/api/Raids")
    print(response.status_code)


@bot.command(aliases=['raid'])
async def timestamp(ctx, *, strinput):
    print(strinput)
    # utc = datetime.now(tzutc())
    # print('UTC TIME: ' + str(utc))

    # local = utc.astimezone(tzlocal())
    # print('Local TIME: ' + str(local))
    fmt = "%Y-%m-%d %H:%M %Z%z"

    # print(datetime.strptime(strinput, "%Y-%m-%dT%H:%M"))
    # stringformat = '{:%Y-%m-%d %H:%M:%S}'.format(strinput)

    botdate = datetime.strptime(strinput, "%Y-%m-%d %H:%M")

    local = pytz.timezone("America/Los_Angeles")
    local_dt = local.localize(botdate, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    # print(type(botdate))

    await ctx.send(utc_dt.strftime('%Y-%m-%d %H:%M'), components=[
        Select(
            placeholder='Select raid',
            options=[
                SelectOption(label="The Hiddenhoard of Abnankâra", value="Hiddenhoard of Abnankâra"),
                SelectOption(label="Amdân Dammul", value="Amdân Dammul"),
                SelectOption(label="The Fall of Khazadûm", value="Fall of Khazadûm"),
                SelectOption(label="Remmorchant", value="Remmorchant")
            ],
            custom_id="select1",
        ),
        Select(
            placeholder='Select tier',
            options=[
                SelectOption(label="T1", value="t1"),
                SelectOption(label="T2", value="t2"),
                SelectOption(label="T3", value="t3"),
                SelectOption(label="T4", value="t4"),
                SelectOption(label="T5", value="t5")
            ],
            custom_id="select2",
        ),
        Button(label="Submit", style=3, custom_id="button1"),
    ]
                   )
    print(botdate)
    while True:
        selectinter = await bot.wait_for("select_option")

        if selectinter.component.custom_id == "select1":
            raidselect = selectinter.values[0]
            # await selectinter.send(content=f"{selectinter.values[0]} selected!")
            print(selectinter.values[0])

        if selectinter.component.custom_id == "select2":
            tier = selectinter.values[0]
            # await selectinter.send(content=f"{selectinter.values[0]} selected!")
            print(selectinter.values[0])
            break

    interaction = await bot.wait_for(
        "button_click", check=lambda inter: inter.custom_id == "button1"
    )
    if interaction.component.custom_id:
        url = "http://localhost:2386/api/Raids"

        post_data = {'raidname': raidselect,
                     'tier': tier,
                     'raiddate': strinput.replace(" ", "T")}
        # json_ob_tiba = json.dumps(post_data, indent=4, sort_keys=True, default=str)

        # print(json_ob_tiba)
        await interaction.send(content=f"{raidselect}, {tier}, {botdate} submitted")
        response = requests.post(url, json=post_data)
        print(response.status_code)
    # requests.post(url, data={key: value}, json={key: value}, args)


#bot.run(os.getenv('TOKEN'))
