import time
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


table_index = np.array(category_map[category_map.category.isin(['Book'])].table_id)


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys =[i.text for i in soup.find('tr').find_all('th')]
    vals = []
    for i in soup.find('tr').find_all('td'):
        result = [val.text.strip().replace("\n", "").replace("\t", "") for val in i.find_all('li')]
        if not result:
            if(i.find('br')):
                for x in i.findAll('br'):
                    x.replace_with(',')
                result = i.text.split(',')
            elif "â€“" in i.text:
                result = [val.strip().replace("\n", "").replace("\t", "") for val in i.text.split("â€“")]
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
    for n in range(51):
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


def get_Publisher(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Publisher"
    for n in range(51):
        if(int(table_index[n][1:]) <= 2800 ):
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
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Schedule(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Schedule"
    for n in range(51):
        if(int(table_index[n][1:]) <= 2800 ):
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
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d        


def get_Format(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Format"
    for n in range(51):
        if(int(table_index[n][1:]) <= 2800 ):
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
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d        


def get_Genre(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Genre"
    for n in range(51):
        if(int(table_index[n][1:]) <= 2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].strip().lower())
                        d[dictionary['Tablename']].append(dictionary[k][i].strip().lower())
                elif(len(dictionary[k].split(','))>1):
                    for i in range(len(dictionary[k].split(','))):
                        u.add(dictionary[k].split(',')[i].strip().lower())
                        d[dictionary['Tablename']].append(dictionary[k].split(',')[i].strip().lower())
                else:
                    u.add(dictionary[k].strip().lower())
                    d[dictionary['Tablename']].append(dictionary[k].strip().lower())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
        
    if(fake):
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Publication_date(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Publication date"
    for n in range(51):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace('\xa0',' '))
                        d[dictionary['Tablename']].append(dictionary[k][i].replace('\xa0',' '))
                else:
                    u.add(dictionary[k].replace('\xa0',' '))
                    d[dictionary['Tablename']].append(dictionary[k].replace('\xa0',' '))
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
        
    if(fake):
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_No_of_issues(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "No. of issues"
    for n in range(51):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    r = re.findall("[0-9]+",",".join(dictionary[k])) 
                    s = 0
                    for i in range(len(r)):
                        s += int(r[i])     
                    u.add(s)
                    d[dictionary['Tablename']].append(s)
                else:
                    r = re.findall("[0-9]+",dictionary[k])
                    s = 0
                    for i in range(len(r)):
                        s += int(r[i])
                    u.add(s)
                    d[dictionary['Tablename']].append(s)
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
        
    if(fake):
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"]["No_of_issues"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Main_character(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Main character(s)"
    for n in range(51):
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
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"]["Main_character"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Written_by(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Written by"
    for n in range(51):
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
        for it in range(51): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Book"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


# Extract all data :

def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Publisher","Schedule","Format","Genre","Publication_date"
                           ,"No_of_issues","Main_character","Written_by"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data

# Sentence generator :

def PublisherSent(tb,dn,F,it,tval = True,prem = False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ",".join(di[tb[it]])
            ps1 = [ "The name of the book is "+dn[tb[it]][0]+"and it was published by "+All
                   , All+" published ,The book named "+dn[tb[it]][0]
                   , "The book named"+dn[tb[it]][0]+" was published by "+All ]
        else:
            ps1=[None]
        return ps1
    
    else:
        if(di[tb[it]][0]!= None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts1 = [dn[tb[it]][0] + " was published by " + All
                    ,All + " is the publisher of the " + dn[tb[it]][0]]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                All = ','.join(NT)
                ts1 = [ dn[tb[it]][0] + " was published by " + All
                    ,All + " is the publisher of the " + dn[tb[it]][0] ]
        else:
            ts1 = [None]
    
        return ts1


def ScheduleSent(tb,dn,F,it,tval = True,prem = False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "It used to be published "+All 
                   , All+" an issue of this book was published"
                   , "An issue used to be published "+All ]
        else:
            ps1=[None]
            
        return ps1
    
    else:
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts1 = [ dn[tb[it]][0] + " was published " + All
                    ,dn[tb[it]][0]+ " is a " + All + " book"]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                All = ','.join(NT)
                ts1 = [dn[tb[it]][0] + " was published " + All
                    ,dn[tb[it]][0]+ " is a " + All + " book"]
        else:
            ts1=[None]
    return ts1


def FormatSent(tb,dn,F,it,tval = True,prem = False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "It is a "+All , dn[tb[it]][0]+" was a "+All ]
        else:
            ps1 = [None]
            
        return ps1
    
    else:
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts1 = [dn[tb[it]][0] + " is a " + All]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                All = ','.join(NT)
                ts1 = [dn[tb[it]][0] + " is a " + All]
        else:
            ts1 = [None]
        return ts1


def GenreSent(tb,dn,F,it,tval = True,prem = False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["It falls in "+All+" category"
                   ,"This book is of "+All+" genre"
                   ,dn[tb[it]][0]+" is of "+All+" genre" ]
        else:
            ps1=[None]
            
        return ps1
    else:
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts1 = [dn[tb[it]][0] + " falls in the genres of " + All
                    ,dn[tb[it]][0] + " is a " + random.sample(di[tb[it]],1)[0] +" book"
                    ,dn[tb[it]][0] + " falls into "+ str(len(di[tb[it]])) + " category"]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                All = ','.join(NT)
                ts1 = [dn[tb[it]][0] + " falls in the genres of " + All
                    ,dn[tb[it]][0] + " is a " + random.sample(NT,1)[0] +" book"
                    ,dn[tb[it]][0] + " falls into "+ str(len(NT)) + " category"]
        else:
            ts1=[None]

        return ts1


def Publication_dateSent(tb,dn,F,it,tval = True,prem = False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = ["This book was published in "+ ",".join(di[tb[it]])]
        else:
            ps1=[None]
            
        return ps1
    
    else:
        if(di[tb[it]][0] != None):
            if(tval):
                ts1 = [dn[tb[it]][0] + " was published from " + random.sample(di[tb[it]],1)[0]
                    ,dn[tb[it]][0] + " was published in year " + re.findall("[0-9][0-9]+",random.sample(di[tb[it]],1)[0])[0]
                    ,dn[tb[it]][0]+" was published before "+str(int(re.findall("[0-9][0-9]+",random.sample(di[tb[it]],1)[0])[-1])+3)
                    ,dn[tb[it]][0]+" was published after "+str(int(re.findall("[0-9][0-9]+",random.sample(di[tb[it]],1)[0])[0])-2)]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts1 = [dn[tb[it]][0] + " was published from " + NT[0]
                    ,dn[tb[it]][0] + " was published in year " + re.findall("[0-9][0-9]+",NT[0])[0]
                    ,dn[tb[it]][0]+" was published after "+str(int(re.findall("[0-9][0-9]+",random.sample(di[tb[it]],1)[0])[-1])+3)
                    ,dn[tb[it]][0]+" was published before "+str(int(re.findall("[0-9][0-9]+",random.sample(di[tb[it]],1)[0])[0])-2)]
        else:
            ts1 = [None]
        return ts1


def No_of_issuesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            ps1 = [ "The no. of issues of the book is "+str(di[tb[it]][0])
                  , "The book has "+str(di[tb[it]][0])+" issues"]
        else:
            ps1=[None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                ts.append(dn[tb[it]][0]+" had "+str(di[tb[it]][0])+" issues" )
                ts.append(dn[tb[it]][0]+" had more than "+str(random.randint(0,di[tb[it]][0]-1))+" issues")
                ts.append(dn[tb[it]][0]+" had less than "+str(random.randint(di[tb[it]][0]+2,di[tb[it]][0]+15))+" issues")
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts.append(dn[tb[it]][0]+" had "+str(random.randint(di[tb[it]][0]+2,di[tb[it]][0]+15))+" issues" )
                ts.append(dn[tb[it]][0]+" had less than "+str(random.randint(0,di[tb[it]][0]-1))+" issues")
                ts.append(dn[tb[it]][0]+" had more than "+str(random.randint(di[tb[it]][0]+2,di[tb[it]][0]+15))+" issues")
        else:
            ts.append(None)
        
        return ts


def Main_characterSent(tb,dn,F,it,tval = True,prem = False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ",".join(di[tb[it]])
            ps1 =['The main characters of this book are '+All , All+"are the main characters of the book"] 
        else:
            ps1=[None]
        return ps1
    
    else:
        if(di[tb[it]][0] != None):
            if(tval):
                ts1 = [random.sample(di[tb[it]],1)[0] + " was a main character in " + dn[tb[it]][0]
                ,random.sample(di[tb[it]],1)[0] + " was a character in the book"
                ,"There are "+str(len(di[tb[it]])) + " characters in the book"
                ,"The book has more than "+str(len(di[tb[it]])-random.randint(1,len(di[tb[it]])))+" characters"
                ,"The book has less than "+str(len(di[tb[it]])+random.randint(1,4))+" characters"]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,3))
                ts1 = [random.sample(NT,1)[0] + " was a main character in " + dn[tb[it]][0]
                ,random.sample(NT,1)[0] + " was a character in the book"
                ,"There are "+str(len(NT)) + " characters in the book"
                ,"The book has less than "+str(len(di[tb[it]])-random.randint(1,len(di[tb[it]])))+" characters"
                ,"The book has more than "+str(len(di[tb[it]])+random.randint(1,4))+" characters"]
        else:
            ts1 = [None]
        return ts1


def Written_bySent(tb,dn,F,it,tval = True,prem = False):
    di = F[1]
    univ = F[0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ",".join(di[tb[it]])
            ps1 =["The book was written by "+All,All+"wrote the book "+dn[tb[it]][0]] 
        else:
            ps1=[None]
        return ps1
    
    else:
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts1 = ["The book was authored by "+All
                ,All+" authored the book"
                ,"The book is by "+random.sample(di[tb[it]],1)[0]
                ,random.sample(di[tb[it]],1)[0]+" is the author of "+dn[tb[it]][0] ]
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                All = ','.join(NT)
                ts1 = ["The book was authored by "+All
                ,All+" authored the book"
                ,"The book is by "+random.sample(NT,1)[0]
                ,random.sample(NT,1)[0]+" is the author of "+dn[tb[it]][0] ]
        else:
            ts1=[None]
        
        return ts1    

# 1st multi-row templates
def multi_row1(tb,dn,F,it,tval=True):
    Ug,G = F["Genre"]
    Up,P = F["Publisher"]
    Uni,Ni = F["No_of_issues"]

    ts = {}
    
    if(tval):
        if(P[tb[it]][0]!= None and G[tb[it]][0] != None):
            ts["Publisher,Genre"] = []
            Al1 = ",".join(P[tb[it]])
            Al2 = ",".join(random.sample(G[tb[it]],random.randint(1,len(G[tb[it]])) ) )
            ts["Publisher,Genre"].append(Al1+" publishes in "+Al2+" genres")
        if(Ni[tb[it]][0]!= None and G[tb[it]][0] != None):
            ts["No_of_issues,Genre"] = []
            Al2 = ",".join(random.sample(G[tb[it]],random.randint(1,len(G[tb[it]])) ) )
            ts["No_of_issues,Genre"].append(str(Ni[tb[it]][0])+" number of issues in "+Al2+"genres")
            ts["No_of_issues,Genre"].append("There are "+("more" if (Ni[tb[it]][0]>len(G[tb[it]])) else "less") +" number of issues than genres")
            
    else:
        if(P[tb[it]][0]!= None and G[tb[it]][0] != None):
            ts["Publisher,Genre"] = []
            Al1 = ",".join(P[tb[it]])
            NT = random.sample(list(set(Ug)-set(G[tb[it]])),random.randint(3,5))
            Al2 = ",".join(random.sample(NT,random.randint(1,len(NT)) ) )
            ts["Publisher,Genre"].append(Al1+" publishes in "+Al2+" genres")
        if(Ni[tb[it]][0]!= None and G[tb[it]][0] != None):
            ts["No_of_issues,Genre"] = []
            Al2 = ",".join(random.sample(G[tb[it]],random.randint(1,len(G[tb[it]])) ) )
            ts["No_of_issues,Genre"].append(str(random.randint(Ni[tb[it]][0]+1,Ni[tb[it]][0]+10))+" number of issues in "+Al2+"genres")
            ts["No_of_issues,Genre"].append("There are "+("more" if (Ni[tb[it]][0]<len(G[tb[it]])) else "less") +" number of issues than genres")
        
    return ts

# 2nd multi-row templates
def multi_row2(tb,dn,F1,it,tval=True):
    Uw,W = F1["Written_by"]
    Us,S = F1["Schedule"]
    Up,P = F1["Publisher"]
    Uf,F = F1["Format"]
    
    ts = {}
    if(tval):
        if(P[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Publisher,Schedule"] = []
            ts["Publisher,Schedule"].append( ",".join(P[tb[it]])+" publishes "+",".join(S[tb[it]]) )
        if(P[tb[it]][0] != None and F[tb[it]][0] != None):
            ts["Publisher,Format"] = []
            ts["Publisher,Format"].append( ",".join(P[tb[it]])+" publishes in "+F[tb[it]][0]+" format" )
        if(W[tb[it]][0] != None and F[tb[it]][0] != None):
            ts["Written_by,Format"] = []
            ts["Written_by,Format"].append( ",".join(W[tb[it]])+" writes in "+F[tb[it]][0]+ " format" )
    else:
        if(P[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Publisher,Schedule"] = []
            NP = random.sample(list(set(Up)-set(P[tb[it]])),random.randint(1,2))
            NS = random.sample(list(set(Us)-set(S[tb[it]])),1)
            ts["Publisher,Schedule"].append( ",".join(P[tb[it]])+" publishes "+",".join(NS) )
        if(P[tb[it]][0] != None and F[tb[it]][0] != None):
            ts["Publisher,Format"] = []
            NP = random.sample(list(set(Up)-set(P[tb[it]])),random.randint(1,2))
            NF = random.sample(list(set(Uf)-set(F[tb[it]])),1)
            ts["Publisher,Format"].append( ",".join(NP)+" publishes in "+F[tb[it]][0]+" format" )
        if(W[tb[it]][0] != None and F[tb[it]][0] != None):
            ts["Written_by,Format"] = []
            NW = random.sample(list(set(Uw)-set(W[tb[it]])),random.randint(1,2))
            NF = random.sample(list(set(Uf)-set(F[tb[it]])),1)
            ts["Written_by,Format"].append( ",".join(NW)+" writes in "+NF[0]+ " format" )
    return ts

# 3rd multi-row templates
def multi_row3(tb,dn,F,it,tval=True):
    Uw,W = F["Written_by"]
    Um,M = F["Main_character"]
    Up,P = F["Publisher"]
    Us,S = F["Schedule"]
    
    ts = {}
    if(tval):
        if(M[tb[it]][0] != None and W[tb[it]][0] != None):
            ts["Main_character,Written_by"] = []
            Al1 = ",".join(M[tb[it]])
            Al2 = ",".join(W[tb[it]])
            ts["Main_character,Written_by"].append("Book about "+Al1+" was written by "+Al2)
        if(M[tb[it]][0] != None and P[tb[it]][0] != None):
            ts["Main_character,Publisher"] = []
            Al1 = ",".join(M[tb[it]])
            Al2 = ",".join(P[tb[it]])
            ts["Main_character,Publisher"].append("Book about "+Al1+" is published by "+Al2)
        if(M[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Main_character,Schedule"] = []
            Al1 = ",".join(M[tb[it]])
            Al2 = ",".join(S[tb[it]])
            ts["Main_character,Schedule"].append("Book about "+Al1+" is published "+Al2)
        
    else:
        if(M[tb[it]][0] != None and W[tb[it]][0] != None):
            ts["Main_character,Written_by"] = []
            NM = random.sample(list(set(Um)-set(M[tb[it]])),random.randint(1,3))
            NW = random.sample(list(set(Uw)-set(W[tb[it]])),random.randint(1,2))
            Al1 = ",".join(NM)
            Al2 = ",".join(W[tb[it]])
            ts["Main_character,Written_by"].append("Book about "+Al1+" was written by "+Al2)
        if(M[tb[it]][0] != None and P[tb[it]][0] != None):
            ts["Main_character,Publisher"] = []
            NM = random.sample(list(set(Um)-set(M[tb[it]])),random.randint(1,3))
            NP = random.sample(list(set(Up)-set(P[tb[it]])),1)
            Al1 = ",".join(NM)
            Al2 = ",".join(P[tb[it]])
            ts["Main_character,Publisher"].append("Book about "+Al1+" is published by "+Al2)
        if(M[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Main_character,Schedule"] = []
            NM = random.sample(list(set(Um)-set(M[tb[it]])),random.randint(1,3))
            NS = random.sample(list(set(Us)-set(S[tb[it]])),1)
            Al1 = ",".join(M[tb[it]])
            Al2 = ",".join(NS)
            ts["Main_character,Schedule"].append("Book about "+Al1+" is published "+Al2)
        
    return ts

# 4th multi-row templates
def multi_row4(tb,dn,F,it,tval=True):
    Uw,W = F["Written_by"]
    Upd,Pd = F["Publication_date"]
    
    ts = {}
    if(tval):
        if(W[tb[it]][0] != None and Pd[tb[it]][0] != None):
            ts["Written_by,Publication_date"] = []
            Al1 = ",".join(Pd[tb[it]])
            Al2 = ",".join(W[tb[it]])
            ts["Written_by,Publication_date"].append(Al2+" was alive on "+Al1)
        
    else:
        if(W[tb[it]][0] != None and Pd[tb[it]][0] != None):
            ts["Written_by,Publication_date"] = []
            NW = random.sample(list(set(Uw)-set(W[tb[it]])),random.randint(1,2))
            NPd = random.sample(list(set(Upd)-set(Pd[tb[it]])),1)
            Al1 = ",".join(NPd)
            Al2 = ",".join(W[tb[it]])
            ts["Written_by,Publication_date"].append(Al2+" was alive on "+Al1)
        
    return ts