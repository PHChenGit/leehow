import os
from typing import Final
import asyncio
import requests
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
import logging
import logging.handlers

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready() -> None:
    slash = await bot.tree.sync()
    print(f'{client.user} is now running!\n')
    print(f"Loaded {len(slash)} slash commands\n")

# 載入指令程式檔案
@bot.command()
async def load(ctx: commands.Context, extension):
    print(f"load {extension}")
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# 卸載指令檔案
@bot.command()
async def unload(ctx: commands.Context, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

# 重新載入程式檔案
@bot.command()
async def reload(ctx: commands.Context, extension):
    await ctx.send("reloading")
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main() -> None:
    async with bot:
       await load_extensions()
       await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
