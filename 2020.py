import TBA_Tools as tba
import pandas as pd

'''
MTEvents = tba.GetTeamEvents('frc3959', '2020')

for e in MTEvents:
    print(e)
'''


EventList = []

'''
for e in MTEvents:
    print(e)
    EventList.append( e['key'])

'''
data = []

LRTeamList = tba.GetTeamKeyListAtEvent('2020tnme')
print('team         event       rank, avg RP, avg Auto, avg endgame, avg teleop')
for t in LRTeamList:
    #print(t)
    ts = tba.GetTeamStatuses(t, '2020')
    #print(ts)
    for te in ts:
        if ts[te] is not None:
            #print(t,' : ',ts[te], len(ts[te]))
            #print(t, ' : ', ts[te]['qual']['ranking'].keys(), ts[te]['qual']['ranking'])
            print(t, ' : ', te, ' : ', ts[te]['qual']['ranking']['rank'], ', ',
                  ts[te]['qual']['ranking']['sort_orders'][0], ', ',
                  "{0:.2f}".format(ts[te]['qual']['ranking']['sort_orders'][1]/ts[te]['qual']['ranking']['matches_played']), ', ',
                  "{0:.2f}".format(ts[te]['qual']['ranking']['sort_orders'][2] / ts[te]['qual']['ranking']['matches_played']), ', ',
                  "{0:.2f}".format(ts[te]['qual']['ranking']['sort_orders'][3] / ts[te]['qual']['ranking']['matches_played']), ', ',
                  )

'''
    if len(ts) > 0:
        for e in ts.keys():
            if ts[e]['qual']['ranking']['rank'] is not None:
                #print(e)
                print(t['key'], ' ', e)
                s = {}
                s['team'] = t['key']
                s['event'] = e
                s['RP_average'] = ts[e]['qual']['ranking']['sort_orders'][0]
                s['rank'] = ts[e]['qual']['ranking']['rank']
                s['wins'] = ts[e]['qual']['ranking']['record']['wins']
                s['losses'] = ts[e]['qual']['ranking']['record']['losses']
                s['ties'] = ts[e]['qual']['ranking']['record']['ties']
                s['MatchCount'] = ts[e]['qual']['ranking']['matches_played']
                if ts[e]['playoff'] is not None:
                    s['playoff_distance'] = ts[e]['playoff']['level']
                    s['playoff_status'] = ts[e]['playoff']['status']
                else:
                    s['playoff_distance'] = 'None'
                    s['playoff_status'] = 'None'
                data.append(s)
'''
print(data)
'''
df = pd.DataFrame(data)
df.to_csv('LR_Team_2019_Performance.csv',
              columns=df.columns.values,
              line_terminator = '\r\n',
              index=False)

#'''
#print(tba.GetTeamStatuses('frc2221','2019'))
'''
s = tba.GetTeamStatuses('frc2992', '2019')
for e in s.keys():
    #print(s[e].keys())
    #print(s[e])
    #print(s[e]['playoff'])
    if s[e]['qual']['ranking']['rank'] is not None:
        print(s[e]['qual']['ranking']['rank'])
    if s[e]['playoff'] is not None:
        print('not none', s[e]['playoff']['level'])
    else:
        print('team sucks')
    #print(s[e]['qual'].keys())
    #print(s[e]['qual']['status'])
    #print(s[e]['qual']['ranking'])
    #print(s[e]['qual']['ranking']['sort_orders'][0])
#'''
#print(LRTeamList)
