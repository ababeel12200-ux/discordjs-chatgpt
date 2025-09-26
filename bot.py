import discord
from discord.ext import commands
from transformers import pipeline

# Initialize the text generation pipeline with a lightweight model
generator = pipeline('text-generation', model='gpt2')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, prompt):
    # Generate a response from the prompt
    response = generator(prompt, max_length=50)
    # Send back the generated text
    await ctx.send(response[0]['generated_text'])

# Run the bot with your Discord token (replace 'YOUR_BOT_TOKEN' with your actual token)
bot.run('YOUR_BOT_TOKEN')
