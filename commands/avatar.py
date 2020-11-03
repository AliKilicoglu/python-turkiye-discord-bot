import discord
import utils

async def run(client, message, args, prefix):
    if len(args) == 0:
        embed = discord.Embed(description=f"{user.mention} avatarı", color=utils.COLOR_EMBED)
        embed.set_image(url=user.avatar_url)

        await message.channel.send(embed = embed)

    else:
        user = utils.get_user(message.guild, args[0])
        if not user:
            await message.channel.send(f"`{args[0]}` adlı kullanıcı bulunamadı.")
            await message.add_reaction(utils.NEGATIVE)
            return

        embed = discord.Embed(description=f"{user.mention} avatarı", color=utils.COLOR_EMBED)
        embed.set_image(url=user.avatar_url)

        await message.channel.send(embed = embed)
