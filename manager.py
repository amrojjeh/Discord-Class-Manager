import discord
import os

client = discord.Client()

PREFIX = "!"

@client.event
async def on_ready():
	print(f"We logged in as: {client.user}")

async def remove_category(guild, category_name):
	selected = None
	for category in guild.categories:
		if (category.name.lower() == category_name.lower()):
			selected = category
	if (selected == None):
		return 1
	for channel in selected.channels:
		await channel.delete()
	await selected.delete()
	return 0

async def get_teacher_role(guild, teacher_name, create_if_not_found):
	# if role doesn't exist, create it
	teacherRole = None
	for role in guild.roles:
		if (role.name == teacher_name):
			teacherRole = role

	if (teacherRole == None and create_if_not_found):
		teacherRole = await guild.create_role(name=teacher_name, colour=discord.Colour.blue(), reason="Didn't exist")
	return teacherRole

# THIS DOES NOT DELETE DUPLICATES
async def add_channels(category, teacher_name):
	requiredTextChannels = ["general", "p1", "p2", "p3", "p4", "p5", "p6", "p7"]
	requiredVoiceChannels = ["Classroom"]

	channels_to_delete = []

	text_channels = category.text_channels
	voice_channels = category.voice_channels

	teacherRole = await get_teacher_role(category.guild, teacher_name, True)

	overwritesGeneral = {
		category.guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
		teacherRole: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True)
	}

	# Remove unneeded channels
	for channel in category.channels:
		if (channel.name not in requiredTextChannels and channel.name not in requiredVoiceChannels):
			channels_to_delete.append(channel)

	for channel in channels_to_delete:
		await channel.delete()

	# Add needed channels
	for channelName in requiredTextChannels:
		if (channelName not in (t.name for t in text_channels)):
			if channelName != "general":
				periodRole = await get_teacher_role(category.guild, teacher_name + channelName, True)
				overwritesPeriod = {
					category.guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
					periodRole: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True)
				}
				await category.create_text_channel(channelName, overwrites=overwritesPeriod)
			else:
				await category.create_text_channel(channelName, overwrites=overwritesGeneral)

	for channelName in requiredVoiceChannels:
		if (channelName not in (v.name for v in voice_channels)):
			await category.create_voice_channel(channelName)

async def add_teacher(guild, teacher_name):
	# Check if channel exists
	# if not create channels
	category_found = False

	for category in guild.categories:
		if (category != None and category.name.lower() == teacher_name.lower()):
			await add_channels(category, teacher_name)
			category_found = True

	if (not category_found):
		category = await guild.create_category(teacher_name)
		await add_channels(category, teacher_name)

def is_guild_owner(message):
	return message.author.id == message.author.guild.owner.id

@client.event
async def on_message(message):
	if (message.author.bot):
		return

	if (message.content.startswith(PREFIX + "join")):
		words = message.content.split(" ")
		if (len(words) >= 2 ):
			teacher = words[1]
			period = None
			if (len(words) == 3):
				period = words[2]
			role = await get_teacher_role(message.author.guild, teacher, False)
			if (role == None):
				await message.channel.send("Teacher not found!")
				return
			for author_role in message.author.roles[1:]:
				await message.author.remove_roles(author_role)
			await message.author.add_roles(role)
			if (period != None):
				periodRole = await get_teacher_role(message.author.guild, teacher + period, False)
				if (periodRole == None):
					await message.channel.send("Period doesn't exist!")
				else:
					await message.author.add_roles(periodRole)
			await message.channel.send(f"You joined {teacher}'s class!")
		else:
			await message.channel.send(f"Usage: {PREFIX}join TEACHER [PERIOD]")

	if (message.content.startswith(PREFIX + "add") and is_guild_owner(message)):
		words = message.content.split(" ")
		if (len(words) == 2):
			teacher = words[1]
			await add_teacher(message.author.guild, teacher)
			await message.channel.send(f"Teacher added!")
		else:
			await message.channel.send(f"Usage: {PREFIX}add TEACHER")

	if (message.content.startswith(PREFIX + "remove") and is_guild_owner(message)):
		words = message.content.split(" ")
		if (len(words) >= 2):
			category = " ".join(words[1:])
			if (await remove_category(message.author.guild, category) != 0):
				await message.channel.send("Category doesn't exist")
			else:
				await message.channel.send("Category deleted")

token = ""
with open("token.txt", "r") as file:
	token = file.read()

client.run(token)
