import discord
import openai

DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
openai.api_key = OPENAI_API_KEY

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        user_input = message.content[6:]
        if not user_input:
            await message.channel.send("Type something after !chat")
            return

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        ai_reply = response.choices[0].message.content
        await message.channel.send(ai_reply)

client.run(DISCORD_TOKEN)
