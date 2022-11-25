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


table_index = np.array(category_map[category_map.category.isin(['Organization'])].table_id)


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys = []
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
    for n in range(79):
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





def get_Website(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Website"
    for n in range(79):
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
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Headquarters(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Headquarters"
    for n in range(79):
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
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
            
    return list(u),d


def get_Founded(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Founded"
    k2 = "Formation"
    for n in range(79):
        if(int(table_index[n][1:]) <= 2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                        u.add(",".join(dictionary[k1]).replace('\xa0',' '))
                        d[dictionary['Tablename']].append(",".join(dictionary[k1]).replace('\xa0',' '))
                else:
                    u.add(dictionary[k1].replace("\xa0"," "))
                    d[dictionary['Tablename']].append(dictionary[k1].replace('\xa0',' '))
            if(k2 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(",".join(dictionary[k2]).replace('\xa0',' '))
                        d[dictionary['Tablename']].append(",".join(dictionary[k2]).replace('\xa0',' '))
                else:
                    u.add(dictionary[k2].replace('\xa0',' '))
                    d[dictionary['Tablename']].append(dictionary[k2].replace('\xa0',' '))
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys() ):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"]["Founded"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Industry(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Industry"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",,",",").lower().strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",,",",").lower().strip())
                else:
                    for i in range(len(dictionary[k].replace(",,",",").split(","))):
                        u.add(dictionary[k].replace(",,",",").lower().split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k].replace(",,",",").lower().split(",")[i].strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Key_people(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Key people"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        s = dictionary[k][i]
                        if(len(re.sub(r"\(.*\)","",s).strip())!=0):
                            u.add(re.sub(r"\(.*\)","",s).strip())
                            d[dictionary['Tablename']].append(re.sub(r"\(.*\)","",s).strip())
                else:
                    for i in range(len(dictionary[k].replace(",,",",").split(","))):
                        s = dictionary[k].replace(",,",",").split(",")[i]
                        if(len(re.sub(r"\(.*\)","",s).strip())!=0):
                            u.add(re.sub(r"\(.*\)","",s).strip())
                            d[dictionary['Tablename']].append(re.sub(r"\(.*\)","",s).strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Products(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Products"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].strip())
                else:
                     for i in range(len(dictionary[k].replace(",,",",").split(","))):
                        u.add(dictionary[k].replace(",,",",").split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k].replace(",,",",").split(",")[i].strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Number_of_employees(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Number of employees"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    s = dictionary[k].replace("\xa0"," ").replace(",","")
                    if(len(re.sub(r"\(.*\)","",s).strip())!=0):
                        u.add(re.sub(r"\(.*\)","",s).strip())
                        d[dictionary['Tablename']].append(re.sub(r"\(.*\)","",s).strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Traded_as(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Traded as"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        s = dictionary[k][i].replace("\xa0","")
                        t = re.findall("[A-Za-z ]+:.[A-Z0-9 ]+",s)
                        for j in range(len(t)):
                            u.add(t[j])
                            d[dictionary['Tablename']].append(t[j])
                else:
                    s = dictionary[k].replace("\xa0","")
                    t = re.findall("[A-Za-z ]+:.[A-Z0-9 ]+",s)
                    for j in range(len(t)):
                        u.add(t[j])
                        d[dictionary['Tablename']].append(t[j])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Founder(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Founder"
    k2 = "Founders"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i])
                        d[dictionary['Tablename']].append(dictionary[k1][i])
                else:
                    for i in range(len(dictionary[k1].split(","))):
                        u.add(dictionary[k1].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k1].split(",")[i])
                        
            if(k2 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i])
                        d[dictionary['Tablename']].append(dictionary[k2][i])
                else:
                    for i in range(len(dictionary[k2].split(","))):
                        u.add(dictionary[k2].split(",")[i])
                        d[dictionary['Tablename']].append(dictionary[k2].split(",")[i])
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys() ):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"]["Founder"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Area_served(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Area served"
    for n in range(79):
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
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Type(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Type"
    for n in range(79):
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
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Subsidiaries(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Subsidiaries"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].strip())
                        d[dictionary['Tablename']].append(dictionary[k][i].strip())
                else:
                    for i in range(len(dictionary[k].split(","))):
                        u.add(dictionary[k].split(",")[i].strip())
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i].strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    
    if(fake):
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Parent(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Parent"
    for n in range(79):
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
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Owner(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Owner"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys() and n!=78):
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
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Predecessor(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Predecessor"
    for n in range(79):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys() and n!=78):
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
        for it in range(79): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Organization"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d

# Extract all data :

def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Website","Headquarters","Founded","Industry","Key_people","Products"
          ,"Number_of_employees","Traded_as","Founder","Area_served","Type"
          ,"Subsidiaries","Parent","Owner","Predecessor"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data

# Sentence generator :

def WebsiteSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    alldom = [".com",".co.in",".co.fr",".co.za",".com.br",".org"]
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ "The name of the website is "+di[tb[it]][0]
                  , "It has a website named "+di[tb[it]][0] 
                  , di[tb[it]][0]+" is the name of it's website"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            
            if(tval):
                All = ','.join(di[tb[it]])
                dom = re.findall("\.[a-z.]+",",".join(di[tb[it]][0]))
                ts.append( "It's website is "+ All)
                ts.append( "The website has a domain name "+",".join(dom))
                ts.append( "Information for "+dn[tb[it]][0]+" is present at "+All)
            
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),3)
                All = ','.join(NT)
                dom = re.findall("\.[a-z.]+",",".join(di[tb[it]]))
                ndom = random.sample(list(set(alldom)-set(dom)),random.randint(1,2))
                ts.append( "It's website is "+ All )
                ts.append( "The website has a domain name "+",".join(ndom) )
                ts.append( "Information for "+dn[tb[it]][0]+" is present at "+All )

        else:
            ts.append(None)
        
        return ts


def HeadquartersSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The headquarters are located at "+All
                  , All+" is where the headquarters are located" 
                  , dn[tb[it]][0]+" company's headquarters are located at "+All ]
        else:
            ps1= [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append("The main office is located at "+All)
                ts.append(All+" is where the head office is located")
                ts.append(All+" is the primary location of "+dn[tb[it]][0])
                ts.append("At least one office is present at "+All)
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ts.append("The main office is located at "+All)
                ts.append(All+" is where the head office is located")
                ts.append(All+" is the primary location of "+dn[tb[it]][0])
                ts.append("At least one office is present at "+All)
                
        else:
            ts.append(None)
        
        return ts


def FoundedSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            year = int(re.findall("[0-9][0-9][0-9][0-9]" , ",".join(di[tb[it]]) )[0])
            ps1 = [ "It was founded in "+str(year) 
                  , "In "+str(year)+" this company was founded"
                  , "This company was found on "+str(year) ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            year = int(re.findall("[0-9][0-9][0-9][0-9]" , ",".join(di[tb[it]]) )[0])
            if(tval):
                ts.append( dn[tb[it]][0] +" was established in "+str(year) )
                ts.append( "It was set up in "+str(year) )
                ts.append( "It was established after "+str(random.randint(year-40,year-5)) )
                ts.append( "It was established before "+str(random.randint(year+10,year+40)) )
                ts.append( "It was established "+str(2020-year)+" years ago")
                ts.append( "It was set up "+str(2020-year)+" years ago")
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                nyear = int(re.findall("[0-9][0-9][0-9][0-9]" , ",".join(NT))[0] )
                ts.append( dn[tb[it]][0] +" was established in "+str(nyear) )
                ts.append( "It was set up in "+str(nyear) )
                ts.append( "It was established before "+str(random.randint(year-40,year-5)) )
                ts.append( "It was established after "+str(random.randint(year+10,year+40)) )
                ts.append( "It was established "+str(2020-nyear)+" years ago")
                ts.append( "It was set up "+str(2020-nyear)+" years ago")

        else:
            ts.append(None)
        
        return ts


def IndustrySent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = ["sector","area","field"]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "It is a "+All+" industry"
                  , All+" are the industries this company works in"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append("It is a "+ All +" company")
                ts.append("This company works in "+ random.sample(di[tb[it]],1)[0]+" "+random.sample(syn,1)[0] )
                ts.append("This company deals with "+All )
                ts.append("It is involved in "+str(len(di[tb[it]]))+" "+random.sample(syn,1)[0]+"s" )
                ts.append("It is involved in more than "+str(random.randint(0,len(di[tb[it]])-1))+" "+random.sample(syn,1)[0]+"s" )
                ts.append("It is involved in less than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+" "+random.sample(syn,1)[0]+"s" )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                All = ','.join(NT)
                ts.append( "It is a "+ All +" company" )
                ts.append("This company works in "+ random.sample(di[tb[it]],1)[0]+" "+random.sample(syn,1)[0] )
                ts.append("This company deals with "+All )
                ts.append("It is involved in "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+4))+" "+random.sample(syn,1)[0]+"s" )
                ts.append("It is involved in less than "+str(random.randint(0,len(di[tb[it]])-1))+" "+random.sample(syn,1)[0]+"s" )
                ts.append("It is involved in more than "+str(random.randint(len(di[tb[it]])+1,len(di[tb[it]])+5))+" "+random.sample(syn,1)[0]+"s" )

        else:
            ts.append(None)
        
        return ts


def Key_peopleSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The key people of the company is "+All
                  , All+" are the key people in the company"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The most imporatant people are "+All )
                ts.append( "There are more than "+str(random.randint(0,length-1)) )
                ts.append( "There are less than "+str(random.randint(length+1,length+5)) )
                ts.append( random.sample(di[tb[it]],1)[0]+" takes important decisions in the company" )
                ts.append( All+" leads most of the employees of the company")
                ts.append( All+" earns the high salaries")
                ts.append( All+" combinely hold majority shares of the company")
                ts.append( All+" are the front runners of the company")
                ts.append( "The company is run by "+All )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( "The most important people are "+All )
                ts.append( "There are less than "+str(random.randint(0,length-1)) )
                ts.append( "There are more than "+str(random.randint(length+1,length+5)) )
                ts.append( random.sample(NT,1)[0]+" takes important decisions in "+dn[tb[it]][0] )
                ts.append( All+" leads most of the employees of the company")
                ts.append( All+" earns the high salaries")
                ts.append( All+" combinely hold majority shares of "+dn[tb[it]][0] )
                ts.append( All+" are the front runners of the company" )
                ts.append( "The company is run by "+All )
        else:
            ts.append(None)
        
        return ts


def ProductsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" make "," manufacture "]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "Products made by this company are "+All
                  , All+" are the products made by this company"
                  , All+" are made by them"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "It"+random.sample(syn,1)[0]+",".join(random.sample(di[tb[it]],random.randint(1,length))) )
                ts.append( dn[tb[it]][0]+random.sample(syn,1)[0]+str(length)+" products")
                ts.append( "They"+random.sample(syn,1)[0]+" more than "+str(random.randint(0,length-1))+" items" )
                ts.append( "They"+random.sample(syn,1)[0]+" less than "+str(random.randint(length+1,length+5))+" items" )
                ts.append( "The company produces "+random.sample(di[tb[it]],1)[0] )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( "It"+random.sample(syn,1)[0]+",".join(random.sample(NT,random.randint(1,len(NT))) ) )
                ts.append( dn[tb[it]][0]+random.sample(syn,1)[0]+str(random.randint(length+1,length+5))+" products")
                ts.append( "They"+random.sample(syn,1)[0]+" less than "+str(random.randint(0,length-1))+" items" )
                ts.append( "They"+random.sample(syn,1)[0]+" more than "+str(random.randint(length+1,length+5))+" items" )
                ts.append( "The company produces "+random.sample(NT,1)[0] )
                
        else:
            ts.append(None)
        
        return ts


def Number_of_employeesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    typ = ["micro","small","medium-sized","large"]
    if(prem):
        if(di[tb[it]][0] != None):
            ne = int(re.findall("[0-9]+",di[tb[it]][0])[0])
            ps1 = [ "There are "+str(ne)+" employees in it"
                  , "It has "+str(ne)+" employees"]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            ne = int(re.findall("[0-9]+",di[tb[it]][0])[0])
            t = (typ[2] if ne<250 else typ[3])
            if(tval):
                ts.append( "There are "+str(ne)+" employees working in the company" )
                ts.append( "There are more than "+str(random.randint(ne-100,ne-50))+" employees working in "+dn[tb[it]][0] )
                ts.append( "There are less than "+str(random.randint(ne+100,ne+200))+" employees working in "+dn[tb[it]][0] )
                ts.append( "It is a "+ t +" enterprise" )
            else: # not done
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                nt = random.sample(list(set(typ)-set([t])),1)[0]
                ts.append( "There are "+str(re.findall("[0-9]+",NT)[0])+" employees working in the company" )
                ts.append( "There are less than "+str(random.randint(ne-100,ne-50))+" employees working in "+dn[tb[it]][0] )
                ts.append( "There are more than "+str(random.randint(ne+100,ne+200))+" employees working in "+dn[tb[it]][0] )
                ts.append( "It is a "+ nt +" enterprise" )                
                
        else:
            ts.append(None)
        
        return ts


def Traded_asSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "It is traded as "+All
                  , "The trading names of this company are "+All
                  , "This company is traded as "+All]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            
            if(tval):
                rr = random.sample(di[tb[it]],1)[0]
                r = rr.split(":")
                ts.append( "It is traded in "+r[0]+" as "+r[1] )
                ts.append( r[1]+" is this companies index in "+r[0] )
                ts.append( "This is traded as "+r[1]+" in "+r[0] )
                ts.append( "The company shares are named "+r[1]+" in "+r[0] )
                ts.append( "At least few people invest in "+rr )
                ts.append( "People can "+random.sample(["buy","sell"],1)[0]+" shares of "+r[1]+" from "+r[0] )
                ts.append( "Prices of "+r[1]+" can change in "+r[0] )
                ts.append( r[1]+" are the stocks of "+dn[tb[it]][0]+" in "+r[0] )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(2,4))
                rr = random.sample(NT,1)[0]
                r = rr.split(":")
                ts.append( "It is traded in "+r[0]+" as "+r[1] )
                ts.append( r[1]+" is this companies index in "+r[0] )
                ts.append( "This is traded as "+r[1]+" in "+r[0] )
                ts.append( "The company shares are named "+r[1]+" in "+r[0] )
                ts.append( "At least few people invest in "+rr )
                ts.append( "People can "+random.sample(["buy","sell"],1)[0]+" shares of "+r[1]+" from "+r[0] )
                ts.append( "Prices of "+r[1]+" can change in "+r[0] )
                ts.append( r[1]+" are the stocks of "+dn[tb[it]][0]+" in "+r[0] )
                                
        else:
            ts.append(None)
        
        return ts


def FounderSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" creators "," founding fathers "]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The founders of this company are "+All
                  , All+" founded this company"
                  , dn[tb[it]][0]+" was founded by "+All]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "It was created by "+random.sample(di[tb[it]],1)[0] )
                ts.append( All+" were the founding fathers of "+dn[tb[it]][0] )
                ts.append( "There were "+str(length)+random.sample(syn,1)[0]+"of "+dn[tb[it]][0] )
                ts.append( "More than "+str(random.randint(0,length-1))+" people"+random.sample(syn,1)[0]+"this company")
                ts.append( "Less than "+str(random.randint(length+1,length+5))+" people"+random.sample(syn,1)[0]+"this company" )
                ts.append( dn[tb[it]][0]+" was founded by "+str(length)+" people")
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( "It was created by "+random.sample(NT,1)[0] )
                ts.append( All+" were the founding fathers of "+dn[tb[it]][0] )
                ts.append( "There were "+str(random.randint(0,length-1))+random.sample(syn,1)[0]+"of "+dn[tb[it]][0] )
                ts.append( "Less than "+str(random.randint(0,length-1))+" people"+random.sample(syn,1)[0]+"this company")
                ts.append( "More than "+str(random.randint(length+1,length+5))+" people"+random.sample(syn,1)[0]+"this company" )
                ts.append( dn[tb[it]][0]+" was founded by "+str(random.randint(length+1,length+5))+" people")
                
        else:
            ts.append(None)
            
        return ts


def Area_servedSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" serves "," caters "," works "]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" are the areas served by "+dn[tb[it]][0]
                  , dn[tb[it]][0]+" serves in "+All
                  , "The services of the company are available in "+All]
        else:
            ps1= [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                if(di[tb[it]][0] != "Worldwide"):
                    ts.append( "It serves in "+str(length)+" places" )
                    ts.append( "It does not serve Worldwide" )
                    ts.append( dn[tb[it]][0]+" company"+random.sample(syn,1)[0]+"in "+All )
                    ts.append( "It"+random.sample(syn,1)[0]+"in more than "+str(random.randint(0,length-1))+" places" )
                    ts.append( "It"+random.sample(syn,1)[0]+"in less than "+str(random.randint(length+1,length+6))+" places" )
                    ts.append( "Services by this company can be accessed in "+random.sample(di[tb[it]][0],1)[0] )
                else:
                    ts.append( "It serves in everywhere in the world" )
                    ts.append( "It does serves Worldwide" )
                    ts.append( dn[tb[it]][0]+" company"+random.sample(syn,1)[0]+" "+All )
                    ts.append( "Services by this company can be accessed worldwide" )
            else:
                if(di[tb[it]][0] == "Worldwide"):
                    NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                    All = ','.join(NT)
                    ts.append( "It serves in "+str(random.randint(length+1,length+4))+" places" )
                    ts.append( "It does not serve Worldwide" )
                    ts.append( dn[tb[it]][0]+" company"+random.sample(syn,1)[0]+"in "+All )
                    ts.append( "It"+random.sample(syn,1)[0]+"in less than "+str(random.randint(0,length-1))+" places" )
                    ts.append( "Services by this company can be accessed in "+random.sample(NT,1)[0] )
                else:
                    NT = random.sample(list(set(univ)-set(di[tb[it]])-set(["Worldwide"])),random.randint(1,3))
                    All = ','.join(NT)
                    ts.append( "It serves in "+str(random.randint(length+1,length+4))+" places" )
                    ts.append( "It does not serve Worldwide" )
                    ts.append( dn[tb[it]][0]+" company"+random.sample(syn,1)[0]+"in "+All )
                    ts.append( "It"+random.sample(syn,1)[0]+"in less than "+str(random.randint(0,length-1))+" places" )
                    ts.append( "It"+random.sample(syn,1)[0]+"in more than "+str(random.randint(length+1,length+6))+" places" )
                    ts.append( "Services by this company can be accessed in "+random.sample(NT,1)[0] )
                    ts.append( "It serves in everywhere in the world" )
                    ts.append( "It does serves Worldwide" )
                    ts.append( dn[tb[it]][0]+" company"+random.sample(syn,1)[0]+" worldwide" )
                    ts.append( "Services by this company can be accessed worldwide" )
                    
        else:
            ts.append(None)
        
        return ts


def TypeSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The type of the company is "+All 
                  , All+" is the type of the company" 
                  , "The company is "+All ]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" is a "+All+" company" )
                if(re.findall("[Pp]ublic",All)):
                    ts.append( "It is a public company"  )
                    ts.append( "It is not a private company" )
                    ts.append( "General people can invest in the company" )
                    ts.append( "The company is traded in a stock market" )
                    ts.append( "The company must have a trading name" )
                if(re.findall("[Pp]rivate",All)):
                    ts.append( "It is a private company" )
                    ts.append( "It is not a public company" )
                    ts.append( "Few individuals have stake in the company" )
                    ts.append( "No public offering of the company was there" )
                    ts.append( "The company doesn't have a trading name" )
                    ts.append( "Few individuals hold majority shares in the company" )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                Alln = ','.join(NT)
                All = ','.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" is a "+Alln+" company" )
                if(re.findall("[Pp]rivate",All)):
                    ts.append( "It is a public company"  )
                    ts.append( "It is not a private company" )
                    ts.append( "General people can invest in the company" )
                    ts.append( "The company is traded in a stock market" )
                    ts.append( "The company must have a trading name" )
                if(re.findall("[Pp]ublic",All)):
                    ts.append( "It is a private company" )
                    ts.append( "It is not a public company" )
                    ts.append( "Few individuals have stake in the company" )
                    ts.append( "No public offering of the company was there" )
                    ts.append( "The company doesn't have a trading name" )
                    ts.append( "Few individuals hold majority shares in the company" )
                
        else:
            ts.append(None)
        
        return ts


def SubsidiariesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The subsidiaries of this company are "+All
                   , All+" are the subsidiaries of this company"
                   , dn[tb[it]][0]+" is a parent company of "+All ]
        else:
            ps1 = [None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( dn[tb[it]][0]+" owns "+All )
                ts.append( dn[tb[it]][0]+" owns "+str(length)+" companies" )
                ts.append( dn[tb[it]][0]+" owns less than "+str(random.randint(length+1,length+5))+" companies" )
                ts.append( dn[tb[it]][0]+" owns more than "+str(random.randint(0,length-1))+" companies" )
                ts.append( dn[tb[it]][0]+" manages "+str(length)+" companies" )
                ts.append( dn[tb[it]][0]+" is a holding company of "+random.sample(di[tb[it]],1)[0] )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts.append( dn[tb[it]][0]+" owns "+All )
                ts.append( dn[tb[it]][0]+" owns "+str(random.randint(0,length-1))+" companies" )
                ts.append( dn[tb[it]][0]+" owns less than "+str(random.randint(length+1,length+5))+" companies" )
                ts.append( dn[tb[it]][0]+" owns more than "+str(random.randint(0,length-1))+" companies" )
                ts.append( dn[tb[it]][0]+" manages "+str(random.randint(length+1,length+5))+" companies" )
                ts.append( dn[tb[it]][0]+" is a holding company of "+random.sample(NT,1)[0] )
                
        else:
            ts.append(None)
        
        return ts


def ParentSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ 'The parent of this company is '+di[tb[it]][0] 
                  , di[tb[it]][0]+" is the parent of this company" 
                  , di[tb[it]][0]+" is a parent of "+dn[tb[it]][0] ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                ts.append( di[tb[it]][0]+" owns "+dn[tb[it]][0] )
                ts.append( di[tb[it]][0]+" manages "+dn[tb[it]][0] )
                ts.append( di[tb[it]][0]+" is a holding company of "+dn[tb[it]][0] )
                ts.append( dn[tb[it]][0]+" is a subsidiary of "+di[tb[it]][0] )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( NT+" owns "+dn[tb[it]][0] )
                ts.append( NT+" manages "+dn[tb[it]][0] )
                ts.append( NT+" is a holding company of "+dn[tb[it]][0] )
                ts.append( di[tb[it]][0]+" is a subsidiary of "+dn[tb[it]][0] )
        else:
            ts.append(None)
        
        return ts


def OwnerSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ 'The owner of this company is '+di[tb[it]][0] 
                  , di[tb[it]][0]+" is the owner of this company" 
                  , di[tb[it]][0]+" is a owner of "+dn[tb[it]][0] ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                ts.append( di[tb[it]][0]+" is a parent of "+dn[tb[it]][0] )
                ts.append( di[tb[it]][0]+" manages "+dn[tb[it]][0] )
                ts.append( di[tb[it]][0]+" is a holding company of "+dn[tb[it]][0] )
                ts.append( dn[tb[it]][0]+" is a subsidiary of "+di[tb[it]][0] )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( NT+" is a parent of "+dn[tb[it]][0] )
                ts.append( NT+" manages "+dn[tb[it]][0] )
                ts.append( NT+" is a holding company of "+dn[tb[it]][0] )
                ts.append( di[tb[it]][0]+" is a subsidiary of "+dn[tb[it]][0] )
        else:
            ts.append(None)
        
        return ts


def PredecessorSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" was the predecessor company" 
                  , dn[tb[it]][0]+" used to belong to "+All ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( All+" is a predecessor of this company" )
                ts.append( "The company was previously owned by "+random.sample(di[tb[it]],1)[0] )
                ts.append( 'The company was owned by more than '+str(random.randint(0,length-1))+" companies" )
                ts.append( 'The company was owned by less than '+str(random.randint(length+1,length+5))+" companies" )
                ts.append( dn[tb[it]][0]+" was a successor company of "+random.sample(di[tb[it]],1)[0] )
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))[0]
                All = ','.join(NT)
                ts.append( All+" is a predecessor of this company" )
                ts.append( "The company was previously owned by "+random.sample(NT,1)[0] )
                ts.append( 'The company was owned by less than '+str(random.randint(0,length-1))+" companies" )
                ts.append( 'The company was owned by more than '+str(random.randint(length+1,length+5))+" companies" )
                ts.append( dn[tb[it]][0]+" was a successor company of "+random.sample(NT,1)[0] )
        else:
            ts.append(None)
        
        return ts

# 1st multi-row templates
def multi_row1(tb,dn,F,it,tval=True):
    Ua,A = F["Area_served"]
    Ufd,Fd = F["Founded"]
    Uh,H = F["Headquarters"]
    
    if(Fd[tb[it]][0] != None):
        year = int(re.findall("[0-9][0-9][0-9][0-9]" , ",".join(Fd[tb[it]]) )[0])
    
    ts = {}
    if(tval):
        if(A[tb[it]][0] != None and H[tb[it]][0] != None):
            ts["Area_served,Headquarters"] = []
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(H[tb[it]])
            ts["Area_served,Headquarters"].append( "It serves at "+Al1+" and it's head office is at "+Al2 )
        if(A[tb[it]][0] != None and Fd[tb[it]][0] != None):
            ts["Area_served,Founded"] = []
            Al1 = ",".join(A[tb[it]])
            ts["Area_served,Founded"].append( "In "+str(2020-year)+" years the company expanded to "+Al1 )
        
    else:
        if(A[tb[it]][0] != None and H[tb[it]][0] != None):
            ts["Area_served,Headquarters"] = []
            NT = random.sample(list(set(Ua)-set(A[tb[it]])),random.randint(1,5))
            Al1 = ",".join(NT)
            Al2 = ",".join(H[tb[it]])
            ts["Area_served,Headquarters"].append( "It serves at "+Al1+" and it's head office is at "+Al2 )
        if(A[tb[it]][0] != None and Fd[tb[it]][0] != None):
            ts["Area_served,Founded"] = []
            NT = random.sample(list(set(Ua)-set(A[tb[it]])),random.randint(1,3))
            Al1 = ",".join(NT)
            ts["Area_served,Founded"].append( "In "+str(random.randint(2020-year+2,2020-year+6))+" years the company expanded to "+Al1 )
        
    return ts

# 2nd multi-row templates
def multi_row2(tb,dn,Ff,it,tval=True):
    Uk,K = Ff["Key_people"]
    Un,N = Ff["Number_of_employees"]
    Uf,F = Ff["Founder"]
    Ui,I = Ff["Industry"]
    
    if(N[tb[it]][0] != None):
        ne = int(re.findall("[0-9]+",N[tb[it]][0])[0])
    
    ts = {}
    if(tval):
        if(K[tb[it]][0] != None and N[tb[it]][0] != None):
            ts["Key_people,Number_of_employees"] = []
            Al1 = ",".join(K[tb[it]])
            ts["Key_people,Number_of_employees"].append( Al1+" runs company for "+str(ne)+" employees" )
        if(K[tb[it]][0] != None and F[tb[it]][0] != None):
            ts["Key_people,Founder"] = []
            still_working = True
            for s in F[tb[it]]:
                if(re.findall(s," ".join(K[tb[it]])) ):
                    ts["Key_people,Founder"].append(s+" still plays an active role in the company")
                else:
                    still_working = False
                    ts["Key_people,Founder"].append(s+" does not play an active role in the company any more")
            if(not still_working):
                ts["Key_people,Founder"].append("The founder is no longer employed in the company")
            else:
                ts["Key_people,Founder"].append("The founder is still employed in the company")
        if(K[tb[it]][0] != None and I[tb[it]][0] != None):
            ts["Key_people,Industry"] = []
            Al1 = ",".join(random.sample(K[tb[it]],random.randint(1,len(K[tb[it]]))) )
            Al2 = ",".join(random.sample(I[tb[it]],random.randint(1,len(I[tb[it]]))) )
            ts["Key_people,Industry"].append( Al1+" works in the "+Al2 )
        if(F[tb[it]][0] != None and I[tb[it]][0] != None):
            ts["Founder,Industry"] = []
            Al1 = ",".join(random.sample(F[tb[it]],random.randint(1,len(F[tb[it]]))) )
            Al2 = ",".join(random.sample(I[tb[it]],random.randint(1,len(I[tb[it]]))) )
            ts["Founder,Industry"].append( Al1+" works in the "+Al2 )
        
    else:
        if(K[tb[it]][0] != None and N[tb[it]][0] != None):
            ts["Key_people,Number_of_employees"] = []
            NK = random.sample(list(set(Uk)-set(K[tb[it]])),random.randint(1,3))
            Al1 = ",".join(NK)
            ts["Key_people,Number_of_employees"].append( Al1+" runs company for "+str(ne)+" employees" )
        if(K[tb[it]][0] != None and F[tb[it]][0] != None):
            ts["Key_people,Founder"] = []
            still_working = True
            for s in F[tb[it]]:
                if(not re.findall(s," ".join(K[tb[it]])) ):
                    ts["Key_people,Founder"].append(s+" still plays an active role in the company")
                else:
                    still_working = False
                    ts["Key_people,Founder"].append(s+" does not play an active role in the company any more")
            if(not still_working):
                ts["Key_people,Founder"].append("The founder is no longer employed in the company")
            else:
                ts["Key_people,Founder"].append("The founder is still employed in the company")
                
        if(K[tb[it]][0] != None and I[tb[it]][0] != None):
            ts["Key_people,Industry"] = []
            NK = random.sample(list(set(Uk)-set(K[tb[it]])),random.randint(1,4))
            NI = random.sample(list(set(Ui)-set(I[tb[it]])),random.randint(1,2))
            Al1 = ",".join(random.sample(NK,random.randint(1,len(NK))) )
            Al2 = ",".join(random.sample(NI,random.randint(1,len(NI))) )
            ts["Key_people,Industry"].append( Al1+" works in the "+Al2 )
        if(F[tb[it]][0] != None and I[tb[it]][0] != None):
            ts["Founder,Industry"] = []
            NF = random.sample(list(set(Uf)-set(F[tb[it]])),random.randint(1,4))
            NI = random.sample(list(set(Ui)-set(I[tb[it]])),random.randint(1,2))
            Al1 = ",".join(random.sample(NF,random.randint(1,len(NF))) )
            Al2 = ",".join(random.sample(NI,random.randint(1,len(NI))) )
            ts["Founder,Industry"].append( Al1+" works in the "+Al2 )
        
    return ts

# 3rd multi-row templates
def multi_row3(tb,dn,F,it,tval=True):
    Up,P = F["Products"]
    Ui,I = F["Industry"]
    Upt,Pt = F["Parent"]
    Upd,Pd = F["Predecessor"]
    
    ts = {}
    if(tval):
        if(P[tb[it]][0] != None and I[tb[it]][0] != None):
            ts["Products,Industry"] = []
            Al1 = ",".join(random.sample(P[tb[it]],random.randint(1,len(P[tb[it]]))) )
            Al2 = ",".join(random.sample(I[tb[it]],random.randint(1,len(I[tb[it]]))) )
            ts["Products,Industry"].append( Al1+" products are made in "+Al2+" industry" )
        if(Pt[tb[it]][0] != None and Pd[tb[it]][0] != None):
            ts["Parent,Predecessor"] = []
            ts["Parent,Predecessor"].append( dn[tb[it]][0]+" is a stand alone company" )
        
    else:
        if(P[tb[it]][0] != None and I[tb[it]][0] != None):
            ts["Products,Industry"] = []
            NP = random.sample(list(set(Up)-set(P[tb[it]])),random.randint(1,4))
            Al1 = ",".join(random.sample(NP,random.randint(1,len(NP))) )
            Al2 = ",".join(random.sample(I[tb[it]],random.randint(1,len(I[tb[it]]))) )
            ts["Products,Industry"].append( Al1+" products are made in "+Al2+" industry" )
        if(Pt[tb[it]][0] != None and Pd[tb[it]][0] != None):
            ts["Parent,Predecessor"] = []
            ts["Parent,Predecessor"].append( dn[tb[it]][0]+" is not a stand alone company" )
        
    return ts