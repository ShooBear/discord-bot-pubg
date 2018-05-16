from pubg_python import PUBG, Shard

import requests

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNTYwNzQ0MC0zNjViLTAxMzYtMjVjNy0wMDg1ZmQ1NjFmZDAiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI1OTQxMzU3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFwaV90ZXN0Iiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.V51tutepJSpIqkMnDtc4clfP1PAvFMztmcLgA5xD1Q0'

api = PUBG(token, Shard.PC_KAKAO)
headers = {
    'Accept': 'application/vnd.api+json',
    'Authorization': 'Bearer ' + token,
}

def sample_matches():
    sample = api.samples().filter(created_at_start='2018-05-04T00:00:00Z').get()
    for match in sample.matches:
        print(match.id)

def sample_players():
    players = api.players().filter(player_names=['Shoo-Bear', 'kakao_fashgo'])

    for player in players:
        player_id = player.id
        print(player_id)


def test():
    players = api.players().filter(created_at_start='2018-05-12T00:00:00Z', player_names=['kakao_fashgo'])
    player = players[0]
    print(player.matches)
    match = api.matches().get(player.matches[0].id)
    print(match.game_mode)

    roster = match.rosters[0]
    for roster in match.rosters:
        for participant in roster.participants:
            if participant.attributes['stats']['name'] == 'kakao_fashgo':
                my_team = roster
                break

    participant = roster.participants[0]
    print(participant.name)

def proto_type_pubg(id):
    player_list = ['kakao_fashgo', 'Shoo-Bear', 'Big__Ssong', 'Beom-Tiger']
    player_dict = dict()
    for player in player_list:
        player_dict[player] = {
            'kill': list(),
            'death': list()
        }

    players = api.players().filter(player_names=[id])
    player = players[0]
    match = api.matches().get(player.matches[0].id)
    matchid = match._data['id']
    match = api.matches().get(matchid)
    asset = match.assets[0]
    print(asset.url)
    telemetry = api.telemetry(asset.url)
    death_event = list()
    for event in telemetry.events:
        try:
            if event.event == 'LogPlayerKill':
                death_event.append(event)
        except Exception:
            pass

    for kill in death_event:
        if kill.killer.name in player_list:
            who = is_who(kill.victim.account_id, kill.killer.name, kill.victim.name, 'kill')
            if player_dict.get(kill.killer.name):
                player_dict[kill.killer.name]['kill'].append(who)

        if kill.victim.name in player_list:
            who = is_who(kill.killer.account_id, kill.killer.name, kill.victim.name, 'death')
            if player_dict.get(kill.victim.name):
                player_dict[kill.victim.name]['death'].append(who + " 그놈의 남은 피는 " + str(kill.killer.health))
    displayer_str = str()

    for k, v in player_dict.items():
        if len(player_dict[k]['kill']) == 0 and len(player_dict[k]['death']) == 0:
            continue
        displayer_str += k + ' Result!!\n'
        displayer_str += '\n'.join(player_dict[k]['kill'])
        displayer_str += '\n'
        displayer_str += '\n'.join(player_dict[k]['death'])
        displayer_str += '\n\n'
    return displayer_str.replace('_', '\_')

def is_who(accountid, killer, victim, type):
    try:
        seasonid = 'division.bro.official.2018-05'
        url_fmt = 'https://api.playbattlegrounds.com/shards/{region}/players/{accountid}/seasons/{seasons}'
        url = url_fmt.format(region='pc-kakao', accountid=accountid, seasons=seasonid)
        ret = requests.get(url, headers=headers)
        data = ret.json()
        stat = data['data']['attributes']['gameModeStats']['squad']
        KD = round(stat['kills'] / stat['losses'], 2)
        rating = round(stat['winPoints'])
        played = stat['roundsPlayed']
        top10 = round(stat['top10s'] / played * 100)
        win = round(stat['wins'] / played * 100)
        headshot = round(stat['headshotKills'] / stat['kills'] * 100, 1)
        avgdeal = round(stat['damageDealt'] / played)
        avgboost = round(stat['boosts'] / played, 1)
        yupo = stat['roundMostKills']
        avgheal= round(stat['heals'] / played, 1)
        avgplaytime_squad = round(stat['timeSurvived']/60/60/stat['days'], 1)
        ret_str_fmt = "[{rating}] Win: {win}% Top10: {top10}% KD: {KD} HeadShot: {headshot}% avgDeal: {avgDeal}"
        ret_str = ret_str_fmt.format(rating=rating, KD=KD, win=win, top10=top10, headshot=headshot, avgDeal=avgdeal)
        if type == 'kill':
            title_str = "{killer} 가 ".format(killer=killer)
        else:
            title_str = str()

        if headshot > 35:
            title_str = title_str + '헤드샷을 잘박는 '
        if avgdeal > 250:
            title_str = title_str + '딜({avgdeal})좀 하는 '.format(avgdeal=avgdeal)
        if yupo > 7:
            title_str = title_str + '여포({yupo})를 해본 '.format(yupo=yupo)
        if avgboost > 2:
            title_str = title_str + '드링크({avgboost})를 좋아하는 '.format(avgboost=avgboost)
        if avgheal > 3:
            title_str = title_str + '구상({avgheal})을 잘쓰는 '.format(avgheal=avgheal)
        if avgplaytime_squad > 3:
            title_str = title_str + '하루에 {avgplaytime}시간을 하는 '.format(avgplaytime=avgplaytime_squad)
        if KD > 2:
            title_str = title_str + str(round(KD)) + "인분은 하는 고수 "
        else:
            title_str = title_str + str(round(KD)) + "인분 하는 배린이 "
        if type == 'kill':
            title_str = title_str + victim + " 을 죽였습니다"
        else:
            title_str = title_str + "[{killer}] 이 [{victim}]을 죽였습니다".format(killer=killer, victim=victim)
    except Exception:
        title_str = "[{type}] 결과를 가져오는데 실패했당".format(type=type)
    return title_str

#stat = is_newbie('account.25198e0127704d85896cddbd0af0a7f1')
#ret = proto_type_pubg('Big__Ssong')
#print(ret)