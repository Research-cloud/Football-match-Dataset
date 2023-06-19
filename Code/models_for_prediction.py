#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_fscore_support
import seaborn as sns
from matplotlib.colors import ListedColormap


# In[2]:


# importing historical data of matches
Targetdf = pd.read_csv('final_dataset.csv')


# In[3]:


Targetdf


# In[4]:


print(Targetdf.columns)
 


# In[5]:


#split into test and train data
y=Targetdf['Result']
X= Targetdf.drop(['Result','Date','Home_Team','Away_Team','Home_Goal_L5','Away_Goal_L5'], axis = 1)
X_train, X_test, y_train, y_test = train_test_split( X,y , random_state=200,test_size=0.20, shuffle=True)


# # Random Forest Classifier

# In[6]:


accList = []
depth = []
MaxAccD = 0
mx = 0
for i in range(100):
    if i == 0:
        continue
    clf = RandomForestClassifier(max_depth=i, random_state=0)
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    if mx < acc:
        mx = acc
        MaxAccD = i
    accList.append(acc)
    depth.append(i)

clf = RandomForestClassifier(max_depth=MaxAccD, random_state=0)
print('Depth :', MaxAccD)
clf.fit(X_train, y_train)
acc = clf.score(X_test, y_test)
print('Accuracy', acc)

plt.plot(depth, accList)
plt.xlabel('depth')
plt.ylabel('accuracy')
plt.show()

y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()

confusion_matrix = metrics.confusion_matrix(y_test, y_predict,labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
 
cm_display.plot()
plt.show()

print(metrics.classification_report(y_test, y_predict))


# # SVM Classifier

# In[7]:


clf = svm.SVC(kernel = 'linear')
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))

clf = svm.SVC(kernel = 'rbf')
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))


clf = svm.SVC(kernel = 'sigmoid')
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))

clf = svm.SVC(kernel = 'poly' , degree = 3)
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))


# # Naive Bayes Classifier

# In[8]:


clf = MultinomialNB()
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test, y_test))
y_predict = clf.predict(X_test)

plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()

confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()

print(metrics.classification_report(y_test, y_predict))


# # KNN 

# In[9]:


mx = 0
n = 0
accList = []
nList = []
for i in range(200):
    if i == 0 or i == 1:
        continue
    neigh = KNeighborsClassifier(n_neighbors=i)
    neigh.fit(X, y)
    acc = neigh.score(X_test, y_test)
    if mx < acc:
        mx = acc;
        n = i
    nList.append(i)
    accList.append(acc)
        
plt.plot(nList, accList)
plt.xlabel('no of neighbours')
plt.ylabel('accuracy')
plt.show()

neigh = KNeighborsClassifier(n_neighbors=n)
neigh.fit(X, y)
acc = neigh.score(X_test, y_test)
print(n)
print('Accuracy :' , acc)


y_predict = neigh.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()

confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = neigh.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = neigh.classes_)
cm_display.plot()
plt.show()

print(metrics.classification_report(y_test, y_predict))


# In[10]:


col_list = []
for i in range(380):
    if y[i] == 'W':
        col_list.append('g')
    elif y[i] == 'D':
        col_list.append('b')
    else:
        col_list.append('r')
plt.scatter(X['Hp_2_MP'], X['Ap_2_MP'], c = col_list)
plt.plot([0.0,0.2,0.4,0.6,0.8,1.0], [0.0,0.2,0.4,0.6,0.8,1.0])

plt.show()


# In[11]:


dff = pd.read_csv('Downloads/final_tweetData_per_match.csv')


# In[12]:


dff
teams = set(dff['Home_Team'])


# In[20]:


totalTweets = {}
for i in range(380):
    team1 = dff['Home_Team'][i]
    team2 = dff['Away_Team'][i]
    tt1 = dff['Home_Pos'][i] + dff['Home_Neg'][i]
    tt2 = dff['Away_Pos'][i] + dff['Away_Neg'][i]
    if team1 not in totalTweets.keys():
        totalTweets[team1] = tt1
    else:
        totalTweets[team1] = totalTweets[team1] + tt1
    if team2 not in totalTweets.keys():
        totalTweets[team2] = tt1
    else:
        totalTweets[team2] = totalTweets[team2] + tt2


fig = plt.figure(figsize = (15, 2.5))        
plt.bar(list(totalTweets.keys())[:10], list(totalTweets.values())[:10], width = 0.2)
plt.xlabel('teams')
plt.ylabel('no. of tweets')
plt.show()   
fig = plt.figure(figsize = (15, 2.5))
plt.bar(list(totalTweets.keys())[10:], list(totalTweets.values())[10:], width = 0.2)
plt.xlabel('teams')
plt.ylabel('no. of tweets')
plt.show()



# In[21]:


ndf = {'Date' : [] , 'Home_Team' : [] , 'Away_Team' : [],'Home_Pos' : [], 'Away_Pos' : [], 'Result' : []}
for i in range(380):
    hpos = float(dff['Home_Pos'][i])
    hneg = float(dff['Home_Neg'][i])
    apos = float(dff['Away_Pos'][i])
    aneg = float(dff['Away_Neg'][i])
    result = dff['Result'][i]
    ndf['Date'].append(dff['Date'][i])
    ndf['Home_Team'].append(dff['Home_Team'][i])
    ndf['Away_Team'].append(dff['Away_Team'][i])
    ndf['Home_Pos'].append(hpos/(hpos+hneg))
    ndf['Away_Pos'].append(apos/(apos+aneg))
    ndf['Result'].append(result)


# In[22]:


newdff = pd.DataFrame.from_dict(ndf)


# In[23]:


newdff


# In[24]:


newdff = newdff.drop(['Date', 'Home_Team' , 'Away_Team'], axis = 1)


# In[25]:


y=newdff['Result']
X= newdff.drop(['Result'], axis = 1)
 
# using the train test split function
X_train, X_test, y_train, y_test = train_test_split( X,y , random_state=175,test_size=0.20, shuffle=True)


# # Random forest classifier

# In[26]:


accList = []
depth = []
MaxAccD = 0
mx = 0
for i in range(100):
    if i == 0:
        continue
    clf = RandomForestClassifier(max_depth=i, random_state=0)
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    if mx < acc:
        mx = acc
        MaxAccD = i
    accList.append(acc)
    depth.append(i)

clf = RandomForestClassifier(max_depth=MaxAccD, random_state=0)
print('Depth :', MaxAccD)
clf.fit(X_train, y_train)
acc = clf.score(X_test, y_test)
print('Accuracy', acc)

plt.plot(depth, accList)
plt.xlabel('depth')
plt.ylabel('accuracy')
plt.show()

y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()

confusion_matrix = metrics.confusion_matrix(y_test, y_predict,labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()

print(metrics.classification_report(y_test, y_predict))


# # SVM classifier

# In[27]:


clf = svm.SVC(kernel = 'linear')
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))

clf = svm.SVC(kernel = 'rbf')
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))


clf = svm.SVC(kernel = 'sigmoid')
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))

clf = svm.SVC(kernel = 'poly' , degree = 3)
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test,y_test))
y_predict = clf.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()
confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()
print(metrics.classification_report(y_test, y_predict))


# # Naive bayes

# In[28]:


clf = MultinomialNB()
clf.fit(X_train, y_train)
print('Accuracy :',clf.score(X_test, y_test))
y_predict = clf.predict(X_test)

plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()

confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = clf.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot()
plt.show()

print(metrics.classification_report(y_test, y_predict))


# # KNN

# In[29]:


mx = 0
n = 0
accList = []
nList = []
for i in range(200):
    if i == 0 or i == 1:
        continue
    neigh = KNeighborsClassifier(n_neighbors=i)
    neigh.fit(X, y)
    acc = neigh.score(X_test, y_test)
    if mx < acc:
        mx = acc;
        n = i
    nList.append(i)
    accList.append(acc)
        
plt.plot(nList, accList)
plt.xlabel('no of neighbours')
plt.ylabel('accuracy')
plt.show()

neigh = KNeighborsClassifier(n_neighbors=n)
neigh.fit(X, y)
acc = neigh.score(X_test, y_test)
print('No of neighbors:',n)
print('Accuracy :' , acc)

y_predict = neigh.predict(X_test)
plt.hist(y_predict)
plt.xlabel('outcomes')
plt.ylabel('no. of occurrences')
plt.show()

confusion_matrix = metrics.confusion_matrix(y_test, y_predict, labels = neigh.classes_)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = neigh.classes_)
cm_display.plot()
plt.show()

print(metrics.classification_report(y_test, y_predict))


# In[ ]:





# In[ ]:




