import TBA_Tools as tba

el = tba.GetEventList('2022')
'''
for e in el:
    if e['week'] in [0]:
        print(e['key'], ' ', e['week'], ' ', e['name'], ' ', e['country'], ' ', e.keys())
'''
data = []
matches = tba.GetEventMatchesVerbose('2020scmb')
for m in matches:
    if m['actual_time'] is not None:
        print(m['key'], ' ', m)
