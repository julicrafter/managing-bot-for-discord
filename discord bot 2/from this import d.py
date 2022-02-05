
import random #for 8ball function
import discord #for discord
import time # for the sleep and wait fuctions


from discord.ext import commands #for command
from discord.ext import tasks #for chanching presence in background automactical
from itertools import cycle # for cycle fuction is tasks.loop

intents = discord.Intents.all()
discord.member = True                                                                
client = commands.Bot(command_prefix = "!",intents = intents, )
status = cycle(["Dir am Helfen" , "Am Langweilen" , "be all time ready"])

#infos
@client.command(aliases = ["Infos", "infos","Info","info"] )
async def Infos(context):    

    myembed = discord.Embed(title="Current Version" , description="The bot is in V1.0", color=0x1B84CA)
    myembed.add_field(name="Version Code:" , value="V1.0.0" , inline=False)
    myembed.add_field(name = "Date Released:", value="05.02.2022", inline=False)
    myembed.add_field(name="Last Update Released" , value="05.02.2022" , inline=False)
    myembed.set_footer(text="Bot Codet by juli_crafter#8905")
    myembed.set_author(name="juli_crafter#8905")
    
    await context.message.channel.send(embed=myembed)
    



#ping
@client.command()
async def ping(ctx):
    await ctx.send(f"pong {round(client.latency * 1000)}ms")


#8ball
@client.command(aliases = ['8ball', "test"])
async def _8ball(ctx,*,question):
    responses = ["yes", "no"]
    
    await ctx.send(f'Question: {question}\nAnswer:{random.choice(responses)} ')


#clear  to deleate a bunch of massange at once 
#do not forget to count teh !clear message to
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount = 10):
    
    
    await ctx.channel.purge(limit = amount)


#kick   
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*, reason = None,amount = 1): #the amount ist for the deliting of the message
    await member.kick(reason = reason)
    time.sleep(10) # waiting 10 secs
    await ctx.channel.purge(limit = amount) # delleting the command message



#ban   
@client.command()
@commands.has_permissions(ban_members = True) #permission check
async def ban(ctx, member : discord.Member,*, reason = None,amount = 1): #the amount ist for the deliting of the message
    await member.ban(reason = reason)
    time.sleep(10)# waiting 10 secs
    await ctx.channel.purge(limit = amount) # delleting the command message


#unban with massage in the chat
@client.command()
@commands.has_permissions(ban_members = True , administrator = True )
async def unban(ctx, *, member,amount = 1):
    banned_user = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    
    for ban_entry in banned_user:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user) 
            await ctx.send(f'unbanned {user.name}#{user.discriminator}')
            return   


#status change 
@tasks.loop(seconds = 60)
async def status_change():
     await client.change_presence(activity = discord.Game(next(status)))

#onready and status
@client.event 
async def on_ready():
    
    status_change.start()
    
    haupt = client.get_channel(892097003989893123)
    await haupt.send("test")
    
#command not existing
@client.event
async def on_command_error(ctx , error, amount):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("command not found error 10")
        time.sleep(30)
        await ctx.channel.purge(limmit = amount)

#clear error
@client.event
async def clear_error(ctx, error, amount = 1):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("please specify an amount to delete")
        time.sleep(30)
        await ctx.channel.purge(limit = amount)

#permission error
@client.event
async def on_command_error(ctx , error, amount = 1):
    if isinstance(error , commands.MissingPermissions):
        await ctx.send("You dont have enough permissions")
        time.sleep(30)
        await ctx.channel.purge(limit = amount)

#coustum check

def is_it_me(ctx):
    return ctx.author.id == 293433578145185793


@client.command()
@commands.check(is_it_me)
async def example(ctx):
    
    await ctx.send(f"hi am the Bot author {ctx.author}")
    

    
        
        
#to decect what bot on the discord developer portal
#insert at token the token out of the discord developer portal
client.run('token')