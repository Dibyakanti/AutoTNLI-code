from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import sys
import math
import json
import datetime
from util import *


if './' not in sys.path:
    sys.path.append('./')


table_index = np.array(category_map[category_map.category.isin(['Food&Drink'])].table_id)


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys = []
    keys =[i.text for i in soup.find('tr').find_all('th')]
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


def get_Table_Title():
    d = {}
    tb = []
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            tb.append(dictionary['Tablename'])
            if("Title" in dictionary.keys()):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(dictionary['Title'])
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return d,tb


N,T = get_Table_Title()

def get_Manufacturer(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Manufacturer"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Country_of_origin(T,N,fake=False,sel=0):
    u1 = set([])
    u2 = set([])
    d = {}
    k1 = "Country of origin"
    k2 = "Place of origin"
    for n in range(80):
        if(int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u1.add(dictionary[k1][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k1][i].replace(",,",",").strip())
                else:
                    dictionary[k1].replace(",,",",")
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
                    dictionary[k2].replace(",,",",")
                    for i in range(len(dictionary[k2].split(","))):
                        u1.add(dictionary[k2].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k2].split(",")[i].strip())

            if(k1 not in dictionary.keys() and k2 not in dictionary.keys() ):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k1.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u1,d,it,sel)
        
    return list(u1),d


def get_Variants(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Variants"
    k2 = "Flavour"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k1][i].replace(",,",",").strip())
                else:
                    dictionary[k1].replace(",,",",")
                    for i in range(len(dictionary[k1].split(","))):
                        u.add(dictionary[k1].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k1].split(",")[i].strip())
            
            if(k2 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i].replace(",,",",").strip())
                        d[dictionary['Tablename']].append(dictionary[k2][i].replace(",,",",").strip())
                else:
                    dictionary[k2].replace(",,",",")
                    for i in range(len(dictionary[k2].split(","))):
                        u.add(dictionary[k2].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k2].split(",")[i].strip())
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys() ):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"]["Variants"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Introduced(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Introduced"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        year = re.findall("[0-9][0-9][0-9][0-9]",dictionary[k][i])[0]
                        u.add(year)
                        d[dictionary['Tablename']].append(year)
                else:
                    year = re.findall("[0-9][0-9][0-9][0-9]",dictionary[k])[0]
                    u.add(year)
                    d[dictionary['Tablename']].append(year)
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Related_products(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Related products"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].lower().strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].lower().strip())
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i].lower().strip())
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i].lower().strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Alcohol_by_volume(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Alcohol by volume"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        perc = re.findall("[0-9.]+",dictionary[k][i])
                        for j in range (len(perc)):
                            u.add(perc[j])
                            d[dictionary['Tablename']].append(perc[j])
                else:
                    perc = re.findall("[0-9.]+",dictionary[k])
                    for j in range (len(perc)):
                        u.add(perc[j])
                        d[dictionary['Tablename']].append(perc[j])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d        


def get_Website(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Website"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Color(T,N,it,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Color"
    k2 = "Colour"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
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
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k1.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Main_ingredients(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Main ingredients"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Type(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Type"
    for n in range(80):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(80): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["FoodnDrinks"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d

# Extract all data :

def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Manufacturer","Country_of_origin","Variants","Introduced","Related_products"
      	,"Alcohol_by_volume","Website","Color","Main_ingredients","Type"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data

# Sentence generator :

def ManufacturerSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ dn[tb[it]][0]+" is manufactured by "+di[tb[it]][0] 
                   ,"It is manufactured by "+di[tb[it]][0] 
                   ,di[tb[it]][0]+" manufactured "+dn[tb[it]][0] ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                ts.append('The food was manufactured by '+di[tb[it]][0])
                ts.append(di[tb[it]][0]+" was made by "+dn[tb[it]][0]+" company")
                ts.append(dn[tb[it]][0]+" company makes "+di[tb[it]][0])
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append('The food was manufactured by '+NT)
                ts.append(dn[tb[it]][0]+" was made by "+NT+" company")
                ts.append(NT+" company makes "+dn[tb[it]][0])
        else:
            ts.append(None)
                
        return ts


def Country_of_originSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" is the country of origin"
                   ,All+" is where it originated from"
                   ,dn[tb[it]][0]+" originated from "+All ]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts = ['The food is from '+All,
                 "It is made in "+ str(len(di[tb[it]])) +" countries",
                 "It is made in less than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+" countries",
                 "It is made in more than "+str(random.randint(0,len(di[tb[it]])-1))+" countries",
                 "It was first made in "+random.sample(di[tb[it]],1)[0],
                 dn[tb[it]][0]+" is a "+ All +" food",
                 "This food has been first made in "+All]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                All = ','.join(NT)
                ts = ['The food is from '+All,
                 "It is made in "+ str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5)) +" countries",
                 "It is made in more than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+" countries",
                 "It is made in less than "+str(random.randint(0,len(di[tb[it]])-1))+" countries",
                 "It was first made in "+random.sample(NT,1)[0],
                 dn[tb[it]][0]+" is a "+ random.sample(NT,1)[0] +" food",
                 "This food has been first made in "+All]
        else:
            ts.append(None)
        return ts


def VariantsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "Variants of this food are "+All
                  , All+" are the variants of "+dn[tb[it]][0]
                  , "Several variants of this food are "+All ]
        else:
            ps1 = [None]
        return ps1
    else:
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts1 = "This is available in "+All
                ts2 = "There are "+str(len(di[tb[it]]))+" flavours of this product"
                ts3 = "There are less than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+" variants"
                ts4 = "There are more than "+str(random.randint(0,len(di[tb[it]])-1))+" variants"
                ts5 = random.sample(di[tb[it]],1)[0]+" is one of the flavours of this"
                ts6 = ','.join(random.sample(di[tb[it]],random.randint(1,len(di[tb[it]]))) )+" are the variants of "+dn[tb[it]][0]
                ts7 = "There are "+ ("single"if len(di[tb[it]])==1 else "multiple") + " flavour"
                ts8 = "It comes in "+str(len(di[tb[it]]))+" flavours"
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,5))
                All = ','.join(NT)
                ts1 = "This is available in "+All
                ts2 = "There are "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+" flavours of this product"
                ts3 = "There are more than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+" variants"
                ts4 = "There are less than "+str(random.randint(0,len(di[tb[it]])-1))+" variants"
                ts5 = random.sample(NT,1)[0]+" is one of the flavours of this"
                ts6 = ','.join(random.sample(NT,random.randint(1,len(NT))) )+" are the variants of "+dn[tb[it]][0]
                ts7 = "There are "+ ("multiple"if len(di[tb[it]])==1 else "single") + " flavour"
                ts8 = "It comes in "+str( random.randint(0,len(di[tb[it]])-1) )+" flavours"

            return ts1,ts2,ts3,ts4,ts5,ts6,ts7,ts8
        else:
            return [None]


def IntroducedSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = ["brought into existence","launched","inaugurated","instigated"]
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ "It was introduced in "+di[tb[it]][0]
                  , di[tb[it]][0]+" is when it was introduced"
                  , dn[tb[it]][0]+" was introduced in "+di[tb[it]][0]]
        else:
            ps1=[None]
        return ps1
    else:
        if(di[tb[it]][0] != None):
            year = int(di[tb[it]][0])
            if(tval):
                ts1 = "It was  "+random.sample(syn,1)[0]+" in "+di[tb[it]][0]
                ts2 = "It was "+random.sample(syn,1)[0]+" after "+str(random.randint(year-50,year-10))
                ts3 = "It was "+random.sample(syn,1)[0]+" before "+str(random.randint(year+10,year+60))
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts1 = "It was "+random.sample(syn,1)[0]+" in "+NT
                ts2 = "It was "+random.sample(syn,1)[0]+" before "+str(random.randint(year-50,year-10))
                ts3 = "It was "+random.sample(syn,1)[0]+" after "+str(random.randint(year+10,year+60))

            return ts1,ts2,ts3
        else:
            return [None]


def Related_productsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = ["similar","related","close"]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "It is related to "+All
                  , All+" are related to it"
                  , All+" are related to "+dn[tb[it]][0]]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        length = len(di[tb[it]])
        if(di[tb[it]][0] != None):
            if(tval):
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to "+ ','.join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to "+str(length)+" products" )
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to more than "+str(random.randint(0,length-1)) )
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to less than "+str(random.randint(length+1,length+5)) )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to "+ ','.join(random.sample(NT,random.randint(1,len(NT)))) )
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to "+str(random.randint(length+1,length+3))+" products" )
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to less than "+str(random.randint(0,length-1))+" products" )
                ts.append(dn[tb[it]][0] +" is "+ random.sample(syn,1)[0] +" to more than "+str(random.randint(length+1,length+5))+" products" )
        else:
            ts.append(None)
        
        return ts


def Alcohol_by_volumeSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = '% or '.join(di[tb[it]])
            ps1 = [ dn[tb[it]][0]+" is "+All+"% by volume of alcohol"
                  , "Alcohol is "+All+"% by volume in it"
                  , All+"% alcohol is present in it"]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            mn = int(math.floor(float(di[tb[it]][0])))
            mx = int(math.floor(float(di[tb[it]][-1])))
            if(tval):
                ts.append(str(random.sample([mn,mx],1)[0])+"% is alcohol in "+dn[tb[it]][0])
                ts.append(str(100-mx)+"% is not alcohol")
                ts.append("It has more than "+str(random.randint(mn-3,mn-1))+"% alcohol" )
                ts.append("It has less than "+str(random.randint(mx+5,mx+15))+"% alcohol" )
                ts.append("Alcohol is the "+("major" if mx >= 50 else "not major")+"part of this beverage")
            else:
                NT = random.randint(mx+1,mx+10)
                ts.append(str(NT)+"% is alcohol in "+dn[tb[it]][0])
                ts.append(str(100-NT)+"% is not alcohol")
                ts.append("It has less than "+str(random.randint(mn-3,mn-1))+"% alcohol" )
                ts.append("It has more than "+str(random.randint(mx+5,mx+15))+"% alcohol" )
                ts.append("Alcohol is the "+("major" if mx < 50 else "not major")+"part of this beverage")
        else:
            ts.append(None)
        
        return ts


def WebsiteSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = ["ordered","purchased"]
    alldom = [".com",".co.in",".co.fr",".co.za"]
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ "The name of the website is "+di[tb[it]][0]
                  , "It has a website named "+di[tb[it]][0] 
                  , di[tb[it]][0]+" is the name of it's website"]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            
            if(tval):
                dom = re.findall("\.[a-z.]+",di[tb[it]][0])[0]
                ts.append("This can be "+random.sample(syn,1)[0]+" from "+di[tb[it]][0])
                ts.append("This detail of the beverage can be found at "+di[tb[it]][0])
                ts.append("Official website of this is "+di[tb[it]][0])
                ts.append('the website has a domain name of '+dom)                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                dom = re.findall("\.[a-z.]+",di[tb[it]][0])[0]
                ndom = random.sample(list(set(alldom)-set([dom])),1)[0]
                ts.append("This can be "+random.sample(syn,1)[0]+" from "+NT )
                ts.append("The detail of the beverage can be found at "+NT)
                ts.append("Official website of this is "+NT)
                ts.append('the website has a domain name of '+ndom )
        else:
            ts.append(None)
        
        return ts


def ColorSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" are the colors of this food"
                  , "Colors of this food are "+All
                  , "The food comes in "+All]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append("It comes in "+All)
                ts.append("It does not come in "+",".join(random.sample(list(set(univ)-set(di[tb[it]])),2)) )
                ts.append("It come in "+str(len(di[tb[it]]))+" color(s)" )
                ts.append("It comes in more than "+str(random.randint(0,len(di[tb[it]])-1))+" color(s)" )
                ts.append("It comes in less than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+4))+" color(s)" )
                ts.append("It comes in "+("single color" if len(di[tb[it]])==1 else "multiple colors") )
            else:
                All = ','.join(di[tb[it]])
                ts.append("It does not come in "+All)
                ts.append("It comes in "+",".join(random.sample(list(set(univ)-set(di[tb[it]])),2)) )
                ts.append("It come in "+str(len(di[tb[it]]))+" color(s)" )
                ts.append("It comes in less than "+str(random.randint(0,len(di[tb[it]])-1))+" color(s)" )
                ts.append("It comes in more than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+4))+" color(s)" )
                ts.append("It comes in "+("single color" if len(di[tb[it]])!=1 else "multiple colors") )
        else:
            ts.append(None)
        
        return ts


def Main_ingredientsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The main ingredients of "+dn[tb[it]][0]+" are "+All
                  , All+" are the main ingredients of "+dn[tb[it]][0] 
                  , "The main ingredients are "+All ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        length = len(di[tb[it]])
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append(All+' are used for making '+dn[tb[it]][0])
                ts.append("More than "+ str(random.randint(0,length-1)) +" ingredients are required for "+dn[tb[it]][0] )
                ts.append("Less than "+ str(random.randint(length+1,length+4)) +" ingredients are required for "+dn[tb[it]][0] )
                ts.append(",".join(random.sample(di[tb[it]],random.randint(1,length)))+" is used to make this" )
                ts.append(",".join(random.sample(di[tb[it]],1))+" is not sufficient for making it" )
                ts.append(",".join(random.sample(di[tb[it]],random.randint(1,length)))+" are necessary to prepare this" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(2,5))
                All = ','.join(NT)
                ts.append(All+' are used for making '+dn[tb[it]][0])
                ts.append("Less than "+ str(random.randint(0,length-1)) +" ingredients are required for "+dn[tb[it]][0] )
                ts.append("More than "+ str(random.randint(length+1,length+4)) +" ingredients are required for "+dn[tb[it]][0] )
                ts.append(",".join(random.sample(NT,random.randint(1,len(NT))))+" is used to make this" )
                ts.append(",".join(random.sample(NT,1))+" is not sufficient for making it" )
                ts.append(",".join(random.sample(NT,random.randint(1,len(NT))))+" are necessary to prepare this" )
                
        else:
            ts.append(None)
        
        return ts


def TypeSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The product is of type "+All
                  , dn[tb[it]][0]+" is a "+All
                  , "It is a type of "+All ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        length = len(di[tb[it]])
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append('The type of '+dn[tb[it]][0]+" is "+All)
                ts.append("It is "+All)
                ts.append('It is not '+",".join(random.sample(list(set(univ)-set(di[tb[it]])),random.randint(2,5))))
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(2,5))
                All = ','.join(di[tb[it]])
                ts.append('The type of '+dn[tb[it]][0]+" is "+",".join(NT))
                ts.append("It is "+",".join(NT))
                ts.append('It is not '+All)
                
        else:
            ts.append(None)
        
        return ts

# 1st multi-row templates
def multi_row1(tb,dn,F,it,tval=True):
    Ur,R = F["Related_products"]
    Uv,V = F["Variants"]
    Um,M = F["Main_ingredients"]
    Uc,C = F["Color"]
    
    ts = {}
    if(tval):
        # 1
        if(R[tb[it]][0] != None and V[tb[it]][0] != None):
            ts["Related_products,Variants"] = []
            l1 = str(len(R[tb[it]]))
            l2 = str(len(V[tb[it]]))
            ts["Related_products,Variants"].append( "There are "+l1+" related products to this but "+l2+" variants" )
            ts["Related_products,Variants"].append("There are "+ ("more" if int(l1)>int(l2) else "less")+" related products than variants")
        if(R[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Related_products,Main_ingredients"] = []
            l1 = str(len(R[tb[it]]))
            l2 = str(len(M[tb[it]]))
            ts["Related_products,Main_ingredients"].append( "There are "+l1+" related products to this but "+l2+" necessary ingrediets" )
            ts["Related_products,Main_ingredients"].append("There are "+ ("more" if int(l1)>int(l2) else "less")+" related products than necessary ingredients")
        if(R[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Related_products,Color"] = []
            l1 = str(len(R[tb[it]]))
            l2 = str(len(C[tb[it]]))
            ts["Related_products,Color"].append( "There are "+l1+" related products to this but it comes in "+l2+" colors" )
            ts["Related_products,Color"].append("There are "+ ("more" if int(l1)>int(l2) else "less")+" related products than color it comes in")
        # 2
        if(V[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Variants,Main_ingredients"] = []
            l1 = str(len(V[tb[it]]))
            l2 = str(len(M[tb[it]]))
            ts["Variants,Main_ingredients"].append( "There are "+l1+" variants of this but "+l2+" necessary ingredients" )
            ts["Variants,Main_ingredients"].append("There are "+ ("more" if int(l1)>int(l2) else "less")+" variants than necessary ingredients")
        if(V[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Variants,Color"] = []
            l1 = str(len(V[tb[it]]))
            l2 = str(len(C[tb[it]]))
            ts["Variants,Color"].append( "There are "+l1+" variants of this but it comes in "+l2+" colors" )
            ts["Variants,Color"].append("There are "+ ("more" if int(l1)>int(l2) else "less")+" variants than color it comes in")
        # 3
        if(M[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Main_ingredients,Color"] = []
            l1 = str(len(M[tb[it]]))
            l2 = str(len(C[tb[it]]))
            ts["Main_ingredients,Color"].append( "There are "+l1+" necessary ingredients to make this but it comes in "+l2+" colors" )
            ts["Main_ingredients,Color"].append("There are "+ ("more" if int(l1)>int(l2) else "less")+" main ingredients than color it comes in")
    
    else:
        # 1
        if(R[tb[it]][0] != None and V[tb[it]][0] != None):
            ts["Related_products,Variants"] = []
            l1 = str(len(R[tb[it]]))
            l2 = str(len(V[tb[it]]))
            ts["Related_products,Variants"].append( "There are "+str(random.randint(int(l1)+1,int(l1)+4))+" related products to this but "+str(random.randint(int(l2)+1,int(l2)+5))+" variants" )
            ts["Related_products,Variants"].append("There are "+ ("more" if int(l1)<int(l2) else "less")+" related products than variants")
        if(R[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Related_products,Main_ingredients"] = []
            l1 = str(len(R[tb[it]]))
            l2 = str(len(M[tb[it]]))
            ts["Related_products,Main_ingredients"].append( "There are "+str(random.randint(int(l1)+1,int(l1)+4))+" related products to this but "+str(random.randint(int(l2)+1,int(l2)+2))+" necessary ingrediets" )
            ts["Related_products,Main_ingredients"].append("There are "+ ("more" if int(l1)<int(l2) else "less")+" related products than necessary ingredients")
        if(R[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Related_products,Color"] = []
            l1 = str(len(R[tb[it]]))
            l2 = str(len(C[tb[it]]))
            ts["Related_products,Color"].append( "There are "+str(random.randint(int(l1)+1,int(l1)+4))+" related products to this but it comes in "+str(random.randint(int(l2)+1,int(l2)+4))+" colors" )
            ts["Related_products,Color"].append("There are "+ ("more" if int(l1)<int(l2) else "less")+" related products than color it comes in")
        # 2
        if(V[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Variants,Main_ingredients"] = []
            l1 = str(len(V[tb[it]]))
            l2 = str(len(M[tb[it]]))
            ts["Variants,Main_ingredients"].append( "There are "+str(random.randint(int(l1)+1,int(l1)+4))+" variants of this but "+str(random.randint(int(l2)+1,int(l2)+3))+" necessary ingredients" )
            ts["Variants,Main_ingredients"].append("There are "+ ("more" if int(l1)<int(l2) else "less")+" variants than necessary ingredients")
        if(V[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Variants,Color"] = []
            l1 = str(len(V[tb[it]]))
            l2 = str(len(C[tb[it]]))
            ts["Variants,Color"].append( "There are "+str(random.randint(int(l1)+1,int(l1)+4))+" variants of this but it comes in "+str(random.randint(int(l2)+1,int(l2)+4))+" colors" )
            ts["Variants,Color"].append("There are "+ ("more" if int(l1)<int(l2) else "less")+" variants than color it comes in")
        # 3
        if(M[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Main_ingredients,Color"] = []
            l1 = str(len(M[tb[it]]))
            l2 = str(len(C[tb[it]]))
            ts["Main_ingredients,Color"].append( "There are "+str(random.randint(int(l1)+1,int(l1)+4))+" necessary ingredients to make this but it comes in "+str(random.randint(int(l2)+1,int(l2)+4))+" colors" )
            ts["Main_ingredients,Color"].append("There are "+ ("more" if int(l1)<int(l2) else "less")+" main ingredients than color it comes in")

    return ts

# 2nd multi-row templates
def multi_row2(tb,dn,F,it,tval=True):
    Uv,V = F["Variants"]
    Um,M = F["Manufacturer"]
    
    ts = {}
    if(tval):
        if(M[tb[it]][0] != None and V[tb[it]][0] != None):
            ts["Manufacturer,Variants"] = []
            Al1 = ','.join(M[tb[it]])
            l1 = str(len(V[tb[it]]))
            ts["Manufacturer,Variants"].append( Al1+" manufactures "+l1+" variants of the product" )
    
    else:
        if(M[tb[it]][0] != None and V[tb[it]][0] != None):
            ts["Manufacturer,Variants"] = []
            Al1 = ','.join(M[tb[it]])
            l1 = str(random.randint(len(V[tb[it]])+1,len(V[tb[it]])+5))
            ts["Manufacturer,Variants"].append( Al1+" manufactures "+l1+" variants of the product" )        

    return ts

# 3rd multi-row templates
def multi_row3(tb,dn,F,it,tval=True):
    Ut,T = F["Type"]
    Ua,A = F["Alcohol_by_volume"]
    Uv,V = F["Variants"]
    Uc,C = F["Color"]
    
    ts = {}
    if(tval):
        if(T[tb[it]][0] != None and A[tb[it]][0] != None):
            ts["Type,Alcohol_by_volume"] = []
            Al1 = random.sample(T[tb[it]],1)[0]
            Al2 = random.sample(A[tb[it]],1)[0]
            ts["Type,Alcohol_by_volume"].append(Al1+" has "+Al2+"% alcohol by volume")
        if(T[tb[it]][0] != None and V[tb[it]][0] != None):
            ts["Type,Variants"] = []
            Al1 = random.sample(T[tb[it]],1)[0]
            Al2 = ",".join(random.sample(V[tb[it]],random.randint(1,len(V[tb[it]])) ) )
            ts["Type,Variants"].append(Al1+" comes in "+Al2+" flavours")
        if(T[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Type,Color"] = []
            Al1 = random.sample(T[tb[it]],1)[0]
            Al2 = ",".join(random.sample(C[tb[it]],random.randint(1,len(C[tb[it]])) ) )
            ts["Type,Color"].append(Al1+" comes in "+Al2+" colors")
        
    else:
        if(T[tb[it]][0] != None and A[tb[it]][0] != None):
            ts["Type,Alcohol_by_volume"] = []
            Al1 = random.sample(T[tb[it]],1)[0]
            a = float(A[tb[it]][0]) + float(random.randint(1,3))
            Al2 = str(a)
            ts["Type,Alcohol_by_volume"].append(Al1+" has "+Al2+"% alcohol by volume")
        if(T[tb[it]][0] != None and V[tb[it]][0] != None):
            ts["Type,Variants"] = []
            Al1 = random.sample(T[tb[it]],1)[0]
            NT = random.sample(list(set(Uv)-set(V[tb[it]])),random.randint(2,4))
            Al2 = ",".join(random.sample(NT,random.randint(1,len(NT)) ) )
            ts["Type,Variants"].append(Al1+" comes in "+Al2+" flavours")
        if(T[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Type,Color"] = []
            Al1 = random.sample(T[tb[it]],1)[0]
            NT = random.sample(list(set(Uc)-set(C[tb[it]])),random.randint(2,4))
            Al2 = ",".join(random.sample(NT,random.randint(1,len(NT)) ) )
            ts["Type,Color"].append(Al1+" comes in "+Al2+" colors")
        
    return ts