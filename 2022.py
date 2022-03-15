from pprint import pprint

import TBA_Tools as tba
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

today = date.today()

def GetEvents():
    EventList = pd.DataFrame(tba.GetEventList(tba.curyear))
    EventList.to_csv("2022_EventList.csv", columns=EventList.columns.values, line_terminator = '\r\n', index=False)


def GetAllMatches():
    EventList = pd.read_csv("2022_EventList.csv")
    r = EventList[['key','name', 'start_date','end_date','city','country','event_type']]

    #Events = []
    AllMatches = []

    for idx, row in r.iterrows():
        #print(row['start_date'])
        if datetime.strptime(row['start_date'],'%Y-%m-%d') <= datetime.today():
            Matches = tba.GetEventMatchesVerbose(row['key'])
            for match in Matches:
                if match['actual_time'] is not None:
                    try:
                        AllMatches.append(FlattenMatch(match))
                    except:
                        print("********Match Failed*********")
                        pprint(match)
                        print('*****************************')

    df = pd.DataFrame(AllMatches)
    #print(AllMatches)
    df.to_csv("2022_Matches.csv", columns=df.columns, line_terminator = '\r\n', index=False)

def FlattenMatch(match):
    Match = {}
    Match['key'] = match['key']
    Match['event_key'] = match['event_key']

    Match['comp_level'] = match['comp_level']

    winner = match['winning_alliance']
    loser = ''
    if winner == 'red':
        loser = 'blue'
    else:
        winner = 'blue'
        loser = 'red'

    Match['w_score'] = match['alliances'][winner]['score']
    Match['l_score'] = match['alliances'][loser]['score']
    Match['w_autoPoints'] = match['score_breakdown'][winner]['autoPoints']
    Match['w_autoTaxiPoints'] = match['score_breakdown'][winner]['autoTaxiPoints']
    Match['w_autoCargoTotal'] = match['score_breakdown'][winner]['autoCargoTotal']
    Match['w_autoLowerGoals'] = match['score_breakdown'][winner]['autoCargoLowerBlue'] + \
                                match['score_breakdown'][winner]['autoCargoLowerFar'] + \
                                match['score_breakdown'][winner]['autoCargoLowerNear'] + \
                                match['score_breakdown'][winner]['autoCargoLowerRed']
    Match['w_autoUpperGoals'] = match['score_breakdown'][winner]['autoCargoUpperBlue'] + \
                                match['score_breakdown'][winner]['autoCargoUpperFar'] + \
                                match['score_breakdown'][winner]['autoCargoUpperNear'] + \
                                match['score_breakdown'][winner]['autoCargoUpperRed']

    Match['w_teleopCargoPoints'] = match['score_breakdown'][winner]['teleopCargoPoints']
    Match['w_teleopCargoTotal'] = match['score_breakdown'][winner]['teleopCargoTotal']
    Match['w_teleopLowerGoals'] = match['score_breakdown'][winner]['teleopCargoLowerBlue'] + \
                                  match['score_breakdown'][winner]['teleopCargoLowerFar'] + \
                                  match['score_breakdown'][winner]['teleopCargoLowerNear'] + \
                                  match['score_breakdown'][winner]['teleopCargoLowerRed']
    Match['w_teleopUpperGoals'] = match['score_breakdown'][winner]['teleopCargoUpperBlue'] + \
                                  match['score_breakdown'][winner]['teleopCargoUpperFar'] + \
                                  match['score_breakdown'][winner]['teleopCargoUpperNear'] + \
                                  match['score_breakdown'][winner]['teleopCargoUpperRed']

    Match['w_endgamePoints'] = match['score_breakdown'][winner]['endgamePoints']
    lowBar = 0
    midBar = 0
    highBar = 0
    travBar = 0
    bots = ['endgameRobot1','endgameRobot2','endgameRobot3']
    for bot in bots:
        if(match['score_breakdown'][winner][bot] == 'Low'):
            lowBar += 1
        elif(match['score_breakdown'][winner][bot] == 'Mid'):
            midBar += 1
        elif(match['score_breakdown'][winner][bot] == 'High'):
            highBar += 1
        elif(match['score_breakdown'][winner][bot] == 'Traversal'):
            travBar += 1
    Match['w_lowBars'] = lowBar
    Match['w_midBars'] = midBar
    Match['w_highBars'] = highBar
    Match['w_travBars'] = travBar
    if(match['score_breakdown'][winner]['cargoBonusRankingPoint'] == True):
        Match['w_cargoBonusRankingPoint'] = 1
    else:
        Match['w_cargoBonusRankingPoint'] = 0
    if(match['score_breakdown'][winner]['hangarBonusRankingPoint'] == True):
        Match['w_hangarBonusRankingPoint'] = 1
    else:
        Match['w_hangarBonusRankingPoint'] = 0
    if(match['score_breakdown'][winner]['quintetAchieved'] == True):
        Match['w_quintetAchieved'] = 1
    else:
        Match['w_quintetAchieved'] = 0

    Match['l_autoPoints'] = match['score_breakdown'][loser]['autoPoints']
    Match['l_autoTaxiPoints'] = match['score_breakdown'][loser]['autoTaxiPoints']
    Match['l_autoCargoTotal'] = match['score_breakdown'][loser]['autoCargoTotal']
    Match['l_autoLowerGoals'] = match['score_breakdown'][loser]['autoCargoLowerBlue'] + \
                                match['score_breakdown'][loser]['autoCargoLowerFar'] + \
                                match['score_breakdown'][loser]['autoCargoLowerNear'] + \
                                match['score_breakdown'][loser]['autoCargoLowerRed']
    Match['l_autoUpperGoals'] = match['score_breakdown'][loser]['autoCargoUpperBlue'] + \
                                match['score_breakdown'][loser]['autoCargoUpperFar'] + \
                                match['score_breakdown'][loser]['autoCargoUpperNear'] + \
                                match['score_breakdown'][loser]['autoCargoUpperRed']

    Match['l_teleopCargoPoints'] = match['score_breakdown'][loser]['teleopCargoPoints']
    Match['l_teleopCargoTotal'] = match['score_breakdown'][loser]['teleopCargoTotal']
    Match['l_teleopLowerGoals'] = match['score_breakdown'][loser]['teleopCargoLowerBlue'] + \
                                  match['score_breakdown'][loser]['teleopCargoLowerFar'] + \
                                  match['score_breakdown'][loser]['teleopCargoLowerNear'] + \
                                  match['score_breakdown'][loser]['teleopCargoLowerRed']
    Match['l_teleopUpperGoals'] = match['score_breakdown'][loser]['teleopCargoUpperBlue'] + \
                                  match['score_breakdown'][loser]['teleopCargoUpperFar'] + \
                                  match['score_breakdown'][loser]['teleopCargoUpperNear'] + \
                                  match['score_breakdown'][loser]['teleopCargoUpperRed']

    Match['l_endgamePoints'] = match['score_breakdown'][loser]['endgamePoints']
    lowBar = 0
    midBar = 0
    highBar = 0
    travBar = 0
    bots = ['endgameRobot1','endgameRobot2','endgameRobot3']
    for bot in bots:
        if(match['score_breakdown'][loser][bot] == 'Low'):
            lowBar += 1
        elif(match['score_breakdown'][loser][bot] == 'Mid'):
            midBar += 1
        elif(match['score_breakdown'][loser][bot] == 'High'):
            highBar += 1
        elif(match['score_breakdown'][loser][bot] == 'Traversal'):
            travBar += 1
    Match['l_lowBars'] = lowBar
    Match['l_midBars'] = midBar
    Match['l_highBars'] = highBar
    Match['l_travBars'] = travBar
    if(match['score_breakdown'][loser]['cargoBonusRankingPoint'] == True):
        Match['l_cargoBonusRankingPoint'] = 1
    else:
        Match['l_cargoBonusRankingPoint'] = 0
    if(match['score_breakdown'][loser]['hangarBonusRankingPoint'] == True):
        Match['l_hangarBonusRankingPoint'] = 1
    else:
        Match['l_hangarBonusRankingPoint'] = 0
    if(match['score_breakdown'][loser]['quintetAchieved'] == True):
        Match['l_quintetAchieved'] = 1
    else:
        Match['l_quintetAchieved'] = 0
    youtube = ''
    for v in match['videos']:
        if v['type'] == 'youtube':
            if youtube == '':
                youtube = 'https://youtu.be/' + v['key']
            else:
                youtube = youtube + ' ; ' + 'https://youtu.be/' + v['key']
    Match['YouTubeLink'] = youtube

    return Match

def ScoreCheckCalc( value, score):
    if(score == 0 or pd.isna(score)):
        return 0
    else:
        return value

#GetAllMatches()
AllMatches = pd.read_csv("2022_Matches.csv")
#AllMatches = AllMatches.assign('w_%HighGoal'=lambda x: x.)
pprint(AllMatches.columns)
matchCount = len(AllMatches)

AllMatches['w_%HighGoal'] = ScoreCheckCalc((4*AllMatches['w_autoUpperGoals']+2*AllMatches['w_teleopUpperGoals'])/AllMatches['w_score'], AllMatches['w_score'])
AllMatches['l_%HighGoal'] = ScoreCheckCalc((4*AllMatches['l_autoUpperGoals']+2*AllMatches['l_teleopUpperGoals'])/AllMatches['l_score'], AllMatches['l_score'])

AllMatches['w_%LowGoal'] = ScoreCheckCalc((2*AllMatches['w_autoLowerGoals']+AllMatches['w_teleopLowerGoals'])/AllMatches['w_score'], AllMatches['w_score'])
AllMatches['l_%LowGoal'] = ScoreCheckCalc((2*AllMatches['l_autoLowerGoals']+AllMatches['l_teleopLowerGoals'])/AllMatches['l_score'], AllMatches['l_score'])

AllMatches['w_%HangingScore'] = ScoreCheckCalc((AllMatches['w_endgamePoints'])/AllMatches['w_score'], AllMatches['w_score'])
AllMatches['l_%HangingScore'] = ScoreCheckCalc((AllMatches['l_endgamePoints'])/AllMatches['l_score'], AllMatches['l_score'])

AllMatches['w_%Taxi'] = ScoreCheckCalc((AllMatches['w_autoTaxiPoints'])/AllMatches['w_score'], AllMatches['w_score'])
AllMatches['l_%Taxi'] = ScoreCheckCalc((AllMatches['l_autoTaxiPoints'])/AllMatches['l_score'], AllMatches['l_score'])
'''
scoreContributions = AllMatches[['w_autoUpperGoals', 'l_autoUpperGoals',
                                 'w_autoLowerGoals', 'l_autoLowerGoals',
                                 'w_teleopUpperGoals', 'l_teleopUpperGoals',
                                 'w_teleopLowerGoals', 'l_teleopLowerGoals',
                                 'w_endgamePoints', 'l_endgamePoints',
                                 'w_autoTaxiPoints', 'l_autoTaxiPoints',
                                 'w_%HighGoal', 'l_%HighGoal',
                                 'w_%LowGoal', 'l_%LowGoal',
                                 'w_%HangingScore', 'l_%HangingScore',
                                 'w_%Taxi', 'l_%Taxi']].describe()
'''
scoreContributions = AllMatches.describe()
sums = AllMatches[['w_quintetAchieved','l_quintetAchieved',
                  'w_cargoBonusRankingPoint', 'l_cargoBonusRankingPoint',
                  'w_hangarBonusRankingPoint', 'l_hangarBonusRankingPoint',
                  'w_lowBars','l_lowBars',
                  'w_midBars','l_midBars',
                  'w_highBars','l_highBars',
                  'w_travBars','l_travBars'
                ]].sum()
#sums = sums.assign('percent' = lambda x:)
'''
sums = 100*sums/matchCount
sums.plot(kind='bar')
plt.subplots_adjust(bottom=0.3, top=0.99)
plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
plt.show()
'''
'''
pprint(AllMatches[['w_%HighGoal', 'l_%HighGoal',
                   'w_%LowGoal', 'l_%LowGoal',
                   'w_%HangingScore', 'l_%HangingScore',
                   'w_%Taxi', 'l_%Taxi']])
'''
#print(scoreContributions)
print(AllMatches[AllMatches['w_travBars']==3][['key','event_key']])
#print(sums)
ev = pd.DataFrame(tba.GetEventMatchesVerbose('2022dc306'))
#pprint(ev[ev['key']=='2022dc306_qm7'])
#pprint(tba.GetMatcheVerbose('2022bcvi_f1m1'))
#pprint(tba.GetMatcheVerbose('2022dc306_qm7'))
pprint(AllMatches[pd.isna(AllMatches['l_%Taxi'])])
#print(tba.GetEventDetail('2022tuis3'))

#'https://www.thebluealliance.com/api/v3/match/2022dc306_qm7'
#'https://www.thebluealliance.com/api/v3/match/2022dc306_qm7'
