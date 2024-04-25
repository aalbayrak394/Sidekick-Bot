import os
import discord
from dotenv import load_dotenv
from blogger_api import BloggerAPI
import time

load_dotenv()

api = BloggerAPI()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("sidekick is in " + str(guild_count) + " guilds.")
    
    while True:
        await send_new_posts()
        time.sleep(300)


async def send_new_posts():
    channel = bot.get_channel(int('CHANNEL_ID'))
    new_posts = api.get_new_posts()
    for post in new_posts:
        if channel:
            await channel.send(f"New blog post: **{post['title']}**\n{post['url']}")
        else:
            print('Failed to find channel with ID:')


if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)