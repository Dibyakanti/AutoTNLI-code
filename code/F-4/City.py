#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import sys
import json

if './' not in sys.path:
    sys.path.append('./')
    
# from Py_f import Psn as P


# In[3]:


Catg = pd.read_csv("../../autotnlidatasetandcode/table_categories modified.tsv",sep="\t") 


# In[4]:


Ptab = np.array(Catg[Catg.category.isin(["City"])].table_id)
tablesFolder = "../files/json/"


# In[5]:


def parseFile(filename,tablesFolder):
    
    f = open(tablesFolder+filename+".json")
    data = json.load(f)
    data['Tablename'] = filename
    
    return data


# In[6]:


def get_Metro():
    u = set([])
    d = {}
    k = "Metro"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(len(dictionary[k]) >= 2 ):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k][0].split("("))):
                        u.add(dictionary[k][0].split("(")[i].strip(")").lower())
                        d[dictionary['Tablename']].append(dictionary[k][0].split("(")[i].strip(")").lower())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return list(u),d


# In[8]:


# getM()[1]


# In[9]:


def get_Urban():
    u = set([])
    d = {}
    k = "Urban"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(len(dictionary[k]) >= 2 ):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k][0].split("("))):
                        u.add(dictionary[k][0].split("(")[i].strip(")").lower())
                        d[dictionary['Tablename']].append(dictionary[k][0].split("(")[i].strip(")").lower())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return list(u),d


# In[11]:


# getU()[1]


# In[12]:


def get_Density():
    u = set([])
    d = {}
    k = "Density"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(len(dictionary[k]) >= 2 ):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
#                     for i in range(len(dictionary[k][0].split("("))):
                    for i in range(2):
                        u.add(dictionary[k][0].split("(")[i].strip(")").lower())
                        d[dictionary['Tablename']].append(dictionary[k][0].split("(")[i].strip(")").lower())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return list(u),d


# In[14]:


# getD()[1]


# In[13]:


def get_Metro_density():
    u = set([])
    d = {}
    k = "Metro density"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(len(dictionary[k]) >= 2 ):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
#                     for i in range(len(dictionary[k][0].split("("))):
                    for i in range(2):
                        u.add(dictionary[k][0].split("(")[i].strip(")").lower())
                        d[dictionary['Tablename']].append(dictionary[k][0].split("(")[i].strip(")").lower())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return list(u),d


# In[14]:


# getMd()[1]


# In[15]:


def get_Urban_density():
    u = set([])
    d = {}
    k = "Urban density"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(len(dictionary[k]) >= 2 ):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
#                     for i in range(len(dictionary[k][0].split("("))):
                    for i in range(2):
                        u.add(dictionary[k][0].split("(")[i].strip(")").lower())
                        d[dictionary['Tablename']].append(dictionary[k][0].split("(")[i].strip(")").lower())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return list(u),d


# In[16]:


# getUd()[1]


# In[17]:


'''
1.getM 2.getU 3.getD 4.getMd 5.getUd
'''


# In[18]:


def MSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" people "," citizen "," residents "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps = [  ]
            
        else:
            ps=[None]
        return ps
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
#                 All = ','.join(di[tb[it]])
                for i in range(length):
                    s = di[tb[it]][i]
                    if(re.findall("km")):
                        ts.append(  )
                    elif(re.findall("mi")):
                        ts.append()
                    else:
                        ts.append()
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                ts.append(  )
                
        else:
            ts.append(None)
            
        return ts


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




