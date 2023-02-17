# from dateutil.tz import tzutc, tzlocal

from discord_components import DiscordComponents, Select, SelectOption, Button, ButtonStyle, interaction, ComponentsBot
import os
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
import discord
import discord.integrations
import requests

# @client.event

# async def on_ready():
#  print("The bot plan is online")

#client = discord.ext.commands.Bot("!")

#DiscordComponents(client)


# load_dotenv()
import bot


class PlanCog(commands.Cog):
    def __init__(self, bot):
        client = discord.ext.commands.Bot("!")
        load_dotenv()
        # self.bot = client
        DiscordComponents(client)
        self.bot = bot
        self.headers = {
            "Authorization": "Bot {0}".format(bot.token)
        }

    # load_dotenv()

    @commands.Cog.listener()
    async def on_custom_event(self, ctx, raidselect, tier, botdate, bot):
        embeds = discord.Embed(title="Raid:",
                               # timestamp=botdate.datetime.utcnow(),
                               color=discord.Color.dark_green())
        embeds.add_field(name="Raid", value=f"{raidselect}")
        embeds.add_field(name="Date", value=f"{botdate}")
        embeds.add_field(name="Tier", value=f"{tier}")

        await ctx.send(embed=embeds)

        def check(reaction, user):
            return user == ctx.message.author and reaction

        while True:
            reaction = await bot.wait_for("reaction_add", check=check)
            reactuser = {ctx.author.name}

            # await ctx.send(f"you reacted with: {reaction[0]}")
            print(ctx.author.name + f' has reacted with {reaction[0]}!')
            print(ctx.author.name + str({reaction}))
            print(reactuser)
        #  print("Button clicked")

        #  await ctx.send("React pls")

    @commands.command()
    async def selectraid(self, client, ctx):
        raid = await ctx.send(
            "Select raid and tier",
            components=[

                Select(
                    placeholder="Select something!",
                    options=[
                        SelectOption(label="The Hiddenhoard of Abnankâra", value="Hiddenhoard of Abnankâra"),
                        SelectOption(label="b", value="b"),
                    ],
                    custom_id="select1",
                ),
                Select(
                    placeholder="Tier",
                    options=[
                        SelectOption(label="T1", value="1")
                    ],
                    custom_id="select2",
                ),
                Button(label="Button", style=3, custom_id="button1"),
            ]
        )
        while True:
            selectinter = await client.wait_for("select_option")

            if selectinter.component.custom_id == "select1":
                raidselect = selectinter.values[0]
                await selectinter.send(content=f"{selectinter.values[0]} selected!")
                print(selectinter.values[0])

            if selectinter.component.custom_id == "select2":
                tier = selectinter.values[0]
                await selectinter.send(content=f"{selectinter.values[0]} selected!")
                print(selectinter.values[0])
                break

        interaction = await client.wait_for(
            "button_click", check=lambda inter: inter.custom_id == "button1"
        )

    # client.dispatch("custom_event", ctx, raidselect, tier)
    #  def astimezone(self, tz):
    #  if self.tzinfo is tz:
    #    return self
    # Convert self to UTC, and attach the new time zone object.
    # utc = (self - self.utcoffset()).replace(tzinfo=tz)
    # Convert from UTC to tz's local time.
    #  return tz.fromutc(utc)

    @commands.command(aliases=['raid'])
    async def timestamp(self, ctx, *, strinput):
        print(strinput)
        # utc = datetime.now(tzutc())
        # print('UTC TIME: ' + str(utc))

        # local = utc.astimezone(tzlocal())
        # print('Local TIME: ' + str(local))
        fmt = "%Y-%m-%d %H:%M %Z%z"

        # stringformat = '{:%Y-%m-%d %H:%M:%S}'.format(strinput)

        botdate = datetime.strptime(strinput, "%Y-%m-%d %H:%M")
        print(botdate.strftime(fmt))

        await ctx.send(botdate.strftime('%Y-%m-%d %H:%M'), components=[
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
            interaction = await bot.wait_for("select_option", check=lambda inter: inter.custom_id)

            if interaction.component.custom_id == "select1":
                raidselect = interaction.values[0]
                await interaction.send(content=f"{interaction.values[0]} selected!")
                print(interaction.values[0])

            if interaction.component.custom_id == "select2":
                tier = interaction.values[0]
                await interaction.send(content=f"{interaction.values[0]} selected!")
                print(interaction.values[0])
                break

        interaction = await client.wait_for(
            "button_click", check=lambda inter: inter.custom_id == "button1"
        )
        if interaction.component.custom_id:
            url = "http://localhost:2386/api/Raids"

            post_data = {'raidname': raidselect,
                         'tier': tier,
                         'raiddate': strinput.replace(" ", "T")}
        await interaction.send(content=f"{raidselect}, {tier}, {botdate} submitted")
        response = requests.post(url, json=post_data)
        print(response.status_code)
        client.dispatch("custom_event", ctx, raidselect, tier, botdate)


def setup(bot):
    bot.add_cog(PlanCog(bot))
    print("loaded plan cog")

# (os.getenv('TOKEN'))
#  await ctx.send(datetime.datetime.now().strftime('%d:%m:%Y'))

# print(datetime.datetime.now().strftime('%d:%m:%Y'))


# client.run(os.getenv('TOKEN'))
