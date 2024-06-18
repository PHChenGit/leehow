import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import aiohttp
import asyncio

from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from tabulate import tabulate
import pandas as pd

from db import get_users, insert_user
import json

async def getStats(session, username):
    print(f"getStats, user: {username}")
    url = f'https://leetcode-stats-api.herokuapp.com/{username}'
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            print(f"Received data for {username}: {data}")
            return data
        else:
            error_msg = f"Failed to fetch data for {username}, status code: {response.status}"
            print(error_msg)
            return {"error": error_msg}



class Slash(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        # name指令名稱，description指令敘述
        self.bot = bot

    @app_commands.command(name="board", description="Show leetcode leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                users = get_users()
                print(f"Users from DB: {users}")
                tmp = []
                for u in users:
                    user_data = await getStats(session, u)

                    if 'error' in user_data:
                        await interaction.response.send_message(user_data['error'])
                        return

                    score = (
                        1 * user_data["easySolved"]
                        + 3 * user_data["mediumSolved"]
                        + 5 * user_data["hardSolved"]
                    )
                    tmp.append(
                        [
                            u,
                            f"{user_data['easySolved']} / {user_data['totalEasy']}",
                            f"{user_data['mediumSolved']} / {user_data['totalMedium']}",
                            f"{user_data['hardSolved']} / {user_data['totalHard']}",
                            f"{user_data['totalSolved']} / {user_data['totalQuestions']}",
                            score,
                        ]
                    )

                sorted_data = sorted(tmp, key=lambda x: x[-1], reverse=True)
                for idx, sublist in enumerate(sorted_data):
                    sublist.insert(0, idx + 1)

                table = tabulate(
                    sorted_data,
                    headers=["#", "Name", "easy", "medium", "hard", "total", "scores"],
                    tablefmt="pretty",
                )

                print(table)

                await interaction.response.send_message(f"```\n{table}\n```")
        except Exception as e:
            print(f"Error in leaderboard: {e}")
            await interaction.response.send_message(f"An error occurred: {e}")

    # @app_commands.describe(參數名稱 = 參數敘述)
    # 參數: 資料型態，可以限制使用者輸入的內容
    @app_commands.command(name="add", description="Add a friend")
    @app_commands.describe(name="leetcode name")
    async def add(self, interaction: discord.Interaction, name: str):
        try:
            users = get_users()
            print(f'users, {len(users)}')
            for user in users:
                print(f'{user}')
                if user == name:
                    await interaction.response.send_message(f"User: {name} already exists")
                    return

            print('ready insert user')
            insert_user(name)
            await interaction.response.send_message(f"{name} is added into db successfully")
        except Exception as e:
            print(f"Error: {e}")
            await interaction.response.send_message(f"An error occurred: {e}")



async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
