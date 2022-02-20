import discord
from replit import db
from discord.ext import commands
from webserver import keep_alive
import os

client = commands.Bot(command_prefix = '!', case_insensitive=True)

ALLOWEDCHARACTERS = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f']

def readfile(filename):
  f = open(filename,'r')
  x = f.read().splitlines()
  f.close()
  return x

def create_text(name,array):
  f = open(f"{name}.txt", "w")
  for item in array:
    f.write(f'{item}\n')
  f.close()

def valid_address(address):
    if len(address) != 42:
        print ("Wrong length",len(address))
        return False
    newaddress = address[2:42]
    for letter in newaddress:
        if letter not in ALLOWEDCHARACTERS:
            print("Wrong character",letter)
            return False
    return True

@client.command(name='change')
async def change(ctx, args):
    await ctx.message.delete()
    if ctx.channel.name == '💳・wallet-collection':
      if str(ctx.author.id) in db['IDs']:
        if valid_address(args):
          db['Addresses'][db['IDs'].index(str(ctx.author.id))] = args
    
@client.command(name='printdb')
async def printdb(ctx):
  create_text('IDs',db['IDs'])
  create_text('Usernames',db['Usernames'])
  create_text('Addresses',db['Addresses'])

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.channel.id == 944236837361287308:
      if message.author == client.user:
          return
      content = message.content
      await message.delete()
      if content[0:2] == '0x':
          if valid_address(content):
              if content not in db['Addresses']:
                  if (str(message.author.id) not in db['IDs']):
                      db['IDs'].append(str(message.author.id))
                      usernames = await client.fetch_user(message.author.id)
                      db['Usernames'].append(str(usernames))
                      db['Addresses'].append(content)


keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)