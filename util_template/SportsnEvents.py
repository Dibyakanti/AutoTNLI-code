#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import sys

if './' not in sys.path:
    sys.path.append('./')
    
# from Py_f import Psn as P


# In[1]:


getfa = {
"Movie_tr1":{"Directed_by":[0,1,2],"Produced_by":[0,1,2],"Screenplay_by":[1],"SR":[0,1,2],"M":[0,1,2],"Cin":[1],"EdiB":[0,1,2],"PC":[1],
    "Dby":[0,1,2],"Rdate":[0,1,2],"Rtime":[1],"Cty":[0,1,2],"Lang":[0,1,2],"Budg":[1],"BO":[1]},
"Book_tr1":{"Publisher":[1],"Schedule":[1],"Format":[0,1,2],"Genre":[0,1,2],"Publication_date":[1],
        "No_of_issues":[1],"Main_character":[0,1,2],"Written_by":[0,1,2]},
"FnD_tr1":{"Manufacturer":[1],"Country_of_origin":[0,1,2],"Variants_Flavour":[0,1,2],"Introduced":[1],"Related_products":[0,1,2],
    "Alcohol_by_volume":[1],"Website":[1],"Color":[0,1,2],"Main_ingredients":[0,1,2],"Type":[0,1,2]},
"Organiz_tr1":{"Wesbsite":[1],"Headquarters":[1],"Founded_Formation":[1],"Industry":[0,1,2],"Key_people":[0,1,2],"Products":[0,1,2]
	,"Number_of_employees":[1],"Traded_as":[0,1,2],"Founder_Founders":[0,1,2],"Area_served":[0,1,2],"Type":[1],"Subsidiaries":[0,1,2]
	,"Parent":[1],"Owner":[1],"Predecessor":[1]},
"Paint_tr1":{"Artist":[1],"Year":[1],"Medium_Type":[1],"Dimensions":[1],"Location":[1]},
"Fest_tr1":{"Type":[0,1,2],"Observed_by":[0,1,2],"Frequency":[1],"Celebrations":[0,1,2],"Significance":[0,1,2],"Observances":[0,1,2],
    "Date":[1],"Related_to":[0,1,2],"Also_called":[0,1,2],"Official_name":[1],"Begins":[1],"Ends":[1],
    "2021_date":[1],"2020_date":[1],"2019_date":[1],"2018_date":[1]},
"SpEv_tr1":{"Venue":[0,1,2],"Date":[1],"Competitors":[0,1,2],"Teams":[1],
	"No_of_events":[1],"Established":[1],"Official_site":[1]},
"Univ_tr1":{"Website":[1],"Type":[0,1,2],"Established":[1],"Undergraduates":[1],"Postgraduates":[1],
    "Motto_Motto_in_English":[0,1,2],"Location":[1],"Nickname":[1],"Campus":[1],"Colors":[0,1,2],
    "Students":[1],"Academic_staff":[1],"Administrative_staff":[1],"President":[1],"Endowment":[1],"Mascot":[1],
    "Provost":[1],"Sporting_affiliations":[0,1,2],"Academic_affiliations":[0,1,2],"Former_names":[1]}
}


# In[4]:


Catg = pd.read_csv("/content/drive/My Drive/Auto-TNLI/data/table_categories.tsv",sep="\t")
# Catg = pd.read_csv("../../autotnlidatasetandcode/table_categories modified.tsv",sep="\t")


# In[5]:


Ptab = np.array(Catg[Catg.category.isin(["Sports","Sports Event"])].table_id)
tablesFolder = "/content/drive/My Drive/Auto-TNLI/data/tables"
# tablesFolder = "../../autotnlidatasetandcode/tables"


# In[6]:


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
#     keys =[i.text for i in soup.find('tr').find_all('th')]
    keys = []
#     keys.append(soup.find('caption').text)
    keys =[i.text.replace("\xa0"," ") for i in soup.find('tr').find_all('th')]
    if(soup.find('caption')):
        keys.insert(0,soup.find('caption').text)
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


# In[9]:


def get_Table_Title():
    d = {}
    tb = []
    for n in range(80):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
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


# In[10]:


N,T = get_Table_Title()
# N


# In[23]:


'''
d1 : dict for that table
univ : list of a set
df : dataframe of Born/Death to get the table name
sel: selection bit
it : choose table name from the dataframe
'''
def FakeDICT(tb,dn,univ,di,it,sel=0,subNone = False): # selection bit selects whethet to substitute/delete/add
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
        elif(len(di[tb[it]])>0):
            possible_sub = random.sample(list(set(univ)-set(d1[tb[it]])),1)
            for i in range(6): # Probability that none is chose = 1/7
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


# In[24]:


def get_Venue(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Venue"
    k2 = "Location"
    for n in range(80):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i])
                        d[dictionary['Tablename']].append(dictionary[k1][i])
                else:
                    length = len(dictionary[k1].split(")"))
                    for i in range(length):
                        if(len(dictionary[k1].split(")")[i])>1):
                            u.add(dictionary[k1].split(")")[i].strip().strip(".").strip(",") +(")" if length>1 else ""))
                            d[dictionary['Tablename']].append(dictionary[k1].split(")")[i].strip().strip(".").strip(",") +(")" if length>1 else ""))
            
            if(k2 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i])
                        d[dictionary['Tablename']].append(dictionary[k2][i])
                else:
                    length = len(dictionary[k2].split(")"))
                    for i in range(length):
                        if(len(dictionary[k2].split(")")[i])>1):
                            u.add(dictionary[k2].split(")")[i].strip().strip(".").strip(",") +(")" if length>1 else ""))
                            d[dictionary['Tablename']].append(dictionary[k2].split(")")[i].strip().strip(".").strip(",") +(")" if length>1 else ""))
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys()):
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(getfa["SpEv_tr1"]["Venue"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[25]:


# getVL(T,N,0)[1]


# In[26]:


def get_Date(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Date"
    k2 = "Dates"
    for n in range(80):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i].replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k1][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k1].split(","))):
                    length = len(dictionary[k1].split(")"))
                    for i in range(length):
                        if(len(dictionary[k1].split(")")[i])>1):
                            u.add(dictionary[k1].split(")")[i].strip().strip(".") .replace("\xa0"," ")+(")" if length>1 else ""))
                            d[dictionary['Tablename']].append(dictionary[k1].split(")")[i].strip().strip(".") .replace("\xa0"," ")+(")" if length>1 else ""))
            
            if(k2 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i].replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k2][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k2].split(","))):
                    length = len(dictionary[k2].split(")"))
                    for i in range(length):
                        if(len(dictionary[k2].split(")")[i])>1):
                            u.add(dictionary[k2].split(")")[i].strip().strip(".") .replace("\xa0"," ")+(")" if length>1 else ""))
                            d[dictionary['Tablename']].append(dictionary[k2].split(")")[i].strip().strip(".") .replace("\xa0"," ")+(")" if length>1 else ""))
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys()):
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(getfa["SpEv_tr1"]["Date"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[27]:


# getD(T,N,0)[1]


# In[28]:


def get_Competitors(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Competitors"
    for n in range(80):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary[k])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k][i] .replace("\xa0"," "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i] .replace("\xa0"," "))
#                     u.add(dictionary[k])
#                     d[dictionary['Tablename']].append(dictionary[k])
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(getfa["SpEv_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
    return list(u),d


# In[29]:


# getC()[1]
# table 254 does not have country so split by "from"


# In[30]:


def get_Teams(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Teams"
    for n in range(80):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary[k])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k][i] .replace("\xa0"," "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i] .replace("\xa0"," "))
#                     u.add(dictionary[k])
#                     d[dictionary['Tablename']].append(dictionary[k])
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(getfa["SpEv_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
    return list(u),d


# In[31]:


# getT()[1]


# In[32]:


def get_No_of_events(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "No. of events"
    for n in range(80):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary[k])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k][i] .replace("\xa0"," "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i] .replace("\xa0"," "))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(getfa["SpEv_tr1"]["No_of_events"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
    return list(u),d


# In[33]:


# getN()[1]


# In[34]:


def get_Established(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Established"
    k2 = "Founded"
    for n in range(80):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i].replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k1][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k1].split(","))):
                        u.add(dictionary[k1].strip().strip(".") .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k1].strip().strip(".") .replace("\xa0"," "))
            
            if(k2 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i].replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k2][i].replace("\xa0"," "))
                else:
#                     for i in range(len(dictionary[k2].split(","))):
                        u.add(dictionary[k2].strip().strip(".") .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k2].strip().strip(".") .replace("\xa0"," "))
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys()):
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(getfa["SpEv_tr1"]["Established"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[35]:


# getEF()[1]


# In[36]:


def get_Official_site(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Official site"
    for n in range(80):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary[k])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k][i] .replace("\xa0"," "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i] .replace("\xa0"," "))
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i] .replace("\xa0"," "))
#                     u.add(dictionary[k])
#                     d[dictionary['Tablename']].append(dictionary[k])
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(getfa["SpEv_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[37]:


# getO()[1]


# #### Dictionary of all extracted data from html/json:

# In[ ]:


def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Venue","Date"
          ,"Competitors","Teams","No_of_events","Established","Official_site"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data
# F is the Extracted_data[key]


# #### Sentences :

# In[39]:


def VenueSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" were the venues of "+Nm
                  , "The venue for "+Nm+" was "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "All the events of the sports "+Nm+" are conducted in "+All )
                ts.append( "Events of the sports happened in "+All )
                ts.append( random.sample(di[tb[it]],1)[0]+" was the official place where "+Nm+" happened" )
                ts.append( Nm+" was held in "+random.sample(di[tb[it]],1)[0] )
                ts.append( Nm+" happened in "+("multiple" if length>1 else "single")+" place" )
#                 ts.append( Nm+" takes place in more than "+str(random.randint(0,length-1))+" places" )
                ts.append( Nm+" took place in "+random.sample(di[tb[it]],1)[0] )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( "All the events of the sports "+Nm+" are conducted in "+All )
                ts.append( "Events of the sports happened in "+All )
                ts.append( random.sample(NT,1)[0]+" was the official place where "+Nm+" happened" )
                ts.append( Nm+" was held in "+random.sample(NT,1)[0] )
                ts.append( Nm+" happened in "+("multiple" if length>1 else "single")+" place" )
#                 ts.append( Nm+" takes place in more than "+str(random.randint(0,length-1))+" places" )
                ts.append( Nm+" took place in "+random.sample(NT,1)[0] )
                
        else:
            ts.append(None)
            
        return ts


# In[40]:


# VLSent(T,N,getVL()[1],getVL()[0],10)


# In[41]:


def DateSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "It was held in "+All
                  , All+" was when it was held"]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(re.findall("[0-9]+"," ".join(di[tb[it]])))
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The sporting event "+Nm+" took place on "+random.sample(di[tb[it]],1)[0] )
                ts.append( Nm+" was held over a few days" )
                ts.append( Nm+" was a "+("single" if length <=2 else "multiple")+" day event" )
#                 ts.append(  )
#                 ts.append(  )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                All = ','.join(NT)
                ts.append( "The sporting event "+Nm+" took place on "+random.sample(NT,1)[0] )
                ts.append( Nm+" was held over a few days" )
                ts.append( Nm+" was a "+("single" if length >2 else "multiple")+" day event" )
                
        else:
            ts.append(None)
            
        return ts


# In[42]:


# DSent(T,N,getD(),1)


# In[43]:


def CompetitorsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" contestants "," contenders "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" were the competitors in "+Nm
                  , All+" competed in "+Nm ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(re.findall("[0-9]+"," ".join(di[tb[it]])))
            X = re.findall("[0-9]+",','.join(di[tb[it]]))[0] 
            X = int(X.strip())
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( str(X)+random.sample([" people"," players"],1)[0]+" competed in the "+Nm )
                ts.append( "The sport "+Nm+" had "+str(X)+random.sample(syn,1)[0] )                
                ts.append( "The sport "+Nm+" had more than "+str(random.randint(5,X-4))+random.sample(syn,1)[0] )
                ts.append( "The sport "+Nm+" had less than "+str(random.randint(X+2,X+20))+random.sample(syn,1)[0] )
                if(length>=2):
                    Y = re.findall("[0-9]+",','.join(di[tb[it]]))[1]
                    Y = int(Y.strip())
                    ts.append( str(X)+random.sample(syn,1)[0]+"from "+str(Y)+" nations" )
                    ts.append( "In the sport "+Nm+" ,"+str(Y)+" nations participated" )
                    ts.append( "More than "+str(random.randint(0,Y-1))+" nations participated in the event" )
                    ts.append( "Less than "+str(random.randint(Y+5,Y+10))+" nations participated in the event" )
                    ts.append( str(Y)+" nations took part in "+Nm )
                    ts.append( "The sport "+Nm+" has "+str(X)+random.sample(syn,1)[0]+" from more than "+str(random.randint(0,Y-1))+" nations" )
                    ts.append( "The sport "+Nm+" has "+str(X)+random.sample(syn,1)[0]+" from less than "+str(random.randint(Y+2,Y+20))+" nations" )
                    ts.append( "The sport "+Nm+" has more than"+str(random.randint(5,X-4))+random.sample(syn,1)[0]+" from "+str(Y)+" nations" )
                    ts.append( "The sport "+Nm+" has less than"+str(random.randint(X+2,X+20))+random.sample(syn,1)[0]+" from "+str(Y)+" nations" )
                    ts.append( "The sport "+Nm+" has more than"+str(random.randint(5,X-4))+random.sample(syn,1)[0]+" from more than "+str(random.randint(0,Y-1))+" nations" )
                    ts.append( "The sport "+Nm+" has less than"+str(random.randint(X+4,X+20))+random.sample(syn,1)[0]+" from less than "+str(random.randint(Y+2,Y+20))+" nations" )
            else:
#                 NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
#                 All = ','.join(NT)
                X = re.findall("[0-9]+",','.join(di[tb[it]]))[0] 
                X = int(X.strip())
                nX = random.randint(X+1,X+7)
                ts.append( str(nX)+random.sample([" people"," players"],1)[0]+" competed in the "+Nm )
                ts.append( "The sport "+Nm+" had "+str(nX)+random.sample(syn,1)[0] )                
                ts.append( "The sport "+Nm+" had less than "+str(random.randint(5,X-4))+random.sample(syn,1)[0] )
                ts.append( "The sport "+Nm+" had more than "+str(random.randint(X+2,X+20))+random.sample(syn,1)[0] )
                if(length>=2):
                    Y = re.findall("[0-9]+",','.join(di[tb[it]]))[1]
                    Y = int(Y.strip())
                    nY = random.randint(Y+1,Y+7)
                    ts.append( str(nX)+random.sample(syn,1)[0]+"from "+str(nY)+" nations" )
                    ts.append( "In the sport "+Nm+" ,"+str(nY)+" nations participated" )
                    ts.append( "Less than "+str(random.randint(0,Y-1))+" nations participated in the event" )
                    ts.append( "More than "+str(random.randint(Y+5,Y+10))+" nations participated in the event" )
                    ts.append( str(Y)+" nations took part in "+Nm )
                    ts.append( "The sport "+Nm+" has "+str(nX)+random.sample(syn,1)[0]+" from less than "+str(random.randint(0,Y-1))+" nations" )
                    ts.append( "The sport "+Nm+" has "+str(nX)+random.sample(syn,1)[0]+" from more than "+str(random.randint(Y+2,Y+20))+" nations" )
                    ts.append( "The sport "+Nm+" has less than"+str(random.randint(5,X-4))+random.sample(syn,1)[0]+" from "+str(Y)+" nations" )
                    ts.append( "The sport "+Nm+" has more than"+str(random.randint(X+2,X+20))+random.sample(syn,1)[0]+" from "+str(Y)+" nations" )
                    ts.append( "The sport "+Nm+" has less than"+str(random.randint(5,X-4))+random.sample(syn,1)[0]+" from less than "+str(random.randint(0,Y-1))+" nations" )
                    ts.append( "The sport "+Nm+" has more than"+str(random.randint(X+4,X+20))+random.sample(syn,1)[0]+" from more than "+str(random.randint(Y+2,Y+20))+" nations" )
                
        else:
            ts.append(None)
            
        return ts


# In[44]:


# CSent(T,N,getC()[1],getC()[0],10)


# In[45]:


def TeamsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" squad "," teams "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" teams "+random.sample(["competed","participated"],1)[0]+" in "+Nm
                  , All+" were the number of teams who competed in "+Nm ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
#             length = len(re.findall("[0-9]"," ".join(di[tb[it]])))
            X = int(re.findall("[0-9]+",di[tb[it]][0])[0])
            if(tval):
#                 All = ','.join(di[tb[it]])
                ts.append( "The number of"+random.sample(syn,1)[0]+"in the sport "+Nm+" is "+str(X) )
                ts.append( "There are "+str(X)+random.sample(syn,1)[0]+"in sport "+Nm )
                ts.append( "There are more than "+str(random.randint(2,X-4))+random.sample(syn,1)[0]+"in sport "+Nm )
                ts.append( "There are less than "+str(random.randint(X+4,X+10))+random.sample(syn,1)[0]+"in sport "+Nm )
                ts.append( str(X)+" teams competed against each other in "+Nm )
                ts.append( Nm+" saw a competition between "+str(X)+random.sample(syn,1)[0] )
                
            else:
#                 NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
#                 All = ','.join(NT)
                nX = random.randint(X+1,X+7)
                ts.append( "The number of"+random.sample(syn,1)[0]+"in the sport "+Nm+" is "+str(nX) )
                ts.append( "There are "+str(nX)+random.sample(syn,1)[0]+"in sport "+Nm )
                ts.append( "There are less than "+str(random.randint(2,X-4))+random.sample(syn,1)[0]+"in sport "+Nm )
                ts.append( "There are more than "+str(random.randint(X+4,X+10))+random.sample(syn,1)[0]+"in sport "+Nm )
                ts.append( str(nX)+" teams competed against each other in "+Nm )
                ts.append( Nm+" saw a competition between "+str(nX)+random.sample(syn,1)[0] )
                
        else:
            ts.append(None)
            
        return ts


# In[46]:


# TSent(T,N,getT()[1],getT()[0],20)


# In[47]:


def No_of_eventsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" events "," games "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
    #         All = ','.join(di[tb[it]])
            X = int(di[tb[it]][0].strip().strip("."))
            ps1 = [ "The no. of events in sport was "+str(X)
                   , str(X)+" events were there in "+Nm ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
#             length = len(re.findall("[0-9]"," ".join(di[tb[it]])))
            X = int(di[tb[it]][0].strip().strip("."))
            if(tval):
#                 All = ','.join(di[tb[it]])
                ts.append( "There were "+str(X)+random.sample(syn,1)[0]+"in "+Nm )
                ts.append( "There were more than "+str(random.randint(1,X-2))+random.sample(syn,1)[0]+"in "+Nm )
                ts.append( "There were less than "+str(random.randint(X+2,X+8))+random.sample(syn,1)[0]+"in "+Nm )
                ts.append( str(X)+random.sample(syn,1)[0]+"were held in "+Nm )
                ts.append( "More than "+str(random.randint(1,X-2))+random.sample(syn,1)[0]+"were held in "+Nm )
                ts.append( "Less than "+str(random.randint(X+2,X+8))+random.sample(syn,1)[0]+"were held in "+Nm )
                
            else:
#                 NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
#                 All = ','.join(NT)
                nX = random.randint(X+1,X+7)
                ts.append( "There were "+str(nX)+random.sample(syn,1)[0]+"in "+Nm )
                ts.append( "There were less than "+str(random.randint(1,X-2))+random.sample(syn,1)[0]+"in "+Nm )
                ts.append( "There were more than "+str(random.randint(X+2,X+8))+random.sample(syn,1)[0]+"in "+Nm )
                ts.append( str(nX)+random.sample(syn,1)[0]+"were held in "+Nm )
                ts.append( "Less than "+str(random.randint(1,X-2))+random.sample(syn,1)[0]+"were held in "+Nm )
                ts.append( "More than "+str(random.randint(X+2,X+8))+random.sample(syn,1)[0]+"were held in "+Nm )
                
        else:
            ts.append(None)
            
        return ts


# In[48]:


# NSent(T,N,getN()[1],getN()[0],20)


# In[49]:


def EstablishedSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" established "," founded "]
    jub = {25:" Silver ",40:" Ruby ",50:" Gold ",60:" Diamond ",65:" Sapphire ",70:" Platinum ",75:" Palladium "
           ,100:" Centennial ",125:" Quasquicentennial ",150:" Sesquicentennial ",175:" Dodransbicentennial ",200:" Bicentennial "}
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" was"+random.sample(syn,1)[0]+"on "+All
                  , All+" is when "+Nm+" was"+random.sample(syn,1)[0] ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
#             length = len(re.findall("[0-9]"," ".join(di[tb[it]])))
            year = int(re.findall("[0-9][0-9][0-9][0-9]",di[tb[it]][0])[0])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" was started on "+All )
                ts.append( "In the year "+str(year)+" the sport was played for the first time" )
                ts.append( "The sport event never happened before "+str(year) )
                ts.append( Nm+" was"+random.sample(syn,1)[0]+str(2020-year)+" years ago" )
                for i in jub.keys():
                    if(year+i<=2020):
                        ts.append(Nm+" event has celebrated it's "+jub[i]+"jubilee on "+str(year+i))
                    else:
                        ts.append(Nm+" will celebrate it's "+jub[i]+"jubilee on "+str(year+i))
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                nyear = random.randint(year+10,year+20)
                ts.append( Nm+" was started on "+All )
                ts.append( "In the year "+str(nyear)+" the sport was played for the first time" )
                ts.append( "The sport event never happened before "+str(nyear) )
                ts.append( Nm+" was"+random.sample(syn,1)[0]+str(2020-year+random.randint(5,40))+" years ago" )
                for i in jub.keys():
                    if(nyear+i<=2020):
                        ts.append(Nm+" event has celebrated it's "+jub[i]+"jubilee on "+str(nyear+i))
                    else:
                        ts.append(Nm+" will celebrate it's "+jub[i]+"jubilee on "+str(nyear+i))
                
                
        else:
            ts.append(None)
            
        return ts


# In[51]:


# EFSent(T,N,getEF(),15)


# In[36]:


def Official_siteSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
#     syn = [" events "," games "]
    udom = ["com","in","edu","uk","co","us"]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The official site of "+Nm+" is "+All 
                  , "The sport has the official site "+All ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
#             length = len(re.findall("[0-9]"," ".join(di[tb[it]])))
            dom = []
            for i in range(len(di[tb[it]][0].split("."))):
                if(len(di[tb[it]][0].split(".")[i])<=3 and i>0):
                    dom.append(di[tb[it]][0].split(".")[i])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The website of the sport is "+All )
                ts.append( "The website has domain name "+random.sample(dom,1)[0] )
                ts.append( "Information about "+Nm+" could be found at "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ndom = random.sample(list(set(udom)-set(dom)),random.randint(1,2))
                ts.append( "The website of the sport is "+All)
                ts.append( "The website has domain name "+random.sample(ndom,1)[0] )
                ts.append( "Information about "+Nm+" could be found at "+All )
                
        else:
            ts.append(None)
            
        return ts


# In[37]:


# OSent(T,N,getO()[1],getO()[0],44)


# #### Multi-row :

# In[1]:


def multi_row1(tb,dn,F,it,tval=True):
    Ul,L = F["Venue"]
    Ud,D = F["Date"]
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(L[tb[it]][0] != None and D[tb[it]][0] != None):
            ts["Venue,Date"] = []
            Al1 = ",".join(random.sample(L[tb[it]],1))
            Al2 = ",".join(random.sample(D[tb[it]],1))
            ts["Venue,Date"].append( Nm+" was held at "+Al1+" on "+Al2 )
        
        
    else:
        if(L[tb[it]][0] != None and D[tb[it]][0] != None):
            ts["Venue,Date"] = []
            Al1 = ",".join(random.sample(list(set(Ul)-set(L[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Ud)-set(D[tb[it]])),1))
            ts["Venue,Date"].append( Nm+" was held at "+Al1+" on "+Al2 )
        
    return ts


# In[39]:


# multi_row1(T,N,5)


# In[40]:


def multi_row2(tb,dn,F,it,tval=True):
    Ut,T = F["Teams"]
    Un,N = F["No_of_events"]
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(T[tb[it]][0] != None and N[tb[it]][0] != None):
            ts["Teams,No_of_events"] = []
            Al1 = ",".join(random.sample(T[tb[it]],1))
            Al2 = ",".join(random.sample(N[tb[it]],1))
            ts["Teams,No_of_events"].append( Al1+" teams played "+Al2+" games" )
        
        
    else:
        if(T[tb[it]][0] != None and N[tb[it]][0] != None):
            ts["Teams,No_of_events"] = []
            Al1 = ",".join(random.sample(list(set(Ut)-set(T[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Un)-set(N[tb[it]])),1))
            ts["Teams,No_of_events"].append( Al1+" teams played "+Al2+" games" )
        
    return ts


# In[41]:


# multi_row2(T,N,35)

