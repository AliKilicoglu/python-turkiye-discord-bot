#               Python Türkiye Discord Botu
#                   Kadir Aksoy - 2020
# https://github.com/kadir014/python-turkiye-discord-bot


import os
import discord
import utils
from libs import restdb

intents = discord.Intents.all()
client = discord.Client(intents=intents)

prefix = "!"


############################################
#                                          #
#               EVENT İŞLEME               #
#                                          #
############################################


@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name=f"!yardım"))

    # Kullanıcıları veritabanından al
    sunucu = client.get_guild(617712082678448158)
    restdb.load_all()

    for user in restdb.userlist:
        u = sunucu.get_member(user.id)
        if u:
            user.discord = u

    print("\nKullanıcılar veritabanından alındı\n")
    print("Bot başarıyla giriş yaptı\n_________________________________\n")

@client.event
async def on_member_join(member):
    print(f"Kullanıcı giriş yaptı: {member.name}")

@client.event
async def on_guild_remove(member):
    print(f"Kullanıcı çıkış yaptı: {member.name}")


############################################
#                                          #
#               KOMUT İŞLEME               #
#                                          #
############################################


commands = list()

for (dirpath, dirnames, filenames) in os.walk("./commands"):
    for filename in filenames:
        if not filename[-3:] == '.py': continue
        commands.append(filename[:-3])

print("Yüklenen komutlar:")
for cmd in commands:
    print(f"  {cmd}")

@client.event
async def on_message(message):
    if message.author.bot: return
    elif isinstance(message.channel, discord.channel.DMChannel): return

    if message.content.startswith(prefix):
        cmd, args = message.content.split(" ")[0][len(prefix):], message.content.split(" ")[1:]

        if cmd in commands:
            cmdfile = __import__(f"commands.{cmd}", fromlist=[cmd])

            try:
                await cmdfile.run(client, message, args, prefix)
                await message.add_reaction(utils.POSITIVE)

            except Exception as e:
                await utils.feed_error(e, client, message, args, prefix)
                await message.add_reaction(utils.NEGATIVE)

        # DEBUGGING

        elif cmd == "ping":
            await message.channel.send(f"Pong! `{client.latency}`ms")

        elif cmd == "debug":
            if args[0] == "get_user":
                dt, user = utils.calctime(utils.get_user, message.guild, args[1])
                if user: await message.channel.send(f"`get_user` düzgün çalışıyor\nExecute time: {int(dt*1000)}ms\n@return -> discord.User({user.name}#{user.discriminator})")
                else: await message.channel.send(f"`get_user` düzgün çalışıyor\nExecute time: {int(dt*1000)}ms\n@return -> None")


client.run(os.environ["TOKEN"])
