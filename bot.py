import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_ID = "microsoft/DialoGPT-large"  # Change if you want

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

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

    if message.content.startswith("!d "):
        prompt = message.content[6:]

        payload = {"inputs": prompt}
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_ID}",
            headers=headers,
            json=payload,
            timeout=20,
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'error' in data:
                reply = f"API error: {data['error']}"
            else:
                reply = data[0]["generated_text"]
        else:
            reply = f"HTTP error {response.status_code}"

        await message.channel.send(reply)

client.run(TOKEN)
