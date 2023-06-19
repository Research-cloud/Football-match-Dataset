#!/usr/bin/env python
# coding: utf-8

# In[55]:


import pandas as pd


# In[14]:


import requests
standings_url = "https://fbref.com/en/comps/9/2021-2022/2021-2022-Premier-League-Stats"
data = requests.get(standings_url)
from bs4 import BeautifulSoup
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
links = standings_table.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]


# In[15]:


print(len(links))
#https://fbref.com/en/squads/b8fd03ef/2021-2022/matchlogs/c9/schedule/Manchester-City-Scores-and-Fixtures-Premier-League


# In[16]:


newlinks = []
for l in links:
    list = l.split('/')
    newlist = list[:5]
    newlist.append('matchlogs/c9/schedule')
    lst = list[5].split('-')
    lst = lst[:-1]
    team1 = ' '.join(lst)
    lst.append('Scores-and-Fixtures-Premier-League')
    lst = '-'.join(lst)
    newlist.append(lst)
    newlist = '/'.join(newlist)
    newlinks.append(f'https://fbref.com{newlist}')


# In[89]:


match_data = {'Date' : [], 'Home_Team' : [], 'Away_Team' : [], 'Home_Goal' : [], 'Away_Goal' : [], 'Result' : []}
for l in newlinks:
    team1 = l.split('/')[10].split('-Scores')[0].replace('-',' ')
    data = requests.get(l)
    soup = BeautifulSoup(data.text)
    Data = soup.select('#matchlogs_for > tbody')[0].select('tr')

    for d in Data:
        Date = d.select('th.left')[0].text.replace('\n','').replace(' ','')
        Data = d.select('td')
        Venue = Data[3].text.replace('\n','').replace(' ','')
        Result = Data[4].text.replace('\n','').replace(' ','')
        GF = Data[5].text.replace('\n','').replace(' ','')
        GA = Data[6].text.replace('\n','').replace(' ','')
        team2 = Data[7].text
        if team2 == 'Wolves':
            team2 = 'Wolverhampton Wanderers'
        if team2 == 'Manchester Utd':
            team2 =  'Manchester United'   
        if team2 == 'Brighton':
            team2 = 'Brighton and Hove Albion'
        if team2 == 'Newcastle Utd':
            team2 =  'Newcastle United'
        if team2 == 'West Ham':
            team2 = 'West Ham United'  
        if team2 == 'Tottenham':
            team2 = 'Tottenham Hotspur'
            
        if Venue == 'Away':
            Home_Team = team2
            Away_Team = team1
            Home_Goal = GA
            Away_Goal = GF
            if Result == 'L':
                Result = 'W'   
            elif Result == 'W':
                Result = 'L'
        else:
            Home_Team = team1
            Away_Team = team2
            Home_Goal = GF
            Away_Goal = GA
        match_data['Date'].append(Date)
        match_data['Home_Team'].append(Home_Team)
        match_data['Away_Team'].append(Away_Team)
        match_data['Home_Goal'].append(Home_Goal)
        match_data['Away_Goal'].append(Away_Goal)
        match_data['Result'].append(Result)


# In[96]:


print(len(match_data['Date']))


# In[91]:


match_df = pd.DataFrame.from_dict(match_data)


# In[92]:


result_df = match_df.drop_duplicates()


# In[93]:


match_data


# In[94]:


len(result_df)


# In[76]:


for name in set(match_data['Away_Team']):
    print(name)


# In[95]:


result_df.to_csv('league_match_data.csv')


# In[ ]:




