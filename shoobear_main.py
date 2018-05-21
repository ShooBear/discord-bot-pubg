# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import time
from test_pubgy import proto_type_pubg

TOKEN = 'NDM3OTcyNTU3NTYwNDE0MjE4.Dd0fzQ.lrM0MBAujgkQlCmLg_LN5BFamjM'

player_list = ['kakao_fashgo', 'Shoo-Bear', 'Big__Ssong', 'Beom-Tiger',
               'Big-_-Ssong', 'ShooBear', 'fashgo', 'Beom_Tiger']
region = 'steam'
leader = 'Big-_-Ssong'
client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!서버변경'):
        global region
        if region == 'steam':
            region = 'kakao'
        elif region == 'kakao':
            region = 'steam'
        msg = "[!] 변경 되었습니다. 현재 서버는 {region} 입니다.".format(region=region)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!사용자변경'):
        try:
            global leader
            old_leader = leader
            new_leader = message.content.split()[1]
            if new_leader in player_list:
                leader = new_leader
                msg = "[!] 변경 되었습니다. 현재 검사대상은 {leader} 입니다.".format(leader=leader)
            else:
                msg = "검사대상 변경에 실패하였습니다. 현재 검사 대상은 {leader} 입니다.".format(leader=old_leader)
            await client.send_message(message.channel, msg)
        except Exception as e:
            await client.send_message(message.channel, str(e))


    if message.content.startswith('!확인'):
        msg = "서버 : {server} 유저 : {user}".format(server=region, user=leader)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!쳌'):
        try:
            title = proto_type_pubg(leader, region)
            await client.send_message(message.channel, str(title))
        except Exception as e:
            await client.send_message(message.channel, str(e))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
