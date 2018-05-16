# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import time
from test_pubgy import proto_type_pubg

TOKEN = 'NDM3OTcyNTU3NTYwNDE0MjE4.Dd0fzQ.lrM0MBAujgkQlCmLg_LN5BFamjM'

client = discord.Client()

player_list = ['kakao_fashgo', 'Shoo-Bear', 'Big__Ssong', 'Beom-Tiger']

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!까보까'):
        msg = 'Hello {0.author.mention}'.format(message)
        try:
            leaderid = message.content.split()[1]
            if leaderid not in player_list:
                leaderid = 'Big__Ssong'
        except Exception:
            leaderid = 'Big__Ssong'
        title = proto_type_pubg(leaderid)
        await client.send_message(message.channel, title)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
