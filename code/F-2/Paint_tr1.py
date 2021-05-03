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


# In[2]:


getfa = {	
"Movie_tr1":{"Dir":[0,1,2],"Prod":[0,1,2],"SP":[1],"SR":[0,1,2],"M":[0,1,2],"Cin":[1],"EdiB":[0,1,2],"PC":[1],
    "Dby":[0,1,2],"Rdate":[0,1,2],"Rtime":[1],"Cty":[0,1,2],"Lang":[0,1,2],"Budg":[1],"BO":[1]},
"Book_tr1":{"P":[1],"Sch":[1],"Fmt":[0,1,2],"Gen":[0,1,2],"PubDate":[1],
        "NI":[1],"MChar":[0,1,2],"Wby":[0,1,2]},
"FnD_tr1":{"Mf":[1],"COP":[0,1,2],"VF":[0,1,2],"In":[1],"RPd":[0,1,2],
    "Abv":[1],"W":[1],"C":[0,1,2],"MIn":[0,1,2],"T":[0,1,2]},
"Organiz_tr1":{"W":[1],"Hq":[1],"Fd":[1],"In":[0,1,2],"Kp":[0,1,2],"Pdt":[0,1,2],"Ne":[1],"Ta":[0,1,2],"F":[0,1,2],
    "As":[0,1,2],"T":[1],"S":[0,1,2],"P":[1],"O":[1],"Pred":[1]},
"Paint_tr1":{"Artist":[1],"Year":[1],"Medium":[1],"Dimensions":[1],"Location":[1]},
"Fest_tr1":{"Type":[0,1,2],"Observed_by":[0,1,2],"Frequency":[1],"Celebrations":[0,1,2],"Significance":[0,1,2],"Observances":[0,1,2],
    "Date":[1],"Related_to":[0,1,2],"Also_called":[0,1,2],"Official_name":[1],"Begins":[1],"Ends":[1],
    "2021_date":[1],"2020_date":[1],"2019_date":[1],"2018_date":[1]},
"SpEv_tr1":{"Venue_Location":[0,1,2],"Date_Dates":[1],"Competitors":[0,1,2],"Teams":[1],
	"No_of_events":[1],"Established_Founded":[1],"Official_site":[1]},
"Univ_tr1":{"Website":[1],"Type":[0,1,2],"Established":[1],"Undergraduates":[1],"Postgraduates":[1],
    "Motto_Motto_in_English":[0,1,2],"Location":[1],"Nickname":[1],"Campus":[1],"Colors":[0,1,2],
    "Students":[1],"Academic_staff":[1],"Administrative_staff":[1],"President":[1],"Endowment":[1],"Mascot":[1],
    "Provost":[1],"Sporting_affiliations":[0,1,2],"Academic_affiliations":[0,1,2],"Former_names":[1]}
}


# In[3]:


# Catg = pd.read_csv("../../autotnlidatasetandcode/table_categories modified.tsv",sep="\t") 
Catg = pd.read_csv("/content/drive/My Drive/Auto-TNLI/data/table_categories modified.tsv",sep="\t") 


# In[4]:


Ptab = np.array(Catg[Catg.category.isin(['Painting'])].table_id)
# tablesFolder = "../../autotnlidatasetandcode/tables"
tablesFolder = "/content/drive/My Drive/Auto-TNLI/data/tables"


# In[5]:


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys =[i.text for i in soup.find('tr').find_all('th')]
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


# In[6]:


# key = {}
# for n in range(130):
#     if(int(Ptab[n][1:]) <=2800 ): # not necessary
#         dictionary = parseFile(Ptab[n]+".html", tablesFolder)
#         print(dictionary['Tablename'] ," : ")
#         for k in dictionary.keys():
#             if(k in key.keys()):
#                 key[k] += 1
#             else:
#                 key[k] = 1
#             print(k)
# {k: v for k, v in sorted(key.items(), key=lambda item: item[1])}


# In[7]:


def get_Table_Title():
    d = {}
    tb = []
    for n in range(132):
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


# In[8]:


N,T = get_Table_Title()
# T


# In[28]:


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


# In[10]:


def get_Artist(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Artist"
    for n in range(132):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in dictionary[k]:
                        if( not re.findall("[Aa]ttributed",i) and not re.findall("[Uu]nknown",i)): 
                            u.add(i.strip())
                            d[dictionary['Tablename']].append(i.strip())
                else:
                    i = dictionary[k]
                    if( not re.findall("[Aa]ttributed",i) and not re.findall("[Uu]nknown",i)): 
                        u.add(dictionary[k].strip())
                        d[dictionary['Tablename']].append(dictionary[k].strip())
                    else:
                        d[dictionary['Tablename']].append(None)
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(132): # for getting all the fakes in one go
            sel = random.sample(getfa["Paint_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[11]:


# get_Artist(T,N,0)[1]


# In[12]:


def get_Year(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Year"
    for n in range(132):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                r = re.findall("[0-9][0-9][0-9]+",dictionary[k])
                t = 0
                for s in r:
                    if(t != int(s)):
                        if(int(s)>1000):
                            u.add(s)
                        d[dictionary['Tablename']].append(s)
                        t = int(s.strip())
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(132): # for getting all the fakes in one go
            sel = random.sample(getfa["Paint_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[13]:


# get_Year(T,N,0)[1]


# In[14]:


def get_Medium(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Medium"
    k2 = "Type"
    for n in range(132):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i].lower())
                        d[dictionary['Tablename']].append(dictionary[k1][i].lower())
                else:
                    for i in range(len(dictionary[k1].split(","))):
                        u.add(dictionary[k1].split(",")[i].lower())
                        d[dictionary['Tablename']].append(dictionary[k1].split(",")[i].lower())
                        
            if(k2 in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i].lower())
                        d[dictionary['Tablename']].append(dictionary[k2][i].lower())
                else:
                    for i in range(len(dictionary[k2].split(","))):
                        u.add(dictionary[k2].split(",")[i].lower())
                        d[dictionary['Tablename']].append(dictionary[k2].split(",")[i].lower())
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys() ):
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(132): # for getting all the fakes in one go
            sel = random.sample(getfa["Paint_tr1"]["Medium"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[15]:


# get_Medium(T,N,0)[1]


# In[49]:


def get_Dimensions(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Dimensions"
    for n in range(132):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                s = dictionary[k].replace('\xa0','').replace('\u200b','')
                r = re.findall("[0-9.]+",s)
                for ss in r:
                    u.add(float(ss.strip()))
                    d[dictionary['Tablename']].append(float(ss.strip()))
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(132): # for getting all the fakes in one go
            sel = random.sample(getfa["Paint_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel,subNone=False)
        
    return list(u),d


# In[50]:


# get_Dimensions(T,N,True)[1]


# In[18]:


def get_Location(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Location"
    for n in range(132):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
#                 print(dictionary['Tablename'],' : ',dictionary['Starring'])
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
#                     for i in range(len(dictionary[k])):
                    u.add(",".join(dictionary[k]))
                    d[dictionary['Tablename']].append(",".join(dictionary[k]))
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])
                    
            else:
#                 print(dictionary['Tablename'],':',"!!!")
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(132): # for getting all the fakes in one go
            sel = random.sample(getfa["Paint_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# In[19]:


# get_Location(T,N,0)[1]


# #### All extracted data :

# In[20]:


def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Artist","Year","Medium","Dimensions","Location"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data
# F is the Extracted_data[key]


# #### Sentences :

# In[21]:


def ArtistSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
#     syn = ["sector","area","field"]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The artist of "+dn[tb[it]][0]+" was "+All
                  , dn[tb[it]][0]+" was painted by "+All
                  , All+" made "+dn[tb[it]][0]+" painting" ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" was created by "+All )
                ts.append( All+" created this painting" )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ts.append( dn[tb[it]][0]+" was created by "+All )
                ts.append( All+" created this painting" )
                
        else:
            ts.append(None)
        
        return ts


# In[22]:


# AtSent(T,N,getAt()[1],getAt()[0],7)


# In[23]:


def YearSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
#     syn = ["sector","area","field"]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ dn[tb[it]][0]+" was painted in "+di[tb[it]][0]
                  , "This was made in "+di[tb[it]][0] 
                  , "This was painted in "+di[tb[it]][0]]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            y = int(di[tb[it]][0])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" was painted in the year "+di[tb[it]][0] )
                ts.append( dn[tb[it]][0]+" was painted before "+str(random.randint(y+20,y+100)) )
                ts.append( dn[tb[it]][0]+" was painted after "+str(random.randint(1000,y-30)) )
                ts.append( dn[tb[it]][0]+" was painted in the "+str(int(y/100)+1)+"th century" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
#                 All = ','.join(NT)
                ts.append( dn[tb[it]][0]+" was painted in the year "+NT )
                ts.append( dn[tb[it]][0]+" was painted after "+str(random.randint(y+20,y+100)) )
                ts.append( dn[tb[it]][0]+" was painted before "+str(random.randint(1000,y-30)) )
                ts.append( dn[tb[it]][0]+" was painted in the "+str(int(y/100)-1)+"th century" )
                
        else:
            ts.append(None)
        
        return ts


# In[24]:


# YSent(T,N,getY()[1],getY()[0],7)


# In[25]:


def MediumSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
#     syn = ["sector","area","field"]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "It was made in "+All 
                  , All+" was the medium for this"
                  , dn[tb[it]][0]+" was of "+All+" type" ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( All+" was used as a medium for this painting" )
                ts.append( "The type of this painting is "+All )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ts.append( All+" was used as a medium for this painting" )
                ts.append( "The type of this painting is "+All )
                
        else:
            ts.append(None)
        
        return ts


# In[9]:


# MTSent(T,N,getMT()[1],getMT()[0],10)


# In[26]:


def DimensionsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
#             All = ','.join(di[tb[it]])
            dd = di[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            ps1 = [ "The dimensions are "+str(lc)+" cm by "+str(wc)+" cm and "+str(li)+" inch by "+str(wi)+" inch"
                  , "The painting "+dn[tb[it]][0]+" is "+str(lc)+" cm by "+str(wc)+" cm and "+str(li)+" inch by "+str(wi)+" inch"
                  , str(lc)+" cm by "+str(wc)+" cm and "+str(li)+" inch by "+str(wi)+" inch"+" is the size of the painting" ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            dd = di[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            if(tval):
#                 All = ','.join(di[tb[it]])
                ts.append( "The painting is "+str(lc)+" cm by "+str(wc)+" cm in size" )
                ts.append( "The painting is "+str(li)+" inch by "+str(wi)+" inch in size" )
                ts.append( "The area is "+str(lc*wc)+" sq.cm" )
                ts.append( "The area is "+str(li*wi)+" sq.inch" )
                ts.append( "Length is "+str(lc-wc)+" cm more than width" )
                ts.append( "Length is "+str(li-wi)+" inch more than width" )
                ts.append( "The perimeter of the painting is "+str(2*(lc+wc))+" cm" )
                
            else:
#                 NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
#                 All = ','.join(NT)
                rnd = float(random.randint(3,8))
                ts.append( "The painting is "+str(lc+rnd)+" cm by "+str(wc+rnd)+" cm in size" )
                ts.append( "The painting is "+str(wi)+" inch by "+str(li)+" inch in size" )
                ts.append( "The area is "+str(lc*wi)+"sq.cm" )
                ts.append( "The area is "+str(li*wc)+"sq.inch" )
                ts.append( "Length is "+str(lc-wc+rnd)+"cm more than width" )
                ts.append( "Length is "+str(li-wi+2*rnd)+"inch more than width" )
                ts.append( "The perimeter of the painting is "+str(2*rnd*(li+wi))+"inch" )
                
        else:
            ts.append(None)
        
        return ts


# In[29]:


# DSent(T,N,getD()[1],getD()[0],10)
# get_Data(True)["Dimensions"][1]


# In[11]:


def LocationSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ dn[tb[it]][0]+" is at "+All
                  , "The painting is at "+All 
                  , "It is located in "+All ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" is now kept in the "+All)
                ts.append( All+" is the location of the painting" )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ts.append( dn[tb[it]][0]+" is now kept in the "+All)
                ts.append( All+" is the location of the painting" )
                
        else:
            ts.append(None)
        
        return ts


# In[13]:


# LSent(T,N,getL()[1],getL()[0],10)


# In[32]:


def multi_row1(tb,dn,F,it,tval=True):
    Ua,A = F["Artist"]
    Um,M = F["Medium"]
    Ul,L = F["Location"]
    
    ts = {}
    if(tval):
        if(A[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Artist,Medium"] = []
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(M[tb[it]])
            ts["Artist,Medium"].append( Al1+" used "+Al2+" medium for painting" )
        if(A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = []
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(L[tb[it]])
            ts["Artist,Location"].append( Al1+"'s painting is located in "+Al2 )
        if(A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = []
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(L[tb[it]])
            ts["Artist,Location"].append( "Atleast one of the painting by "+Al1+" is at "+Al2 )
        
    else: 
        if(A[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Artist,Medium"] = []
#             NA = random.sample(list(set(Ua)-set(A[tb[it]])),1)
            NM = random.sample(list(set(Um)-set(M[tb[it]])),1)
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(NM)
            ts["Artist,Medium"].append( Al1+" used "+Al2+" medium for painting" )
        if(A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = [] 
            NA = random.sample(list(set(Ua)-set(A[tb[it]])),1)
#             NL = random.sample(list(set(Ul)-set(L[tb[it]])),1)
            Al1 = ",".join(NA)
            Al2 = ",".join(L[tb[it]])
            ts["Artist,Location"].append( Al1+"'s painting is located in "+Al2 )
        if(A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = []
#             NA = random.sample(list(set(Ua)-set(A[tb[it]])),1)
            NL = random.sample(list(set(Ul)-set(L[tb[it]])),1)
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(NL)
            ts["Artist,Location"].append( "Atleast one of the painting by "+Al1+" is at "+Al2 )
        
    return ts


# In[15]:


# multi_row1(T,N,14,False)


# In[50]:


def multi_row2(tb,dn,F,it,tval=True):
    Ua,A = F["Artist"]
    Ud,D = F["Dimensions"]
    Uy,Y = F["Year"]
    
    ts = {}
    if(tval):
        if(A[tb[it]][0] != None and Y[tb[it]][0] != None):
            ts["Artist,Year"] = []
            Al1 = ",".join(A[tb[it]])
#             Al2 = ",".join(M[tb[it]])
            year = int(Y[tb[it]][0])
            ts["Artist,Year"].append( dn[tb[it]][0]+" was created by "+Al1+" in the "+str(int(year/100)+1)+"th century" )
            ts["Artist,Year"].append( Al1+" made a painting in "+str(int(year/100)+1)+"th century" )
            syn = [" completed "," started "]
            ts["Artist,Year"].append( Al1+random.sample(syn,1)[0]+"this painting after "+str(random.randint(1000,year-40)) )
        if(A[tb[it]][0] != None and D[tb[it]][0] != None):
            ts["Artist,Dimensions"] = []
            dd = D[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            Al1 = ",".join(A[tb[it]])
#             Al2 = ",".join(L[tb[it]])
            ts["Artist,Dimensions"].append( Al1+"'s painting was "+str(lc)+" cm by "+str(wc)+" cm in size" )
            ts["Artist,Dimensions"].append( Al1+"'s painting was "+str(li)+" cm by "+str(wi)+" cm in size" )
        
    else: 
        if(A[tb[it]][0] != None and Y[tb[it]][0] != None):
            ts["Artist,Year"] = []
#             NA = random.sample(list(set(Ua)-set(A[tb[it]])),1)
            Al1 = ",".join(A[tb[it]])
            year = int(Y[tb[it]][0])
            ts["Artist,Year"].append( dn[tb[it]][0]+" was created by "+Al1+" in the "+str(int(year/100)-random.randint(1,3))+"th century" )
            ts["Artist,Year"].append( Al1+" made a painting in "+str(int(year/100)-random.randint(1,3))+"th century" )
            syn = [" completed "," started "]
            ts["Artist,Year"].append( Al1+random.sample(syn,1)[0]+"this painting after "+str(random.randint(year+40,year+200)) )
        if(A[tb[it]][0] != None and D[tb[it]][0] != None):
            ts["Artist,Dimensions"] = []
            dd = D[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            Al1 = ",".join(A[tb[it]])
#             Al2 = ",".join(L[tb[it]])
            rnd = float(random.randint(3,8))
            ts["Artist,Dimensions"].append( Al1+"'s painting was "+str(lc+rnd)+" cm by "+str(wc-rnd)+" cm in size" )
            ts["Artist,Dimensions"].append( Al1+"'s painting was "+str(li+rnd)+" inch by "+str(wi+rnd)+" inch in size" )
    return ts


# In[16]:


# multi_row2(T,N,14,False)

