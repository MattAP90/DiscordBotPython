import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import asyncio
import os
import re
from dotenv import load_dotenv

#initial set up
load_dotenv()
TOKEN = os.getenv('TOKEN')
FILMCHAN = os.getenv('FILM_CHANNEL')
GENCHAN = os.getenv('GENERAL')
FILMROLE = os.getenv('FILM_FRIENDS')
LEMOTE = os.getenv('LEBRON_EMOTE')
BDAY_PATH = os.getenv('BDAY_PATH')
FENTE = os.getenv('FENTE')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# event set up and testing
events = []
daily = datetime.time(hour=11, minute=0)
bDay = datetime.time(hour=11, minute=1)
movie_time = datetime.time(hour=0, minute=30)
events.append(daily)
events.append(movie_time)
events.append(bDay)
dates = [{"month": 1, "day": 1, "name": "New Year's", "gif": "https://tenor.com/view/new-years-eve-party-bye2020-gif-19775655"},
         {"month": 1, "day": 15, "name": "MLK Day", "gif": "https://tenor.com/view/martinlutherking-ihaveadream-gif-4834306"},
         {"month": 2, "day": 21, "name": "Shammy Shake Season", "gif": "https://tenor.com/view/shamrock-shake-mcdonalds-nasty-st-patricks-day-my-beloved-gif-21685751"},
         {"month": 3, "day": 17, "name": "St. Patrick's Day", "gif": "https://tenor.com/view/beer-green-beer-irish-gif-5217346"},
         {"month": 4, "day": 1, "name": "April Fool's", "gif": "https://tenor.com/view/never-gonna-give-you-up-rickroll-april-fool-gif-20978739"},
         {"month": 4, "day": 22, "name": "Earth Day", "gif": "https://tenor.com/view/flat-earth-flat-earth-flache-erde-scan-gif-12294998"},
         {"month": 3, "day": 21, "name": "Spring Equinox", "gif": "https://tenor.com/view/birds-branch-spring-its-spring-cute-gif-17419196"},
         {"month": 6, "day": 21, "name": "Summer Solstice", "gif": "https://tenor.com/view/summer-solstice-happy-summer-first-day-of-summer-summer-vacation-solstice-gif-8939684"},
         {"month": 7, "day": 4, "name": "Merica Day", "gif": "https://tenor.com/view/freedom-america-gif-14280685"},
         {"month": 9, "day": 11, "name": "Never Forget", "gif": "https://tenor.com/view/karuta-george-bush-drop-mintsjams-gif-25890730"},
         {"month": 9, "day": 21, "name": "Fall Equinox", "gif": "https://tenor.com/view/fall-pumpkin-spice-coffee-pumkin-gif-18685786"},
         {"month": 10, "day": 31, "name": "Halloween", "gif": "https://tenor.com/view/skeleton-dancing-skeletons-boo-cartoon-gif-18326832313355216882"},
         {"month": 11, "day": 11, "name": "Veteran's Day", "gif": "https://tenor.com/view/veterans-day-army-twerking-celebration-gif-7117066"},
         {"month": 12, "day": 24, "name": "Santa Be Comin", "gif": "https://tenor.com/view/elf-will-ferrell-buddy-santas-coming-gif-3577188"},
         {"month": 12, "day": 25, "name": "Santa Came...", "gif": "https://tenor.com/view/santa-santa-claus-papa-noel-twerk-twerking-gif-7219802"},
         {"month": 12, "day": 31, "name": "New Year's Eve", "gif": "https://tenor.com/view/happy-new-year2020-new-years-eve-dance-dancing-lets-dance-gif-13147621"},
         {"month": 12, "day": 21, "name": "Winter Solstice", "gif": "https://tenor.com/view/first-day-of-winter-shortest-day-of-the-year-sleeping-short-day-back-to-bed-gif-19516219"}
         ]


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents = intents)

@tasks.loop(time=daily)
async def dailyCheck():
    now = datetime.datetime.now().timetuple()
    month = now.tm_mon
    day = now.tm_mday
    for date in dates:
        if date["month"] == month and date["day"] == day:
            holiday = date["name"]
            gif = date["gif"]
            channel = bot.get_channel(int(GENCHAN))
            await channel.send(f"{holiday}\n{gif}")
    await asyncio.sleep(60)

@tasks.loop(time=bDay)
async def bDayCheck():
    now = datetime.datetime.now().timetuple()
    month = now.tm_mon
    day = now.tm_mday
    list_of_bdays = None
    bdayCount = None
    with open(BDAY_PATH, 'r') as bday_file:
        list_of_bdays = bday_file.readlines()
        bdayCount = len(list_of_bdays)
        if bdayCount > 0:
            for i in range(bdayCount):
                info = list_of_bdays[i].split()
                print(info)
                if month == int(info[1]) and day == int(info[2]):
                    channel = bot.get_channel(int(GENCHAN))
                    print(channel)
                    await channel.send(f"Happy Birthday <@!{info[0]}>! \nhttps://tenor.com/view/dog-funny-old-age-aging-gif-15870718538183839440")
    await asyncio.sleep(60)

@tasks.loop(time=movie_time)
async def movieNight():
    now = datetime.datetime.now().timetuple()
    if now.tm_wday == 3:
        channel = bot.get_channel(int(FILMCHAN))
        await channel.send(f"<@!{FILMROLE}> it is time", file=discord.File(r'pics/Skillz_in_the_sky.png'))
    await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"{bot.user} is online.")
    dailyCheck.start()
    bDayCheck.start()
    movieNight.start()

@bot.command(name="hi", description="Bot says 'hello' back")
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.display_name}")

@bot.command(name="dance", description="Dance back")
async def dance(ctx):
    await ctx.reply("https://tenor.com/view/pepe-dance-cryptocurrency-crypto-dancing-gif-22212526")

@bot.command(name='setbday', brief="set birthday of author", description="sets bday of user that sent date 'mm/dd'")
async def setbday(ctx):
    month = 1
    day = 1
    author = ctx.author.id
    msg = ctx.message.content
    msg = msg.strip("!bday")
    msg = msg.strip()
    date = re.search("[0-9]{2}/[0-9]{2}", msg)
    if date is None:
        date = re.search("[0-9]{1}/[0-9]{2}", msg)
    if date is None:
        date = re.search("[0-9]{2}/[0-9]{1}", msg)
    if date is None:
        date = re.search("[0-9]{1}/[0-9]{1}", msg)
    if date is None:
        await ctx.reply(f"{msg} is not a valid bday format try 'mm/dd'")
    
    date = date.group(0)
    new_date = ""
    for i in range(len(date)):
        new_date = new_date + date[i]
    new_date = new_date.split("/")
    month = int(new_date[0])
    day = int(new_date[1])
    if month > 12:
        await ctx.reply(f"{month} is an invalid month")
    if day > 31:
        await ctx.reply(f"{day} is an invalid day")
    
    list_of_bdays = None 
    bdayCount = None
    with open(BDAY_PATH, 'r') as bday_file:
        list_of_bdays = bday_file.readlines()
        bdayCount = len(list_of_bdays)
        found = False
        if bdayCount > 0:
            for i in range(bdayCount):
                info = list_of_bdays[i].split()
                if author == int(info[0]):
                    list_of_bdays[i] = str(author) + " " + str(month) + " " + str(day) + "\n"
                    found = True
        if not found:
            list_of_bdays.append(str(author) + " " + str(month) + " " + str(day) + "\n")
            bdayCount += 1
    
    with open(BDAY_PATH, 'w') as bday_file:
        print(list_of_bdays)
        bday_file.writelines(list_of_bdays)
    
    await ctx.send(f"bday is set to {month}/{day} for <@!{author}>")

@bot.command(name='bdays', brief="list of bdays", description="prints a list of all bdays in the discord")
async def bdays(ctx):
    list_of_bdays = None
    bdayCount = None
    bday_list = "Birthdays:\n"
    with open(BDAY_PATH, 'r') as bday_file:
        list_of_bdays = bday_file.readlines()
        bdayCount = len(list_of_bdays)
        for i in range(bdayCount):
            info = list_of_bdays[i].split()
            name = bot.get_user(int(info[0])).display_name
            month = info[1]
            day = info[2]
            bday_list = bday_list + name + " - " + month + "/" + day + "\n"
    await ctx.send(f"{bday_list}")

@bot.event
async def on_message(blah):
    msg = blah.content
    msg = msg.upper()
    if 'LEBRON' in msg:
        if blah.author.id == int(FENTE):
            await blah.reply("https://tenor.com/view/lebron-james-lebron-king-james-lakers-lake-show-gif-5899000798739324893")
        else:
            await blah.add_reaction(bot.get_emoji(int(LEMOTE)))
    await bot.process_commands(blah)

bot.run(TOKEN)