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
 #print('\n\n\n')
 #print(events[0])
 events_df = pd.DataFrame(events)
 #print('\n\n\n')
 include_events = ['Regional','District']
 events_df = events_df[['key','event_type_string', 'week', 'start_date']]
 events_df.set_index('key', inplace=True)
 #events_df = events_df[events_df['event_type_string'].isin(include_events)]
 #print(events_df.head())
else:
 print('crap!')

team_event_results = []

print(events_df.loc['2018gacmp']['week'])


for team in teams:
    print('working on team: ', team)

    rURL = baseURL+'team/'+team+'/events/2018/statuses'

    r = requests.get(rURL, headers)

    if r.status_code == 200:
        team_stat = json.loads(r.content)
        el = [*team_stat]

        for e in el:
            print('working on event: ', e)

            if e != '2018roe':
                team_event_result = {}
                team_event_result['team'] = team

                team_event_result['event'] = e
                team_event_result['week'] = events_df.loc[e]['week']
                team_event_result['Overall_Result_Text'] = re.sub('</b>','',re.sub('<b>','',team_stat[e]['overall_status_str']))
                team_event_result['Plyoff_Result_Text'] = re.sub('</b>','',re.sub('<b>','',team_stat[e]['alliance_status_str']))
                team_event_result['rank'] = team_stat[e]['qual']['ranking']['rank']

                if team_stat[e]['alliance_status_str'] != "--":
                    team_event_result['plyoff_team'] = team_stat[e]['alliance']['number']
                    team_event_result['plyoff_pick'] = team_stat[e]['alliance']['pick']
                    team_event_result['plyoff_record'] = str(team_stat[e]['playoff']['record'])
                else:
                    team_event_result['plyoff_team'] = -1
                    team_event_result['plyoff_pick'] = -1
                    team_event_result['plyoff_record'] = 'NA'

                team_event_result['quals_record'] = str(team_stat[e]['qual']['ranking']['record'])
                team_event_result['quals_size'] = team_stat[e]['qual']['num_teams']
                team_event_result['quals_dqs'] = team_stat[e]['qual']['ranking']['dq']
                team_event_result['quals_matchs'] = team_stat[e]['qual']['ranking']['matches_played']
                team_event_result['quals_avg_rp'] = team_stat[e]['qual']['ranking']['sort_orders'][0]
                team_event_result['quals_total_endgame_points'] = team_stat[e]['qual']['ranking']['sort_orders'][1]
                team_event_result['quals_total_auto_points'] = team_stat[e]['qual']['ranking']['sort_orders'][2]
                team_event_result['quals_total_ownership_points'] = team_stat[e]['qual']['ranking']['sort_orders'][3]
                team_event_result['quals_total_vault_points'] = team_stat[e]['qual']['ranking']['sort_orders'][4]

                team_event_results.append(team_event_result)

    else:
        print('crap!')

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


