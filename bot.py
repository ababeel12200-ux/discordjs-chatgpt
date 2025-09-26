import discord
from discord.ext import commands
import requests
import os

DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')  # Discord bot token from environment

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, prompt):
    API_URL = "https://api.pawan.krd/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        # No authorization needed for this proxy
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        res_json = response.json()
        try:
            text = res_json['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError):
            text = "Sorry, I couldn't generate a response."
    else:
        text = f"API Error {response.status_code}: {response.text}"

    await ctx.send(text)

bot.run(DISCORD_BOT_TOKEN)
