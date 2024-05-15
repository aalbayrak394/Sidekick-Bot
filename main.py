import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
from blogger_api import BloggerAPI
from datetime import datetime, time, timedelta

load_dotenv()

api = BloggerAPI()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='/')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# dictionary to store birthdays of members
birthdays = {}

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("sidekick is in " + str(guild_count) + " guilds.")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity("Waiting for new posts...")
    )

    if not send_new_posts.is_running():
        send_new_posts.start()
    
    if not check_for_birthdays.is_running():
        check_for_birthdays.start()


@tasks.loop(time=time(hour=0, minute=0), count=None)
async def check_for_birthdays():
    channel = bot.get_channel(CHANNEL_ID)

    today = datetime.now()
    for user, bday in birthdays.items():
        if today.month == bday.month and today.day == bday.day:
            if channel:
                await bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game("Happy Birthday! 🎂")
                )
                await channel.send(f"Happy Birthday <@{user}>! Time for some cake! 🎂")
            else:
                print('Failed to find channel with ID:')


@tasks.loop(minutes=15, count=None)
async def send_new_posts():
    channel = bot.get_channel(CHANNEL_ID)
    new_posts = api.get_new_posts(timedelta=timedelta(minutes=15))
    for post in new_posts:
        if channel:
            await channel.send(f"\n**{post['title']}**\n\n{post['url']}")
        else:
            print(f'Failed to find channel with ID: {channel}')


@bot.command()
async def bday(ctx, *args):
    if args[0] == 'list':
        if not birthdays:
            await ctx.send('There are no birthdays stored yet...')
        else:
            for user, birthday in birthdays.items():
                await ctx.send(f'- {user} : {birthday}')

    elif args[0] == 'create':
        birthday = datetime.strptime(args[1], '%Y-%m-%d')
        birthdays[ctx.author] = birthday.date()
        await ctx.send(f'Successfully stored the birthday!')

    elif args[0] == 'delete':
        if ctx.author in birthdays.keys():
            del birthdays[ctx.author]
            await ctx.send('Successfully deleted your birthday.')
        else:
            await ctx.send(f'There is no birthday stored for you anyway.')

    else:
        await ctx.send("Sorry, I don't know this command")


if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)