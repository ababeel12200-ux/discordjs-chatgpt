import discord
from discord.ext import commands
import requests
import os

DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')  # Set your bot token in environment variables

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Set bot activity status on ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    activity = discord.Game(name="Destinyfucks.com")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def chat(ctx, *, prompt):
    print(f"Chat command triggered with prompt: {prompt}")
    API_URL = "https://freegpt.one/api/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        async with ctx.typing():
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            print(f"API status code: {response.status_code}")
            if response.status_code == 200:
                res_json = response.json()
                text = res_json['choices'][0]['message']['content'].strip()
            else:
                text = f"API Error {response.status_code}: {response.text}"
    except Exception as e:
        print(f"Exception during API call: {e}")
        text = f"Error: {e}"

    await ctx.send(text)

# Optional: help command override if needed
@bot.command()
async def help(ctx):
    help_text = (
        "Use `!chat <your message>` to chat with the bot.
"
        "Example: `!chat Hello, how are you?`"
    )
    await ctx.send(help_text)

bot.run(DISCORD_BOT_TOKEN)
