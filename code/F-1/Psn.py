#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import sys
import math
import json

if './' not in sys.path:
    sys.path.append('./')


# In[3]:


rev_d_Months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
d_Months = {1: 'January',2: 'February',3: 'March',4: 'April',5: 'May',6: 'June',7: 'July',8: 'August',9: 'September',10: 'October',11: 'November',12: 'December'}


# In[4]:


getfa = {
"Psn":{"Spouse":[1],"Occupation":[0,1,2],"Education":[1],"Children":[1],"Genres":[0,1,2],"Labels":[0,1,2],"Website":[1]
  ,"Conviction":[0,1,2],"Institutions":[1],"Fields":[0,1,2],"Doctoral_students":[0,1,2],"Awards":[0,1,2],"Relatives":[0,1]
  ,"Resting_place":[1],"Parents":[1],"Instruments":[0,1,2],"Residence":[1],"Years_active":[1]},
"Movie_tr1":{"Directed_by":[0,1,2],"Produced_by":[0,1,2],"Screenplay_by":[1],"Starring":[0,1,2],"Music_by":[0,1,2],"Cinematography":[1]
  ,"Edited_by":[0,1,2],"Productioncompany":[1],"Distributed_by":[0,1,2],"Release_date":[0,1,2],"Running_time":[1]
  ,"Country":[0,1,2],"Language":[0,1,2],"Budget":[1],"Box_office":[1]},
"Book_tr1":{"Publisher":[1],"Schedule":[1],"Format":[0,1,2],"Genre":[0,1,2],"Publication_date":[1],
        "No_of_issues":[1],"Main_character":[0,1,2],"Written_by":[0,1,2]},
"FnD_tr1":{"Manufacturer":[1],"Country_of_origin":[0,1,2],"Variants":[0,1,2],"Introduced":[1],"Related_products":[0,1,2],
    "Alcohol_by_volume":[1],"Website":[1],"Color":[0,1,2],"Main_ingredients":[0,1,2],"Type":[0,1,2]},
"Organiz_tr1":{"Wesbsite":[1],"Headquarters":[1],"Founded":[1],"Industry":[0,1,2],"Key_people":[0,1,2],"Products":[0,1,2]
	,"Number_of_employees":[1],"Traded_as":[0,1,2],"Founder":[0,1,2],"Area_served":[0,1,2],"Type":[1],"Subsidiaries":[0,1,2]
	,"Parent":[1],"Owner":[1],"Predecessor":[1]},
"Paint_tr1":{"Artist":[1],"Year":[1],"Medium":[1],"Dimensions":[1],"Location":[1]},
"Fest_tr1":{"Type":[0,1,2],"Observed_by":[0,1,2],"Frequency":[1],"Celebrations":[0,1,2],"Significance":[0,1,2],"Observances":[0,1,2],
    "Date":[1],"Related_to":[0,1,2],"Also_called":[0,1,2],"Official_name":[1],"Begins":[1],"Ends":[1],
    "2021_date":[1],"2020_date":[1],"2019_date":[1],"2018_date":[1]},
"SpEv_tr1":{"Venue":[0,1,2],"Date":[1],"Competitors":[0,1,2],"Teams":[1],
	"No_of_events":[1],"Established":[1],"Official_site":[1]},
"Univ_tr1":{"Website":[1],"Type":[0,1,2],"Established":[1],"Undergraduates":[1],"Postgraduates":[1],
    "Motto":[0,1,2],"Location":[1],"Nickname":[1],"Campus":[1],"Colors":[0,1,2],
    "Students":[1],"Academic_staff":[1],"Administrative_staff":[1],"President":[1],"Endowment":[1],"Mascot":[1],
    "Provost":[1],"Sporting_affiliations":[0,1,2],"Academic_affiliations":[0,1,2],"Former_names":[1]}
}


# In[7]:


# Catg = pd.read_csv("../../autotnlidatasetandcode/table_categories modified.tsv",sep="\t") 
Catg = pd.read_csv("/content/drive/My Drive/Auto-TNLI/data/table_categories modified.tsv",sep="\t") 


# In[8]:


Ptab = np.array(Catg[Catg.category.isin(['Person','Musician'])].table_id)
# tablesFolder = "../../autotnlidatasetandcode/tables"
tablesFolder = "/content/drive/My Drive/Auto-TNLI/data/tables"


# In[9]:


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys =[i.text.replace("\xa0"," ") for i in soup.find('tr').find_all('th')]
    vals = []
    for i in soup.find('tr').find_all('td'):
        if(i.parent.find('th')):
            result = [val.text.strip().replace("\n", "").replace("\t", "") for val in i.find_all('li')]
            if not result:
                if(i.find('br')):
                    for x in i.findAll('br'):
                        x.replace_with(',')
#                 print(i.text)
                    result = i.text.split(',')
                if "â€“" in i.text:
                    result = [val.strip().replace("\n", "").replace("\t", "") for val in i.text.split("â€“")]
                elif " to " in i.text:
                    result = [val.strip().replace("\n", "").replace("\t", "") for val in i.text.split("to")]
                else:
                    result = i.text.strip().replace("\n", "").replace("\t", "")
            vals.append(result)
    title = keys[0]
    dictionary = dict(zip(keys[1:], vals))
    dictionary["Title"] = title
    dictionary["Tablename"] = filename.split(".")[0]
    return dictionary


# In[10]:


# Ptab = np.array(Catg[Catg.category.isin(['Person','Musician'])].table_id)
# tablesFolderJ = "../files/json/"
tablesFolderJ = "/content/drive/My Drive/Auto-TNLI/data/json/"
def parseFileJ(filename,tablesFolder):
    
    f = open(tablesFolder+filename+".json")
    data = json.load(f)
    data['Tablename'] = filename
    
    return data


# In[11]:


def get_Table_Title():
    d = {}
    tb = []
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary.keys() and len(dictionary["Born"].split('(')) > 1):
                yB = re.findall("[0-9][0-9][0-9]+-[0-9]+-[0-9]+",dictionary["Born"])
                if(len(yB)>0):
                    tb.append(dictionary['Tablename'])
                    if("Title" in dictionary.keys()):
        #                 print(dictionary['Tablename'],' : ',dictionary['Title'])
                        d[dictionary['Tablename']] = []
                        d[dictionary['Tablename']].append(dictionary['Title'])
                    else:
        #                 print(dictionary['Tablename'],':',"!!!")
                        d[dictionary['Tablename']] = []
                        d[dictionary['Tablename']].append(None)
    return d,tb


# In[12]:


N,T = get_Table_Title()


# In[13]:


'''
d1 : dict for that table
univ : list of a set
df : dataframe of Born/Death to get the table name
sel: selection bit
it : choose table name from the dataframe
'''
def FakeDICT(tb,dn,univ,di,it,sel=0,subNone = True): # selection bit selects whethet to substitute/delete/add
    d1 = di
    univ = list(univ)
    if(sel==0): # add
        if(d1[tb[it]][0]==None):
            d1[tb[it]]=[]
        ulimit = min(2,len(di[tb[it]])+1) # choose an upper limit of how many to add
        n_add = ulimit
        if(ulimit>1):
            n_add = random.randint(1,ulimit)
        add = random.sample(list(set(univ)-set(d1[tb[it]])),n_add)
        d1[tb[it]] =  list(set(d1[tb[it]]).union(set(add)))
        return d1
    elif(sel==1): 
        if(len(di[tb[it]])>0 and di[tb[it]][0] != None):
            if(len(di[tb[it]])>1):
                keep = random.sample(d1[tb[it]],1)
                ulimit = min(len(list(set(univ)-set(d1[tb[it]]))),len(d1[tb[it]])-1)
                substitute = random.sample(list(set(univ)-set(d1[tb[it]])),ulimit)
            else:
                keep=[]
                substitute = random.sample(list(set(univ)-set(d1[tb[it]])),len(d1[tb[it]]))
            d1[tb[it]] =  list(set(substitute).union(set(keep)))
        elif(len(di[tb[it]])>0 and subNone):
            possible_sub = random.sample(list(set(univ)-set(d1[tb[it]])),1)
            for i in range(4): # Probability that none is chose = 1/5
                possible_sub.append(random.sample(list(set(univ)-set(d1[tb[it]])),1)[0])
            possible_sub.append(None)
            sub = random.sample(possible_sub,1)
            d1[tb[it]][random.randint(0,len(d1[tb[it]])-1)] = sub[0]
        return d1
    elif(sel==2): # delete nd : for size = 1
        if(len(di[tb[it]])>1 and di[tb[it]][0] != None):
            llimit = max(1,len(d1[tb[it]])-1)
            keep = random.sample(d1[tb[it]], random.randint(1,llimit) ) 
            d1[tb[it]] = keep
        return d1
    
    return None


# In[14]:


'''
DfB : Date of birth/death dataframe
DfS : Marriage info dataframe
sel : selection bit to select which dataframe to change 
'''
def FakeDFB(DfB):
    df = DfB
    for it in range(len(df)):
        df.Born_Y[it] = df[df.Born_Y != df.Born_Y[it]].sample().Born_Y.tolist()[0]
        if(df.isna().Died_Y[it] != True):
            df.Died_Y[it] = df.loc[df.Died_Y != df.Died_Y[it]].loc[df.Died_Y> df.Born_Y[it]+10].loc[df.Died_Y < df.Born_Y[it]+100].sample().Died_Y.tolist()[0]
            df.Died_M[it] = d_Months[random.randint(1,12)]
            df.Died_D[it] = str(random.randint(1,28))
        df.Born_M[it] = d_Months[random.randint(1,12)]
        df.Born_D[it] = str(random.randint(1,28))
    for i in range(len(df)):
        if(df.isna().Died_Y[it]):
            df.Age[it] = None 
        else:
            df['Age'][it]= int(df['Died_Y'][it]) - int(df['Born_Y'][it])
    return df


# In[15]:


'''
The BIRTH and DEAD dates and then converted them into a dataframe and also found the AGE
'''
def get_BDA(T,N,fake=False,sel=1):
    data={}
    data['Table'] = []
    data['Born_Y'] = []
    data['Born_M'] = []
    data['Born_D'] = []
    data['Died_Y'] = []
    data['Died_M'] = []
    data['Died_D'] = []
    data['Age'] = []
    data['Name'] = []
    placeB = {}
    placeD = {}
#     nn = 0
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary.keys() and len(dictionary["Born"].split('(')) > 1): #and int(dictionary["Born"].split("(")[1].split(')')[0][0])<=9 ):
                yB = re.findall("[0-9][0-9][0-9]+-[0-9]+-[0-9]+",dictionary["Born"])
                if("Died" not in dictionary.keys() and len(yB)>0): # died not in dict
#                     nn = nn+1
                    yB = yB[0]
#                     print(dictionary['Tablename']," "," : ",yB," ; " ,"Still alive !")
                    data["Table"].append(dictionary['Tablename'])
                    data['Born_Y'].append(int(yB.split('-')[0]))
                    data['Born_M'].append(d_Months[int(yB.split('-')[1])])
                    data['Born_D'].append(yB.split('-')[2])
                    data['Died_Y'].append(None)
                    data['Died_M'].append(None)
                    data['Died_D'].append(None)
                    placeD[dictionary['Tablename']] = []
                    placeD[dictionary['Tablename']].append(None)
                    placeB[dictionary['Tablename']] = []
                    if(not re.findall("[0-9]+",dictionary["Born"].split(',')[-1])):
                        braces = re.findall("\([A-Zb-z].*,.*\)",dictionary["Born"])
                        if(braces):
                            dictionary["Born"] = dictionary["Born"].replace(braces[0],"")
                        i = len(dictionary["Born"].split(','))-1
                        while(not re.findall("[0-9]+",dictionary["Born"].split(',')[i]) and i>0):
                            placeB[dictionary['Tablename']].append(dictionary["Born"].split(',')[i].strip())
                            i = i-1
                    else:
                        placeB[dictionary['Tablename']].append(None)
                    data['Name'].append(dictionary["Title"])    
                
                elif(len(yB)>0): # died in dict
                    yB = yB[0]
                    yD = re.findall("[0-9][0-9][0-9]+-[0-9]+-[0-9]+",dictionary["Died"])[0]
                    data["Table"].append(dictionary['Tablename'])
                    data['Born_Y'].append(int(yB.split('-')[0]))
                    data['Born_M'].append(d_Months[int(yB.split('-')[1])])
                    data['Born_D'].append(yB.split('-')[2])
                    data['Died_Y'].append(int(yD.split('-')[0]))
                    data['Died_M'].append(d_Months[int(yD.split('-')[1])])
                    data['Died_D'].append(yD.split('-')[2])
                    placeD[dictionary['Tablename']] = []
                    placeB[dictionary['Tablename']] = []
                    if(not re.findall("[0-9]+",dictionary["Born"].split(',')[-1])):
                        braces = re.findall("\([A-Zb-z].*,.*\)",dictionary["Born"])
                        if(braces):
                            dictionary["Born"] = dictionary["Born"].replace(braces[0],"")
                        i = len(dictionary["Born"].split(','))-1
                        while(not re.findall("[0-9]+",dictionary["Born"].split(',')[i]) and i>0):
                            placeB[dictionary['Tablename']].append(dictionary["Born"].split(',')[i].strip())
                            i = i-1
                    else:
                        placeB[dictionary['Tablename']].append(None)
                    if(not re.findall("[0-9]+",dictionary["Died"].split(',')[-1])):
                        i = -1
                        if(braces):
                            dictionary["Died"] = dictionary["Died"].replace(braces[0],"")
                        while(not re.findall("[0-9]+",dictionary["Died"].split(',')[i])):
                            placeD[dictionary['Tablename']].append(dictionary["Died"].split(',')[i].strip())
                            i = i-1
                    else:
                        placeD[dictionary['Tablename']].append(None)
                    data['Name'].append(dictionary["Title"])
    df = pd.DataFrame(data,columns=['Table','Name','Born_Y','Born_M','Born_D','Died_Y'])
    
    for i in range(len(df['Table'])):
        if(df.isna().Died_Y[i]):
            data['Age'].append(None) # have to be removed 2020 - int(data['Born_Y'][i])
        else:
            data['Age'].append(int(data['Died_Y'][i]) - int(data['Born_Y'][i]))

    df = pd.DataFrame(data,columns=['Table','Name','Born_Y','Born_M','Born_D','Died_Y','Died_M','Died_D','Age'])
    
    country = set([])
    state = set([])
    place = set([])
    
    for i in placeB.keys(): # rules for getting country,state,place to be used while making sentences
        p = placeB[i]
#         print(i,p)
        if(p[0] != None):
            if(len(p)==1):
                place.add(p[0])
            elif(len(p)==2):
                country.add(p[0])
                place.add(p[1])
            else:
                country.add(p[0])
                state.add(p[1])
                place.add(p[2])
                
    for i in placeD.keys():
        p = placeD[i]
        if(p[0] != None):
            if(len(p)==1):
                place.add(p[0])
            elif(len(p)==2):
                country.add(p[0])
                place.add(p[1])
            else:
                country.add(p[0])
                state.add(p[1])
                place.add(p[2])
    
    if(fake):
        df = FakeDFB(df)
        for it in range(len(T)):
            def substitute(d2,d1,it):
                sub = random.sample(list(set(d2)-set(d1[it])),1)
                d1[it] = sub[0]
                return d1

            p = placeB[T[it]]
            if(p[0] != None):
                if(len(p)==1):
                    p = substitute(place,p,0)
                elif(len(p)==2):
                    p = substitute(country,p,0)
                    p = substitute(place,p,1)
                else:
                    p = substitute(country,p,0)
                    p = substitute(state,p,1)
                    p = substitute(place,p,2)

            placeB[T[it]] = p

            p = placeD[T[it]]
            if(p[0] != None):
                if(len(p)==1):
                    p = substitute(place,p,0)
                elif(len(p)==2):
                    p = substitute(country,p,0)
                    p = substitute(place,p,1)
                else:
                    p = substitute(country,p,0)
                    p = substitute(state,p,1)
                    p = substitute(place,p,2)

            placeD[T[it]] = p
        
    return df,placeB,placeD,country,state,place


# In[16]:


# get_BDA(T,N)[0]


# In[17]:


def get_Spouse(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Spouse"
    k2 = "Spouse(s)"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFileJ(Ptab[n], tablesFolderJ)
            dictionary2 = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary2.keys() and len(dictionary2["Born"].split('(')) > 1):
                d[dictionary['Tablename']] = []
                if(k1 in dictionary.keys()):
                    if(type(dictionary[k1]) == list):
                        for i in range(len(dictionary[k1])):
                            u.add(dictionary[k1][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k1][i].replace("\xa0"," "))
                    else:
                        for i in range(len(dictionary[k1].replace(",(","(").split(","))):
                            u.add(dictionary[k1].replace(",(","(").split(",")[i].replace(",(","(").replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k1].replace(",(","(").split(",")[i].replace(",(","(").replace("\xa0"," "))

                if(k2 in dictionary.keys()):
                    if(type(dictionary[k2]) == list):
                        for i in range(len(dictionary[k2])):
                            u.add(dictionary[k2][i].replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k2][i].replace("\xa0"," "))
                    else:
                        for i in range(len(dictionary[k2].replace(",(","(").split(","))):
                            u.add(dictionary[k2].split(",")[i].replace(",(","(").replace("\xa0"," "))
                            d[dictionary['Tablename']].append(dictionary[k2].replace(",(","(").split(",")[i].replace(",(","(").replace("\xa0"," "))

                if(k1 not in dictionary.keys() and k2 not in dictionary.keys()):
                    d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k1.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[18]:


# get_Spouse(T,N,1)[1]


# In[19]:


def get_Children(T,N,fake=False,sel=0):
    u = set([])
    ds = {}
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary.keys() and len(dictionary["Born"].split('(')) > 1):
#                 ds['Table'].append(dictionary['Tablename'])
                if("Children" in dictionary.keys()):
                    ds[dictionary["Tablename"]] = []
#                     print(dictionary['Tablename'],':',dictionary["Children"])
                    if(type(dictionary['Children']) == list):
#                         ds['No.Ch'].append(len(dictionary['Children']))
                        u.add(len(dictionary['Children']))
                        ds[dictionary["Tablename"]].append(len(dictionary['Children']))
                    elif(len(dictionary['Children'].split(",")) <= 1):
                        n = 0;
                        t = 1;
                        for i in range(len(re.findall('[0-9]',dictionary['Children']))):
                            n = n + t*int(re.findall('[0-9]',dictionary['Children'])[len(re.findall('[0-9]',dictionary['Children'])) - i -1 ])                        
                            t = t*10
#                         ds['No.Ch'].append(n)
                        u.add(n)
                        ds[dictionary["Tablename"]].append(n)
                    else:
                        ds[dictionary["Tablename"]].append(None)
                else:
                    ds[dictionary["Tablename"]] = []
                    ds[dictionary["Tablename"]].append(None)

    
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"]["Children"],1)[0]
            if(sel==2 and len(L[T[it]])<2):
                sel = 1
            ds= FakeDICT(T,N,u,ds,it,sel)
            
    return list(u),ds


# In[20]:


# get_Children(T,N)[1]


# In[21]:


def get_Occupation(T,N,fake=False,sel=0):
    s = set([]) # universal set of all occupations
    occ = {}    # dictionary of table number to occupation
    k = "Occupation"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary.keys() and len(dictionary["Born"].split('(')) > 1): #and int(dictionary["Born"].split("(")[1].split(')')[0][0])<=9 ):
                if "Occupation" in dictionary.keys():
                    occ[dictionary['Tablename']] = []
                    if(type(dictionary['Occupation'])==list):
#                         print(dictionary['Tablename'],':',dictionary["Occupation"])
                        for i in range(len(dictionary['Occupation'])):
                            s.add(dictionary['Occupation'][i])
                            occ[dictionary['Tablename']].append(dictionary['Occupation'][i])
                    else:
#                         print(dictionary['Tablename'],':',dictionary["Occupation"].split(', '))
                        for i in range(len(dictionary['Occupation'].split(', '))):
                            s.add(dictionary['Occupation'].split(', ')[i])
                            occ[dictionary['Tablename']].append(dictionary['Occupation'].split(', ')[i])
                else:
                    occ[dictionary['Tablename']] = []
                    occ[dictionary['Tablename']].append(None)
#                     print(dictionary['Tablename'],':',"!!!")
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(occ[T[it]])<2):
                sel = 1
            occ = FakeDICT(T,N,s,occ,it,sel)
        
    return list(s),occ


# In[22]:


# getOcc(T,N,0)[1]


# In[86]:


def get_Education(T,N,fake=False,sel=0):  
    u = set([])
    ed = {}
    al = {}
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFileJ(Ptab[n], tablesFolderJ)
            dictionary2 = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary2.keys() and len(dictionary2["Born"].split('(')) > 1):
                ed[dictionary['Tablename']] = []
                al[dictionary['Tablename']] = []
                if("Education" in dictionary.keys()):
#                     print(dictionary['Tablename'],':',re.findall("[a-zA-Z ][a-zA-Z]+","".join(dictionary["Education"]) ))
                    if(type(dictionary['Education']) == list): #and len(dictionary['Education'])>1):
                        dictionary['Education'] = ", ".join(dictionary['Education'])
                        dictionary['Education'] = re.sub("\(.*\)","",dictionary['Education'])
                        for i in range(len(dictionary['Education'].split(','))):
                            u.add(dictionary['Education'].split(',')[i].strip())
                            ed[dictionary['Tablename']].append(dictionary['Education'].split(',')[i].strip())  
                            al[dictionary['Tablename']].append(None)
                    else:
                        dictionary['Education'] = re.sub("\(.*\)","",dictionary['Education'])
                        for i in range(len(dictionary['Education'].split(','))):
                                u.add(dictionary['Education'].split(',')[i].strip())
                                ed[dictionary['Tablename']].append(dictionary['Education'].split(',')[i].strip())  
                                al[dictionary['Tablename']].append(None)
                                
                elif("Alma mater" in dictionary.keys()):
#                     print(dictionary['Tablename'],':',re.findall("[a-zA-Z ][a-zA-Z ]+","".join(dictionary["Alma mater"]) ))
                    if(type(dictionary['Alma mater']) == list): #and len(dictionary['Alma mater'])>1):
                        dictionary['Alma mater'] = ", ".join(dictionary['Alma mater'])
                        dictionary['Alma mater'] = re.sub("\(.*\)","",dictionary['Alma mater'])
                        for i in range(len(dictionary['Alma mater'].split(','))):
                            u.add(dictionary['Alma mater'].split(',')[i].strip())
                            al[dictionary['Tablename']].append(dictionary['Alma mater'].split(',')[i].strip())
                            ed[dictionary['Tablename']].append(None)
                    else:
                        dictionary['Alma mater'] = re.sub("\(.*\)","",dictionary['Alma mater'])
                        for i in range(len(dictionary['Alma mater'].split(','))):
                                u.add(dictionary['Alma mater'].split(',')[i].strip())
                                al[dictionary['Tablename']].append(dictionary['Alma mater'].split(',')[i].strip())
                                ed[dictionary['Tablename']].append(None)
                else:
#                     print(dictionary['Tablename'],':',"?!!")
                    ed[dictionary['Tablename']].append(None)
                    al[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"]["Education"],1)[0]
            if(sel==2 and len(ed[T[it]])<2):
                sel = 1
            ed = FakeDICT(T,N,u,ed,it,sel,subNone = False)
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"]["Education"],1)[0]
            if(sel==2 and len(al[T[it]])<2):
                sel = 1
            al = FakeDICT(T,N,u,al,it,sel,subNone = False)
        
    return list(u),ed,al


# In[89]:


# get_Education(T,N,True)


# In[111]:


def get_Genres(T,N,fake=False,sel=0):
    s = set([])
    G = {}
    k = "Genres"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFileJ(Ptab[n], tablesFolderJ)
            dictionary2 = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary2.keys() and len(dictionary2["Born"].split('(')) > 1):
                G[dictionary['Tablename']] = []
                if("Genres" in dictionary.keys()):
                    if(type(dictionary[k]) == list):
                        for i in range(len(dictionary[k])):
                            s.add(dictionary[k][i].replace(",,",","))
                            G[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                    else:
                        dictionary[k].replace(",,",",")
                        for i in range(len(dictionary[k].split(","))):
                            s.add(dictionary[k].split(",")[i])
                            G[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                else:
                    G[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(G[T[it]])<2):
                sel = 1
            G = FakeDICT(T,N,s,G,it,sel)
        
    return list(s),G


# In[113]:


# get_Genres(T,N)[1]


# In[104]:


def get_Labels(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Labels"
    for n in range(700):
        if(int(Ptab[n][1:]) <= 2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary.keys() and len(dictionary["Born"].split('(')) > 1):
                d[dictionary['Tablename']] = []
                if("Labels" in dictionary.keys()):
                    if(type(dictionary[k]) == list):
                        for i in range(len(dictionary[k])):
                            u.add(dictionary[k][i].replace(",,",","))
                            d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                    else:
                        dictionary[k].replace(",,",",")
                        for i in range(len(dictionary[k].split(","))):
                            u.add(dictionary[k].split(",")[i])
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                else:
                    d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d= FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[108]:


# get_Labels(T,N)[1]


# In[157]:


def get_Website(T,N,fake=False,sel=0):
    W = {}
    u = set([])
    k = "Website"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary.keys() and len(dictionary["Born"].split('(')) > 1):
                W[dictionary['Tablename']] = []
                if("Website" in dictionary.keys() and re.findall("\.",dictionary['Website'])):
                    W[dictionary['Tablename']] = [dictionary['Website']]
                    u.add(dictionary['Website'])
                else:
                    W[dictionary['Tablename']].append(None) 
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(W[T[it]])<2):
                sel = 1
            W = FakeDICT(T,N,u,W,it,sel)
        
    return list(u),W


# In[159]:


# get_Website(T,N)[1]


# In[132]:


def get_Conviction(T,N,fake=False,sel=0):
    s = set([])
    C = {}
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if ("Born" in dictionary.keys() and len(dictionary["Born"].split('(')) > 1):
                C[dictionary['Tablename']] = []
                if("Conviction(s)" in dictionary.keys()):
                    k = "Conviction(s)"
                    if(type(dictionary[k]) == list):
                        for i in range(len(dictionary[k])):
                            s.add(dictionary[k][i].replace(",,",","))
                            C[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                    else:
                        dictionary[k].replace(",,",",")
                        for i in range(len(dictionary[k].split(","))):
                            s.add(dictionary[k].split(",")[i])
                            C[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                elif("Criminal charge" in dictionary.keys()):
                    k = "Criminal charge"
                    if(type(dictionary[k]) == list):
                        for i in range(len(dictionary[k])):
                            s.add(dictionary[k][i].replace(",,",","))
                            C[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                    else:
                        dictionary[k].replace(",,",",")
                        for i in range(len(dictionary[k].split(","))):
                            s.add(dictionary[k].split(",")[i])
                            C[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                else:
                    C[dictionary['Tablename']].append(None) 
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"]["Conviction"],1)[0]
            if(sel==2 and len(C[T[it]])<2):
                sel = 1
            C = FakeDICT(T,N,s,C,it,sel)
        
    return list(s),C


# In[134]:


# get_Conviction(T,N)[1]


# #### Extract all data:

# In[73]:


def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["BDA","Spouse","Occupation","Education","Children","Genres","Labels"
          ,"Website","Conviction","Institutions","Fields","Doctoral_students","Awards"
          ,"Relatives","Resting_place","Parents","Instruments","Residence","Years_active"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data
# F is the Extracted_data[key]


# In[75]:


# get_Data()


# ### Rules and functions to create sentences

# In[32]:


'''
Born sentences true and false
df : Birth dataframe
'''
def BornSent(tb,dn,F,it,tval=True,prem=False):
    df = F[0]
    pB = F[1]
    pD = F[2]
    C = F[3]
    S = F[4]
    P = F[5]
    Nm = dn[tb[it]][0]
    if(prem):
        ps1 = [ "The person named "+df['Name'][it]+"'s date of birth is "+str(df['Born_M'][it])+" "+str(df['Born_D'][it])+", "+str(df['Born_Y'][it]) 
               , str(df['Born_M'][it])+" "+str(df['Born_D'][it])+", "+str(df['Born_Y'][it]) + " is when " + df['Name'][it] + " was born" 
               , "On "+str(df['Born_M'][it])+" "+str(df['Born_D'][it])+", "+str(df['Born_Y'][it]) +" a person named "+df['Name'][it]+" was born"]

        return ps1
    
    else:
        ts = []
        if(tval):
            # Born on
            ts.append(df['Name'][it]+" was born on "+str(df['Born_M'][it])+" "+str(df['Born_D'][it])+", "+str(df['Born_Y'][it]))
            # Born before
            if(df[df.Born_Y > (df.Born_Y[it])].Table.count() != 0):
                ts.append(df['Name'][it]+" was born before " + str(df[df.Born_Y > (df.Born_Y[it])].sample()['Born_Y'].tolist()[0]))
            elif(df[df.Died_Y > (df.Born_Y[it])].Table.count()!=0):
                ts.append(df['Name'][it]+" was born before " + str(df[df.Died_Y > (df.Born_Y[it])].sample()['Died_Y'].tolist()[0]))
            else:
                ts.append(df['Name'][it]+" was born before " + str(df['Born_Y'][it]+13))
            # Born after    
            if(df[df.Born_Y < (df.Born_Y[it])].Table.count() != 0):
                ts.append(df['Name'][it]+" was born after " + str(df[df.Born_Y < (df.Born_Y[it])].sample()['Born_Y'].tolist()[0]))
            elif(df[df.Died_Y < (df.Born_Y[it])].Table.count()!=0):
                ts.append(df['Name'][it]+" was born after " + str(df[df.Died_Y < (df.Born_Y[it])].sample()['Died_Y'].tolist()[0]))
            else:
                ts.append(df['Name'][it]+" was born after " + str(df['Born_Y'][it]-17))
            # Is a leap year
            if(df.Born_Y[it]%400==0):
                ts.append(df['Name'][it] + " was born in a leap year")
            elif(df.Born_Y[it]%100==0):
                ts.append(df['Name'][it] + " was not born in a leap year")
            elif(df.Born_Y[it]%4==0):
                ts.append(df['Name'][it] + " was born in a leap year")
            else:
                ts.append(df['Name'][it] + " was not born in a leap year")
            # Century
            cent = int(df.Born_Y[it]/100)+1
            if(cent == 21):
                ts.append(df['Name'][it] + " was born in 21st century")
            else:
                ts.append(df['Name'][it] + " was born in " + str(cent) + "th century")
            # Place
            if(pB[tb[it]][0]!=None):
                ts.append("The person was born in "+random.sample(pB[tb[it]],1)[0])
                
                
        else:# False statements
            # Born on
            ts.append(df.Name[it] + " was born on " + str(d_Months[random.randint(1,12)])+" "+str(random.randint(1,28))+", "+ str(random.randint(df['Born_Y'][it]-6,df['Born_Y'][it]-1))) 
            # Born after
            if(df[df.Born_Y > (df.Born_Y[it])].Table.count() != 0):
                ts.append(df['Name'][it]+" was born after " + str(df[df.Born_Y > (df.Born_Y[it])].sample()['Born_Y'].tolist()[0]))
            elif(df[df.Died_Y > (df.Born_Y[it])].Table.count()!=0):
                ts.append(df['Name'][it]+" was born after " + str(df[df.Died_Y > (df.Born_Y[it])].sample()['Died_Y'].tolist()[0]))
            else:
                ts.append(df['Name'][it]+" was born after " + str(df['Born_Y'][it]+13))
            # Born before    
            if(df[df.Born_Y < (df.Born_Y[it])].Table.count() != 0):
                ts.append(df['Name'][it]+" was born before " + str(df[df.Born_Y < (df.Born_Y[it])].sample()['Born_Y'].tolist()[0]))
            elif(df[df.Died_Y < (df.Born_Y[it])].Table.count()!=0):
                ts.append(df['Name'][it]+" was born before " + str(df[df.Died_Y < (df.Born_Y[it])].sample()['Died_Y'].tolist()[0]))
            else:
                ts.append(df['Name'][it]+" was born before " + str(df['Born_Y'][it]-17))
            # Is a leap year
            if(df.Born_Y[it]%400==0):
                ts.append(df['Name'][it] + " was not born in a leap year")
            elif(df.Born_Y[it]%100==0):
                ts.append(df['Name'][it] + " was born in a leap year")
            elif(df.Born_Y[it]%4==0):
                ts.append(df['Name'][it] + " was not born in a leap year")
            else:
                ts.append(df['Name'][it] + " was born in a leap year")
            # Century
            cent = int(df.Born_Y[it]/100)- random.randint(0,3)
            if(cent == 21):
                ts.append(df['Name'][it] + " was born in 21st century")
            else:
                ts.append(df['Name'][it] + " was born in " + str(cent) + "th century")
            if(pB[tb[it]][0]!=None):
                NP = random.sample(list(set(C).union(set(S),set(P))-set(pB[tb[it]])),1)[0]
                ts.append("The person was born in "+NP)
                
        return ts        


# In[44]:


# BSent(T,N,getBirthDeathAge(300),125,False)


# In[33]:


def DiedSent(tb,dn,F,it,tval=True,prem=False):
    df = F[0]
    pB = F[1]
    pD = F[2]
    C = F[3]
    S = F[4]
    P = F[5]
    Nm = dn[tb[it]][0]
    if(prem):
        if(df.isna().Died_Y[it] == False):
            ps1 = [ "The person named "+df['Name'][it]+" died on "+str(df['Died_M'][it])+" "+str(df['Died_D'][it])+","+str(int(df['Died_Y'][it])) 
                   , str(df['Died_M'][it])+" "+str(df['Died_D'][it])+","+str(int(df['Died_Y'][it])) + " is when " + df['Name'][it] + " died" 
                   , "On "+str(df['Died_M'][it])+" "+str(df['Died_D'][it])+","+str(int(df['Died_Y'][it])) +" a person named "+df['Name'][it]+" died"]
        else:
            ps1 = [None]
            
        return ps1
    
    else:
        ts = []
        if(tval):
            if(df.isna().Died_Y[it] == False):
                # Died on
                ts.append(df.Name[it] + " died on " + str(df['Died_M'][it])+" "+str(df['Died_D'][it])+","+ str(int(df['Died_Y'][it])))
                # Died before
                ts.append(df.Name[it] + " died before " + str(random.randint(int(df['Died_Y'][it])+1,int(df['Died_Y'][it])+5)))
                # Died after
                ts.append(df.Name[it] + " died after " + str(random.randint(int(df['Died_Y'][it])-5,int(df['Died_Y'][it])-1)))
                # Is a leap year
                if(df.Died_Y[it]%400==0):
                    ts.append(df['Name'][it] + " died in a leap year")
                elif(df.Died_Y[it]%100==0):
                    ts.append(df['Name'][it] + " did not die in a leap year")
                elif(df.Died_Y[it]%4==0):
                    ts.append(df['Name'][it] + " died in a leap year")
                else:
                    ts.append(df['Name'][it] + " did not die in a leap year")
                # Century
                cent = int(df.Died_Y[it]/100)+1
                if(cent == 21):
                    ts.append(df['Name'][it] + " was born in 21st century")
                else:
                    ts.append(df['Name'][it] + " was born in " + str(cent) + "th century")
                if(pD[tb[it]][0]!=None):
                    ts.append("The person was born in "+random.sample(pD[tb[it]],1)[0])

            else:
                ts.append(None)

        else:
            if(df.isna().Died_Y[it] == False):
                # Died on 
                ts.append(df.Name[it] + " died on " + str(d_Months[random.randint(1,12)])+" "+str(random.randint(1,28))+", "+ str(random.randint(df['Died_Y'][it]+1,df['Died_Y'][it]+8)))
                # Died after
                ts.append(df.Name[it] + " died after " + str(random.randint(int(df['Died_Y'][it])+1,int(df['Died_Y'][it])+5)))
                # Died before
                ts.append(df.Name[it] + " died before " + str(random.randint(int(df['Died_Y'][it])-5,int(df['Died_Y'][it])-1)))
                # Is a leap year
                if(df.Died_Y[it]%400==0):
                    ts.append(df['Name'][it] + " did not die in a leap year")
                elif(df.Died_Y[it]%100==0):
                    ts.append(df['Name'][it] + " died in a leap year")
                elif(df.Died_Y[it]%4==0):
                    ts.append(df['Name'][it] + " did not die in a leap year")
                else:
                    ts.append(df['Name'][it] + " died in a leap year")
                # Century
                cent = int(df.Died_Y[it]/100) - random.randint(0,3)
                if(cent == 21):
                    ts.append(df['Name'][it] + " was born in 21st century")
                else:
                    ts.append(df['Name'][it] + " was born in " + str(cent) + "th century")
                if(pD[tb[it]][0]!=None):
                    NP = random.sample(list(set(C).union(set(S),set(P))-set(pD[tb[it]])),1)[0]
                    ts.append("The person was born in "+NP)

            else:
                ts.append(None)

        return ts


# In[2]:


# DSent(T,N,getBDA(T,N,0),2,True,True)


# In[37]:


def AgeSent(tb,dn,F,it,tval=True,prem=False):
    df = F[0]
    if(prem):
        if(df.isna().Age[it] == False):
            ps1 = [ "The person's age was "+str(int(df.Age[it]))
                   ,str(int(df.Age[it]))+" was the age of the person"]
        else:
            ps1 = [None]
            
        return ps1
    
    ts = []
    if(tval):
        if(df.isna().Age[it] == False):
            ts.append(df.Name[it]+"\'s age was "+ str(int(df.Age[it])) +' when he died')
            ts.append(df.Name[it]+" lived to "+str(int(df.Age[it]))+" age")
            ts.append(df.Name[it]+" was "+str(int(df.Age[it]))+" years old when he died")
            age = df.Age[it]
            if(age<13):
                ts.append(df.Name[it]+" died as a child")
            elif(age>=13 and age<18):
                ts.append(df.Name[it]+" died as a teenager")
            elif(age>=18 and age<35):
                ts.append(df.Name[it]+" died as a younger adult")
            elif(age>=35 and age<55):
                ts.append(df.Name[it]+" died as a middle-aged adult")
            elif(age>=55):
                ts.append(df.Name[it]+" died as an old adult")
            
        else:
            ts.append(None)
            
    else:
        if(df.isna().Age[it] == False):
            ts.append(df.Name[it] +"\'s age was "+ str(random.randint(df.Age[it]-10,df.Age[it]-1)) +' when he died')
            ts.append(df.Name[it]+" lived to "+str(random.randint(df.Age[it]-10,df.Age[it]-1))+" age")
            ts.append(df.Name[it]+" was "+str(random.randint(df.Age[it]-10,df.Age[it]-1))+" years old when he died")
            age = df.Age[it]
            u = set(["child","teenager","younger adult","middle-aged adult","old adult"])
            if(age<13):
                ts.append(df.Name[it]+" died as a "+random.sample(list(u-set(["child"])),1)[0] )
            elif(age>=13 and age<18):
                ts.append(df.Name[it]+" died as a "+random.sample(list(u-set(["teenager"])),1)[0])
            elif(age>=18 and age<35):
                ts.append(df.Name[it]+" died as a "+random.sample(list(u-set(["younger adult"])),1)[0])
            elif(age>=35 and age<55):
                ts.append(df.Name[it]+" died as a "+random.sample(list(u-set(["middle-aged adult"])),1)[0])
            elif(age>=55):
                ts.append(df.Name[it]+" died as a "+random.sample(list(u-set(["old adult"])),1)[0])
        else:
            ts.append(None)

    return ts


# In[1]:


# ASent(T,N,getBDA(T,N,0),2,False,True)


# In[23]:


def OccupationSent(tb,dn,F,it,tval=True,prem=False): # input : dictionary,list(uninversal),...
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ Nm+" worked as a "+All
                   ,All+" are the occupations of this person"
                   ,All+" are the person's occupation"  ]
        else:
            ps1 = [None]
            
        return ps1
    
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                ts.append(Nm + " has " + str(len(di[tb[it]])) + " occupations")
                ts.append(Nm + " is a " + random.sample(di[tb[it]],1)[0])
                ts.append(Nm + " had more than " + str(random.randint(0,len(di[tb[it]])-1)) + " occupations")
                ts.append(Nm + " had less than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5)) + " occupations")
            else:
                ts.append(None)
        else: # Not done
            if(len(di[tb[it]]) != 0):
                ts.append(Nm + " has " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+8)) + " occupations")
                ts.append(Nm + " is a " + random.sample(list(set(univ)-set(di[tb[it]])),1)[0])
                ts.append(Nm + " had more than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5)) + " occupations")
                ts.append(Nm + " had less than " + str(random.randint(0,len(di[tb[it]])-1)) + " occupations")
            else:
                ts.append(None)
    
    return ts


# In[43]:


# OccSent(T,N,getOcc(T,N,0),2,True,True)


# In[48]:


def SpouseSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        All = ", ".join(di[tb[it]])
        if(di[tb[it]][0] != None):
            ps1 = [ Nm+" was wedded to "+All
                   ,Nm+" was married with "+All
                   ,Nm+" got married to "+All]
        else:
            ps1 = [None]
        return ps1

    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                c = random.sample(di[tb[it]],1)[0]
                m = c.split("(")[0]
                y = re.findall("[0-9][0-9]+",c)
                n = len(di[tb[it]])
                ts.append(Nm+" was married to " +m)
                ts.append(Nm+" has married "+str(n)+" times")
                ts.append(Nm+" has married more than "+str(random.randint(0,n-1))+" times")
                ts.append(Nm+" has married less than "+str(random.randint(n+1,n+4))+" times" )
                if(n>1):
                    ts.append(Nm+" was divorced atleast once")
                else:
                    ts.append(Nm+" was never divorced")
                if(len(y) != 0):
                    ts.append(Nm+" was married to "+m+" from "+y[0])
                if(len(y)>1):
                    span = int(y[1])-int(y[0])
                    ts.append(Nm+" was married to "+m+" for "+str(span)+" years")
            
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                c = random.sample(NT,1)[0]
                m = c.split("(")[0]
                y = re.findall("[0-9][0-9]+",c)
                n = len(di[tb[it]])
                ts.append(Nm+" was married to " +m)
                ts.append(Nm+" has married "+str(random.randint(n+1,n+7))+" times")
                ts.append(Nm+" has married less than "+str(random.randint(0,n-1))+" times")
                ts.append(Nm+" has married more than "+str(random.randint(n+1,n+4))+" times" )
                if(n>1):
                    ts.append(Nm+" was never divorced")
                else:
                    ts.append(Nm+" was divorced atleast once")
                if(len(y) != 0):
                    ts.append(Nm+" was married to "+m+" from "+y[0])
                if(len(y)>1):
                    span = int(y[1])-int(y[0])
                    ts.append(Nm+" was married to "+m+" for "+str(random.randint(span+1,span+5))+" years")
            
            else:
                ts.append(None)
        
        return ts


# In[49]:


# SpSent(T,N,getSp(T,N,0),2,True,True)


# In[53]:


def ChildrenSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ "The person has "+str(int(di[tb[it]][0]))+" kids"
                   ,str(int(di[tb[it]][0]))+" is the number of kids that the person has"
                   ,str(int(di[tb[it]][0]))+" is the number of children that the person has" ]
        else:
            ps1 = [None]
        return ps1

    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                ts.append(Nm + " has " + str(int(di[tb[it]][0])) + " children")
                ts.append(Nm + " has less than " + str(random.randint(di[tb[it]][0]+1,di[tb[it]][0]+4)) + " children")
            else:
                ts.append(None)

        else:
            if(di[tb[it]][0] != None):
                ts.append(Nm + " has " + str(random.randint(di[tb[it]][0]+1,di[tb[it]][0]+4)) + " children")
                ts.append(Nm + " has less than " + str(int(di[tb[it]][0]-1)) + " children")
            else:
                ts.append(None)
    
        return ts


# In[54]:


# ChSent(T,N,getCh(),3,True)


# In[56]:


def multi_row1(tb,dn,F,it,tval=True):
    Uc,C = F["Children"]
    Us,S = F["Spouse"]
    B = F["BDA"][0]
    
    Nm = dn[tb[it]][0]
    ts = {}
    y = []
    if(S[tb[it]][0] != None):
        y = re.findall("[0-9][0-9]+",S[tb[it]][0])
    
    if(tval):
        if(C[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Children,Spouse"] = []
#             Al1 = ", ".join(random.sample(T[tb[it]],1))
            Al1 = int(C[tb[it]][0])
            Al2 = len(S[tb[it]])
            ts["Children,Spouse"].append( Nm+" has "+str(Al1)+" children and "+str(Al2)+" number of spouses" )
        
        if(B.isna().Born_Y[it]==False and len(y) != 0):
            ts["Born,Spouse"] = []
            age = int(y[0])-int(B.Born_Y[it])
            ts["Born,Spouse"].append(Nm+" was married "+str(age)+" years after being born")
        if(B.isna().Born_Y[it]==False and len(y)>1):
#             ts["Born,Spouse"] = []
            age = int(y[1])-int(B.Born_Y[it])
            ts["Born,Spouse"].append(Nm+" was divorced "+str(age)+" years after being born")
        
        if(B.isna().Died_Y[it]==False and len(y) != 0):
            ts["Died,Spouse"] = []
            age = int(B.Died_Y[it])-int(y[0])
            ts["Died,Spouse"].append(Nm+" was married "+str(age)+" years before dying")
        if(B.isna().Died_Y[it]==False and len(y)>1):
            age = int(B.Died_Y[it])-int(y[1])
            ts["Died,Spouse"].append(Nm+" was divorced "+str(age)+" years before dying")
            
        
    else:
        if(C[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Children,Spouse"] = []
            Al1 = int(C[tb[it]][0])
            Al2 = len(S[tb[it]])
            Al1 = random.randint(Al1+2,Al1+5)
            Al2 = random.randint(Al2+2,Al2+5)
            ts["Children,Spouse"].append( Nm+" has "+str(Al1)+" children and "+str(Al2)+" number of spouses" )
        
        if(B.isna().Born_Y[it]==False and len(y) != 0):
            ts["Born,Spouse"] = []
            age = int(y[0])-int(B.Born_Y[it])
            age = random.randint(age+1,age+5)
            ts["Born,Spouse"].append(Nm+" was married "+str(age)+" years after being born")
        if(B.isna().Born_Y[it]==False and len(y)>1):
            age = int(y[1])-int(B.Born_Y[it])
            age = random.randint(age+1,age+5)
            ts["Born,Spouse"].append(Nm+" was divorced "+str(age)+" years before dying")
            
        if(B.isna().Died_Y[it]==False and len(y) != 0):
            ts["Died,Spouse"] = []
            age = int(B.Died_Y[it])-int(y[0])
            age = random.randint(age+1,age+5)
            ts["Died,Spouse"].append(Nm+" was married "+str(age)+" years before dying")
        if(B.isna().Died_Y[it]==False and len(y)>1):
            age = int(B.Died_Y[it])-int(y[1])
            age = random.randint(age+1,age+5)
            ts["Died,Spouse"].append(Nm+" was divorced "+str(age)+" years before dying")
                        
        
    return ts


# In[57]:


# multi_row1(T,N,7)


# In[58]:


def multi_row2(tb,dn,F,it,tval=True):
    B = F["BDA"][0]
    Uy,Y = F["Years_active"]
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(B.isna().Born_Y[it]==False and Y[tb[it]][0] != None):
            ts["Born,Years_active"] = []
            year = int(Y[tb[it]][0])
            age = year - int(B.Born_Y[it])
            ts["Born,Years_active"].append( Nm+" started working at age "+str(age) )
            if(age<13):
                ts["Born,Years_active"].append(Nm+" started working when he was a child")
            elif(age>=13 and age<18):
                ts["Born,Years_active"].append(Nm+" started working when he was a teenager")
            elif(age>=18 and age<35):
                ts["Born,Years_active"].append(Nm+" started working when he was a younger adult")
            elif(age>=35 and age<55):
                ts["Born,Years_active"].append(Nm+" started working when he was a middle-aged adult")
            elif(age>=55):
                ts["Born,Years_active"].append(Nm+" started working when he was an old adult")
                
        if(B.isna().Born_Y[it]==False and Y[tb[it]][0] != None and len(Y[tb[it]])>1 ):
            if(Y[tb[it]][1]=="present"):
                year = 2020
            else:
                year = int(Y[tb[it]][1])
            age = year - int(B.Born_Y[it])
            if(Y[tb[it]][1]=="present"):
                ts["Born,Years_active"].append(Nm+" has not retired yet")
            else:
                ts["Born,Years_active"].append(Nm+" retired at the age of "+str(age))
            
        
    else:
        u = set(["child","teenager","younger adult","middle-aged adult","old adult"])
        if(B.isna().Born_Y[it]==False and Y[tb[it]][0] != None):
            ts["Born,Years_active"] = []
            year = int(Y[tb[it]][0])
            age = year - int(B.Born_Y[it])
            ts["Born,Years_active"].append( Nm+" started working at age "+str(random.randint(age+2,age+5)) )
            if(age<13):
                ts["Born,Years_active"].append(Nm+" started working when he was a "+random.sample(list(u-set(["child"])),1)[0] )
            elif(age>=13 and age<18):
                ts["Born,Years_active"].append(Nm+" started working when he was a "+random.sample(list(u-set(["teenager"])),1)[0])
            elif(age>=18 and age<35):
                ts["Born,Years_active"].append(Nm+" started working when he was a "+random.sample(list(u-set(["younger adult"])),1)[0])
            elif(age>=35 and age<55):
                ts["Born,Years_active"].append(Nm+" started working when he was a "+random.sample(list(u-set(["middle-aged adult"])),1)[0])
            elif(age>=55):
                ts["Born,Years_active"].append(Nm+" started working when he was a "+random.sample(list(u-set(["old adult"])),1)[0])
        if(B.isna().Born_Y[it]==False and Y[tb[it]][0] != None and len(Y[tb[it]])>1 ):
            if(Y[tb[it]][1]=="present"):
                year = 2020
            else:
                year = int(Y[tb[it]][1])
            age = year - int(B.Born_Y[it])
            if(Y[tb[it]][1]=="present"):
                ts["Born,Years_active"].append(Nm+" retired at the age of "+str(random.randint(age-8,age-2)) )
            else:
                ts["Born,Years_active"].append( random.sample([(Nm+" retired at the age of "+str(random.randint(age+2,age+7))),(Nm+" has not retired yet")],1)[0] )
        
    return ts


# In[59]:


# multi_row2(T,N,1)


# In[ ]:




#!/usr/bin/env python
# coding: utf-8

# In[10]:


# %run Psn_tr1.ipynb


# In[41]:


def GenresSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            AllGen = ', '.join(di[tb[it]])
            ps1 = [ "This person is singing in the genres "+AllGen
                   , AllGen+" these are the genres in which "+Nm+" sings"
                   , Nm+" has songs in the genres "+AllGen ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                AllGen = ', '.join(di[tb[it]])
                ts.append(Nm + " sings in the genres of " + AllGen)
                ts.append(Nm + " sings in the genre " + random.sample(di[tb[it]],1)[0])
                ts.append(Nm + " sings in " + str(len(di[tb[it]])) + " genres")
                ts.append(Nm + " sings in more than " + str(random.randint(0,len(di[tb[it]])-1)))
                ts.append(Nm + " sings in less than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5)))
                ts.append("The person plays "+random.sample(di[tb[it]],1)[0]+" music")
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                NT = random.sample(list(set(univ)-set(di[tb[it]])) , random.randint(2,7))
                AllGen = ', '.join(NT)
                ts.append(Nm + " sings in the genres of " + AllGen)
                ts.append(Nm + " sings in the genre " + random.sample(NT,1)[0])
                ts.append(Nm + " sings in " + str(len(NT)) + " genres")
                ts.append(Nm + " sings in less than " + str(random.randint(0,len(NT)-1)))
                ts.append(Nm + " sings in more than " + str(random.randint(len(NT)+1,len(NT)+5)))
                ts.append("The person plays "+random.sample(NT,1)[0]+" music")
            else:
                ts.append(None)

        return ts


# In[42]:


# GenSent(T,N,getG(300),5,False)


# In[43]:


def EducationSent(tb,dn,F,it,tval=True,prem=False):
    A = F[2]
    E = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(E[tb[it]][0] != None):
            ps1 = [ Nm+" studied at "+random.sample(E[tb[it]],1)[0]
                    ,"This person studied in "+random.sample(E[tb[it]],1)[0]
                    ,random.sample(E[tb[it]],1)[0]+" is where "+Nm+" studied" ]
        else:
            ps1 = [None]
        return ps1
        if(A[tb[it]][0] != None):
            ps2 = [ Nm+" earned his degree from "+random.sample(E[tb[it]],1)[0]
                    ,"This person is a graduate of "+random.sample(E[tb[it]],1)[0]
                    ,random.sample(E[tb[it]],1)[0]+" is where "+Nm+" graduated from" ]
        else:
            ps2 = [None]
        
        return ps2
        
    else:
        if(tval):
            if(E[tb[it]][0] != None):
                ts1 = Nm + " studied from " + random.sample(E[tb[it]],1)[0]
            else:
                ts1 = None
            return [ts1]
            if(A[tb[it]][0] != None):
                ts2 = Nm + " graduated from " + random.sample(A[tb[it]],1)[0]
            else:
                ts2 = None
            return [ts2]
        else:
            if(E[tb[it]][0] != None):
                ts1 = Nm + " studied from " + random.sample(list(set(univ)-set(E[tb[it]])),1)[0]
            else:
                ts1 = None
            return [ts1]
            if(A[tb[it]][0] != None):
                ts2 = Nm + " graduated from " + random.sample(list(set(univ)-set(A[tb[it]])),1)[0]
            else:
                ts2 = None
            return [ts2]


# In[44]:


# EdSent(T,N,diA,diE,UE,27,False,True)


# In[45]:


def LabelsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            AllGen = ', '.join(di[tb[it]])
            ps1 = [AllGen+" are the labels in which this person sings"
                  ,"Songs by "+Nm+" are in "+AllGen+" labels"
                  , Nm+" sings in "+AllGen+" labels"]
        else:
            ps1 = [None]
            
        return ps1    
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                AllGen = ', '.join(di[tb[it]])
                ts.append(Nm + " is associated with the labels " + AllGen)
                ts.append(Nm + " is associated with label " + random.sample(di[tb[it]],1)[0])
                ts.append(Nm + " is associate with " + str(len(di[tb[it]])) + " labels")
                ts.append(Nm + " is associate with more than " + str(random.randint(0,len(di[tb[it]])-1)) + " labels")
                ts.append(Nm + " is associate with less than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+ " labels")
                ts.append("The person works with "+random.sample(di[tb[it]],1)[0])
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                NT = random.sample(list(set(univ)-set(di[tb[it]])) , random.randint(2,7))
                AllGen = ', '.join(NT)
                ts.append(Nm + " is associate with the labels " + AllGen)
                ts.append(Nm + " is associate with label " + random.sample(NT,1)[0])
                ts.append(Nm + " is associate with " + str(len(NT)) + " labels")
                ts.append(Nm + " is associate with less than " + str(random.randint(0,len(NT)-1)) + " labels")
                ts.append(Nm + " is associate with more than " + str(random.randint(len(NT)+1,len(NT)+5))+ " labels")
                ts.append("The person works with "+random.sample(NT,1)[0])
            else:
                ts.append(None)

        return ts


# In[46]:


# LSent(T,N,getL(300),5,True)


# In[47]:


def WebsiteSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    alldom = ['.com', '.co.fr', '.co.in']
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ di[tb[it]][0]+" is this person's website"
                   ,"This person has a website named "+di[tb[it]][0]
                  , di[tb[it]][0]+" is "+Nm+"'s website"]
        else:
            ps1 = [None]
            
        return ps1
    
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                dom = re.findall("\.[a-z.]+",di[tb[it]][0])[0]
                ts.append(Nm + " has the website " + di[tb[it]][0])
                ts.append("The website has domain name "+dom)
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                dom = re.findall("\.[a-z.]+",di[tb[it]][0])[0]
                ndom = random.sample(list(set(alldom)-set(dom)),1)[0]
                ts.append(Nm + " has the website " + random.sample(list(set(univ)-set(di[tb[it]])),1)[0]) 
                ts.append("The website has domain name "+ndom)
            else:
                ts.append(None)
            
        return ts


# In[48]:


# WSent(T,N,getW(T,N,0),1)


# In[49]:


def ConvictionSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ", ".join(di[tb[it]])
            ps1 = [ All+" are the crimes this person is convicted for"
                   , "The crimes that "+Nm+" is convicted for are "+All
                   , "The charges against this person are "+All]
        else:
            ps1 = [None]
            
        return ps1
        
    else:
        ts = []
        if(tval):
            if(di[tb[it]][0] != None):
                All = ", ".join(di[tb[it]])
                ts.append(Nm + " has been convicted for " + All)
                ts.append(Nm + " was convicted for " + random.sample(di[tb[it]],1)[0])
                ts.append(Nm + " was convicted for " + str(len(di[tb[it]])) + " charges")
                ts.append(Nm + " was convicted for more than " + str(random.randint(0,len(di[tb[it]]))))
                ts.append(Nm + " was convicted for less than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+7)))
            else:
                ts.append(None)
        else:
            if(di[tb[it]][0] != None):
                NT = NT = random.sample(list(set(univ)-set(di[tb[it]])) , random.randint(2,5))
                All = ", ".join(NT)
                ts.append(Nm + " has been convicted for " + All)
                ts.append(Nm + " was convicted for " + random.sample(NT,1)[0])
                ts.append(Nm + " was convicted for " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+6)) + " charges")
                ts.append(Nm + " was convicted for less than " + str(random.randint(0,len(di[tb[it]]))))
                ts.append(Nm + " was convicted for more than " + str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+7)))
            else:
                ts.append(None)      

        return ts


# In[50]:


# CRSent(T,N,getCR(300),2,False)


# # Second part starts here

# In[51]:


def get_Institutions(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Institutions"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",",").strip())
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[52]:


# get_Institutions(T,N,True)[1]


# In[53]:


def get_Fields(T,N,it,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Fields"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",",").strip())
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[54]:


# getFl(300)[1]


# In[55]:


def get_Doctoral_students(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Doctoral students"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[56]:


# getStD(300)[1]


# In[57]:


def get_Awards(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Awards"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if(not (re.findall(" list",dictionary[k][i]) or re.findall("List ",dictionary[k][i])) ):
                            u.add(dictionary[k][i].replace(",,",",").strip())
                            d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",",").strip())
                        else:
                            d[dictionary['Tablename']].append(None)
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        if(not (re.findall(" list",dictionary[k].split(",")[i]) or re.findall(".*List ",dictionary[k].split(",")[i])) ):
                            u.add(dictionary[k].split(",")[i].strip())
                            d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip())
                        else:
                            d[dictionary['Tablename']].append(None)
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[58]:


# getAw(300)[1]


# In[59]:


def get_Relatives(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Relatives"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[60]:


# getRel(300)[1]


# In[61]:


def get_Resting_place(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Resting place"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[62]:


# getRP(300)[1]


# In[63]:


def get_Parents(T,N,fake=False,sel=0):
    u1 = set([])
    u2 = set([])
    d = {}
    k1 = "Parent(s)"
    k2 = "Parents"
    for n in range(700):
        if(int(Ptab[n][1:]) <= 2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u1.add(dictionary[k1][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k1][i].replace(",,",",").strip())
                else:
                    dictionary[k1] = dictionary[k1].replace(",,",",")
                    dictionary[k1] = dictionary[k1].replace(" and ",",")
                    for i in range(len(dictionary[k1].split(","))):
                        u1.add(dictionary[k1].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k1].split(",")[i].strip())
                        
            if(k2 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u1.add(dictionary[k2][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k2][i].replace(",,",",").strip())
                else:
                    dictionary[k2] = dictionary[k2].replace(",,",",")
                    dictionary[k2] = dictionary[k2].replace(" and ",",")
                    for i in range(len(dictionary[k2].split(","))):
                        u1.add(dictionary[k2].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k2].split(",")[i].strip())

            if(k1 not in dictionary.keys() and k2 not in dictionary.keys() ):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"]["Parents"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u1,d,it,sel,subNone = False)
        
    return list(u1),d


# In[64]:


# getPrnt(300)[1]


# In[65]:


def get_Instruments(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Instruments"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[66]:


# getIns(300)[1]


# In[67]:


def get_Residence(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Residence"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",","))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",","))
                else:
                    dictionary[k].replace(",,",",")
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[68]:


# get_Residence(T,N,True)[1]


# In[69]:


def get_Years_active(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Years active"
    for n in range(700):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                r = []
                if(type(dictionary[k]) == list):
                    X = re.findall("[0-9][0-9]+"," ".join(dictionary[k]).replace("\xa0","") )
                    for i in range(len(X)):
                        if(len(X[i])>2):
                            r.append(X[i])
                        else:
                            r.append(X[i-1][:2]+X[i])
                        
                    X = re.findall("present"," ".join(dictionary[k]).replace("\xa0","") )
                    if(X or len(r)%2!=0):
                        store = r[-1]
                        r = []
                        r.append(store)
                        r.append('present')
                else:
                    dictionary[k].replace(",,",",")
                    X = re.findall("[0-9][0-9]+",dictionary[k].replace("\xa0","") )
                    for i in range(len(X)):
                        if(len(X[i])>2):
                            r.append(X[i])
                        else:
                            r.append(X[i-1][:2]+X[i])
                    X = re.findall("present",dictionary[k].replace("\xa0","") )
                    if(X or len(r)%2!=0):
                        store = r[-1]
                        r = []
                        r.append(store)
                        r.append('present')
                        
                for i in range(len(r)):
                    d[dictionary['Tablename']].append(r[i])
                    u.add(r[i])
            if(k not in dictionary.keys() or len(d[dictionary['Tablename']])<1):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(len(T)): # for getting all the fakes in one go
            sel = random.sample(getfa["Psn"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel,subNone=False)
            if(len(d[T[it]])>1 and d[T[it]][0] == "present" and d[T[it]][1]=="present"):
                d[T[it]][0] = str(random.randint(1965,1975))
            elif(len(d[T[it]])==1 and d[T[it]][0] == "present"):
                d[T[it]][0] = str(random.randint(1965,1975))
            if(d[T[it]][0]!=None and d[T[it]][0]!="present" and d[T[it]][0]>d[T[it]][-1]):
                temp = d[T[it]][0]
                d[T[it]][0] = d[T[it]][-1]
                d[T[it]][-1] = temp
            elif(d[T[it]][0] == "present"):
                temp = d[T[it]][0]
                d[T[it]][0] = d[T[it]][-1]
                d[T[it]][-1] = temp

    return list(u),d


# In[70]:


# get_Years_active(T,N,True)[1]


# #### Sentences :

# In[71]:


def InstitutionsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" went to "," worked at "," employed at ",]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" are the institutions "+dn[tb[it]][0]+" worked at"
                   , "The person worked at "+All+" institutions" ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ', '.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+random.sample(syn,1)[0]+All )
                ts.append( dn[tb[it]][0]+" was at "+random.sample(di[tb[it]],1)[0]+" at least once" )
                ts.append( dn[tb[it]][0]+" received salary from "+All )
                ts.append( dn[tb[it]][0]+" worked at more than "+str(random.randint(0,length-1))+" places" )
                ts.append( dn[tb[it]][0]+" worked at less than "+str(random.randint(length+1,length+5))+" places" )
                for i in range(len(di[tb[it]])):
                    if(re.findall("[Uu]niversity",di[tb[it]][i]) or re.findall("[Ii]nstitute",di[tb[it]][i]) or re.findall("[Cc]ollege",di[tb[it]][i]) ):
                        syn = [" studied "," taught at "]
                        ts.append(dn[tb[it]][0]+random.sample(syn,1)[0]+di[tb[it]][i])
                        syn = [" literate ", " educated "]
                        ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0])
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ', '.join(NT)
                ts.append( dn[tb[it]][0]+random.sample(syn,1)[0]+All )
                ts.append( dn[tb[it]][0]+" was at "+random.sample(NT,1)[0]+" at least once" )
                ts.append( dn[tb[it]][0]+" received salary from "+All )
                ts.append( dn[tb[it]][0]+" worked at less than "+str(random.randint(0,length-1))+" places" )
                ts.append( dn[tb[it]][0]+" worked at more than "+str(random.randint(length+1,length+5))+" places" )
                for i in range(len(di[tb[it]])):
                    if(re.findall("[Uu]niversity",di[tb[it]][i]) or re.findall("[Ii]nstitute",di[tb[it]][i]) or re.findall("[Cc]ollege",di[tb[it]][i]) ):
                        syn = [" did not study at "]
                        ts.append(dn[tb[it]][0]+random.sample(syn,1)[0]+di[tb[it]][i])
                        syn = [" illiterate ", " not educated "]
                        ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0])
        else:
            ts.append(None)
        
        return ts


# In[72]:


# InSent(T,N,getIn(300),12,False)


# In[73]:


def FieldsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ dn[tb[it]][0]+" worked in "+All+" fields"
                  , All+" are the fields "+dn[tb[it]][0]+" worked in"
                  , "The person worked in "+All+" fields" ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval): # not finished
                All = ', '.join(di[tb[it]])
                syn = [" expert at "," educated in "," knowledgeable at "," worked in "," known for "]
                ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0]+All+" area")
                ts.append("At least one person"+random.sample(syn,1)[0]+random.sample(di[tb[it]],1)[0]+" field")
                syn = [" significant "," valuable "]
                ts.append(dn[tb[it]][0]+" made"+random.sample(syn,1)[0]+"contributions in "+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                syn = [" engaged "," involved "]
                ts.append("The person"+random.sample(syn,1)[0]+"in "+All+" areas")
                ts.append("The person worked in "+("single area" if length==1 else "multiple areas"))
                ts.append(dn[tb[it]][0]+" worked at more than "+str(random.randint(0,length-1))+" places")
                ts.append(dn[tb[it]][0]+" worked at less than "+str(random.randint(length+1,length+5))+" places")
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ', '.join(NT)
                syn = [" expert at "," educated in "," knowledgeable at "," worked in "," known for "]
                ts.append(dn[tb[it]][0]+" is"+random.sample(syn,1)[0]+All+" area")
                ts.append("At least one person"+random.sample(syn,1)[0]+random.sample(NT,1)[0]+" field")
                syn = [" significant "," valuable "]
                ts.append(dn[tb[it]][0]+" made"+random.sample(syn,1)[0]+"contributions in "+", ".join(random.sample(NT,random.randint(1,len(NT)))) )
                syn = [" engaged "," involved "]
                ts.append("The person"+random.sample(syn,1)[0]+"in "+All+" areas")
                ts.append("The person worked in "+("single area" if length!=1 else "multiple areas"))
                ts.append(dn[tb[it]][0]+" worked at less than "+str(random.randint(0,length-1))+" places")
                ts.append(dn[tb[it]][0]+" worked at more than "+str(random.randint(length+1,length+5))+" places")
        else:
            ts.append(None)
        
        return ts


# In[141]:


# FlSent(T,N,getFl(T,N,39),39,False)


# In[ ]:


# getFl(300)[1]


# In[ ]:


def Doctoral_studentsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" were the doctoral students of "+dn[tb[it]][0]
                  , "The doctoral students of "+dn[tb[it]][0]+" are "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval): # not finished
                All = ', '.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" was an advisor to "+", ".join(random.sample(di[tb[it]],random.randint(1,length))))
                syn = [" person "," professor "," faculty "," Ph.D. "]
                ts.append( "The"+random.sample(syn,1)[0]+"supervised "+All )
                ts.append( "The"+random.sample(syn,1)[0]+"mentored "+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored at least "+str(random.randint(1,length)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored more than "+str(random.randint(0,length-1)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored less than "+str(random.randint(length+1,length+5)) )
                ts.append( dn[tb[it]][0]+" knows "+random.sample(di[tb[it]],1)[0] )
                ts.append( dn[tb[it]][0]+" met "+random.sample(di[tb[it]],1)[0]+" atleast once" )
                ts.append( dn[tb[it]][0]+" was the advisee of "+random.sample(di[tb[it]],1)[0] )
                ts.append( dn[tb[it]][0]+" awarded a degree to "+random.sample(di[tb[it]],1)[0] )
                ts.append( random.sample(di[tb[it]],1)[0]+" got a degree under "+dn[tb[it]][0] )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(2,5))
                nl = len(NT)
                All = ', '.join(NT)
                ts.append( dn[tb[it]][0]+" was an advisor to "+", ".join(random.sample(NT,random.randint(1,nl))))
                syn = [" person "," professor "," faculty "," Ph.D. "]
                ts.append( "The"+random.sample(syn,1)[0]+"supervised "+All )
                ts.append( "The"+random.sample(syn,1)[0]+"mentored "+", ".join(random.sample(NT,random.randint(1,nl))) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored at least "+str(random.randint(length+1,length+5)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored less than "+str(random.randint(0,length-1)) )
                ts.append( "The"+random.sample(syn,1)[0]+"has mentored more than "+str(random.randint(length+1,length+5)) )
                ts.append( dn[tb[it]][0]+" knows "+random.sample(NT,1)[0] )
                ts.append( dn[tb[it]][0]+" met "+random.sample(NT,1)[0]+" atleast once" )
                ts.append( dn[tb[it]][0]+" was the advisee of "+random.sample(NT,1)[0] )
                ts.append( dn[tb[it]][0]+" awarded a degree to "+random.sample(NT,1)[0] )
                ts.append( random.sample(NT,1)[0]+" got a degree under "+dn[tb[it]][0] )
        
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# StDSent(T,N,getStD(300),-12)


# In[ ]:


def AwardsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ "The person won "+All
                  , All+" was won by "+dn[tb[it]][0]
                  , All+" were the awards that "+di[tb[it]][0]+" won" ]
        else:
            ps1 = [None]
            
        return ps1
    
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                syn = [" won "+" was winner of "," was rewarded "]
                ts.append( Nm+random.sample(syn,1)[0]+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( Nm+random.sample(syn,1)[0]+str(length)+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" more than "+str(random.randint(0,length-1))+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" less than "+str(random.randint(length+1,length+5))+" awards" )
                ts.append( ", ".join(random.sample(di[tb[it]],random.randint(1,length)))+" was given to "+Nm )
                ts.append( Nm+" was winner of "+", ".join(random.sample(di[tb[it]],random.randint(1,length))) )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                All = ', '.join(NT)
                nl = len(NT)
                syn = [" won "+" was winner of "," was rewarded "]
                ts.append( Nm+random.sample(syn,1)[0]+", ".join(random.sample(NT,random.randint(1,nl))) )
                ts.append( Nm+random.sample(syn,1)[0]+str(random.randint(length+1,length+5))+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" less than "+str(random.randint(0,length-1))+" awards" )
                ts.append( Nm+random.sample(syn,1)[0]+" more than "+str(random.randint(length+1,length+5))+" awards" )
                ts.append( ", ".join(random.sample(NT,random.randint(1,nl)))+" was given to "+Nm )
                ts.append( Nm+" was winner of "+", ".join(random.sample(NT,random.randint(1,nl))) )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# AwSent(T,N,getAw(300),-12,True)


# In[ ]:


def RelativesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" are relatives of "+Nm
                  , Nm+" is related to "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                ppl = []
                for s in di[tb[it]]:
                    if(re.findall("\(.+\)",s)):
                        relation = re.findall("\(.+\)",s)[0]
                        s = s.strip(relation)
                        ppl.append(s)
                        ts.append(s+" was "+relation.strip("(").strip(")")+" to "+Nm)
                    else:
                        ppl.append(s)
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" know each other" )
                ts.append( random.sample(ppl,1)[0]+" is connected to "+Nm+" by blood" )
                ts.append( random.sample(ppl,1)[0]+" is close to "+Nm )
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" connected by blood" )
                ts.append( Nm+" has more than "+str(random.randint(0,length-1))+" relatives" )
                ts.append( Nm+" has less than "+str(random.randint(length+1,length+5))+" relatives" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                All = ', '.join(NT)
                nl = len(NT)
                ppl = []
                for s in NT:
                    if(re.findall("\(.+\)",s)):
                        relation = re.findall("\(.+\)",s)[0]
                        s = s.strip(relation)
                        ppl.append(s)
                        ts.append(s+" was "+relation.strip("(").strip(")")+" to "+Nm)
                    else:
                        ppl.append(s)
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" know each other" )
                ts.append( random.sample(ppl,1)[0]+" is connected to "+Nm+" by blood" )
                ts.append( random.sample(ppl,1)[0]+" is close to "+Nm )
                ts.append( random.sample(ppl,1)[0]+" and "+Nm+" connected by blood" )
                ts.append( Nm+" has less than "+str(random.randint(0,length-1))+" relatives" )
                ts.append( Nm+" has more than "+str(random.randint(length+1,length+5))+" relatives" )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# RelSent(T,N,getRel(300),6,False)


# In[ ]:


def Resting_placeSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ "The resting place of "+Nm+" is "+All
                  , All+" is the resting place of the person"]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                ts.append( Nm+" was buried at "+All )
                ts.append( "People paid last respect to person at "+All )
                ts.append( "The body of the person was last seen at "+All )
                syn = [" creamted "," buried "]
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"at "+All )
                ts.append("The person's body could be found at "+All )
                ts.append( All+" is a cemetery")
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ', '.join(NT)
                nl = len(NT)
                ts.append( Nm+" was buried at "+All )
                ts.append( "People paid last respect to person at "+All )
                ts.append( "The body of the person was last seen at "+All )
                syn = [" creamted "," buried "]
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"at "+All )
                ts.append("The person's body could be found at "+All )
                ts.append( All+" is a cemetery")
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# RPSent(T,N,getRP(300),20)


# In[74]:


def ParentsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" were the parents of "+Nm
                  , "The parents of "+Nm+" are "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                ts.append( random.sample(di[tb[it]],1)[0]+" is a guardian of "+Nm )
                if(re.findall("\([FfMm][ao]ther\)",All)):
                    if(re.findall("\([Ff][a]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the father of "+Nm )
                    elif(re.findall("\([Mm][o]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][0].replace(r[0],"") )
                    if(length>1 and re.findall("\([Mm][o]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][1].replace(r[0],"") )
                    elif(length>1 and re.findall("\([Ff][a]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the father of "+Nm )
                ts.append( random.sample(di[tb[it]],1)[0]+" and "+Nm+" met at least once" )
                ts.append( Nm+" used to stay with "+All )
                ts.append( Nm+" was named by "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ', '.join(NT)
                nl = len(NT)
                ts.append( random.sample(NT,1)[0]+" is a guardian of "+Nm )
                if(re.findall("\([FfMm][ao]ther\)",", ".join(di[tb[it]])) and length>1):
                    if(re.findall("\([Ff][a]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][0].replace(r[0],"") )
                    elif(re.findall("\([Mm][o]ther\)",di[tb[it]][0])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][0])
                        ts.append( di[tb[it]][0].replace(r[0],"")+" is the father of "+Nm )
                    if(length>1 and re.findall("\([Mm][o]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the father of "+Nm )
                    elif(length>1 and re.findall("\([Ff][a]ther\)",di[tb[it]][1])):
                        r = re.findall("\([FfMm][ao]ther\)",di[tb[it]][1])
                        ts.append( di[tb[it]][1].replace(r[0],"")+" is the mother of "+Nm )
                        ts.append( Nm+" was given birth by "+di[tb[it]][1].replace(r[0],"") )
                    ts.append( Nm+" was given birth by "+NT[0] )
                ts.append( random.sample(NT,1)[0]+" and "+Nm+" met at least once" )
                ts.append( Nm+" used to stay with "+All )
                ts.append( Nm+" was named by "+All )
                
        else:
            ts.append(None)
        
        return ts


# In[78]:


# ParentsSent(T,N,get_Parents(T,N),427)


# In[ ]:


def InstrumentsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ All+" instruments were played by "+Nm 
                  , Nm+" played "+All+" instruments" ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                syn = [" how to play "," can play "," used to play "]
                ts.append( Nm+"knows"+random.sample(syn,1)[0]+All )
                ts.append( "This person"+random.sample(syn,1)[0]+str(length)+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"more than "+str(random.randint(0,length-1))+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"less than "+str(random.randint(length+1,length+5))+" instruments" )
                ts.append( Nm+" played "+random.sample(di[tb[it]],1)[0] )
                ts.append( Nm+" did not play "+random.sample(list(set(univ)-set(di[tb[it]])),1)[0] )
                ts.append( Nm+" is an expert at playing "+random.sample(di[tb[it]],1)[0] )
                ts.append( "This person knew"+random.sample(syn,1)[0]+("single" if length==1 else "multiple")+" instrument" )
                ts.append( "This person can make melodious sounds from "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                All = ', '.join(NT)
                nl = len(NT)
                syn = [" how to play "," can play "," used to play "]
                ts.append( Nm+" knows"+random.sample(syn,1)[0]+All )
                ts.append( "This person"+random.sample(syn,1)[0]+str(random.randint(length+1,length+5))+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"less than "+str(random.randint(0,length-1))+" instruments" )
                ts.append( "This person"+random.sample(syn,1)[0]+"more than "+str(random.randint(length+1,length+5))+" instruments" )
                ts.append( Nm+" did not play "+random.sample(di[tb[it]],1)[0] )
                ts.append( Nm+" played "+random.sample(list(set(univ)-set(di[tb[it]])),1)[0] )
                ts.append( Nm+" is an expert at playing "+random.sample(NT,1)[0] )
                ts.append( "This person knew"+random.sample(syn,1)[0]+("single" if length!=1 else "multiple")+" instrument" )
                ts.append( "This person can make melodious sounds from "+All )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# IntSent(T,N,getInt(300),5)


# In[ ]:


def ResidenceSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ', '.join(di[tb[it]])
            ps1 = [ Nm+" had a residence at "+All
                  , All+" is where "+Nm+" had a residence"
                  , "This person is resided at "+All]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            Nm = dn[tb[it]][0]
            if(tval): 
                All = ', '.join(di[tb[it]])
                syn = [" stayed at "," resided at "," lived at "," was atleast once at "]
                ts.append( Nm+random.sample(syn,1)[0]+ ", ".join(di[tb[it]][:random.randint(1,length)]) )
                syn = [" house "," apartment "]
                ts.append( "The person bought "+random.sample(syn,1)[0]+"at "+All )
                ts.append( "The person is known by someone at "+", ".join(di[tb[it]][:random.randint(1,length)]) )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ', '.join(NT)
                nl = len(NT)
                syn = [" stayed at "," resided at "," lived at "," was atleast once at "]
                ts.append( Nm+random.sample(syn,1)[0]+ ", ".join(NT[:random.randint(1,nl)]) )
                syn = [" house "," apartment "]
                ts.append( "The person bought "+random.sample(syn,1)[0]+"at "+All )
                ts.append( "The person is known by someone at "+", ".join(NT[:random.randint(1,nl)]) )
                
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# ResdSent(T,N,getResd(300),-10,False,True)


# In[ ]:


def Years_activeSent(tb,dn,F,it,tval=True,prem=False):
    # Note : Assuming present is 2020
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    y = []
    if(di[tb[it]][0] != None):
        for i in di[tb[it]]:
            x = re.findall("[0-9]+",i)
            if(len(x)>0):
                y.append(x[0])
            else:
                y.append("2020")
    if(prem):
        if(di[tb[it]][0] != None):
    #         All = ', '.join(di[tb[it]])
            ps1 = [ "This person was active from "+"-".join(y)
                  , "-".join(y)+" is when "+Nm+" was active"
                  , "The active years for "+Nm+" were from "+"-".join(y) ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval): 
                All = ', '.join(di[tb[it]])
                if(length>1):
                    span = int(y[1])-int(y[0])
                    ts.append(Nm+" worked for "+str(span)+" years" )
                    ts.append(Nm+" worked for more than "+str(random.randint(span-6,span-1))+" years")
                    ts.append(Nm+" worked for less than "+str(random.randint(span+2,span+10))+" years")
                    ts.append(Nm+" worked from "+"-".join(y))
                    ts.append(Nm+" started working in "+str(y[0]))
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                if(length>1):
                    span = int(y[1])-int(y[0])
                    ts.append(Nm+" worked for "+str(random.randint(span+2,span+10))+" years")
                    ts.append(Nm+" worked for less than "+str(random.randint(span-6,span-1))+" years")
                    ts.append(Nm+" worked for more than "+str(random.randint(span+2,span+10))+" years")
                
                x = re.findall("[0-9]+",NT)
                if(len(x)>0):
                    ny = x[0]
                else:
                    ny = "2020"
                ts.append(Nm+" worked from "+"-".join([ny,str(random.randint(int(ny)+1,2021))]))
                ts.append(Nm+" started working in "+str(random.randint(int(y[0])+1,int(y[0])+10) ))
        else:
            ts.append(None)
        
        return ts


# In[ ]:


# YASent(T,N,getYA(),51)


# In[ ]:


def multi_row3(tb,dn,F,it,tval=True):
    B = F["BDA"][0]
    Ur,R = F["Relatives"]
    Up,P = F["Parents"]
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(R[tb[it]][0]!=None and P[tb[it]][0]!=None):
            ts["Relatives,Parents"] = []
            Al1 = random.sample(R[tb[it]],1)[0].split("(")[0]
            Al2 = random.sample(P[tb[it]],1)[0].split("(")[0]
            ts["Relatives,Parents"].append(Al1+" is related to "+Al2)
            ts["Relatives,Parents"].append(Al2+" is related to "+Al1)
            
        if(B.isna().Born_Y[it]==False and P[tb[it]][0] != None):
            ts["Born,Parents"] = []
            Al1 = random.sample(P[tb[it]],1)[0].split("(")[0]
            y = int(B.Born_Y[it])
            ts["Born,Parents"].append(Al1+" was born before "+str(random.randint(y+1,y+5)) )
    else:
        if(R[tb[it]][0]!=None and P[tb[it]][0]!=None):
            ts["Relatives,Parents"] = []
            Al1 = random.sample(list(set(Ur)-set(R[tb[it]])),1)[0].split("(")[0]
            Al2 = random.sample(P[tb[it]],1)[0].split("(")[0]
            ts["Relatives,Parents"].append(Al1+" is related to "+Al2)
            ts["Relatives,Parents"].append(Al2+" is related to "+Al1)
            
        if(B.isna().Born_Y[it]==False and P[tb[it]][0] != None):
            ts["Born,Parents"] = []
            Al1 = random.sample(P[tb[it]],1)[0].split("(")[0]
            y = int(B.Born_Y[it])
            ts["Born,Parents"].append(Al1+" was born after "+str(random.randint(y+1,y+5)) )
        
    return ts


# In[53]:


# multi_row3(T,N,6)


# In[ ]:




