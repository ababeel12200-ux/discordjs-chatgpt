import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    activity = discord.Game(name="Type !ai to chat | Destinyfucks.com")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!ai "):
        prompt = message.content[4:]
        api_url = "https://api.g4f.dev/api/chat"  # Public GPT4Free endpoint (subject to availability)

        payload = {
            "prompt": prompt,
            "history": []
        }

        try:
            response = requests.post(api_url, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                reply = data.get("response", "No response from API.")
            else:
                reply = f"API error: {response.status_code}"
        except Exception as e:
            reply = f"Request error: {e}"

        await message.channel.send(reply)

client.run(TOKEN)
