#mmr-ちゃん
import os
import re
import requests
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('MMR_DISCORD_TOKEN')

client = commands.Bot(command_prefix='~')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="~mmr [username] for mmr"))
    print(f'{client.user} has connected to Discord!')

def parse_summary(summary):
    summary = summary.split("<br>", 1)[0]
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', summary)
    return cleantext

@client.command(name='mmr')
async def mmr_request(ctx):
    summonername = str(ctx.message.content)[5:]
    url = "https://na.whatismymmr.com/api/v1/summoner"
    r = requests.get(url, params={"name": summonername})
    json_data = r.json() if r and r.status_code == 200 else None
    avg = str(json_data["ranked"]["avg"])
    print(avg)
    if avg == "None":
        await ctx.send(summonername + " hasn't played any ranked games recently")
    else:
        response = "MMR: " + str(json_data["ranked"]["avg"]) + " ± " + str(json_data["ranked"]["err"]) +"\n" + parse_summary(json_data["ranked"]["summary"])
        await ctx.send(response)
client.run(TOKEN)