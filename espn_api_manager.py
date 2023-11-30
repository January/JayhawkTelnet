import requests

team_id = 2305

class ESPNAPIManager:
    def UpdateCFBStats():
        team = requests.get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}').json()
        schedule = requests.get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}/schedule').json()
        win = int(team['team']['record']['items'][0]['stats'][19]['value'])
        loss = int(team['team']['record']['items'][0]['stats'][10]['value'])
        conf_win = ""
        conf_loss = ""
        most_recent = len(schedule['events'])
        # Yes, this sucks. I know. But really, it's ESPN's fault for not putting conference W/L in team info...
        # Also, it's only CFB that does this, as far as I know. It's readily available in CBB.
        last_game = ""
        for d in schedule['events'][most_recent - 1]['competitions'][0]['competitors']:
            if d['id'] == str(team_id):
                conf_wl = d['record'][1]['displayValue'].split("-")
                conf_win = conf_wl[0]
                conf_loss = conf_wl[1]
                if d['winner'] is True:
                    last_game += "W "
                else:
                    last_game += "L "
                last_game += d['score']['displayValue'] + "-"
                for e in schedule['events'][most_recent - 1]['competitions'][0]['competitors']:
                    if e['id'] != str(team_id):
                        last_game += e['score']['displayValue']
                        last_game += " vs. "
                        last_game += e['team']['displayName']
        return({"wins": win, "losses": loss, "conf_wins": conf_win, "conf_losses": conf_loss, "last_game": last_game})