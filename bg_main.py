import requests
import pprint
import os
import json

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNTYwNzQ0MC0zNjViLTAxMzYtMjVjNy0wMDg1ZmQ1NjFmZDAiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI1OTQxMzU3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImFwaV90ZXN0Iiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.V51tutepJSpIqkMnDtc4clfP1PAvFMztmcLgA5xD1Q0'

class Shoobear(object):
    def __init__(self):
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Authorization': 'Bearer ' + token,
        }
        self.telemetry_header = {
            'Accept': 'application/vnd.api+json',
        }

    def get_playerid_from_gameid(self, region, gameid):
        get_playerid_url_fmt = "https://api.playbattlegrounds.com/shards/{region}/players?filter[playerNames]={gameid}"
        playerid_url = get_playerid_url_fmt.format(region=region, gameid=gameid)
        ret = requests.get(playerid_url, headers=self.headers)
        data = ret.json()['data']
        account_id = data[0]['id']
        return account_id

    def get_match_info(self, region, matchid):
        get_matchinfo_url_fmt = "https://api.playbattlegrounds.com/shards/{region}/matches/{matchid}"
        match_url = get_matchinfo_url_fmt.format(region=region, matchid=matchid)
        ret = requests.get(match_url, headers=self.headers)
        data = json.loads(ret.text)
        return data

    def get_telemetry_info(self, region, date, assetid):
        get_telemetryinfo_url_fmt = "https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/{region}/{YYYY}/{MM}/{DD}/{hh}/{mm}/{assetid}-telemetry.json"
        telemetry_url = get_telemetryinfo_url_fmt.format(region=region,
                                                         YYYY=date['YYYY'],
                                                         MM=date['MM'],
                                                         DD=date['DD'],
                                                         hh=date['hh'],
                                                         mm=date['mm'],
                                                         assetid=assetid)
        ret = requests.get(telemetry_url, headers=self.headers)
        return ret



def main():
    player_list = ['kakao_fashgo', 'Shoo-Bear', 'Big__Ssong', 'Beom-Tiger']
    region = 'pc-kakao'

    sb = Shoobear()

    for player in player_list:
        account_id = sb.get_playerid_from_gameid(region, player)
        print(player + " : " + account_id)

    matchid = '58826862-3184-4b03-835f-1567bfe785ad'
    match_info = sb.get_match_info(region, matchid)
    print(match_info)
    #assetid = 'd47994dc-56c3-11e8-b29a-0a58647afd02'
    assetid = match_info['data']['relationships']['assets']['data'][0]['id']
    date = {
        'YYYY': '2018',
        'MM': '05',
        'DD': '13',
        'hh': '15',
        'mm': '6'
    }
    sb.get_telemetry_info(region, date, assetid)


if __name__=="__main__":
    main()