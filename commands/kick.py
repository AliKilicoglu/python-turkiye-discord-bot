import utils


async def run(client, message, args, prefix):
    if message.author.guild_permissions.kick_members:

        if len(args) == 0:
            raise Exception("Bu komut en az bir argüman alır")

        uye = utils.get_user(message.guild, args[0])
        if not uye: raise Exception(f"Üye '{args[0]}' bulunamadı")

        try:
            await uye.kick()
            await message.channel.send(f"{uye.mention} kullanıcısı sunucudan atıldı.")
        except: pass

    else:
        raise Exception("Bu komutu kullanmak için gerekli yetkiye sahip değilsin")
