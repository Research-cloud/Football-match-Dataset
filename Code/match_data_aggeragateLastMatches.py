#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


# In[9]:


team_data = pd.read_csv('league_match_data.csv')


# In[10]:


len(team_data)


# In[11]:


players_data = pd.read_csv('players_data.csv')


# In[12]:


players_data


# In[110]:


team_data = team_data.drop(['Unnamed: 0'], axis = 1)


# In[90]:


teams = list(set(team_data['Home_Team']))
print(teams)


# In[131]:


aggeragated_data = {}
for team in teams:
    aggeragated_data[team] = {}


# In[132]:


for team in teams:

    df = team_data[team_data['Home_Team'] == team][['Date','Home_Goal','Result']]
    if team == 'Manchester City':
        print(df)
    idxs = list(df.index)
    dates = []
    DateG = {}
    result = {}
    for idx in idxs:
        Date = df['Date'][idx].replace('-','')
        HG = df['Home_Goal'][idx]
        r = df['Result'][idx]
        dates.append(Date)
        DateG[Date] = HG
        if r == 'W':
            result[Date] = 1
        else:
            result[Date] = 0
    
    
    df = team_data[team_data['Away_Team'] == team][['Date','Away_Goal','Result']]
    if team == 'Manchester City':
        print(df)
    idxs = list(df.index)
    for idx in idxs:
        Date = df['Date'][idx].replace('-','')
        dates.append(Date)
        r = df['Result'][idx]
        AG = df['Away_Goal'][idx]
        DateG[Date] = AG
        if r == 'L':
            result[Date] = 1
        else:
            result[Date] = 0

    dates.sort()

    glst = []
    rst = []
    start = 0
    smG = [0]
    smR = [0.0]
    for d in dates:

        dt = convertDate(d)
        glst.append(DateG[d])
        rst.append(result[d])
    
    i = 1    
    for d in dates:
        if i == 1:
            aggeragated_data[team][convertDate(d)] = [0,0.0]
        elif i - start <= 5:
            aggeragated_data[team][convertDate(d)] = [smG[i-1],(smR[i-1] / (i - start - 1)) * 100]
        else: 
            aggeragated_data[team][convertDate(d)] = [smG[i-1] - smG[start],((smR[i-1] - smR[start]) / (i - start -1 )) * 100]
            start = start + 1
        smG.append(smG[i-1] + glst[i-1])
        smR.append(smR[i-1] + rst[i-1])
        i = i + 1

    if team == 'Manchester City':
        print(result)
    


# In[ ]:





# In[133]:


aggeragated_data


# In[56]:


def convertDate(Date):
    year = Date[:4]
    month = Date[4:6]
    day = Date[6:]
    
    return '-'.join([year,month,day])


# In[134]:


finalDataFrame = {'Date':[], 'Home_Team' : [], 'Away_Team' : [], 'Home_Goal_L5' : [], 'Away_Goal_L5' : [], 'Home_Win%_L5':[],
                 'Away_Win%_L5' : [], 'Result' : []
                 }


# In[135]:


for i in range(380):
    Date = team_data['Date'][i]
    Home_Team = team_data['Home_Team'][i]
    Away_Team = team_data['Away_Team'][i]
    HG5 = aggeragated_data[Home_Team][Date][0]
    hWin = aggeragated_data[Home_Team][Date][1]
    AG5 = aggeragated_data[Away_Team][Date][0]
    aWin = aggeragated_data[Away_Team][Date][1]
    Result = team_data['Result'][i]
    finalDataFrame['Date'].append(Date)
    finalDataFrame['Home_Team'].append(Home_Team)
    finalDataFrame['Away_Team'].append(Away_Team)
    finalDataFrame['Home_Goal_L5'].append(HG5)
    finalDataFrame['Away_Goal_L5'].append(AG5)
    finalDataFrame['Home_Win%_L5'].append(hWin)
    finalDataFrame['Away_Win%_L5'].append(aWin)
    finalDataFrame['Result'].append(Result)


# In[136]:


finalDataFrame


# In[137]:


df = pd.DataFrame.from_dict(finalDataFrame)


# In[138]:


team_data


# In[139]:


df


# In[140]:


df.to_csv('new_team_data.csv')


# In[141]:


df['Result']


# In[ ]:




