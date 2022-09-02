from config import *
import random
from asyncio import sleep
import os
import discord
from discord.ext import commands, tasks
import sqlite3

database_path = database_path
token = token
owner = owner

vt = sqlite3.connect(database_path)
im = vt.cursor()

im.execute("CREATE TABLE IF NOT EXISTS servers(server integer PRIMARY KEY, channel integer, number integer, counter integer)")

def edit_db(token, db, variable):
	im.execute(f"UPDATE servers SET {db} = {variable} WHERE server = {token}")
	vt.commit()

def select_db(token, db):
	im.execute(f"SELECT {db} FROM servers WHERE server = {token}")
	return im.fetchall()[0][0]

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
Bot = commands.Bot(["!a ", "!a"], Intents = intents, help_command = None)

@Bot.event
async def on_ready():
	update_presence.start()
	print(f"{Bot.user.name} baslatildi.")

@Bot.event
async def on_command_error(ctx, error):
	pass

@Bot.event
async def on_message(message):
	await Bot.process_commands(message)
	if message.content.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
		if message.channel.id == select_db(message.guild.id, "channel") and message.author.bot == False:
			if message.author.id != select_db(message.guild.id, "counter"):
				#if eval(message.content) == select_db(message.guild.id, "number") + 1:
					#edit_db(message.guild.id, "number", eval(message.content))

#remove line 49 and 50, and activate 44 and 45 if you want to count like this example: '30 + 70' this will count instead of 100. But theres some problems like using python functions on discord chat. So i disabled this.

				if int(message.content) == select_db(message.guild.id, "number") + 1:
					edit_db(message.guild.id, "number", int(message.content))
					edit_db(message.guild.id, "counter", message.author.id)
					await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
				else:
					number = select_db(message.guild.id, "number")
					message = await message.channel.send(f":x: Wrong number! :x: Previus number is: **{number}**")
					await sleep(3)
					await message.delete()
			else:
				message = await message.channel.send(":warning: You cant count in a row! :warning:")
				await sleep(3)
				await message.delete()
				

@tasks.loop(seconds = 60)
async def update_presence():
	presences = ["Come to our discord server!", "Weather is good today.", "Regular updates!", "İf you see that, you are lucky.", "İ hope your day is good.", "A random presence!", "Fake Minecraft title screen texts!", "Requests or report? Check my description!", "Some interesting texts.", "10. text!"]
	await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = f"{len(Bot.guilds)} servers | !ahelp | {random.choice(presences)}"))

@Bot.command()
async def reload(ctx, extension):
	if ctx.message.author.id == owner:
		Bot.unload_extension(f"Cogs.{extension}")
		Bot.load_extension(f"Cogs.{extension}")
		await ctx.send(f"All commands reloaded on category {extension}.")

@Bot.command()
async def leaderboard(ctx, page = 1):
    page_count = 1
    leaderboard_list = []
    server_count = 0
    page_leaderboard = {}
    for server in im.execute("SELECT * FROM servers ORDER BY number DESC"):
    	server_test = Bot.get_guild(server[0])
    	if server_test is not None:
    		if server_count != 10:
    			try:
    				server_count += 1
    				leaderboard_list.append(f"> {server_count}. {server_test.name}, {server[2]}\n")
    				page_leaderboard.update({page_count: leaderboard_list})
    			except:
    				pass
    		else:
    			leaderboard_list = []
    			page_count += 1
    			try:
    				server_count += 1
    				leaderboard_list.append(f"> {server_count}. {server_test.name}, {server[2]}\n")
    				page_leaderboard.update({page_count: leaderboard_list})
    			except:
    				pass

    leaderboard_str = "".join(page_leaderboard[page])
    await ctx.send(f"Top counters (server):\n{leaderboard_str}\nshowing {page}. page of total {page_count} pages.")

for filename in os.listdir("./Cogs"):
	if filename.endswith(".py"):
		Bot.load_extension(f"Cogs.{filename[:-3]}")

Bot.run(token)