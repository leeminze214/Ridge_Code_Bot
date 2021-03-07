import discord
import json
from discord.ext import commands, tasks

token = open('tok.txt').read()
bot = commands.Bot(command_prefix='.',intents = discord.Intents.all(), help_command =None)
doc = None
msg_count = 0

def load_resources():
    global doc
    with open('resources.json') as r:
        doc = json.load(r)

async def load_msgs():
    global msg_count
    sent = 0
    for i in bot.guilds:     
        if i.name == 'testing':  
            for j in i.text_channels:
                messages = len(await j.history(limit = None).flatten())         
                sent+=messages
    msg_count = sent

def add_enumerate(it):
    value = ''
    for num,j in enumerate(it):
        num +=1
        value += f'{num}. [{j}]({it[j]})\n'
    return value

#-----------------------------------------------------------------
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
    await load_msgs()


@bot.event
async def on_message(msg):
    global msg_count
    msg_count +=1
    await bot.process_commands(msg)
    
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency is {round(bot.latency*1000,2)}ms')

@bot.command()
async def help(ctx):
    embed = discord.Embed()
    lesson = "`.les <topic>` ---> fetch lessons on <topic>, use 'all' to see all lessons"
    embed.title = "Help"
    embed.description = "I am the Ridge Coder Bot, Here are a list of my functions!"
    embed.add_field(name = 'Access Lessons', value =lesson) 
    await ctx.send(embed=embed)
    
@bot.command()
async def analytics(ctx):
    
    if "Admin" in [i.name for i in ctx.author.roles]:
        members = ctx.guild.member_count
        messages = msg_count
        embed = discord.Embed()
        embed.title ="Analytics"
        embed.add_field(name = "Members", value = members, inline = True)
        embed.add_field(name = "Messages", value = messages, inline = True)
        await ctx.send(embed=embed)
        
    
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
