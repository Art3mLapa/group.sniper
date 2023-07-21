import threading
import requests
import asyncio
import random
import time
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="~", intents=intents)

running = False
text_channel = None
proxy_list = []

with open('proxy_list.txt', 'r') as file:
    proxy_list = file.read().splitlines()

def get_random_proxy():
    return random.choice(proxy_list)

def groupfinder():
    while running:
            id = random.randint(1000000, 9999999)
            proxy = get_random_proxy()
            
            proxy_dict = {
                'https': proxy
            }
                
            re = requests.get(f"https://groups.roblox.com/v1/groups/{id}", proxies=proxy_dict)
            if 'isLocked' not in re.text and 'owner' in re.text:
                if re.json()['publicEntryAllowed'] and re.json()['owner'] == None:
                    embed = discord.Embed(
                       title="Group Hit coemzzz",
                       description=f"https://www.roblox.com/groups/group.aspx?gid={id}",
                       color=discord.Color.green()
                   )
                    bot.loop.create_task(send_message(embed))
                    print(f"[+] Hit: {id}")
                else:
                    print(f"[-] No Entry Allowed: {id}")
            else:
                print(f"[-] Group Locked/Already Owned: {id}")

async def send_message(embed):
    await text_channel.send(embed=embed)


@bot.event
async def on_ready():
    print("Bot is ready.")


@bot.command()
async def start_generation(ctx):
    global running
    global text_channel
    if not running:
        running = True
        text_channel = ctx.channel
        threading.Thread(target=groupfinder).start()
        await ctx.send("Group generation started.")
    else:
        await ctx.send("Group generation is already running.")


@bot.command()
async def stop_generation(ctx):
    global running
    if running:
        running = False
        await ctx.send("Group generation stopped.")
    else:
        await ctx.send("Group generation is not currently running.")

@bot.command()
async def status(ctx):
    status = "Active" if running else "Inactive"
    embed = discord.Embed(title="group.sniper. Settings", color=discord.Color.blue())
    embed.add_field(name="Running", value=status, inline=False)

bot.run("token")
