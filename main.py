#               Python Türkiye Discord Botu
#                   Kadir Aksoy - 2020
# https://github.com/kadir014/python-turkiye-discord-bot


import os
import time
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
    utils.update_levels(sunucu)
    restdb.load_all()

    for user in restdb.userlist:
        u = sunucu.get_member(user.id)
        if u:
            user.discord = u

    #    eğer kullanıcı sunucuda değilse veritabanından sil
    #
    #    else:
    #        print(f"{user.id} (xp:{user.xp}) {u} sunucuda olmadığı için veritabanından silindi")
    #        user.delete()

    async for message in sunucu.get_channel(791005443833069569).history(limit=1):
        utils.SON_SAYI = int(message.content)

    print("\nVeritabanı belleğe alındı\n")
    print("Bot başarıyla giriş yaptı\n_________________________________\n")

@client.event
async def on_member_join(member):
    print(f"Kullanıcı giriş yaptı: {member.name}")
    restdb.new_user(member.id)

    r1 = member.guild.get_role(712997327513845822)
    r4 = member.guild.get_role(731954285595590678)
    r5 = member.guild.get_role(731954451782565900)
    try: await member.add_roles(r1)
    except: pass
    try: await member.add_roles(r4)
    except: pass
    try: await member.add_roles(r5)
    except: pass

@client.event
async def on_member_remove(member):
    print(f"Kullanıcı çıkış yaptı: {member.name}")
    restdb.userlist.get_by_userid(member.id).delete()


############################################
#                                          #
#               KOMUT İŞLEME               #
#                                          #
############################################


commands = list()
pass_cmds = ("say", "embed", "temizle")

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
                if cmd in pass_cmds: return
                await message.add_reaction(utils.POSITIVE)

            except Exception as e:
                await utils.feed_error(e, client, message, args, prefix)
                if cmd in pass_cmds: return
                await message.add_reaction(utils.NEGATIVE)

        # DEBUGGING

        elif cmd == "ping":
            await message.channel.send(f"Pong! `{client.latency}`ms")

        elif cmd == "debug":
            if args[0] == "get_user":
                dt, user = utils.calctime(utils.get_user, message.guild, args[1])
                if user: await message.channel.send(f"`get_user` düzgün çalışıyor\nExecute time: {int(dt*1000)}ms\n@return -> discord.User({user.name}#{user.discriminator})")
                else: await message.channel.send(f"`get_user` düzgün çalışıyor\nExecute time: {int(dt*1000)}ms\n@return -> None")

    else:
        # SAYI SAYMA OYUNU
        if message.channel.id == 791005443833069569:
            if message.content.isdigit():
                if int(message.content) == utils.SON_SAYI + 1:
                    utils.SON_SAYI = int(message.content)

                else:
                    try: await message.author.send(f"Sayı sayma oyununda girmeniz gereken sayı `{utils.SON_SAYI + 1}` iken siz `{int(message.content)}` girdiniz.")
                    except: pass
                    await message.delete()
                    return
            else:
                try: await message.author.send(f"Lütfen sayı sayma oyununda sayı kullanınız.")
                except: pass
                await message.delete()
                return

        # KELİME TÜRETMECE OYUNU
        elif message.channel.id == 791005667056943105:
            pass

        # NORMAL MESAJ
        else:
            if not (message.author.id in utils.SON_MESAJLAR): utils.SON_MESAJLAR[message.author.id] = time.time()
            if time.time() - utils.SON_MESAJLAR[message.author.id] < 5: return

            user = restdb.userlist.get_by_userid(message.author.id)
            if not user:
                restdb.new_user(message.author.id)
                user = restdb.userlist.get_by_userid(message.author.id)

            xp = restdb.userlist.get_by_userid(message.author.id)

            inc = len(message.content.replace(" ", "")) / 20
            if inc <= 1: inc = 1
            else: inc = int(inc)

            user.xp += inc
            user.update()

            if user.level_updated:
                user.level_updated = False

                await utils.update_level_role(message.author, user.level)

            utils.SON_MESAJLAR[message.author.id] = time.time()


utils.LOGTIME = time.time()
client.run(os.environ["TOKEN"])
