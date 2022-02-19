import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

MatchData = pd.read_csv("Roe_Team_Match_History.csv")
TeamData = pd.read_csv("Roe_Team_Event_Results.csv")

#print(TeamData.head())
rnkAvg = TeamData.loc[:,['team','rank']].groupby('team').mean()

rnkAvg.sort_values('rank', inplace=True)
#rnkAvg.set_index('team', inplace=True)
#print(rnkAvg)


ownershipAvg = MatchData.loc[:,['team',
                                'autoSwitchOwnershipSec',
                                'autoScaleOwnershipSec',
                                'autoSwitchAtZero',
                                'foulPoints',
                                'rp',
                                'vaultPoints',
                                'teleopSwitchOwnershipSec',
                                'teleopScaleOwnershipSec',
                                'totalPoints']].groupby('team').mean()
#print(ownershipAvg)

data = rnkAvg.join(ownershipAvg)
#print(data)

teams = rnkAvg.index

colors=[]
for t in teams:
    if t == 'frc3959':
        colors.append('g')
    else:
        colors.append('b')

fig,(ax1,ax2) = plt.subplots(nrows=2,ncols=1)

#print(colors)
p = data['autoSwitchOwnershipSec'].plot(kind='bar', color=colors, x='team', y='autoSwitchOwnershipSec', ax=ax1).set_title('Avg autoSwitchOwnershipSec')
#p.set

p2 = data['autoScaleOwnershipSec'].plot(kind='bar', color=colors, x='team', y='autoScaleOwnershipSec', ax=ax2).set_title('Avg autoSwitchOwnershipSec')

plt.tight_layout()
plt.show()



