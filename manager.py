import discord
from discord.ext import commands
import functools
import os

class Teacher:
	# name : str, schedule : [(period : str, subject : str)]
	def __init__(self, name):
		self.name = name
		self.schedule = []
	def __str__(self):
		if not self.schedule:
			return f"{self.name} : []"
		string = f"\t{self.name}: [({self.schedule[0][0]}, {self.schedule[0][1]})"
		for period, subject in self.schedule[1:]:
			string += f", ({period}, {subject})"
		string += "]\n"
		return string
	def add_period(self, period, subject):
		self.schedule.append((period, subject))
	def get_subject(self, period):
		for p, s in self.schedule:
			if p == period:
				return s
		return None

class GuildInfo:
	# topic : str, teachers : [Teacher]
	def __init__(self, guild, teachers):
		self.guild = guild
		self.teachers = teachers
	def __str__(self):
		string = f"Teachers in {self.guild.name}:\n"
		for teacher in self.teachers:
			string += str(teacher)
		return string
	def get_teacher(self, teacher_name):
		for teacher in self.teachers:
			if teacher.name.lower() == teacher_name.lower():
				return teacher
		return None

guild_infos = []

async def load_guild_info(guild):
	if (not os.path.exists(guild.name + ".txt")):
		return []
	with open(guild.name + ".txt", "r") as f:
		return f.readlines()

async def build_guild_info(guild):
	raw = await load_guild_info(guild)
	if len(raw) == 0:
		return

	teachers = []
	teacher = None

	for line in raw:
		if line[0] != "\t":
			if teacher:
				teachers.append(teacher)
			teacher = Teacher(line.strip())
			continue

		words = line.split()
		teacher.add_period(words[0], words[1])

	if teacher:
		teachers.append(teacher)
	guild_info = GuildInfo(guild, teachers)
	guild_infos.append(guild_info)
	print(guild_info)

async def get_guild_info(guild):
	for gi in guild_infos:
		if gi.guild == guild:
			return gi
	return None

async def get_teacher(guild, teacher_name):
	gi = await get_guild_info(guild)
	if gi:
		return gi.get_teacher(teacher_name)
	return None

async def get_role(guild, role_name, create_if_not_found=False):
	# if role doesn't exist, create it
	role = None
	for guild_role in guild.roles:
		if (guild_role.name.lower() == role_name.lower()):
			role = guild_role

	if (role == None and create_if_not_found):
		role = await guild.create_role(name=role_name, colour=discord.Colour.blue(), reason="Didn't exist")
	return role

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

@bot.command()
async def join(ctx, teacher_name, period):
	# Get teacher role
	teacher = await get_teacher(ctx.guild, teacher_name)
	if (not teacher):
		await ctx.send(f"{teacher_name} isn't an SLHS teacher!")
		return

	subject = teacher.get_subject(period)
	if (not subject):
		await ctx.send(f"{period} isn't registered!")
		return

	teacher_role = await get_role(ctx.guild, teacher.name, True)
	period_role = await get_role(ctx.guild, period, True)
	subject_role = await get_role(ctx.guild, subject, True)

	# Leave previous class
	await leave(ctx)

	# Add roles
	await ctx.author.add_roles(teacher_role)
	await ctx.author.add_roles(period_role)
	await ctx.author.add_roles(subject_role)
	await ctx.send(f"You joined {teacher.name}'s class!")


# Doesn't check if the role corresponds to teacher.
@bot.command()
async def leave(ctx):
	left = False
	for author_role in ctx.author.roles[1:]:
		if (ctx.me.roles[1] > author_role):
				await ctx.author.remove_roles(author_role)
				left = True
	if left:
		await ctx.send("You left your previous class")

@bot.command()
async def schedule(ctx):
	raw = await load_guild_info(ctx.guild)
	await ctx.send("```\n" + "".join(raw) + "```")

@bot.command()
@commands.has_role("admin")
async def reset(ctx):
	pass

@bot.listen()
async def on_ready():
	print(f"We logged in as: {bot.user}")
	for guild in bot.guilds:
		await build_guild_info(guild)

token = ""
with open("token.txt", "r") as file:
	token = file.read()

bot.run(token)
