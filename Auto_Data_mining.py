import json
import requests
import operator

myToken = 'URGab8tLhUZabkbIiBVGOjmKiyqlAmLO6Nqh4vc5DmqcGAC0XSDSBgQ3bnsu2nLf'
baseURL = 'https://www.thebluealliance.com/api/v3/'
eventKey = '2018alhu'
# event/2018alhu/matches/keys

rURL = baseURL + 'events/2018/keys'

# print(rURL)

headers = {
    'accept': 'application/json',
    'X-TBA-Auth-Key': myToken
}

r = requests.get(rURL, headers)

# print(r.status_code)
if r.status_code == 200:
    events = json.loads(r.content)

else:
    print('crap!')

# print(events)
print(len(events))

matches = []
'''
print(len(events))

mtch = events[0]
rURL = baseURL+'event/'+mtch+'/matches'

headers = {'accept': 'application/json',
           'X-TBA-Auth-Key': myToken}
r = requests.get(rURL, headers)

#print(r.status_code)
if r.status_code == 200:
  matches = matches + json.loads(r.content)

else:
  print('crap!')

print(len(matches))  



'''
data = 'event, date, match, matchType, matchNum, color, autoSwitchTime, autoScaleTime, autoScore, autoSwitchAtZero, youtube \r\n'

outfile = open("data.csv", "w")
errorFile = open("errors.txt", "w")

outfile.write(data)

for mtch in events:
    rURL = baseURL + 'event/' + mtch + '/matches'
    headers = {
        'accept': 'application/json',
        'X-TBA-Auth-Key': myToken
    }
    r = requests.get(rURL, headers)

    if r.status_code == 200:
        ms = json.loads(r.content)
        for m in ms:
            try:
                d = m['event_key'] + ','
                d = d + str(m['actual_time']) + ','
                d = d + m['key'] + ', '
                d = d + m['comp_level'] + ','
                d = d + str(m['match_number']) + ','
                d = d + 'blue,'
                d = d + str(15 - m['score_breakdown']['blue']['autoSwitchOwnershipSec']) + ','
                d = d + str(15 - m['score_breakdown']['blue']['autoScaleOwnershipSec']) + ', '
                d = d + str(m['score_breakdown']['blue']['autoPoints']) + ','
                d = d + str(m['score_breakdown']['blue']['autoSwitchAtZero']) + ','
                if (len(m['videos']) > 0):
                    d = d + '=HYPERLINK("https://youtu.be/' + str(m['videos'][0]['key']) + '")\r\n'
                else:
                    d = d + '"no video"\r\n'
                outfile.write(d)
            except(ValueError, KeyError, TypeError):
                print("error on blue: " + m['key'])
                errorFile.write("error on blue: " + m['key'] + '\r\n')

            try:
                d = m['event_key'] + ','
                d = d + str(m['actual_time']) + ','
                d = d + m['key'] + ','
                d = d + m['comp_level'] + ','
                d = d + str(m['match_number']) + ','
                d = d + 'red,'
                d = d + str(15 - m['score_breakdown']['red']['autoSwitchOwnershipSec']) + ','
                d = d + str(15 - m['score_breakdown']['red']['autoScaleOwnershipSec']) + ','
                d = d + str(m['score_breakdown']['red']['autoPoints']) + ','
                d = d + str(m['score_breakdown']['red']['autoSwitchAtZero']) + ','
                if (len(m['videos']) > 0):
                    d = d + '=HYPERLINK("https://youtu.be/' + str(m['videos'][0]['key']) + '")\r\n'
                else:
                    d = d + '"no video"\r\n'
                outfile.write(d)
            except(ValueError, KeyError, TypeError):
                print("error on blue: " + m['key'])
                errorFile.write("error on blue: " + m['key'] + '\r\n')

# print(matches)
# print(data)

# '''



