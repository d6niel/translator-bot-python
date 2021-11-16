import discord
import logging
import re
from discord import activity
from discord.ext import commands
from discord.message import Message
from googletrans import Translator

### Outputs logs to a file ###
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

bot = commands.Bot(
    command_prefix=".", help_command=None, activity=discord.Game(name=".help | .info")
)  # Initializes commands to a prefix
translator = Translator()  # Initializes translator function
embed = discord.Embed()  # Initializes embed messages

# Channel variables
general_channel = None
bot_channel = None
english_channel = None

default_language = "english"

auto_translation = bool()
current_auto_translation_setting = "Off"

in_settings = False

# List of all languages
languages = set()
with open("languages.txt", "r") as f:
    for l in f.readlines():
        m = re.match("^(.*);(.*)", l)
        languages.add(m.group(1))
        languages.add(m.group(2))


### On ready triggers ###
@bot.event
async def on_ready():

    # Declares when bot is started up
    print("We have logged in as {0.user}".format(bot))

    # Assigns specific channels to variables
    global general_channel, bot_channel, english_channel
    general_channel = bot.get_channel(906118413540265997)
    bot_channel = bot.get_channel(906151626241372170)
    english_channel = bot.get_channel(906156397392175154)


### Translates text when .tl command is used ###
@bot.command()
async def tl(ctx, lang, *, text_to_translate=""):

    # Checks if user enters langauge
    if lang not in languages:
        embed.description = """
                            Watch out, no translation language selected! 
                            Correct command formatting should be: *.tl "new_language" "text_to_translate*". 
                            Please type **.help formatting** if you need help with formatting.
                            """
    elif lang in languages:
        # Translates
        res = translator.translate(text_to_translate, dest=lang)
        embed.title = "Translation"
        embed.description = f"{text_to_translate} -> {res.text}"

    await ctx.send(embed=embed, delete_after=5)


### Settings menu ###
@bot.command()
async def settings(ctx, arg1="", arg2=""):
    global default_language, auto_translation, current_auto_translation_setting

    arg1 = arg1.lower()
    arg2 = arg2.lower()

    # Default settings message
    embed.title = "Settings"
    if not arg1:
        embed.description = f"""Here is a list of all available settings: 
                            \n• **Default**: Changes default translating language *(Current language: {default_language})*.
                            \n• **Auto**: Toggles Automatic Translation *(Current setting: {current_auto_translation_setting})*."""
    # Change default translating language
    elif arg1 == "default":
        embed.title = "Settings -> Default"
        # Checks if the language was given by the user
        if arg2 == "":
            embed.description = "Please select the new default translating language *(For a list of all available languages type **.lang**)*"

        # Checks if the language selected by the user is valid
        elif arg2 in languages:
            default_language = arg2
            print(default_language)
            embed.description = f"*New language set: {arg2}!*"

        # Error message if language is invalid
        elif arg2 not in languages:
            embed.description = "*Language not found! For a list of all available languages please type **.lang***"

    elif arg1 == "auto":
        embed.title = "Settings -> Auto Translation"
        if arg2 == "on":
            auto_translation = True
            current_auto_translation_setting = "On"
            embed.description = "Automatic translation has been turned on."
        elif arg2 == "off":
            auto_translation = False
            current_auto_translation_setting = "Off"
            embed.description = "Automatic translation has been turned off."
        else:
            embed.description = "Unknown argument! This setting only has two values: on or off. Please type **.help formatting** if you need help with formatting. "

    # Displays error message if unknown command
    elif arg1 != ("default", "auto"):
        embed.description = """Unknown command! Here is a list of all available settings: 
                            \n• Default: Changes default translating language *(Current language: {})*. """.format(
            default_language
        )

    await ctx.send(embed=embed, delete_after=5)


### List of all available languages ###
@bot.command()
async def lang(ctx):
    embed.title = "Languages"
    print_languages = open("languages.txt", "r").read().replace(";", " **or** ")
    embed.description = print_languages
    await ctx.send(embed=embed, delete_after=10)


### List of all available commands ###
@bot.command()
async def help(ctx, arg1=""):

    arg1 = arg1.lower()

    if arg1 == "":
        embed.title = "Help"
        embed.description = """All available commands:
                            \n• **Settings** *(.settings)*: Change all Translator Bot settings. Type **.settings** for more info.
                            \n• **Translation** *(.tl)*: Translate any message to (almost) any language. 
                            \n• **Languages** *(.lang)*: Displays a list of all available languages.
                            \n\n**- Formatting** *(.help formatting)*: Displays formatting and more info for every command."""

    elif arg1 == "formatting":
        embed.title = "Help -> Formatting"
        embed.description = """Here's a list showing the correct formatting for every bot command:
                            \n• **Settings**: 
                            \n*.settings default "language"*
                            \n*.settings auto on, .settings auto off*
                            \n• **Translation**: *.tl "new_language" "text_to_translate*" 
                            \n• **Languages**: *.lang*"""
    await ctx.send(embed=embed, delete_after=10)


### Information section ###
@bot.command()
async def info(ctx):

    embed.title = "Translator Bot Info"
    embed.set_image(url="https://i.lensdump.com/i/g7wchF.png")
    embed.description = """For help type .help or .help formatting.
                        \nFollow the bot's development on GitHub: https://github.com/d6niel/translator-python."""

    await ctx.send(embed=embed, delete_after=10)


### On message triggers ###
@bot.event
async def on_message(message):
    # Ignores messages from Bot
    if message.author == bot.user:
        return

    # Automatically translates any message from general channel to english in english channel
    if not message.content.startswith((".tl", ".settings", ".lang", ".help")):
        if auto_translation:
            if message.channel.name == "general":
                res = translator.translate(message.content, dest="en")
                embed.title = "Translation"
                embed.description = message.content + " -> " + res.text
                await english_channel.send(embed=embed)
    else:
        await message.delete()  # Deletes messages that are commands

    await bot.process_commands(message)  # Fixes on_message blocking bot.command


token = open("token.txt", "r").read()
bot.run(token)
