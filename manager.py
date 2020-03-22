import discord
from discord.ext import commands 

class CommonPermissions:
	hidden = discord.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False)
	available = discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True)

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

async def get_role(guild, role_name, create_if_not_found=False):
	# if role doesn't exist, create it
	role = None
	for guildRole in guild.roles:
		if (guildRole.name.lower() == role_name.lower()):
			role = guildRole

	if (role == None and create_if_not_found):
		role = await guild.create_role(name=role_name, colour=discord.Colour.blue(), reason="Didn't exist")
	return role

async def get_category(guild, category_name, create_if_not_found=False):
	category = None

	for guildCategory in guild.categories:
		if guildCategory.name.lower() == category_name.lower():
			category = guildCategory
	
	if (category == None and create_if_not_found):
		category = await guild.create_category(category_name)
	return category

async def get_text_channel_in_category(category, channel_name, create_if_not_found=False):
	channel = None

	for categoryChannel in category.text_channels:
		if categoryChannel.name.lower() == channel_name.lower():
			channel = categoryChannel
	if (channel == None and create_if_not_found):
		channel = await category.create_text_channel(channel_name)
	
	return channel

async def get_voice_channel_in_category(category, channel_name, create_if_not_found=False):
	channel = None

	for categoryChannel in category.voice_channels:
		if categoryChannel.lower() == channel_name.lower():
			channel = categoryChannel
	if (channel == None and create_if_not_found):
		channel = await category.create_voice_channel(channel_name)
	
	return channel

async def add_channels(category, teacher_role):
	requiredTextChannels = ["general", "p1", "p2", "p3", "p4", "p5", "p6", "p7"]
	requiredVoiceChannels = ["Classroom"]

	for channel_name in requiredTextChannels:
		channel = await get_text_channel_in_category(category, channel_name, True)
		if (channel_name == "general"):
			await channel.set_permissions(teacher_role, overwrite=CommonPermissions.available)
		await channel.set_permissions(category.guild.default_role, overwrite=CommonPermissions.hidden)

	for channel_name in requiredVoiceChannels:
		channel = await get_voice_channel_in_category(category, channel_name, True)
		await channel.set_permissions(category.guild.default_role, overwrite=CommonPermissions.hidden)
		await channel.set_permissions(teacher_role, overwrite=CommonPermissions.available)

async def add_teacher(guild, teacher_name):
	# Create role and category, if they doesn't exist
	teacher_role = await get_role(guild, teacher_name, True)
	category = await get_category(guild, teacher_name, True)

	# Create chanenls
	await add_channels(category, teacher_role)

def is_guild_owner(ctx):
	return ctx.author == ctx.guild.owner

token = ""
with open("token.txt", "r") as file:
	token = file.read()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

@bot.command()
async def join(ctx, teacher, period=""):
	# Get teacher role
	teacherRole = await get_role(ctx.guild, teacher)
	teacherCategory = await get_category(ctx.guild, teacher)
	periodChannel = None

	if (teacherRole == None or teacherCategory == None):
		await ctx.send(f"Teacher, {teacher}, not found!")
		return

	# Get period role
	if (period != ""):
		periodChannel = await get_text_channel_in_category(teacherCategory, period)
		if (periodChannel == None):
			await ctx.send(f"Period, {period}, doesn't exist!")
			return

	# Remove previous roles
	for author_role in ctx.author.roles[1:]:
		category = await get_category(ctx.guild, author_role.name)
		if (category != None):
			for channel in category.text_channels:
				if (channel.overwrites_for(ctx.author) == CommonPermissions.available):
					await channel.set_permissions(ctx.author, overwrite=CommonPermissions.hidden)
		
		if (ctx.me.roles[1] > author_role):
			await ctx.author.remove_roles(author_role)
	
	# Add roles
	await ctx.author.add_roles(teacherRole)
	if (periodChannel != None):
		await periodChannel.set_permissions(ctx.author, overwrite=CommonPermissions.available)
	await ctx.send(f"You joined {teacher}'s class!")


@bot.command()
@commands.has_role("admin")
async def add(ctx, teacher):
	await add_teacher(ctx.guild, teacher)
	await ctx.send(f"Teacher added!")

@bot.command()
@commands.has_role("admin")
async def remove(ctx, *, category):	
	if (await remove_category(ctx.guild, category) != 0):
		await ctx.send("Category doesn't exist")
	else:
		await ctx.send("Category deleted")

@bot.listen()
async def on_ready():
	print(f"We logged in as: {bot.user}")

bot.run(token)
