import json
import requests
import operator
import matplotlib.pyplot as plt
import pandas as pd

myToken = 'URGab8tLhUZabkbIiBVGOjmKiyqlAmLO6Nqh4vc5DmqcGAC0XSDSBgQ3bnsu2nLf'
baseURL = 'https://www.thebluealliance.com/api/v3/'
eventKey = '2018alhu'

# event/2018alhu/matches/keys

# rURL = baseURL + 'event/' + eventKey + '/matches/keys'

# print(rURL)

# headers = {'accept': 'application/json',
#           'X-TBA-Auth-Key': myToken}

# r = requests.get(rURL, headers)

# print(r.status_code)

# if r.status_code == 200:
#  matches = json.loads(r.content)
# else:
#  print('crap!')

# Get 3959 matches

rURL = baseURL + 'team/frc3959/matches/2018'
headers = {'accept': 'application/json',
           'X-TBA-Auth-Key': myToken}
r = requests.get(rURL, headers)
# print(r.status_code)

if r.status_code == 200:
    events = json.loads(r.content)
else:
    print('crap!')

# extract match data
# print(events[0]['alliances']['blue']['team_keys'])

event = events[0]
ourEvents = []

#print(events[0])

for event in events:
    match = {}

    addit = True

    match['actual_time'] = event['actual_time']
    match['event_key'] = event['event_key']
    match['match_key'] = event['key']
    match['match_type'] = event['comp_level']
    match['match_number'] = event['match_number']

    if 'frc3959' in event['alliances']['blue']['team_keys']:
        match['our_color'] = 'blue'
        match['our_time'] = 15 - event['score_breakdown']['blue']['autoSwitchOwnershipSec']
        match['game_data'] = event['score_breakdown']['blue']['tba_gameData']
        # print("autoSwitchTime: "+str(events[0]['score_breakdown']['blue']['autoSwitchOwnershipSec']))
        # print("tba_gameData: "+str(events[0]['score_breakdown']['blue']['tba_gameData']))
        if not event['score_breakdown']['blue']['autoSwitchAtZero']:
            addit = False

    elif 'frc3959' in event['alliances']['red']['team_keys']:
        match['our_color'] = 'red'
        match['our_time'] = 15 - event['score_breakdown']['red']['autoSwitchOwnershipSec']
        match['game_data'] = event['score_breakdown']['red']['tba_gameData']
        if not event['score_breakdown']['red']['autoSwitchAtZero']:
            addit = False
    else:
        addit = False

    if addit:
        ourEvents.append(match)

ourEvents.sort(key=operator.itemgetter("actual_time"))

print(json.dumps(ourEvents, indent=1))

df = pd.DataFrame(ourEvents)

plt.figure(1)
plt.plot(df['our_time'], 'k-')
plt.show()
