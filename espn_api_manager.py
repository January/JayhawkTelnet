import requests

team_id = 2305

class ESPNAPIManager:
    #def UpdateCFBStats(win, loss, conf_win, conf_loss, last_game, next_game):
    def UpdateCFBStats():
        team = requests.get(f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}').json()
        print(int(team['team']['record']['items'][0]['stats'][19]['value']))
        print(int(team['team']['record']['items'][0]['stats'][10]['value']))


ESPNAPIManager.UpdateCFBStats()