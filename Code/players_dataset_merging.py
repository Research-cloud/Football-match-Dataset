#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


# In[16]:


standing_url = "https://fbref.com/en/comps/9/2021-2022/schedule/2021-2022-Premier-League-Scores-and-Fixtures"
data = requests.get(standing_url)
soup = BeautifulSoup(data.text)


# In[17]:


print(soup)


# In[18]:


Data = soup.select('tr')
links = {""}
for ele in Data:
    link = ele.find_all('a')
    for l in link:
        if l.text == 'Match Report':
            links.add(l)
links.remove("")        
links = list(links)        
links = [l.get('href') for l in links]
links = [l for l in links if '-2021-Premier-League' or '-2022-Premier-League' in l]


# In[19]:


print(len(links))


# In[20]:


link = "https://fbref.com/en/matches/3adf2aa7/Brentford-Arsenal-August-13-2021-Premier-League"
Data = requests.get(link)
soup = BeautifulSoup(Data.text)


# In[21]:


data = soup.select('span.teamandlogo')
print(data[1].text)


# In[22]:


data = soup.select('div.table_container')
print(data[7].select('th.left')[1].select('a')[0].get('href').split('/'))


# In[23]:


monthToNum = {'January' : '01' , 'February' : '02', 'March' : '03' , 'April' : '04' , 'May' : '05' , 'June' : '06' , 'July' : '07',
             'August' : '08' , 'September' : '09' , 'October' : '10' , 'November' : '11' , 'December' : '12'
             }


# In[24]:


Date = soup.select('h1')[0].text.split(' Match Report – ')[1].replace(',','').split(' ')
Date = Date[3]+'-'+monthToNum[Date[1]]+'-'+Date[2]
print(Date)


# In[25]:


players_link = {""}


# In[26]:


team_and_player_data = {}

for link in links:
    link = f"https://fbref.com{link}"
    Data = requests.get(link)
    soup = BeautifulSoup(Data.text)
    teams = soup.select('span.teamandlogo')
    
    team1_name = soup.select('#content > div.scorebox > div:nth-child(1) > div:nth-child(1) > strong > a')[0].text.replace('\n','').replace(' ','')
    team2_name = soup.select('#content > div.scorebox > div:nth-child(2) > div:nth-child(1) > strong > a')[0].text.replace('\n','').replace(' ','')
    
    data = soup.select('div.table_container')
    
    Date = soup.select('#content > div.scorebox > div.scorebox_meta > div:nth-child(1) > strong > a')[0].text.split(',')
    Date = Date[1]+'-'+monthToNum[Date[0].split(' ')[1]]+'-'+Date[0].split(' ')[2]
    
    if team1_name not in team_and_player_data.keys():
        team_and_player_data[team1_name] = {Date : []}
    else:
        team_and_player_data[team1_name][Date] = []
        
    if team2_name not in team_and_player_data.keys():
        team_and_player_data[team2_name] = {Date : []}
    else:
        team_and_player_data[team2_name][Date] = []
        
    for players in data[0].select('th.left'):
        
        if players.text == 'Player':
            continue
        
        if ' Players' in players.text:
            break
        player_link = players.select('a')[0].get('href')
        player_id = player_link.split('/')[3]
        player_name = player_link.split('/')[4].replace('-',' ')
        team_and_player_data[team1_name][Date].append({player_id : player_name}) 
        players_link.add(player_link)
              
    for players in data[7].select('th.left'):
        
        if players.text == 'Player':
            continue
        if ' Players' in players.text:
            break;
        player_link = players.select('a')[0].get('href')
        player_id = player_link.split('/')[3]
        player_name = player_link.split('/')[4].replace('-',' ')
        team_and_player_data[team2_name][Date].append({player_id : player_name}) 
        players_link.add(player_link)
    


# In[27]:


players_link.remove("")
print(len(players_link))
players_link = list(players_link)


# In[28]:


team_player_data = {}

for key,data in team_and_player_data.items():
    
    if key not in team_player_data.keys():
        team_player_data[key] = {}
        
    for keys,values in data.items():
        lit = keys.replace(' ','').split('-')
        if len(lit[2]) == 1:
            lit[2] = '0'+lit[2]
            key2 = '-'.join(lit)
            team_player_data[key][key2] = values
        else:
            team_player_data[key][keys.replace(' ','')] = values
            
    


# In[29]:


team_player_data


# In[30]:


for key,value in team_player_data.items():
    print(len(value))


# In[ ]:


player_data = {'id' : [], 'name' : [] , 'MP' : [], 'GA' : [], 'GA90' : [], 'SoTA' : [], 'Saves%' : [],
              'CS%' : [] , 'Gls' : [] , 'Ast' : [] , 'PK' : [], 'PKatt' : [], 'CrdY' : [], 'CrdR' : [], 'Sh' : [],
               'SoT%' : [], 'G/Sh' : []
              }


# In[ ]:


for l in players_link[:101]:
 
    lst = l.split('/')
    name = lst[4].replace('-',' ')
    ID = lst[3]
    newList = lst[:4]
    newList.append('/all_comps')
    newList.append(lst[4] + '-Stats---All-Competitions')
    link = 'https://fbref.com/en/players/98ea5115/all_comps/David-Raya-Stats---All-Competitions'
    link = 'https://fbref.com'+ ('/'.join(newList))
    Data = requests.get(link)
    soup = BeautifulSoup(Data.text)
    player_data['id'].append(ID)
    player_data['name'].append(name)
    try:
        
        Data1 = soup.select('#stats_standard_expanded')[0].select('#stats')
        MP = 0
        Gls = 0
        Ast = 0
        PK = 0
        PKatt = 0
        CrdY = 0
        CrdR = 0
        
        for d in Data1:
            try:
                RowData = d.select('td')
            except:
                continue
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                MP = MP+int(RowData[4].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                Gls = Gls + int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
               pass
            try:
                Ast = Ast + int(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PK = PK + int(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PKatt = PKatt + int(RowData[13].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdY = CrdY + int(RowData[14].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdR = CrdR + int(RowData[15].text.replace('\n','').replace(' ',''))
            except:
                pass

        player_data['MP'].append(MP)
        player_data['Gls'].append(Gls)
        player_data['Ast'].append(Ast)
        player_data['PK'].append(PK)
        player_data['PKatt'].append(PKatt)
        player_data['CrdY'].append(CrdY)
        player_data['CrdR'].append(CrdR)
    except:
    
        player_data['MP'].append(0)
        player_data['Gls'].append(0)
        player_data['Ast'].append(0)
        player_data['PK'].append(0)
        player_data['PKatt'].append(0)
        player_data['CrdY'].append(0)
        player_data['CrdR'].append(0)
        
        
    try:    
        Data2 = soup.select('#stats_keeper_expanded')[0].select('#stats')
        GA = 0
        GA90 = 0.0
        SoTA = 0.0
        Saves = 0.0
        CS = 0.0
        i = 0
        for d in Data2:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                GA = GA+int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                GA = GA + 0
            try:
                GA90 = GA90 + float(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                GA90 = GA90 + 0
            try:
                SoTA = SoTA + float(RowData[10].text.replace('\n','').replace(' ',''))
            except:
                SoTA = SoTA + 0
            try:
                Saves = Saves + float(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                Saves = Saves + 0
            try:
                CS = CS + float(RowData[17].text.replace('\n','').replace(' ',''))
            except:
                CS = CS + 0
            i = i + 1    
            
        player_data['GA'].append(GA)
        player_data['GA90'].append(GA90)
        player_data['SoTA'].append(SoTA)
        player_data['Saves%'].append(Saves/i)
        player_data['CS%'].append(CS/i)
    except:
        player_data['GA'].append(0)
        player_data['GA90'].append(0)
        player_data['SoTA'].append(0)
        player_data['Saves%'].append(0)
        player_data['CS%'].append(0)
        
            
            
    try:    
        Data3 = soup.select('#stats_shooting_expanded')[0].select('#stats')
        Sh = 0
        SoT = 0.0
        gsh = 0.0
        i = 0
        for d in Data3:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                print('Sh',RowData[6].text.replace('\n','').replace(' ',''))
                Sh = Sh + int(RowData[6].text.replace('\n','').replace(' ',''))
            except:
                Sh = Sh + 0
            try:
                print('SoT', float(RowData[8].text.replace('\n','').replace(' ','')))
                SoT = SoT + float(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                SoT = SoT + 0
            try:
                print('gsh' , float(RowData[11].text.replace('\n','').replace(' ','')))
                gsh = gsh + float(RowData[11].text.replace('\n','').replace(' ',''))    
            except:
                gsh = gsh + 0
            i = i + 1
            
        player_data['Sh'].append(Sh)
        player_data['SoT%'].append(SoT/i)
        player_data['G/Sh'].append(gsh)
            
    except:
        player_data['Sh'].append(0)
        player_data['SoT%'].append(0)
        player_data['G/Sh'].append(0)
        
        
        
        
    
    
    


# In[ ]:


for l in players_link[101:201]:
 
    lst = l.split('/')
    name = lst[4].replace('-',' ')
    ID = lst[3]
    newList = lst[:4]
    newList.append('/all_comps')
    newList.append(lst[4] + '-Stats---All-Competitions')
    link = 'https://fbref.com/en/players/98ea5115/all_comps/David-Raya-Stats---All-Competitions'
    link = 'https://fbref.com'+ ('/'.join(newList))
    Data = requests.get(link)
    soup = BeautifulSoup(Data.text)
    player_data['id'].append(ID)
    player_data['name'].append(name)
    try:
        
        Data1 = soup.select('#stats_standard_expanded')[0].select('#stats')
        MP = 0
        Gls = 0
        Ast = 0
        PK = 0
        PKatt = 0
        CrdY = 0
        CrdR = 0
        
        for d in Data1:
            try:
                RowData = d.select('td')
            except:
                continue
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                MP = MP+int(RowData[4].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                Gls = Gls + int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
               pass
            try:
                Ast = Ast + int(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PK = PK + int(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PKatt = PKatt + int(RowData[13].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdY = CrdY + int(RowData[14].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdR = CrdR + int(RowData[15].text.replace('\n','').replace(' ',''))
            except:
                pass

        player_data['MP'].append(MP)
        player_data['Gls'].append(Gls)
        player_data['Ast'].append(Ast)
        player_data['PK'].append(PK)
        player_data['PKatt'].append(PKatt)
        player_data['CrdY'].append(CrdY)
        player_data['CrdR'].append(CrdR)
    except:
    
        player_data['MP'].append(0)
        player_data['Gls'].append(0)
        player_data['Ast'].append(0)
        player_data['PK'].append(0)
        player_data['PKatt'].append(0)
        player_data['CrdY'].append(0)
        player_data['CrdR'].append(0)
        
        
    try:    
        Data2 = soup.select('#stats_keeper_expanded')[0].select('#stats')
        GA = 0
        GA90 = 0.0
        SoTA = 0.0
        Saves = 0.0
        CS = 0.0
        i = 0
        for d in Data2:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                GA = GA+int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                GA = GA + 0
            try:
                GA90 = GA90 + float(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                GA90 = GA90 + 0
            try:
                SoTA = SoTA + float(RowData[10].text.replace('\n','').replace(' ',''))
            except:
                SoTA = SoTA + 0
            try:
                Saves = Saves + float(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                Saves = Saves + 0
            try:
                CS = CS + float(RowData[17].text.replace('\n','').replace(' ',''))
            except:
                CS = CS + 0
            i = i + 1    
            
        player_data['GA'].append(GA)
        player_data['GA90'].append(GA90)
        player_data['SoTA'].append(SoTA)
        player_data['Saves%'].append(Saves/i)
        player_data['CS%'].append(CS/i)
    except:
        player_data['GA'].append(0)
        player_data['GA90'].append(0)
        player_data['SoTA'].append(0)
        player_data['Saves%'].append(0)
        player_data['CS%'].append(0)
        
            
            
    try:    
        Data3 = soup.select('#stats_shooting_expanded')[0].select('#stats')
        Sh = 0
        SoT = 0.0
        gsh = 0.0
        i = 0
        for d in Data3:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                Sh = Sh + int(RowData[6].text.replace('\n','').replace(' ',''))
            except:
                Sh = Sh + 0
            try:
                SoT = SoT + float(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                SoT = SoT + 0
            try:
                gsh = gsh + float(RowData[11].text.replace('\n','').replace(' ',''))    
            except:
                gsh = gsh + 0
            i = i + 1
            
        player_data['Sh'].append(Sh)
        player_data['SoT%'].append(SoT/i)
        player_data['G/Sh'].append(gsh)
            
    except:
        player_data['Sh'].append(0)
        player_data['SoT%'].append(0)
        player_data['G/Sh'].append(0)
        
        
        
        
    
    
    


# In[ ]:


for l in players_link[201:301]:
 
    lst = l.split('/')
    name = lst[4].replace('-',' ')
    ID = lst[3]
    newList = lst[:4]
    newList.append('/all_comps')
    newList.append(lst[4] + '-Stats---All-Competitions')
    link = 'https://fbref.com/en/players/98ea5115/all_comps/David-Raya-Stats---All-Competitions'
    link = 'https://fbref.com'+ ('/'.join(newList))
    Data = requests.get(link)
    soup = BeautifulSoup(Data.text)
    player_data['id'].append(ID)
    player_data['name'].append(name)
    try:
        
        Data1 = soup.select('#stats_standard_expanded')[0].select('#stats')
        MP = 0
        Gls = 0
        Ast = 0
        PK = 0
        PKatt = 0
        CrdY = 0
        CrdR = 0
        
        for d in Data1:
            try:
                RowData = d.select('td')
            except:
                continue
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                MP = MP+int(RowData[4].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                Gls = Gls + int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
               pass
            try:
                Ast = Ast + int(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PK = PK + int(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PKatt = PKatt + int(RowData[13].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdY = CrdY + int(RowData[14].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdR = CrdR + int(RowData[15].text.replace('\n','').replace(' ',''))
            except:
                pass

        player_data['MP'].append(MP)
        player_data['Gls'].append(Gls)
        player_data['Ast'].append(Ast)
        player_data['PK'].append(PK)
        player_data['PKatt'].append(PKatt)
        player_data['CrdY'].append(CrdY)
        player_data['CrdR'].append(CrdR)
    except:
    
        player_data['MP'].append(0)
        player_data['Gls'].append(0)
        player_data['Ast'].append(0)
        player_data['PK'].append(0)
        player_data['PKatt'].append(0)
        player_data['CrdY'].append(0)
        player_data['CrdR'].append(0)
        
        
    try:    
        Data2 = soup.select('#stats_keeper_expanded')[0].select('#stats')
        GA = 0
        GA90 = 0.0
        SoTA = 0.0
        Saves = 0.0
        CS = 0.0
        i = 0
        for d in Data2:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                GA = GA+int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                GA = GA + 0
            try:
                GA90 = GA90 + float(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                GA90 = GA90 + 0
            try:
                SoTA = SoTA + float(RowData[10].text.replace('\n','').replace(' ',''))
            except:
                SoTA = SoTA + 0
            try:
                Saves = Saves + float(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                Saves = Saves + 0
            try:
                CS = CS + float(RowData[17].text.replace('\n','').replace(' ',''))
            except:
                CS = CS + 0
            i = i + 1    
            
        player_data['GA'].append(GA)
        player_data['GA90'].append(GA90)
        player_data['SoTA'].append(SoTA)
        player_data['Saves%'].append(Saves/i)
        player_data['CS%'].append(CS/i)
    except:
        player_data['GA'].append(0)
        player_data['GA90'].append(0)
        player_data['SoTA'].append(0)
        player_data['Saves%'].append(0)
        player_data['CS%'].append(0)
        
            
            
    try:    
        Data3 = soup.select('#stats_shooting_expanded')[0].select('#stats')
        Sh = 0
        SoT = 0.0
        gsh = 0.0
        i = 0
        for d in Data3:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                Sh = Sh + int(RowData[6].text.replace('\n','').replace(' ',''))
            except:
                Sh = Sh + 0
            try:
                SoT = SoT + float(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                SoT = SoT + 0
            try:
                gsh = gsh + float(RowData[11].text.replace('\n','').replace(' ',''))    
            except:
                gsh = gsh + 0
            i = i + 1
            
        player_data['Sh'].append(Sh)
        player_data['SoT%'].append(SoT/i)
        player_data['G/Sh'].append(gsh)
            
    except:
        player_data['Sh'].append(0)
        player_data['SoT%'].append(0)
        player_data['G/Sh'].append(0)
        
        
        
        
    
    
    


# In[ ]:


for l in players_link[301:401]:
 
    lst = l.split('/')
    name = lst[4].replace('-',' ')
    ID = lst[3]
    newList = lst[:4]
    newList.append('/all_comps')
    newList.append(lst[4] + '-Stats---All-Competitions')
    link = 'https://fbref.com/en/players/98ea5115/all_comps/David-Raya-Stats---All-Competitions'
    link = 'https://fbref.com'+ ('/'.join(newList))
    Data = requests.get(link)
    soup = BeautifulSoup(Data.text)
    player_data['id'].append(ID)
    player_data['name'].append(name)
    try:
        
        Data1 = soup.select('#stats_standard_expanded')[0].select('#stats')
        MP = 0
        Gls = 0
        Ast = 0
        PK = 0
        PKatt = 0
        CrdY = 0
        CrdR = 0
        
        for d in Data1:
            try:
                RowData = d.select('td')
            except:
                continue
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                MP = MP+int(RowData[4].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                Gls = Gls + int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
               pass
            try:
                Ast = Ast + int(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PK = PK + int(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PKatt = PKatt + int(RowData[13].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdY = CrdY + int(RowData[14].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdR = CrdR + int(RowData[15].text.replace('\n','').replace(' ',''))
            except:
                pass

        player_data['MP'].append(MP)
        player_data['Gls'].append(Gls)
        player_data['Ast'].append(Ast)
        player_data['PK'].append(PK)
        player_data['PKatt'].append(PKatt)
        player_data['CrdY'].append(CrdY)
        player_data['CrdR'].append(CrdR)
    except:
    
        player_data['MP'].append(0)
        player_data['Gls'].append(0)
        player_data['Ast'].append(0)
        player_data['PK'].append(0)
        player_data['PKatt'].append(0)
        player_data['CrdY'].append(0)
        player_data['CrdR'].append(0)
        
        
    try:    
        Data2 = soup.select('#stats_keeper_expanded')[0].select('#stats')
        GA = 0
        GA90 = 0.0
        SoTA = 0.0
        Saves = 0.0
        CS = 0.0
        i = 0
        for d in Data2:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                GA = GA+int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                GA = GA + 0
            try:
                GA90 = GA90 + float(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                GA90 = GA90 + 0
            try:
                SoTA = SoTA + float(RowData[10].text.replace('\n','').replace(' ',''))
            except:
                SoTA = SoTA + 0
            try:
                Saves = Saves + float(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                Saves = Saves + 0
            try:
                CS = CS + float(RowData[17].text.replace('\n','').replace(' ',''))
            except:
                CS = CS + 0
            i = i + 1    
            
        player_data['GA'].append(GA)
        player_data['GA90'].append(GA90)
        player_data['SoTA'].append(SoTA)
        player_data['Saves%'].append(Saves/i)
        player_data['CS%'].append(CS/i)
    except:
        player_data['GA'].append(0)
        player_data['GA90'].append(0)
        player_data['SoTA'].append(0)
        player_data['Saves%'].append(0)
        player_data['CS%'].append(0)
        
            
            
    try:    
        Data3 = soup.select('#stats_shooting_expanded')[0].select('#stats')
        Sh = 0
        SoT = 0.0
        gsh = 0.0
        i = 0
        for d in Data3:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                Sh = Sh + int(RowData[6].text.replace('\n','').replace(' ',''))
            except:
                Sh = Sh + 0
            try:
                SoT = SoT + float(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                SoT = SoT + 0
            try:
                gsh = gsh + float(RowData[11].text.replace('\n','').replace(' ',''))    
            except:
                gsh = gsh + 0
            i = i + 1
            
        player_data['Sh'].append(Sh)
        player_data['SoT%'].append(SoT/i)
        player_data['G/Sh'].append(gsh)
            
    except:
        player_data['Sh'].append(0)
        player_data['SoT%'].append(0)
        player_data['G/Sh'].append(0)
        
        
        
        
    
    
    


# In[ ]:


for l in players_link[401:]:
 
    lst = l.split('/')
    name = lst[4].replace('-',' ')
    ID = lst[3]
    newList = lst[:4]
    newList.append('/all_comps')
    newList.append(lst[4] + '-Stats---All-Competitions')
    link = 'https://fbref.com/en/players/98ea5115/all_comps/David-Raya-Stats---All-Competitions'
    link = 'https://fbref.com'+ ('/'.join(newList))
    Data = requests.get(link)
    soup = BeautifulSoup(Data.text)
    player_data['id'].append(ID)
    player_data['name'].append(name)
    try:
        
        Data1 = soup.select('#stats_standard_expanded')[0].select('#stats')
        MP = 0
        Gls = 0
        Ast = 0
        PK = 0
        PKatt = 0
        CrdY = 0
        CrdR = 0
        
        for d in Data1:
            try:
                RowData = d.select('td')
            except:
                continue
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                MP = MP+int(RowData[4].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                Gls = Gls + int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
               pass
            try:
                Ast = Ast + int(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PK = PK + int(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                PKatt = PKatt + int(RowData[13].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdY = CrdY + int(RowData[14].text.replace('\n','').replace(' ',''))
            except:
                pass
            try:
                CrdR = CrdR + int(RowData[15].text.replace('\n','').replace(' ',''))
            except:
                pass

        player_data['MP'].append(MP)
        player_data['Gls'].append(Gls)
        player_data['Ast'].append(Ast)
        player_data['PK'].append(PK)
        player_data['PKatt'].append(PKatt)
        player_data['CrdY'].append(CrdY)
        player_data['CrdR'].append(CrdR)
    except:
    
        player_data['MP'].append(0)
        player_data['Gls'].append(0)
        player_data['Ast'].append(0)
        player_data['PK'].append(0)
        player_data['PKatt'].append(0)
        player_data['CrdY'].append(0)
        player_data['CrdR'].append(0)
        
        
    try:    
        Data2 = soup.select('#stats_keeper_expanded')[0].select('#stats')
        GA = 0
        GA90 = 0.0
        SoTA = 0.0
        Saves = 0.0
        CS = 0.0
        i = 0
        for d in Data2:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                GA = GA+int(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                GA = GA + 0
            try:
                GA90 = GA90 + float(RowData[9].text.replace('\n','').replace(' ',''))
            except:
                GA90 = GA90 + 0
            try:
                SoTA = SoTA + float(RowData[10].text.replace('\n','').replace(' ',''))
            except:
                SoTA = SoTA + 0
            try:
                Saves = Saves + float(RowData[12].text.replace('\n','').replace(' ',''))
            except:
                Saves = Saves + 0
            try:
                CS = CS + float(RowData[17].text.replace('\n','').replace(' ',''))
            except:
                CS = CS + 0
            i = i + 1    
            
        player_data['GA'].append(GA)
        player_data['GA90'].append(GA90)
        player_data['SoTA'].append(SoTA)
        player_data['Saves%'].append(Saves/i)
        player_data['CS%'].append(CS/i)
    except:
        player_data['GA'].append(0)
        player_data['GA90'].append(0)
        player_data['SoTA'].append(0)
        player_data['Saves%'].append(0)
        player_data['CS%'].append(0)
        
            
            
    try:    
        Data3 = soup.select('#stats_shooting_expanded')[0].select('#stats')
        Sh = 0
        SoT = 0.0
        gsh = 0.0
        i = 0
        for d in Data3:
            RowData = d.select('td')
            if(d.select('th')[0].text.replace('\n','').replace(' ','') == '2021-22'):
                break
            try:
                Sh = Sh + int(RowData[6].text.replace('\n','').replace(' ',''))
            except:
                Sh = Sh + 0
            try:
                SoT = SoT + float(RowData[8].text.replace('\n','').replace(' ',''))
            except:
                SoT = SoT + 0
            try:
                gsh = gsh + float(RowData[11].text.replace('\n','').replace(' ',''))    
            except:
                gsh = gsh + 0
            i = i + 1
            
        player_data['Sh'].append(Sh)
        player_data['SoT%'].append(SoT/i)
        player_data['G/Sh'].append(gsh)
            
    except:
        player_data['Sh'].append(0)
        player_data['SoT%'].append(0)
        player_data['G/Sh'].append(0)
        
        
        
        
    
    
    


# In[31]:


link = 'https://fbref.com/en/players/98ea5115/all_comps/David-Raya-Stats---All-Competitions'
 
Data = requests.get(link)
soup = BeautifulSoup(Data.text)
position = soup.select('p')[0].text
if 'GK' in position:
    position = 'GK'
else:
    position = 'Non-GK'
print(position)


# In[32]:


data = soup.select('#stats_standard_expanded')[0].select('#stats')
season = data[0].select('th')[0].text
MP = 0
for d in data:
    dt = d.select('td')
    MP = MP + int(dt[4].text)
print(MP)
print(len(data))


# In[33]:


shootingdata = soup.select('#stats_shooting_expanded')[0].select('#stats')


# In[34]:


print(shootingdata[0].select('td', {'data-stat' : 'shots'}))


# In[35]:


goalData = soup.select('#stats_keeper_expanded')[0].select('#stats')
tableData = goalData[0].select('td')
for i,data in enumerate(tableData):
    print(i,data.text)


# In[36]:


team_player_data.keys()


# In[37]:


df = pd.read_csv('players_data.csv', index_col = False)


# In[38]:


df


# In[39]:


team_data = pd.read_csv('new_team_data.csv', index_col = False)


# In[40]:


team_data = team_data.drop(['Unnamed: 0'], axis=1)
team_data.head()


# In[41]:



newDF = {'Date' : [], 'Home_Team' : [], 'Away_Team' : [], 'Home_Goal_L5' : [], 'Away_Goal_L5' : [] ,'Home_Win%_L5' : [],
         'Away_Win%_L5' : [] , 'Result' : []}
columns = list(df.columns)
for i in range(15):
   for j in range(len(columns)):
        if j == 0 or j == 1:
           continue
        newDF[f"Hp_{1+i}_" + columns[j]] = []
        newDF[f'Ap_{i+1}_'+ columns[j]] = []
 
for k in range(len(team_data)):
    Date = team_data['Date'][k]
    Home_Team = team_data['Home_Team'][k].replace(' ','')
    if 'Brighton' in Home_Team:
        Home_Team = Home_Team.replace('and','&')    
    Away_Team = team_data['Away_Team'][k].replace(' ','')
    if 'Brighton' in Away_Team:
        Away_Team = Away_Team.replace('and', '&')
    Home_Goal = team_data['Home_Goal_L5'][k]
    Away_Goal = team_data['Away_Goal_L5'][k]
    Hwin = team_data['Home_Win%_L5'][k]
    Awin = team_data['Away_Win%_L5'][k]
    Result = team_data['Result'][k]
    print(Result)
    Home_Player_List = team_player_data[Home_Team][Date]
    Away_Player_List = team_player_data[Away_Team][Date]
    newDF['Date'].append(Date)
    newDF['Home_Team'].append(Home_Team)
    newDF['Away_Team'].append(Away_Team)
    newDF['Home_Goal_L5'].append(Home_Goal)
    newDF['Away_Goal_L5'].append(Away_Goal)
    newDF['Home_Win%_L5'].append(Hwin)
    newDF['Away_Win%_L5'].append(Awin)
    newDF['Result'].append(Result)
    
    for i in range(15):
        if i < len(Home_Player_List):
            H_player = Home_Player_List[i]
            h_id = list(H_player.keys())[0]
            H_fd = df[df['id'] == h_id]
        if i < len(Away_Player_List):
            A_player = Away_Player_List[i]
            A_id = list(A_player.keys())[0]
            A_fd = df[df['id'] == A_id]    
    
        j = 0
        for j in range(len(columns)):
            if j == 0 or j == 1:
                continue
            if i < len(Home_Player_List):    
                H_l = H_fd[columns[j]].tolist() 
                newDF[f"Hp_{i+1}_" + columns[j]].append(H_l[0])
            else:
                newDF[f"Hp_{i+1}_"+columns[j]].append(0)
         
            if i < len(Away_Player_List):    
                A_l = A_fd[columns[j]].tolist() 
                newDF[f"Ap_{i+1}_" + columns[j]].append(A_l[0])
            else:
                newDF[f"Ap_{i+1}_"+columns[j]].append(0)
        i = i + 1       
    


# In[42]:


len(newDF)


# In[54]:


final_df = pd.DataFrame.from_dict(newDF)


# In[55]:


final_df['Result']


# In[56]:


final_df


# In[58]:


final_df.to_csv('final_dataset.csv', index = False)


# In[43]:


team_name_list = list(team_player_data.keys())
print(team_name_list)


# In[44]:


team_match_dates = {}
for team in team_name_list:
    team_match_dates[team] = [dateKeys for dateKeys in team_player_data[team].keys()]


# In[46]:


len(team_match_dates['Liverpool'])

