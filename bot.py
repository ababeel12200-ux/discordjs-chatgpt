import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("AI_API_KEY")

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
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        json_data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
            if response.status_code == 200:
                reply = response.json()['choices'][0]['message']['content']
            else:
                reply = f"OpenAI API error: {response.status_code}"
        except Exception as e:
            reply = f"Error communicating with OpenAI: {e}"

        await message.channel.send(reply)

client.run(TOKEN)
