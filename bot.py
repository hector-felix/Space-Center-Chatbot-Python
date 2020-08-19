import discord

#id = 720904838803619910

token = "NzIwOTAyMzE1MTk1NzYwNjYw.XuMvow.tS-3plkntnm7ymXeIPNB-SopAtc"

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.find("!hello") != -1:
        await message.channel.send("Hiya")

client.run(token)

