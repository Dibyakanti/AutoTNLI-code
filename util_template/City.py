from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import sys
import json

if './' not in sys.path:
    sys.path.append('./')


getfa = {   
"Movie_tr1":{"Dir":[0,1,2],"Prod":[0,1,2],"SP":[1],"SR":[0,1,2],"M":[0,1,2],"Cin":[1],"EdiB":[0,1,2],"PC":[1],
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
"SpEv_tr1":{"Venue_Location":[0,1,2],"Date_Dates":[1],"Competitors":[0,1,2],"Teams":[1],
    "No_of_events":[1],"Established_Founded":[1],"Official_site":[1]},
"Univ_tr1":{"Website":[1],"Type":[0,1,2],"Established":[1],"Undergraduates":[1],"Postgraduates":[1],
    "Motto_Motto_in_English":[0,1,2],"Location":[1],"Nickname":[1],"Campus":[1],"Colors":[0,1,2],
    "Students":[1],"Academic_staff":[1],"Administrative_staff":[1],"President":[1],"Endowment":[1],"Mascot":[1],
    "Provost":[1],"Sporting_affiliations":[0,1,2],"Academic_affiliations":[0,1,2],"Former_names":[1]},
"City_tr1":{"Elevation":[1],"Metro":[1],"Urban":[1],"City":[1],"Location":[1],"Government":[1],
            "Highest_elevation":[1],"Lowest_elevation":[1],"Land":[1],"Water":[1],"Demonym":[1],
            "Province":[1],"Mayor":[1],"Time_zone":[1],"Named_for":[1],"Area_code":[1],"Postal_code":[1]
         ,"Coordinates":[1],"Incorporated":[1],"Density":[1],"Urban_density":[1],"Metro_density":[1]}
}


# Catg = pd.read_csv("../../data/table_categories modified.tsv",sep="\t") 
Catg = pd.read_csv("/content/drive/My Drive/Auto-TNLI/data/table_categories.tsv",sep="\t") 
Ptab = np.array(Catg[Catg.category.isin(['City'])].table_id)
tablesFolder = "/content/drive/My Drive/Auto-TNLI/data/tables"


# tablesFolder = "../../data/json/"


def parseFile(filename,tablesFolder):
    
    f = open(tablesFolder+filename+".json",encoding="utf8")
    data = json.load(f)
    data['Tablename'] = filename
    
    return data


def get_Table_Title():
    d = {}
    tb = []
    for n in range(194):
        if(int(Ptab[n][1:]) <=2800 ):
            dictionary = parseFile(Ptab[n], tablesFolder)
            tb.append(dictionary['Tablename'])
            if("title" in dictionary.keys()):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']] = dictionary['title']
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return d,tb


N,T = get_Table_Title()


def FakeDICT(tb,dn,univ,di,it,sel=0,subNone = False):
    '''
    d1 : dict for that table
    univ : list of a set
    df : dataframe of Born/Death to get the table name
    sel: selection bit to select whether to 0 : add / 1 : substitute / 2 : delete
    it : choose table name from the dataframe
    '''
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


def get_Elevation(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Elevation"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
    
    return list(u),d


def get_Location(T,N,fake=False,sel=0): # Country Location State
    u = set([])
    d = {}
    k1 = "Country"
    k2 = "Location"
    k3 = "State"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k1])):
                    u.add(dictionary[k1][i])
                    d[dictionary['Tablename']].append(dictionary[k1][i])
            elif(k2 in dictionary.keys()):
                k = k2
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
            elif(k3 in dictionary.keys()):
                k = k3
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"]["Location"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
    
    return list(u),d


def get_Government(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Government"
    k2 = "Governing body"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k1 in dictionary.keys()):
                k = k1
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
            elif(k2 in dictionary.keys()):
                k = k2
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k1.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Highest_elevation(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Highest elevation"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Demonym(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Demonym(s)"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"]["Demonym"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Province(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Province"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Mayor(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Mayor"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Time_zone(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Time zone"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Lowest_elevation(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Lowest elevation"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Named_for(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Named for"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Area_code(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Area code(s)"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"]["Area_code"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Postal_code(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Postal code"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Coordinates(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Coordinates"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Incorporated(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Incorporated"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Metro(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Metro"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Urban(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Urban"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                 
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Density(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Density"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Metro_density(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Metro density"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Urban_density(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Urban density"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Area(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Area"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys() and re.findall("[0-9]",".".join(dictionary[k])) ):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_City(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "City"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys() and re.findall("[0-9]",".".join(dictionary[k])) ):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Land(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Land"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys() and re.findall("[0-9]",".".join(dictionary[k])) ):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Water(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Water"
    for n in range(194):
        if(int(Ptab[n][1:]) <= 2800):
            dictionary = parseFile(Ptab[n], tablesFolder)
            if(k in dictionary.keys() and re.findall("[0-9]",".".join(dictionary[k])) ):
                d[dictionary['Tablename']] = []
                for i in range(len(dictionary[k])):
                    u.add(dictionary[k][i])
                    d[dictionary['Tablename']].append(dictionary[k][i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(194): # for getting all the fakes in one go
            sel = random.sample(getfa["City_tr1"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d

# Extract all data :

def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Elevation","Metro","Urban","City","Location","Government","Highest_elevation","Lowest_elevation"
         ,"Land","Water","Demonym","Province","Mayor","Time_zone","Named_for","Area_code","Postal_code"
         ,"Coordinates","Incorporated","Density","Urban_density","Metro_density"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data


# Sentence generator :

def ElevationSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    elevations = F[1] # 
    sentences = []

    if(tval): #
        elevation = elevations[table[it]][0]
    else:
        elevation = random.sample(list(set(F[0])-set(elevations[table[it]])),1)[0]
        
    if (elevations[table[it]][0]==None): #
        return [None]
    elevation = elevation.replace(',', '')
    depth = False
    if '-' in elevation:
        depth = True
        elevation = elevation.replace('-', '')
    reg = re.search(r"(?P<elev1>\d+\.?\d*)\s?(?P<unit1>[a-zA-z]+)\s?\(?(?P<elev2>\d+\.?\d*)?\s?(?P<unit2>[a-zA-Z]+)?\)?", elevation)

    if premise:
        sentences.append(Nm+' is at an elevation of ' + reg.groupdict()['elev1'] + " " + reg.groupdict()['unit1'])
        if reg.groupdict()['elev2']:
            sentences.append(Nm+' is at an elevation of ' + reg.groupdict()['elev2'] + " " + reg.groupdict()['unit2'])
    else:
        sentences.append('The city is at a ' + ('depth' if depth else 'height') + ' of ' + reg.groupdict()['elev1'] + " " + reg.groupdict()['unit1'])
        if reg.groupdict()['elev2']:
            sentences.append('The city is at a ' + ('depth' if depth else 'height') + ' of ' + reg.groupdict()['elev2'] + " " + reg.groupdict()['unit2'])
        sentences.append(Nm+' is ' + reg.groupdict()['elev1'] + " " + reg.groupdict()['unit1'] + ('below' if depth else 'above') + ' sea level')
        if reg.groupdict()['elev2']:
            sentences.append(Nm+' is ' + reg.groupdict()['elev2'] + " " + reg.groupdict()['unit2'] + ('below' if depth else 'above') + ' sea level')
        sentences.append(Nm + ('negatively' if depth else 'positively') + ' elevated')
    return sentences


def LocationSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    locations = F[1]
    sentences = []
    
    if(tval): #
        location = locations[table[it]][0]
    else:
        location = random.sample(list(set(F[0])-set(locations[table[it]])),1)[0]
    
    if (locations[table[it]][0]==None):
        return [None]
#     for location in locations:
    if premise:
        sentences.append(Nm + ' is located in ' + location)
    else: 
        sentences.append(Nm + ' lies in ' + location)
        sentences.append(Nm + ' is a city in ' + location)
        sentences.append(Nm + ' is a part of ' + location)
    return sentences


def GovernmentSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if premise:
        sentences.append(Nm + ' is the government of ' + value)
    else:
        sentences.append(value + ' is the officially decision making body for the ' + Nm + ' city')
        sentences.append(value + ' govern the city ' + Nm)
        sentences.append(Nm + ' is governed by ' + value)
    return sentences


def Highest_elevationSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if premise:
        sentences.append('The highest elevation of ' + Nm + ' is ' + value)
        sentences.append('The ' + Nm + ' city highest elevation is ' + value)
    else:
        sentences.append('The peak of ' + Nm + ' is at ' + value)
        sentences.append(value + ' is the highest peak in the ' + Nm + ' city.')
    
    return sentences


def DemonymSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if not premise:
        sentences.append(value + ' live in ' + Nm)
        sentences.append('The people of the city ' + Nm + ' are also known as ' + value)
        sentences.append('The native of the city ' + Nm + ' are also called ' + value)
        sentences.append('People of the city ' + Nm + ' are called by ' + value)
        sentences.append(value + ' is another name for the people of the city ' + Nm)
    else:
        sentences.append('The demonym of the city ' + Nm + ' is ' + value)
        sentences.append('The city ' + Nm + ' demonym is ' + value)
        
    return sentences


def ProvinceSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        sentences.append('The city ' + Nm + ' is located in ' + value + ' province')
        sentences.append('The city ' + Nm + ' is part of ' + value + ' province')
    else:
        sentences.append('The province of the city ' + Nm + ' is ' + value)
        sentences.append('The city province is ' + value)
        sentences.append('The city ' + Nm + ' province is ' + value)
        
    return sentences



def MayorSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if not premise:
        sentences.append('The day to day governing of the city is supervised by ' + value)
        sentences.append('One of the highest governing people of the city ' + Nm + ' is ' + value)
        sentences.append(value + ' govern the city ' + Nm)
        sentences.append(value + ' take part in the major decisions of the city ' + Nm)
        sentences.append(value + ' is well known person in the city ' + Nm)
        sentences.append(value + ' is an important person in the city ' + Nm)
        sentences.append(value + ' holds a position in the governing body of city ' + Nm)
        sentences.append(value + ' is an important local leader of the city ' + Nm)
        sentences.append(value + ' is responsible for the wellbeing of the people of the city ' + Nm)
    else:
        sentences.append(value + ' is the mayor of ' + Nm)
        sentences.append('The mayor of ' + Nm + ' is ' + value)
    return sentences


def Time_zoneSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    reg = re.search('UTC(?P<time>[+-−]+[0-9]*:?[0-9]?[0-9]*)',value)
    timezone = reg.groupdict()['time']
    if '-' in timezone:
        time = timezone.splt('-')[1]
        zone = '-'
    else:
        time = timezone.split('+')[1]
        zone = '+'
    if not premise:
        sentences.append('The time zone of the city is ' + time + " hours " + 'ahead' if zone == '+' else 'behind the UTC time.')
        sentences.append('The time zone of the city is ' + time + " hours " + 'ahead' if zone == '+' else 'behind the Coordinated Universal Time.')
        sentences.append('The time zone of the city is ' + time + " hours " + 'ahead' if zone == '+' else 'behind the Greenwich Mean Time.')

    else:
        sentences.append('The time-zone of ' + Nm + ' is ' + value)
        sentences.append(value + ' is the time zone of ' + Nm)
    return sentences


def Lowest_elevationSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    val1, val2 = value.split("(")
    val1.strip()
    val2 = val2.split(")")[0].strip()
    if not premise:
        sentences.append('The peak of the city is at ' + val1)
        sentences.append('The peak of the city is at ' + val2)
        sentences.append(val1 + ' is the lowest point in ' + Nm)
        sentences.append(val2 + ' is the lowest point in ' + Nm)
    else:
        sentences.append('The lowest elevation of ' + Nm + ' is ' + val1)
        sentences.append('The lowest elevation of ' + Nm + ' is ' + val2)
        sentences.append('The ' + Nm + ' citys\' lowest elevation is ' + val1)
        sentences.append('The ' + Nm + ' citys\' lowest elevation is ' + val2)
    return sentences


def Named_forSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): #
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if not premise:
        sentences.append('This city is named after ' + value)
    else:
        sentences.append(Nm + ' is named for ' + value)
        sentences.append('This city is named after ' + value)
    return sentences


def Area_codeSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval):
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if not premise:
        sentences.append(value + ' is a prefix required to call a number in ' + Nm)
        sentences.append(value + ' code is required to call a number in ' + Nm)
    else:
        sentences.append(value + ' is the area code of ' + Nm)
        sentences.append(' The city area code is ' + value)
    return sentences


def Postal_codeSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): 
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if not premise:
        sentences.append('The zip code of the city ' + Nm + ' is ' + value)
        sentences.append('To send a mail to the city use ' + value + ' as zip.')
        sentences.append('To send a post to the city use ' + value + ' as zip.')
        sentences.append('PS use ' + value + ' to send mail in the city')
        sentences.append('PS use ' + value + ' to post mail in the city')
        sentences.append('Official address of residents of the city ' + Nm + ' has zip code ' + value)
    else:
        sentences.append('The postal code of the city is ' + value)
        sentences.append('The city has the postal code ' + value)
    return sentences


def CoordinatesSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): 
        value = values[table[it]][0]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]
    
    if 'Coordinates' in value:
        value = value.split("Coordinates")[0]
    if not premise:
        sentences.append(Nm + " is located at " + value)
        sentences.append('In the map the city ' + Nm + ' could be found at ' + value)
        sentences.append('In the map the city could be found at ' + value + ' by ' + Nm)
        sentences.append('The geographic location of the city is at ' + value)
        sentences.append('The location of the city is ' + value.split('/')[1].split('\ufeff')[1].split(' ')[0] + ' longitude by ' + value.split('/')[1].split('\ufeff')[1].split(' ')[1] + ' latitude')
        sentences.append(Nm + ' is ' + ('above' if ('N' in value.split('/')[1].split('\ufeff')[1].split(' ')[0]) else 'below') + ' the equator')
    else:
        sentences.append('The coordinates of the city are ' + value)
        sentences.append(value + ' are the coordinates of the city.')
    return sentences            


def IncorporatedSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    
    if(tval): 
        value = values[table[it]][-1]
    else:
        value = random.sample(list(set(F[0])-set(values[table[it]])),1)[0]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        sentences.append(Nm + ' was constituted as a city in ' + value)
        sentences.append(Nm + ' was legally declared as a city in ' + value)
        sentences.append('On ' + value + ' the city was awarded the legal declaration of a municipal charter.')
    else:
        sentences.append('The city was incorporated in ' + value)
        sentences.append('On ' + value + ' the city was incorporated')
    return sentences


def MetroSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    synonyms = [" people"," citizen"," residents"]
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        for val in values[table[it]]:
            if(re.findall("[km][mi]",val)): # Area
                for val_split in val.split("("): 
                    if(re.findall("[km][mi]",val)):
                        area = re.findall("[1-9].*",val_split)[0].strip()
                        area_val = int(float(area.replace(",","").split(" ")[0]))
                        if(tval):
                            sentences.append("The metro region of "+Nm+" is "+area.replace(",",""))
                            sentences.append("The metro region is more than "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The metro region is less than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
                        else:
                            sentences.append("The metro region of "+Nm+" is "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The metro region is less than "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The metro region is more than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
            else: # Population
                val = val.replace(",","")
                val = val.replace(".","")
                population = re.findall("[0-9]+",val)[0]
                population_val = int(population.replace(",",""))
                if(tval):
                    sentences.append("There are "+str(population_val)+random.sample(synonyms,1)[0]+" in metro region of "+Nm )
                    sentences.append(str(population_val)+random.sample(synonyms,1)[0]+" live in the metro region of "+Nm )
                    sentences.append("There are more than "+str(random.randint(population_val-2000,population_val-500))+random.sample(synonyms,1)[0]+" in the metro region of "+Nm )
                    sentences.append("There are less than "+str(random.randint(population_val+1000,population_val+5000))+random.sample(synonyms,1)[0]+" in the metro region of "+Nm)
                else:
                    sentences.append("There are "+str(random.randint(population_val+100,population_val+5000))+random.sample(synonyms,1)[0]+" in metro region of "+Nm )
                    sentences.append(str(random.randint(population_val+100,population_val+5000))+random.sample(synonyms,1)[0]+" live in the metro region of "+Nm )
                    sentences.append("There are less than "+str(random.randint(population_val-2000,population_val-500))+random.sample(synonyms,1)[0]+" in the metro region of "+Nm )
                    sentences.append("There are more than "+str(random.randint(population_val+1000,population_val+5000))+random.sample(synonyms,1)[0]+" in the metro region of "+Nm)
    else:
        premises = {}
        for val in values[table[it]]:
            if(re.findall("[km][mi]",val)): # Area
                premises["Area"] = []
                premises["Area"].append("The area of the metro region is "+val)
                premises["Area"].append(val+" is the area of the metro region of "+Nm)
                premises["Area"].append("The metro region is "+val+" in area")
            else: # Population
                premises["Population"] = []
                premises["Population"].append("The population of the metro region is "+val)
                premises["Population"].append(val+" is the population of the metro region of "+Nm)
                premises["Population"].append("The metro region has "+val+" population")
                
        if(count(premises.keys()) == 2):
            for area_sent in premises["Area"]:
                sentences.append( area_sent+random.sample(premises["Population"],1)[0])
        else:
            for sent in premises[premises.key()[0]]:
                sentences.append(sent)
                
    return sentences


def UrbanSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    synonyms = [" people"," citizen"," residents"]
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        for val in values[table[it]]:
            if(re.findall("[km][mi]",val)): # Area
                for val_split in val.split("("): 
                    if(re.findall("[km][mi]",val)):
                        area = re.findall("[1-9].*",val_split)[0].strip()
                        area_val = int(float(area.replace(",","").split(" ")[0]))
                        if(tval):
                            sentences.append("The urban region of "+Nm+" is "+area.replace(",",""))
                            sentences.append("The urban region is more than "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The urban region is less than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
                        else:
                            sentences.append("The urban region of "+Nm+" is "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The urban region is less than "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The urban region is more than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
            else: # Population
                val = val.replace(",","")
                val = val.replace(".","")
                population = re.findall("[0-9]+",val)[0]
                population_val = int(population.replace(",",""))
                if(tval):
                    sentences.append("There are "+str(population_val)+random.sample(synonyms,1)[0]+" in urban region of "+Nm )
                    sentences.append(str(population_val)+random.sample(synonyms,1)[0]+" live in the urban region of "+Nm )
                    sentences.append("There are more than "+str(random.randint(population_val-2000,population_val-500))+random.sample(synonyms,1)[0]+" in the urban region of "+Nm )
                    sentences.append("There are less than "+str(random.randint(population_val+1000,population_val+5000))+random.sample(synonyms,1)[0]+" in the urban region of "+Nm)
                else:
                    sentences.append("There are "+str(random.randint(population_val+100,population_val+5000))+random.sample(synonyms,1)[0]+" in urban region of "+Nm )
                    sentences.append(str(random.randint(population_val+100,population_val+5000))+random.sample(synonyms,1)[0]+" live in the urban region of "+Nm )
                    sentences.append("There are less than "+str(random.randint(population_val-2000,population_val-500))+random.sample(synonyms,1)[0]+" in the urban region of "+Nm )
                    sentences.append("There are more than "+str(random.randint(population_val+1000,population_val+5000))+random.sample(synonyms,1)[0]+" in the urban region of "+Nm)
    else:
        premises = {}
        for val in values[table[it]]:
            if(re.findall("[km][mi]",val)): # Area
                premises["Area"] = []
                premises["Area"].append("The area of the urban region is "+val)
                premises["Area"].append(val+" is the area of the urban region of "+Nm)
                premises["Area"].append("The urban region is "+val+" in area")
            else: # Population
                premises["Population"] = []
                premises["Population"].append("The population of the urban region is "+val)
                premises["Population"].append(val+" is the population of the urban region of "+Nm)
                premises["Population"].append("The urban region has "+val+" population")
                
        if(count(premises.keys()) == 2):
            for area_sent in premises["Area"]:
                sentences.append( area_sent+random.sample(premises["Population"],1)[0])
        else:
            for sent in premises[premises.key()[0]]:
                sentences.append(sent)
                
    return sentences


def CitySent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    synonyms = [" people"," citizen"," residents"]
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        for val in values[table[it]]:
            if(re.findall("[km][mi]",val)): # Area
                for val_split in val.split("("):
                    if(re.findall("[km][mi]",val)):
                        area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                        area_val = int(float(area.replace(",","").split(" ")[0]))
                        if(tval):
                            sentences.append(area.replace(",","")+" is the area of "+Nm)
                            sentences.append(Nm+" has an area of "+area.replace(",",""))
                            sentences.append(area.replace(",","")+" is covered by the city")
                            sentences.append("The area of this city is more than "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The area of this city is less than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
                        else:
                            sentences.append(str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" is the area of "+Nm)
                            sentences.append(Nm+" has an area of "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]))
                            sentences.append(str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" is covered by the city")
                            sentences.append(str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" is the area of "+Nm )
                            sentences.append("The area of this city is less than  "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:]) )
                            sentences.append("The area of this city is more than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:]) )
            else: # Population
                val = val.replace(",","")
                val = val.replace(".","")
                population = re.findall("[0-9]+",val)[0]
                population_val = int(population.replace(",",""))
                if(tval):
                    sentences.append("There are "+str(population_val)+random.sample(synonyms,1)[0]+" in "+Nm )
                    sentences.append(str(population_val)+random.sample(synonyms,1)[0]+" live in "+Nm )
                    sentences.append("There are more than "+str(random.randint(population_val-2000,population_val-500))+random.sample(synonyms,1)[0]+" in "+Nm )
                    sentences.append("There are less than "+str(random.randint(population_val+1000,population_val+5000))+random.sample(synonyms,1)[0]+" in "+Nm)
                else:
                    sentences.append("There are "+str(random.randint(population_val+100,population_val+5000))+random.sample(synonyms,1)[0]+" in "+Nm )
                    sentences.append(str(random.randint(population_val+100,population_val+5000))+random.sample(synonyms,1)[0]+" live in "+Nm )
                    sentences.append("There are less than "+str(random.randint(population_val-2000,population_val-500))+random.sample(synonyms,1)[0]+" in "+Nm )
                    sentences.append("There are more than "+str(random.randint(population_val+1000,population_val+5000))+random.sample(synonyms,1)[0]+" in "+Nm)
    else:
        premises = {}
        for val in values[table[it]]:
            if(re.findall("[km][mi]",val)): # Area
                premises["Area"] = []
                premises["Area"].append("The area of the city is "+val)
                premises["Area"].append(val+" is the area of the city named"+Nm)
                premises["Area"].append("The city is "+val+" in area")
            else: # Population
                premises["Population"] = []
                premises["Population"].append("The population of "+Nm+" is "+val)
                premises["Population"].append(val+" is the population of "+Nm)
                premises["Population"].append(Nm+" has "+val+" population")
                
        if(count(premises.keys()) == 2):
            for area_sent in premises["Area"]:
                sentences.append( area_sent+random.sample(premises["Population"],1)[0])
        else:
            for sent in premises[premises.key()[0]]:
                sentences.append(sent)
                
    return sentences


def DensitySent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    synonyms = [" people"," inhabitents"," residents"]
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        for val_split in value[0].split("("):
            if(re.findall("km",val_split)):
                unit = random.sample(["sq km","km 2"],1)[0]
            elif(re.findall("mi",val_split)):
                unit = random.sample(["sq mi"],1)[0]
            else:
                break
            density = re.findall("[0-9].*",val_split)[0].strip().strip(")")
            density_val = int(float(density.replace(",","").split("/")[0]))
            if(tval):
                sentences.append("The city "+Nm+" is "+density.replace(",","")+" populace")
                if(density_val>10):
                    sentences.append("There are "+str(density_val)+random.sample(synonyms,1)[0]+" per "+unit+" in "+Nm)
                    sentences.append("There are more than "+str(random.randint(max(0,density_val-100),density_val-10))+random.sample(synonyms,1)[0]+" per "+unit+" in "+Nm )
                    sentences.append("There are less than "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in "+Nm )
            else:
                sentences.append("The city "+Nm+" is "+str(random.randint(density_val+10,density_val+1000))+"/".join(density.split("/")[1:])+" populace")
                if(density_val>10):
                    sentences.append("There are "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in "+Nm) 
                    sentences.append("There are less than "+str(random.randint(max(0,density_val-100),density_val-10))+random.sample(synonyms,1)[0]+" per "+unit+" in "+Nm )
                    sentences.append("There are more than "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in "+Nm )                  
    else:
        sentences.append("The density of "+random.sample(synonyms,1)[0]+" in "+Nm+" is "+value[0])
        sentences.append(value[0]+" is the density of"+random.sample(synonyms,1)[0]+" in "+Nm)
                
    return sentences


def Urban_densitySent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    synonyms = [" people"," inhabitents"," residents"]
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        for val_split in value[0].split("("):
            if(re.findall("km",val_split)):
                unit = random.sample(["sq km","km 2"],1)[0]
            elif(re.findall("mi",val_split)):
                unit = random.sample(["sq mi"],1)[0]
            else:
                break;
            density = re.findall("[0-9].*",val_split)[0].strip().strip(")")
            density_val = int(float(density.replace(",","").split("/")[0]))
            if(tval):
                sentences.append("The city "+Nm+" is "+density.replace(",","")+" populace in it's urban region")
                if(density_val>10):
                    sentences.append("There are "+str(density_val)+random.sample(synonyms,1)[0]+" per "+unit+" in the urban region of "+Nm)
                    sentences.append("There are more than "+str(random.randint(max(0,density_val-100),density_val-10))+random.sample(synonyms,1)[0]+" per "+unit+" in the urban region of "+Nm )
                    sentences.append("There are less than "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in the urban region of "+Nm )
            else:
                sentences.append("The city "+Nm+" is "+str(random.randint(density_val+10,density_val+1000))+"/".join(density.split("/")[1:])+" populace in it's urban region")
                if(density_val>10):
                    sentences.append("There are "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in the urban region of "+Nm) 
                    sentences.append("There are less than "+str(random.randint(max(0,density_val-100),density_val-10))+random.sample(synonyms,1)[0]+" per "+unit+" in the urban region of "+Nm )
                    sentences.append("There are more than "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in the urban region of "+Nm )                  
    else:
        sentences.append("The density of "+random.sample(synonyms,1)[0]+" in  the urban region of "+Nm+" is "+value[0])
        sentences.append(value[0]+" is the density of"+random.sample(synonyms,1)[0]+" in  the urban region of "+Nm)
                
    return sentences


def Metro_densitySent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    synonyms = [" people"," inhabitents"," residents"]
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        for val_split in value[0].split("("):
            if(re.findall("km",val_split)):
                unit = random.sample(["sq km","km 2"],1)[0]
            elif(re.findall("mi",val_split)):
                unit = random.sample(["sq mi"],1)[0]
            else:
                break;
            density = re.findall("[0-9].*",val_split)[0].strip().strip(")")
            density_val = int(float(density.replace(",","").split("/")[0]))
            if(tval):
                sentences.append("The city "+Nm+" is "+density.replace(",","")+" populace in it's metro region")
                if(density_val>10):
                    sentences.append("There are "+str(density_val)+random.sample(synonyms,1)[0]+" per "+unit+" in the metro region of "+Nm)
                    sentences.append("There are more than "+str(random.randint(max(0,density_val-100),density_val-10))+random.sample(synonyms,1)[0]+" per "+unit+" in the metro region of "+Nm )
                    sentences.append("There are less than "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in the metro region of "+Nm )
            else:
                sentences.append("The city "+Nm+" is "+str(random.randint(density_val+10,density_val+1000))+"/".join(density.split("/")[1:])+" populace in it's metro region")
                if(density_val>10):
                    sentences.append("There are "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in the metro region of "+Nm) 
                    sentences.append("There are less than "+str(random.randint(max(0,density_val-100),density_val-10))+random.sample(synonyms,1)[0]+" per "+unit+" in the metro region of "+Nm )
                    sentences.append("There are more than "+str(random.randint(density_val+10,density_val+1000))+random.sample(synonyms,1)[0]+" per "+unit+" in the metro region of "+Nm )                  
    else:
        sentences.append("The density of "+random.sample(synonyms,1)[0]+" in  the metro region of "+Nm+" is "+value[0])
        sentences.append(value[0]+" is the density of"+random.sample(synonyms,1)[0]+" in  the metro region of "+Nm)
                
    return sentences


def LandSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        val = value[0].split(")")[0]
        for val_split in val.split("("):
            if(re.findall("[km][mi]",val)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                if(tval):
                    sentences.append(area.replace(",","")+" area of the city "+Nm+" is land")
                    sentences.append("Land covers"+area.replace(",","")+" area of the city")
                    sentences.append("More than "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is land" )
                    sentences.append("Less than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is land" )
                else:
                    sentences.append(str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is land")
                    sentences.append("Land covers "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city")
                    sentences.append("Less than  "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is land" )
                    sentences.append("More than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is land" )
    else:
        val = value[0]
        if(re.findall("[km][mi]",val)): # Area
            sentences.append("The land area of the city is "+val)
            sentences.append("The city land area is "+val)
                
    return sentences


def WaterSent(table,t_name,F,it,tval=True,premise=False):
    Nm = t_name[table[it]][0]
    values = F[1]
    sentences = []
    value = values[table[it]]
    
    if (values[table[it]][0]==None):
        return [None]

    if not premise:
        val = value[0].split(")")[0]
        for val_split in val.split("("):
            if(re.findall("[km][mi]",val)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                if(tval):
                    sentences.append(area.replace(",","")+" area of the city "+Nm+" is water")
                    sentences.append("Water covers"+area.replace(",","")+" area of the city")
                    sentences.append("More than "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is water" )
                    sentences.append("Less than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is water" )
                else:
                    sentences.append(str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is water")
                    sentences.append("Water covers "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city")
                    sentences.append("Less than  "+str(random.randint(max(0,area_val-1000),area_val-10))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is water" )
                    sentences.append("More than "+str(random.randint(area_val+10,area_val+1000))+" "+" ".join(area.split(" ")[1:])+" area of the city "+Nm+" is water" )
    else:
        val = value[0]
        if(re.findall("[km][mi]",val)): # Area
            sentences.append("The water area of the city is "+val)
            sentences.append("The city water area is "+val)
                
    return sentences


# 1st multi-row templates
def multi_row1(tb,dn,F,it,tval=True):
    Um,M = F["Metro"]
    Uu,U = F["Urban"]
    Umd,Md = F["Metro_density"]
    Uud,Ud = F["Urban_density"]
    
    m_population = []
    m_density = {}
    m_area = {}
    
    u_population = []
    u_density = {}
    u_area = {}
    
    if(Md[tb[it]][0]!=None and Ud[tb[it]][0]!=None):
        for val_split in Md[tb[it]][0].split("("):
            if(re.findall("km",val_split)):
                density = re.findall("[0-9].*",val_split)[0].strip().strip(")")
                density_val = int(float(density.replace(",","").split("/")[0]))
                m_density["km"]=density_val
            elif(re.findall("mi",val_split)):
                density = re.findall("[0-9].*",val_split)[0].strip().strip(")")
                density_val = int(float(density.replace(",","").split("/")[0]))
                m_density["mi"]=density_val
        for val_split in Ud[tb[it]][0].split("("):
            if(re.findall("km",val_split)):
                density = re.findall("[0-9].*",val_split)[0].strip().strip(")")
                density_val = int(float(density.replace(",","").split("/")[0]))
                u_density["km"]=density_val
            elif(re.findall("mi",val_split)):
                density = re.findall("[0-9].*",val_split)[0].strip().strip(")")
                density_val = int(float(density.replace(",","").split("/")[0]))
                u_density["mi"]=density_val

    if(M[tb[it]][0]!=None and U[tb[it]][0]!=None):
        for val in M[tb[it]]:
            if(re.findall("[km][mi]",val)): # Area
                for val_split in val.split("("): 
                    if(re.findall("[km][mi]",val)):
                        area = re.findall("[1-9].*",val_split)[0].strip()
                        area_val = int(float(area.replace(",","").split(" ")[0]))
                        if(re.findall("km",val)):
                            m_area['km']=area_val
                        else:
                            m_area['mi']=area_val       
            else:
                val = val.replace(",","")
                val = val.replace(".","")
                population = re.findall("[0-9]+",val)[0]
                population_val = int(population.replace(",",""))
                m_population=population_val
        
        for val in U[tb[it]]:
            if(re.findall("[km][mi]",val)): # Area
                for val_split in val.split("("): 
                    if(re.findall("[km][mi]",val)):
                        area = re.findall("[1-9].*",val_split)[0].strip()
                        area_val = int(float(area.replace(",","").split(" ")[0]))
                        if(re.findall("km",val)):
                            u_area['km']=area_val
                        else:
                            u_area['mi']=area_val       
            else:
                val = val.replace(",","")
                val = val.replace(".","")
                population = re.findall("[0-9]+",val)[0]
                population_val = int(population.replace(",",""))
                u_population=population_val
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(Md[tb[it]][0] != None and Ud[tb[it]][0] != None):
            ts["Metro_density,Urban_density"] = []
            if("km"in m_density.keys() and "km" in u_density.keys()):
                if(m_density["km"] > u_density["km"]):
                    ts["Metro_density,Urban_density"].append( "Metro is more densely populated that urban region")
                else:
                    ts["Metro_density,Urban_density"].append( "Urban is more densely populated that metro region")
            else:
                if(m_density["mi"] > u_density["mi"]):
                    ts["Metro_density,Urban_density"].append( "Metro is more densely populated that urban region")
                else:
                    ts["Metro_density,Urban_density"].append( "Urban is more densely populated that metro region")
        if(M[tb[it]][0] != None and U[tb[it]][0] != None):
            ts["Metro,Urban"] = []
            if("km"in m_area.keys() and "km" in u_area.keys()):
                if(m_area["km"] > u_area["km"]):
                    ts["Metro,Urban"].append( "Metro has more area than urban region")
                else:
                    ts["Metro,Urban"].append( "Urban has more area than metro region")
            else:
                if(m_area["mi"] > u_area["mi"]):
                    ts["Metro,Urban"].append( "Metro has more area than urban region")
                else:
                    ts["Metro,Urban"].append( "Urban has more area than metro region")
                    
            if(len(m_population)!=0 and len(u_population)!=0):
                if(m_population[0]>u_population[0]):
                    ts["Metro,Urban"].append( "Metro is more populated than urban region")
                else:
                    ts["Metro,Urban"].append( "Urban is more populated than metro region")
        
    else:
        if(Md[tb[it]][0] != None and Ud[tb[it]][0] != None):
            ts["Metro_density,Urban_density"] = []
            if("km"in m_density.keys() and "km" in u_density.keys()):
                if(m_density["km"] > u_density["km"]):
                    ts["Metro_density,Urban_density"].append( "Metro is more densely populated that urban region")
                else:
                    ts["Metro_density,Urban_density"].append( "Urban is more densely populated that metro region")
            else:
                if(m_density["mi"] > u_density["mi"]):
                    ts["Metro_density,Urban_density"].append( "Metro is more densely populated that urban region")
                else:
                    ts["Metro_density,Urban_density"].append( "Urban is more densely populated that metro region")
        if(M[tb[it]][0] != None and U[tb[it]][0] != None):
            ts["Metro,Urban"] = []
            if("km"in m_area.keys() and "km" in u_area.keys()):
                if(m_area["km"] < u_area["km"]):
                    ts["Metro,Urban"].append( "Metro has more area than urban region")
                else:
                    ts["Metro,Urban"].append( "Urban has more area than metro region")
            else:
                if(m_area["mi"] < u_area["mi"]):
                    ts["Metro,Urban"].append( "Metro has more area than urban region")
                else:
                    ts["Metro,Urban"].append( "Urban has more area than metro region")
                    
            if(len(m_population)!=0 and len(u_population)!=0):
                if(m_population[0] < u_population[0]):
                    ts["Metro,Urban"].append( "Metro is more populated than urban region")
                else:
                    ts["Metro,Urban"].append( "Urban is more populated than metro region")
        
    return ts


# 2nd multi-row templates
def multi_row2(tb,dn,F,it,tval=True):
    Ul,L = F["Land"]
    Uw,W = F["Water"]
    
    l_area={}
    w_area={}
    
    if(L[tb[it]][0]!=None and W[tb[it]][0]!=None):
        for val_split in L[tb[it]][0].split("("):
            if(re.findall("km",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                l_area["km"]=area_val
            elif(re.findall("mi",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                l_area["mi"]=area_val
        for val_split in W[tb[it]][0].split("("):
            if(re.findall("km",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                w_area["km"]=area_val
            elif(re.findall("mi",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                w_area["mi"]=area_val
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(L[tb[it]][0] != None and W[tb[it]][0] != None):
            ts["Land","Water"] = []
            if("km"in l_area.keys() and "km" in w_area.keys()):
                land_percent = round((l_area["km"]*100)/(l_area["km"]+w_area["km"]),2)
                water_percent = round((w_area["km"]*100)/(l_area["km"]+w_area["km"]),2)
                ts["Land","Water"].append( str(land_percent)+" percentage is land in "+Nm )
                ts["Land","Water"].append( str(water_percent)+" percentage is water in "+Nm )
                
                if(l_area["km"] > w_area["km"]):
                    ts["Land","Water"].append( "There is more land area than water covered area in "+Nm )
                else:
                    ts["Land","Water"].append( "There is more water covered area than land area in "+Nm )
            else:
                land_percent = round((l_area["mi"]*100)/(l_area["mi"]+w_area["mi"]),2)
                water_percent = round((w_area["mi"]*100)/(l_area["mi"]+w_area["mi"]),2)
                ts["Land","Water"].append( str(land_percent)+" percentage is land in "+Nm )
                ts["Land","Water"].append( str(water_percent)+" percentage is water in "+Nm )
                if(l_area["mi"] > w_area["mi"]):
                    ts["Land","Water"].append( "There is more land area than water covered area in "+Nm )
                else:
                    ts["Land","Water"].append( "There is more water covered area than land area in "+Nm )
        
        
    else:
        if(L[tb[it]][0] != None and W[tb[it]][0] != None):
            ts["Land","Water"] = []
            if("km"in l_area.keys() and "km" in w_area.keys()):
                land_percent = round((l_area["km"]*100)/(l_area["km"]+w_area["km"]),2)
                water_percent = round((w_area["km"]*100)/(l_area["km"]+w_area["km"]),2)
                ts["Land","Water"].append( str(land_percent+random.randint(1,5))+" percentage is land in "+Nm )
                ts["Land","Water"].append( str(water_percent+random.randint(1,5))+" percentage is water in "+Nm )
                if(l_area["km"] < w_area["km"]):
                    ts["Land","Water"].append( "There is more land area than water covered area in "+Nm )
                else:
                    ts["Land","Water"].append( "There is more water covered area than land area in "+Nm )
            else:
                land_percent = round((l_area["mi"]*100)/(l_area["mi"]+w_area["mi"]),2)
                water_percent = round((w_area["mi"]*100)/(l_area["mi"]+w_area["mi"]),2)
                ts["Land","Water"].append( str(land_percent+random.randint(1,5))+" percentage is land in "+Nm )
                ts["Land","Water"].append( str(water_percent+random.randint(1,5))+" percentage is water in "+Nm )
                if(l_area["mi"] < w_area["mi"]):
                    ts["Land","Water"].append( "There is more land area than water covered area in "+Nm )
                else:
                    ts["Land","Water"].append( "There is more water covered area than land area in "+Nm )
        
    return ts


# 3rd multi-row templates
def multi_row3(tb,dn,F,it,tval=True):
    Uh,H = F["Highest_elevation"]
    Ul,L = F["Lowest_elevation"]
    
    h={}
    l={}
    
    if(H[tb[it]][0]!=None and L[tb[it]][0]!=None):
        for val_split in H[tb[it]][0].split("("):
            if(re.findall("m",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                h["m"]=area_val
            elif(re.findall("ft",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                h["ft"]=area_val
        for val_split in L[tb[it]][0].split("("):
            if(re.findall("m",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                l["m"]=area_val
            elif(re.findall("ft",val_split)):
                area = re.findall("[1-9].*",val_split)[0].strip().strip(")")
                area_val = int(float(area.replace(",","").split(" ")[0]))
                l["ft"]=area_val
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(H[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Highest_elevation","Lowest_elevation"] = []
            if("m"in h.keys() and "m" in l.keys()):
                diff = h["m"]-l["m"]
                ts["Highest_elevation","Lowest_elevation"].append( "Highest point is "+str(diff)+" m above the lowest point of this city" ) 
                ts["Highest_elevation","Lowest_elevation"].append( "Lowest point is "+str(diff)+" m below the highest point of this city" )
                ts["Highest_elevation","Lowest_elevation"].append( "The elevation range of "+Nm+" is "+str(diff)+" m" )
            else:
                diff = h["ft"]-l["ft"]
                ts["Highest_elevation","Lowest_elevation"].append( "Highest point is "+str(diff)+" ft above the lowest point of this city" ) 
                ts["Highest_elevation","Lowest_elevation"].append( "Lowest point is "+str(diff)+" ft below the highest point of this city" )
                ts["Highest_elevation","Lowest_elevation"].append( "The elevation range of "+Nm+" is "+str(diff)+" ft" )
    else:
        if(H[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Highest_elevation","Lowest_elevation"] = []
            if("m"in h.keys() and "m" in l.keys()):
                diff = int(h["m"]-l["m"])
                diff = random.randint(diff,diff+10)
                ts["Highest_elevation","Lowest_elevation"].append( "Highest point is "+str(diff)+" m above the lowest point of this city" ) 
                ts["Highest_elevation","Lowest_elevation"].append( "Lowest point is "+str(diff)+" m below the highest point of this city" )
                ts["Highest_elevation","Lowest_elevation"].append( "The elevation range of "+Nm+" is "+str(diff)+" m" )
            else:
                diff = int(h["ft"]-l["ft"])
                diff = random.randint(diff,diff+10)
                ts["Highest_elevation","Lowest_elevation"].append( "Highest point is "+str(diff)+" ft above the lowest point of this city" ) 
                ts["Highest_elevation","Lowest_elevation"].append( "Lowest point is "+str(diff)+" ft below the highest point of this city" )
                ts["Highest_elevation","Lowest_elevation"].append( "The elevation range of "+Nm+" is "+str(diff)+" ft" )
        
    return ts