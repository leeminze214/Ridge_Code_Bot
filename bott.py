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

def add_enumerate(it):
    value = ''
    for num,j in enumerate(it):
        num +=1
        value += f'{num}. [{j}]({it[j]})\n'
    return value

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
    q = q[0].upper()+q[1:].lower()
    result = None
    embed = discord.Embed()
    if q == 'All':
        embed.title = f"Ridge Coder Lessons"
        
        for i in doc:
            value = add_enumerate(doc[i])
            embed.add_field(name = f'{i}', value = value, inline = True)
        await ctx.send(embed=embed)
        
    else:
        try:
            result =[doc[q],q]
        except:
            pass
        if result == None:
            await ctx.send(f"{ctx.author.mention} Sorry, no lessons found on `{q}`")
            
        else:
            embed.title = "Ridge Coder Lessons"
            value=add_enumerate(result[0])
            embed.add_field(name = f'{result[1]}', value = value)
            await ctx.send(embed=embed)
        
@bot.command()
async def poll(ctx):
    msg = await ctx.send("how are you feeling today?")
    await msg.add_reaction('😀')
    await msg.add_reaction('☹')


bot.run(token, bot = True)
