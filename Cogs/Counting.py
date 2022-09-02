from config import *
from asyncio import sleep
import discord
from discord.ext import commands
import sqlite3

database_path = database_path
discord_link = discord_link

vt = sqlite3.connect(database_path)
im = vt.cursor()

def add_server(token):
	zero = '0'
	im.execute('insert into servers(server,channel,number,counter) values(?,?,?,?)', (token,zero,zero,zero))
	vt.commit()

def edit_db(token, db, variable):
	im.execute(f"UPDATE servers SET {db} = {variable} WHERE server = {token}")
	vt.commit()

def select_db(token, db):
	im.execute(f"SELECT {db} FROM servers WHERE server = {token}")
	return im.fetchall()[0][0]

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
Bot = commands.Bot(["!a ", "!a"], Intents = intents, help_command = None)

class Counting(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@Bot.command()
	async def help(self, ctx):
		await ctx.send(f"Commands list:\n> status: shows bot status\n> setcountingchannel <channel>: sets counting channel\nNeed more help? A detailed instruction on how to use it is on our official discord server: {discord_link}")

	@Bot.command()
	async def status(self, ctx):
		await ctx.send("No information.")

	@Bot.command()
	@commands.has_permissions(administrator = True)
	async def setcountingchannel(self, ctx, channel: discord.TextChannel):
		try:
				add_server(ctx.message.guild.id)
				await ctx.send(f"First run, please use same command **{ctx.message.content}** again. That will never happen again.")
		except:
			edit_db(ctx.message.guild.id, "channel", channel.id)
			await ctx.send(f"Counting channel set to {channel.mention}.")

	#@Bot.command()
	#async def countdown(self, ctx, number):
		#if ctx.message.author.id == owner:
			#message = await ctx.send(number)
			#for count in range(1, int(number) + 1):
				#await sleep(1)
				#await message.edit(content = int(message.content) - 1)
			#await message.edit(content = message.content + "\nCounting is done.")

def setup(bot):
	bot.add_cog(Counting(bot))