import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    activity = discord.Game(name="Chat on politics, world events, more! Type !chat")
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!chat "):
        prompt = message.content[6:]

        system_prompt = (
            "You are an expert commentator on politics, world affairs, and current events. | Destinyfucks.com "
            "Give insightful, honest, and well-informed responses."
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.7,
            )
            reply = response['choices'][0]['message']['content']
        except Exception as e:
            reply = f"OpenAI API error: {e}"

        await message.channel.send(reply[:1900])

client.run(DISCORD_TOKEN)
