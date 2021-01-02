import discord
import utils
from libs import restdb
from libs import imgp


async def run(client, message, args, prefix):
    if len(args) == 0:
        user_dc = message.author

    else:
        user_dc = utils.get_user(message.guild, args[0])
        if not user_dc: raise Exception(f"Üye '{args[0]}' bulunamadı")

    user = restdb.userlist.get_by_userid(user_dc)
    if not user:
        restdb.new_user(user_dc.id)
        user = restdb.userlist.get_by_userid(user_dc.id)

    await imgp.profil_yap(user_dc, user)

    await message.channel.send(file=discord.File(f"data/profile.png"))
