import requests

team_id = "2305"

class ESPNAPIManager:
    def GetSchedule(endpoint, sport):
        schedule = requests.get(endpoint).json()
        summary = []
        initial = schedule['team']['seasonSummary']
        initial += " " + schedule['team']['displayName'] + f" {sport} schedule"
        summary.append(initial)
        for game in schedule['events']:
            home_away = ""
            opponent = ""
            team_score = ""
            opponent_score = ""
            w_l = ""
            string = game['week']['text'] + ": "
            # Get info about every game
            for competitor in game['competitions'][0]['competitors']:
                # Get info about opponent first
                if competitor['id'] != team_id:
                    opponent = competitor['team']['displayName']
                    # Check if the game is finished
                    if 'winner' in competitor.keys():
                        opponent_score = competitor['score']['displayValue']
                        if competitor['winner']:
                            w_l = "L"
                        else:
                            w_l = "W"
                    if competitor['homeAway'] == "away" or game['competitions'][0]['neutralSite']:
                        home_away = "vs."
                    else:
                        home_away = "at"
                # Finally, get the home team's score
                else:
                    # Check if the game is finished
                    if 'winner' in competitor.keys():
                        team_score = competitor['score']['displayValue']
            string += f"{home_away} {opponent}"
            if w_l != "":
                string += f" ({w_l} {team_score}-{opponent_score})"
            summary.append(string)
        return summary

    # Grabs CFB stats from ESPN and returns them as a dict
    def UpdateCFBStats():
        team = requests.get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}').json()
        schedule = requests.get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}/schedule').json()
        win = int(team['team']['record']['items'][0]['stats'][19]['value'])
        loss = int(team['team']['record']['items'][0]['stats'][10]['value'])
        conf_win = ""
        conf_loss = ""
        most_recent = len(schedule['events'])
        # Yes, this sucks. I know. But really, it's ESPN's fault for not putting conference W/L in team info...
        last_game = ""
        for i in range(1, most_recent, 1):
            if schedule['events'][most_recent - i]['competitions'][0]['status']['type']['name'] == "STATUS_FINAL":
                for d in schedule['events'][most_recent - i]['competitions'][0]['competitors']:
                    if d['id'] == str(team_id):
                        conf_wl = d['record'][1]['displayValue'].split("-")
                        conf_win = conf_wl[0]
                        conf_loss = conf_wl[1]
                        if d['winner'] is True:
                            last_game += "W "
                        else:
                            last_game += "L "
                        last_game += d['score']['displayValue'] + "-"
                        for e in schedule['events'][most_recent - i]['competitions'][0]['competitors']:
                            if e['id'] != str(team_id):
                                last_game += e['score']['displayValue']
                                last_game += " vs. "
                                last_game += e['team']['displayName']
                return({"wins": win, "losses": loss, "conf_wins": conf_win, "conf_losses": conf_loss, "last_game": last_game})

    # Returns the CFB schedule as a list
    def CFBSchedule():
        endpoint = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}/schedule"
        return ESPNAPIManager.GetSchedule(endpoint, "football")

    # Grabs men's CBB stats from ESPN and returns them as a dict
    def UpdateMensCBBStats():
        team = requests.get(f'https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}').json()
        schedule = requests.get(f'https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule').json()
        win = int(team['team']['record']['items'][0]['stats'][18]['value'])
        loss = int(team['team']['record']['items'][0]['stats'][9]['value'])
        conf_win = ""
        conf_loss = ""
        most_recent = len(schedule['events'])
        # You know, someday I'll fix that there's a lot of duplicated code here.
        last_game = ""
        for i in range(1, most_recent, 1):
            if schedule['events'][most_recent - i]['competitions'][0]['status']['type']['name'] == "STATUS_FINAL":
                for d in schedule['events'][most_recent - i]['competitions'][0]['competitors']:
                    if d['id'] == str(team_id):
                        conf_wl = d['record'][1]['displayValue'].split("-")
                        conf_win = conf_wl[0]
                        conf_loss = conf_wl[1]
                        if d['winner'] is True:
                            last_game += "W "
                        else:
                            last_game += "L "
                        last_game += d['score']['displayValue'] + "-"
                        for e in schedule['events'][most_recent - i]['competitions'][0]['competitors']:
                            if e['id'] != str(team_id):
                                last_game += e['score']['displayValue']
                                last_game += " vs. "
                                last_game += e['team']['displayName']
                return({"wins": win, "losses": loss, "conf_wins": conf_win, "conf_losses": conf_loss, "last_game": last_game})

    # Returns the CFB schedule as a list
    def MensCBBSchedule():
        endpoint = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule"
        return ESPNAPIManager.GetSchedule(endpoint, "men's basketball")