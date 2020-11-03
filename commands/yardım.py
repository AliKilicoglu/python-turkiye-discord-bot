async def run(client, message, args, prefix):
    r = "".join(open('data/yardim.txt', 'r', encoding="utf-8").readlines())
    await message.channel.send("```diff\n" + r + "\n```")
