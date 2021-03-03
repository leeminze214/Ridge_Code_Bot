import discord
from discord.ext import commands, tasks

token = open('tok.txt').read()
bot = commands.Bot(command_prefix='.',help_command =None)

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))
   
    
bot.run(token)
