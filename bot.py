import os
import discord
import requests
from dotenv import load_dotenv
import asyncio

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_ID = "gpt2"  # Using the stable, public GPT-2 model

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")
    activity = discord.Game(name="Type !chat followed by your message")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!chat "):
        prompt = message.content[6:]

        # Change activity to show bot is processing
        processing_activity = discord.Game(name="Generating response...")
        await client.change_presence(status=discord.Status.do_not_disturb, activity=processing_activity)

        payload = {"inputs": prompt}

        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{MODEL_ID}",
                headers=headers,
                json=payload,
                timeout=20,
            )
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get("error"):
                    reply = f"API error: {data['error']}"
                else:
                    reply = data[0]["generated_text"]
            elif response.status_code == 503:
                reply = "Model is loading, please try again in a moment."
            else:
                reply = f"HTTP error {response.status_code}"
        except Exception as e:
            reply = f"Request failed: {e}"

        await message.channel.send(reply[:1900])

        # Reset activity back to normal after response
        normal_activity = discord.Game(name="Type !chat followed by your message")
        await client.change_presence(status=discord.Status.online, activity=normal_activity)

client.run(DISCORD_TOKEN)
