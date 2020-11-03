import discord
from libs import restdb

async def run(client, message, args, prefix):
    userdict = dict()
    for user in restdb.userlist:
        if user.discord:
            userdict[user] = user.xp

    sortdict = [k for k, v in sorted(userdict.items(), key=lambda item: item[1])]

    embed = discord.Embed(color=0x609ee0)

    for i, u in enumerate(list(reversed(sortdict))[:15]):
        if i == 0:
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
            embed.add_field(name=f"1# {u.discord.name} :first_place:", value=f"Level: `{u.calc_level()}` Toplam XP: `{u.xp}`\n឵឵឵ ឵឵឵", inline=True)
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
        elif i == 1:
            embed.add_field(name="឵឵", value="឵឵\n ", inline=True)
            embed.add_field(name=f"2# {u.discord.name} :second_place:", value=f"Level: `{u.calc_level()}` Toplam XP: `{u.xp}`\n឵឵឵ ", inline=True)
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
        elif i == 2:
            embed.add_field(name="឵឵", value="឵឵\n ", inline=True)
            embed.add_field(name=f"3# {u.discord.name} :third_place:", value=f"Level: `{u.calc_level()}` Toplam XP: `{u.xp}`\n឵឵឵ ", inline=True)
            embed.add_field(name="឵឵", value="឵឵\n឵឵឵ ឵឵឵", inline=True)
        else:
            embed.add_field(name=f"{i+1}# {u.discord.name}", value=f"Level: `{u.calc_level()}` Toplam XP: `{u.xp}`\n឵឵឵ ", inline=True)

    await message.channel.send(embed=embed)
