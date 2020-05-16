# Discord Class Manager
Due to the corona virus, my high school decided to make the switch to online schooling until April 13.
So to compensate, I made a Discord class server so that the students could at least keep an ongoing interaction.

## Crappy Code
Yes, the code crappy, and yes, I did spend a night on it to just get it work.
I originally just intended the bot to make text-channels for each period and class, and make them private to those who join them. Nothing else.
However, if this gets enough attention, I might re-write it and add support for things such as Canvas or remind for example. But since I don't intend to do that currently, the code will remain as it is, crappy and in a single file.

Feel free to fork it though!

## Adding bot
Since I don't have a server, and even if I did, I wouldn't use it to host other people's bots, you're going to have to create a discord bot application. After that, discord will give you a token, and you just put that in token.txt. Pretty simple.

## Usage
If you want to join a class:
!join TEACHER PERIOD

Ex: !join Mark p4

Joining a class will assign the teacher, the period, and the subject taught at that class.

To leave a class (this is automatically done when joining a class:
!leave

**Since the bot removes all the roles the student has when they join a class, make sure to have the roles you want to preserve above the bot's role in the heirarchy.**

## Good luck!
Even though my school has made the swtich to online, that doesn't mean the situation here is bad, just means that we're preventing it from becoming so. If you're being affected by the corona virus, then I wish you luck and good fortune.

## Update and technicalities
I ended up updating the code, so now the code should be much better. I also changed how the bot works, so I thought I'd share that info.

I've updated once again, this time completely removing the categories. If you wish to keep that, then I suggest you download an old version. Here's what's changed:

- Categories and classrooms have been removed
- Roles are now just roles, they do nothing
- I've updated the format for the schedule. It's stored as usual in GUILD_NAME.txt and the format is:
```
TEACHER
	PERIOD SUBJECT
```
- Note the *tab* that comes before period and the space seperating period and subject. Empty lines are not allowed
- You cannot add teachers from discord. You have to manually update the .txt file and reset the bot.
	- I've decided not to add it since the syntax required would be too complicated.
- Seperated some functionality into classes

## Why?
Why have the classrooms been removed? They added a lot of complexity to the discord interface and they were rarely used. Perhaps they'd be more useful if you were a teacher and running classes in discord, but I'd advise against doing so also. Either way, if you wish to have classrooms back but with the updated format, just contact me at amrojjeh@outlook.com and I'll see what I can do. Alternatively, you can also just rollback to the previous commit and download the code and update it yourself.
