import discord
from discord.ext import commands
import requests
import os

# Get tokens from environment variables
HF_API_TOKEN = os.getenv('HF_API_TOKEN')  # Set this as your Railway variable for Hugging Face token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Set this as your Railway variable for Discord bot token

HF_MODEL = 'gpt2'  # Or whichever Hugging Face model you want to use

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, prompt):
    API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    data = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
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
