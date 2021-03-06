import discord
import json
from discord.ext import commands, tasks

token = open('tok.txt').read()
bot = commands.Bot(command_prefix='.',help_command =None)


def load_resources():
    with open('resources.json') as r:
        doc = json.load(r)
    return doc

doc = load_resources()

@bot.event
async def on_member_join(member):
    print('running')
    await member.send(f'Welcome to Ridge Coders, {member.mention}')
    role = discord.utils.get(member.guild.roles, name="coders")
    await member.add_roles(role)
    
@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))
    load_resources()

    
@bot.command(name = 'les')
async def lessons(ctx, *args):
    q = ''.join([i+' ' for i in args])[:-1]
    result = None
    embed = discord.Embed()
    if q == 'all':
        embed.title = f"Ridge Coder Lessons"
        value = ''
        for num,i in enumerate(doc):
            num +=1
            value += f'{num}. [{i}]({doc[i]})\n'
        print(value)
        embed.add_field(name = 'All Lessons', value = value, inline = True)
        await ctx.send(embed=embed)
        
    else:
        for i in range(len(q)):
            try:
                result =[doc[q],q]
            except:
                pass
        if result == None:
            await ctx.send(f"{ctx.author.mention} Sorry, no lessons found on `{q}`")
            
        else:
            embed.title = f"Ridge Coder Lessons"
            embed.description = f"Here are your results on [{result[1]}]({result[0]})."
            await ctx.send(embed=embed)
        
@bot.command()
async def poll(ctx):
    msg = await ctx.send("how are you feeling today?")
    await msg.add_reaction('😀')
    await msg.add_reaction('☹')


bot.run(token, bot = True)
