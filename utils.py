import discord
import time

POSITIVE = "<:positive:715519331655483462>"
NEGATIVE = "<:negative:715519331768729684>"

COLOR_DEFAULT = 0x8a4cfc
COLOR_EMBED   = 0x2f3136
COLOR_ERROR   = 0xf44336
COLOR_WARN    = 0xffd045
COLOR_COVID   = 0x4caf4f


def calctime(func, *args, **kwargs):
    s = time.time()
    r = func(*args, **kwargs)
    return time.time()-s, r

def get_user(guild, arg):
    # guild -> discord.Guild
    # arg   -> user mention string
    # arg   -> user ID
    # arg   -> username / username#discriminator

    if isinstance(arg, discord.User) or isinstance(arg, discord.Member):
        return arg
    else:
        if arg.startswith("<@!"):
            id = int(arg.replace("<", "").replace(">", "").replace("@", "").replace("!", ""))
            user = guild.get_member(id)
            if user: return user
        try:
            user = guild.get_member(int(arg))
            if user: return user
        except:
            argl = arg.lower()
            for member in guild.members:
                if member.name.lower() == argl or str(member).lower() == argl or argl in member.name.lower():
                    return member

def is_dev(user):
    # user -> discord.User

    if user.id in (311542309252497409,):
        return True

async def feed_error(exception, client, message, args, prefix):
    await message.channel.send(f"Komut çalıştırılırken bir hata meydana geldi: `{exception}`")
    print(f"Hata: {str(message.author)} > {prefix}avatar {' '.join(args)} => {exception}")
