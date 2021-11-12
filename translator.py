import discord
import logging
import re
from discord.ext import commands
from discord.message import Message
from googletrans import Translator

# Outputs logs to a file
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='.', help_command=None)  # Initializes commands to a prefix
translator = Translator()   # Initializes translator function
embed = discord.Embed() # Initializes embed messages

# Channel variables
general_channel = None
bot_channel = None
english_channel = None

default_language = 'english'

in_settings = False

languages = open('languages.txt', 'r')


### On ready triggers ###
@bot.event
async def on_ready():
    
    # Declares when bot is started up
    print('We have logged in as {0.user}'.format(bot))
   
    # Assigns specific channels to variables
    global general_channel, bot_channel, english_channel
    general_channel = bot.get_channel(906118413540265997)
    bot_channel = bot.get_channel(906151626241372170)
    english_channel = bot.get_channel(906156397392175154)


### Translates text when .tl command is used ###
@bot.command()
async def tl(ctx, lang, *, to_translate = ''):
    if not lang:
        lang = default_language
    if to_translate:
        tl_from_lang = translator.detect(to_translate)  # Detects language
        res = translator.translate(to_translate, dest = lang)
        await ctx.send(f'{to_translate} -> {res.text}') # Outputs original and translated text

### Settings menu ###
@bot.command()
async def settings(ctx, arg1 = '', arg2 = ''):
    global default_language

    arg1 = arg1.lower()
    arg2 = arg2.lower()

    # Default settings message
    embed.title = 'Settings'
    if not arg1:
        embed.description = '''Here is a list of all available settings: 
                            \n• Default: Changes default translating language *(Current language: {})*.'''.format(default_language)
    # Change default translating language
    elif arg1 == 'default':
        embed.title = 'Settings -> Default'
        
        # Checks if the language was given by the user
        if arg2 == '':
            embed.description = 'Please select the new default translating language *(For a list of all available languages type **.lang**)*'
        
        # Checks if the language selected by the user is valid
        elif arg2 in languages.read():
            default_language = arg2
            embed.description = f'*New language set: {arg2}!*'
        
        # Error message if language is invalid
        else:
            embed.description = '*Language not found! For a list of all available languages please type **.lang***'


    # Displays error message if unknown command
    elif arg1 != ('default'): 
        embed.description = '''Unknown command! Here is a list of all available settings: 
                            \n• Default: Changes default translating language *(Current language: {})*. '''.format(default_language)
    
    
    await ctx.send(embed=embed, delete_after=5)


### List of all available languages ###
@bot.command()
async def lang(ctx):
    embed.title = 'Languages'
    print_languages = languages.read().replace(';',' **or** ')
    embed.description = print_languages
    await ctx.send(embed=embed, delete_after=10)


### List of all available commands ###
@bot.command()
async def help(ctx):

    embed.title = 'Help'
    embed.description = '''All available commands:
                        \n• **Settings** *(.settings)*: Change all Translator Bot settings. Type **.settings** for more info.
                        \n• **Translation** *(.tl)*: Translate any message to (almost) any language. Type **.tl** for more info.
                        \n• **Languages** *(.lang)*: Displays a list of all available languages.'''

    await ctx.send(embed=embed, delete_after=10)


### On message triggers ###       
@bot.event
async def on_message(message):
    # Ignores messages from Bot
    if message.author == bot.user:
        return

    # Automatically translates any message from general channel to english in english channel
    if message.channel.name == 'general' and not message.content.startswith(('.tl', '.settings', '.lang')):
            res = translator.translate(message.content, dest = 'en')
            embed.title = 'Translation'
            embed.description = message.content + ' -> ' + res.text
            await english_channel.send(embed=embed, delete_after=5)
    

    await message.delete()   # Deletes user command message
    await bot.process_commands(message) # Fixes on_message blocking bot.command


token = open('token.txt', 'r').read()
bot.run(token)