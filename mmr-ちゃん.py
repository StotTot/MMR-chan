#mmr-ちゃん
import os
import re
import requests
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError

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

def get_summoner(summoner):
    api_key = os.getenv('TEMP_RIOT_KEY')
    watcher = LolWatcher(api_key)
    my_region = 'na1'
    me = watcher.summoner.by_name(my_region, summoner)
    return watcher.league.by_summoner(my_region, me['id'])


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
        print("______________________________________________________________________________________")
        print(summonername)
        about_summoner = get_summoner(summonername)
        index = -1
        for i in range(len(about_summoner)):
            if "RANKED_SOLO_5x5" in about_summoner[i]:
                index = 1
        soloduo = about_summoner[index]
        print(soloduo)
        print("______________________________________________________________________________________")
        response = "```\nSummoner: " + summonername + "\nTier: " + str(soloduo["tier"]) + " " +  str(soloduo["rank"]) + "\nLP: " + str(soloduo["leaguePoints"]) + "\nMMR: " + str(json_data["ranked"]["avg"]) + " ± " + str(json_data["ranked"]["err"]) +"\n" + parse_summary(json_data["ranked"]["summary"]) + "\nWin rate: " + str(round(100 * (soloduo["wins"]/(soloduo["wins"] + soloduo["losses"])), 2)) + "%\n```"
        await ctx.send(response)
client.run(TOKEN)