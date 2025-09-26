import discord
from discord.ext import commands
import requests
import os

HF_API_TOKEN = os.getenv('HF_API_TOKEN')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_TOKEN')  # changed this line to match your env variable

print(f"HF_API_TOKEN set: {HF_API_TOKEN is not None}")
print(f"DISCORD_BOT_TOKEN set: {DISCORD_BOT_TOKEN is not None}")

HF_MODEL = 'gpt2'
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, prompt):
    API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    data = {"inputs": prompt, "options": {"wait_for_model": True}}
    response = requests.post(API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        generated = response.json()
        if isinstance(generated, list) and 'generated_text' in generated[0]:
           text = generated[0]['generated_text']
        else:
           text = "Sorry, I couldn't generate a response."
    else:
        text = f"API Error {response.status_code}: {response.text}"
    await ctx.send(text)

bot.run(DISCORD_BOT_TOKEN)
