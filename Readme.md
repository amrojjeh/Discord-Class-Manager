# Discord Class Manager
Due to the corona virus, my high school decided to make the switch to online schooling until April 13.
So to compensate, I made a Discord class server so that the students could at least keep an ongoing interaction.

## Crappy Code
Yes, the code crappy, and yes, I did spend a night on it to just get it work.
I originally just intended the bot to make text-channels for each period and class, and make them private to those who join them. Nothing else.
However, if this gets enough attention, I might re-write it and add support for things such as Canvas or remind for example. But since I don't intend to do that currently, the code will remain as it is, crappy and in a single file.

Feel free to fork it though!


## Usage
If you're the owner of the server, here's how you add teachers:
!add TEACHER

If you want to remove a category:
!remove CATEGORY

Note that there isn't a function to remove a teacher, I didn't bother writing it since I'll probably never be removing teachers. But for testing I needed to remove categories, so there's that. Though it won't remove the roles created.

**Since the bot removes all the roles the student has when it joins a class, make sure to have the roles you want to preserve above the bot's role in the heirarchy.**

If you want to join a class:
!join TEACHER [PERIOD]

Ex: !join Mark p4

## Good luck!
Even though my school has made the swtich to online, that doesn't mean the situation here is bad, just means that we're preventing it from becoming so. If you're being affected by the corona virus, then I wish you luck and good fortune.

## Update and technicalities
I ended up updating the code, so now the code should be much better. I also changed how the bot works, so I thought I'd share that info.

There are two things you need to know. First, a teacher to this bot is just a role that also has a category with the same name. The second thing, is that there are two used permissions overwrites, the hidden and available overwrites.
The hidden overwrite makes a channel not visible to everyone, the available overwrite makes it visible to a subset of everyone.

So when a teacher is created, which it can only be created by the admin role, the bot creates a category and a role with the same name, unless they already exist. Then it fills the category with the appropriate channels. Note that the category is *not* private, but the channels are. Everyone with the teacher role has access to general and Classroom, but nothing else in that category.

Now when someone joins a class, assuming the teacher exists, meaning that there is a role and a category with the same name, it will first assign the user with the role, so that s/he has access to general and Classroom. It will then add the available overwrite permission just for the user, but before it does that, the bot also removes all previous roles it can, even if it's not a teacher. **So make sure you have the roles you want to preserve above the bot's role**. The bot will also go back to the old teacher the user had and look for the available overwrite and replace it with the hidden overwrite, so that the user no longer has access to his previous class.

The remove functionality just removes a category without removing the teacher role.
