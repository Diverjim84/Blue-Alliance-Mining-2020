import json
import requests
import operator
import pandas as pd
import re

myToken = 'URGab8tLhUZabkbIiBVGOjmKiyqlAmLO6Nqh4vc5DmqcGAC0XSDSBgQ3bnsu2nLf'
baseURL = 'https://www.thebluealliance.com/api/v3/'
eventKey = '2018roe'

#event/2018alhu/matches/keys

rURL = baseURL+'event/'+eventKey+'/teams/keys'

#print(rURL)

headers = {'accept': 'application/json',

          'X-TBA-Auth-Key': myToken}

r = requests.get(rURL, headers)

#print(r.status_code)
if r.status_code == 200:
    teams = json.loads(r.content)
    print(teams)
else:
    print('crap!')

#Get list of events
rURL = baseURL+'events/2018'
r = requests.get(rURL, headers)

if r.status_code == 200:
     events = json.loads(r.content)
     events_df = pd.DataFrame(events)
     events_df = events_df[['key','event_type_string', 'week', 'start_date']]
     events_df.set_index('key', inplace=True)
else:
    print('crap!')

team_event_results = []

#print(events_df.loc['2018gacmp']['week'])

matches = []

for team in teams:
    print('working on team: ', team)

    rURL = baseURL+'team/'+team+'/matches/2018'

    r = requests.get(rURL, headers)

    if r.status_code == 200:
        team_matches = json.loads(r.content)

        for m in team_matches:
            match = {}
            match['team'] = team
            try:
                match['event'] = m['event_key']
                match['match'] = m['key']
                match['comp_level'] = m['comp_level']
                match['match_number'] = m['match_number']
                match['time'] = m['time']

                if (team in m['alliances']['blue']['team_keys']) or \
                        (team in m['alliances']['blue']['surrogate_team_keys']) :
                    scores = str(m['alliances']['blue']['score']) + ' to ' + str(m['alliances']['red']['score'])
                    if m['winning_alliance'] == 'blue':
                         match['result'] = 'win ' + scores
                    else:
                        match['result'] = 'loss ' + scores
                    #match['alliance'] = m['alliances']['blue']['team_keys']
                    match['Robot1'] = m['alliances']['blue']['team_keys'][0]
                    match['Robot2'] = m['alliances']['blue']['team_keys'][1]
                    match['Robot3'] = m['alliances']['blue']['team_keys'][2]
                    for key, value in m['score_breakdown']['blue'].items():
                        match[key] = value
                elif (team in m['alliances']['red']['team_keys']) or \
                        (team in m['alliances']['red']['surrogate_team_keys']) :
                    scores = str(m['alliances']['red']['score']) + ' to ' + str(m['alliances']['blue']['score'])
                    if m['winning_alliance'] == 'red':
                         match['result'] = 'win ' + scores
                    else :
                        match['result'] = 'loss ' + scores
                    match['Robot1'] = m['alliances']['red']['team_keys'][0]
                    match['Robot2'] = m['alliances']['red']['team_keys'][1]
                    match['Robot3'] = m['alliances']['red']['team_keys'][2]
                    for key, value in m['score_breakdown']['red'].items():
                        match[key] = value
                else:
                    match['result'] = 'Disqualified'
                    #match['alliance'] = ['dq']
                    match['Robot1'] = ''
                    match['Robot2'] = ''
                    match['Robot3'] = ''
                    for key, value in m['score_breakdown']['red'].items():
                        if type(value) is int:
                            match[key] = 0
                        elif type(value) is str:
                            match[key] = ''
                        elif type(value) is bool:
                            match[key] = False
                        else:
                            match[key] = value
                youtube = ''
                for v in m['videos']:
                    if v['type'] == 'youtube':
                        if  youtube == '':
                            youtube = 'https://youtu.be/' + v['key']
                        else:
                            youtube = youtube + ' ; ' + 'https://youtu.be/' + v['key']
                match['video'] = youtube
                matches.append(match)
            except:
                print('\n\n\n')
                print('error on: ', team)
                print(m)
            #print(match)
    else:
        print('crap!')

cols = ['team',
        'event',
        'match',
        'comp_level',
        'match_number',
        'time',
        'result',
        'Robot1',
        'Robot2',
        'Robot3',
        'adjustPoints',
        'autoOwnershipPoints',
        'autoPoints',
        'autoQuestRankingPoint',
        'autoRobot1',
        'autoRobot2',
        'autoRobot3',
        'autoRunPoints',
        'autoScaleOwnershipSec',
        'autoSwitchAtZero',
        'autoSwitchOwnershipSec',
        'endgamePoints',
        'endgameRobot1',
        'endgameRobot2',
        'endgameRobot3',
        'faceTheBossRankingPoint',
        'foulCount',
        'foulPoints',
        'rp',
        'tba_gameData',
        'techFoulCount',
        'teleopOwnershipPoints',
        'teleopPoints',
        'teleopScaleBoostSec',
        'teleopScaleForceSec',
        'teleopScaleOwnershipSec',
        'teleopSwitchBoostSec',
        'teleopSwitchForceSec',
        'teleopSwitchOwnershipSec',
        'totalPoints',
        'vaultBoostPlayed',
        'vaultBoostTotal',
        'vaultForcePlayed',
        'vaultForceTotal',
        'vaultLevitatePlayed',
        'vaultLevitateTotal',
        'vaultPoints',
        'video']

#print(pd.DataFrame(matches).columns.values)
df = pd.DataFrame(matches)

df.sort_values(by =['team','time'], ascending=[True,False], inplace=True)

df.to_csv('Roe_Team_Match_History.csv',
          columns=cols,
          line_terminator = '\r\n',
          index=False)


'''
ter_df = pd.DataFrame(team_event_results)
ter_df.sort_values(by=['team','week'])

print(ter_df.columns.values)
csvHeader = ['team',
             'week',
             'event',
             'rank',
             'Overall_Result_Text',
             'Plyoff_Result_Text',
             'plyoff_team',
             'plyoff_pick',
             'plyoff_record',
             'quals_record',
             'quals_matchs',
             'quals_size',
             'quals_dqs',
             'quals_avg_rp',
             'quals_total_endgame_points',
             'quals_total_auto_points',
             'quals_total_ownership_points',
             'quals_total_vault_points']

ter_df.to_csv('REO_Team_Event_Results.csv',
              columns=csvHeader,
              line_terminator = '\r\n',
              index=False)
'''
'''  
#Get matches
rURL = baseURL+'team/'+teams[0]+'/matches/2018'

headers = {'accept': 'application/json',

          'X-TBA-Auth-Key': myToken}

r = requests.get(rURL, headers)

#print(r.status_code)

if r.status_code == 200:
 team_matches = json.loads(r.content)
 print('\n\n\n')
 print(team_matches[0])
else:
 print('crap!')

'''

#extract match data
#print(events[0]['alliances']['blue']['team_keys'])

'''
event = events[0]

ourEvents= []

for event in events:
 match = {}
 match['actual_time'] = event['actual_time']
 match['event_key'] = event['event_key']
 match['match_key'] = event['key']
 match['match_type'] = event['comp_level']
 match['match_number'] = event['match_number']

 if 'frc3959' in event['alliances']['blue']['team_keys']:
   match['our_color'] = 'blue'
   match['our_time'] = 15-event['score_breakdown']['blue']['autoSwitchOwnershipSec']
   match['game_data'] = event['score_breakdown']['blue']['tba_gameData']

   #print("autoSwitchTime: "+str(events[0]['score_breakdown']['blue']['autoSwitchOwnershipSec']))
   #print("tba_gameData: "+str(events[0]['score_breakdown']['blue']['tba_gameData']))

 elif 'frc3959' in event['alliances']['red']['team_keys']:
   match['our_color'] = 'red'
   match['our_time'] = 15-event['score_breakdown']['red']['autoSwitchOwnershipSec']
   match['game_data'] = event['score_breakdown']['red']['tba_gameData']

 else:
   print("none")

 ourEvents.append(match)

ourEvents.sort(key=operator.itemgetter("actual_time"))

print(ourEvents)
'''


