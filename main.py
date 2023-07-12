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

def groupfinder():
    while running:
        if proxies:
            proxy = random.choice(proxies)
            id = random.randint(1000000, 9999999)
            start_time = time.time()
            r = requests.get(f"https://www.roblox.com/groups/group.aspx?gid={id}")
            end_time = time.time()
            if 'owned' not in r.text:
                re = requests.get(f"https://groups.roblox.com/v1/groups/{id}")
                if 'isLocked' not in re.text and 'owner' in re.text:
                    if re.json()['publicEntryAllowed'] and re.json()['owner'] == None:
                        embed = discord.Embed(title="Group Hit",
                                              description=f"https://www.roblox.com/groups/group.aspx?gid={id}",
                                              color=discord.Color.green())
                        bot.loop.create_task(send_message(embed))  # Send message to text channel
                        print(f"[+] Hit: {id}")
                    else:
                        print(f"[-] No Entry Allowed: {id}")
                else:
                    print(f"[-] Group Locked: {id}")
            else:
                print(f"[-] Group Already Owned: {id}")

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
async def settings(ctx):
    global running
    global proxy
    global proxy_speed
    status = "Active" if running else "Inactive"
    embed = discord.Embed(title="Bot Settings", color=discord.Color.blue())
    embed.add_field(name="Running", value=status, inline=False)
    await ctx.send(embed=embed)

bot.run("token")
