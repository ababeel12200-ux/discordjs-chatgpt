import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    activity = discord.Game(name="Type !ai to chat")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!ai '):
        prompt = message.content[4:]

        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt}

        api_url = "https://api-inference.huggingface.co/models/gpt2-xl"

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, dict) and "error" in result:
                    reply = f"Error from Hugging Face API: {result['error']}"
                else:
                    reply = result[0]['generated_text']
            else:
                reply = f"API error: {response.status_code}"
        except Exception as e:
            reply = f"Exception: {e}"

        await message.channel.send(reply[:1900])

client.run(TOKEN)
