import requests
import dotenv
import os
from pprint import pprint
from datetime import datetime, date, time, timedelta, timezone

dotenv.load_dotenv()
TOKEN = os.environ.get("PANDA_TOKEN")

def generate_24_hour_window():
    today = datetime.now(timezone.utc)
    tomorrow = today + timedelta(days=1)

    return (today.isoformat(), tomorrow.isoformat())


headers = {"Authorization" : f"Bearer {TOKEN}"}

r = requests.get(
    url='https://api.pandascore.co/csgo/matches/upcoming',
    headers=headers,
    params = {
        'per_page' : 100,
        'range[begin_at]' : ', '.join(generate_24_hour_window()),
    }
)

res = r.json()

games_to_show = [game for game in res if game['serie']['tier']=='a' or game['serie']['tier']=='s']
# pprint(games_to_show[0])
display = [{ 
    'tournament' : game['serie']['full_name'], 
    'game_name' : game["name"],
    'game_time' : game["begin_at"] 
    } for game in games_to_show]

for item in display:
    print('Tournament: ', item['tournament'])
    print(item['game_name'])
    print('Game starts at ', datetime.fromisoformat(item['game_time'][:-1]))