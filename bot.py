import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!ai '):
        prompt = message.content[4:]

        headers = {"Authorization": f"Bearer {AI_API_KEY}", "Content-Type": "application/json"}
        json_data = {"prompt": prompt}
        response = requests.post("https://api.your-ai-provider.com/your-ai-endpoint", headers=headers, json=json_data)

        if response.status_code == 200:
            reply = response.json().get("text", "No response from AI.")
        else:
            reply = "AI service error."

        await message.channel.send(reply)

client.run(TOKEN)
