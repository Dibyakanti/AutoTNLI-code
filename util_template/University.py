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


table_index = np.array(category_map[category_map.category.isin(['University'])].table_id)


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
    for n in range(37):
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


'''
fake : represent if we have to make a fake dictionary or not
it : selected which index to create the fake for
sel : select whether to add/modify/delete
'''
def get_Website(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    udom = set(["com","in","edu","co","uk"])
    dom = {}
    k = "Website"
    for n in range(37):
        if(int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            d[dictionary['Tablename']] = []
            dom[dictionary["Tablename"]] = []
            if(k in dictionary.keys()):
                u.add(dictionary[k])
                d[dictionary['Tablename']].append(dictionary[k])
                if(len(dictionary[k].split("."))>3):
                    for i in range(2,len(dictionary[k].split("."))):
                        dom[dictionary["Tablename"]].append(dictionary[k].split(".")[i])
                else:
                    dom[dictionary["Tablename"]].append(dictionary[k].split(".")[-1])
            else:
                d[dictionary['Tablename']].append(None)
                dom[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(dom[T[it]])<2):
                sel = 1
            dom = FakeDICT(T,N,udom,dom,it,sel)
        
    return list(u),d,dom


def get_Type(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Type"
    for n in range(37):
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
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Established(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Established"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    r = " ".join(dictionary[k].replace("\xa0"," "))
                    y = re.findall("[0-9][0-9][0-9][0-9]",r)[0]
                    u.add(y)
                    d[dictionary['Tablename']].append(y)
                else:
                    r = dictionary[k].replace("\xa0"," ")
                    y = re.findall("[0-9][0-9][0-9][0-9]",r)[0]
                    u.add(y)
                    d[dictionary['Tablename']].append(y)
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Undergraduates(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Undergraduates"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
    
                r = dictionary[k]
                n = re.findall("[0-9,]+",r)[0]
                u.add(n.replace(",",""))
                d[dictionary['Tablename']].append(n.replace(",",""))
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Postgraduates(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Postgraduates"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
    
                r = dictionary[k]
                n = re.findall("[0-9,]+",r)[0]
                u.add(n.replace(",",""))
                d[dictionary['Tablename']].append(n.replace(",",""))
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Motto(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k1 = "Motto"
    k2 = "Motto in English"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            d[dictionary['Tablename']] = []
            if(k1 in dictionary.keys()):
                if(type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i])
                        d[dictionary['Tablename']].append(dictionary[k1][i])
                else:
                    u.add(dictionary[k1])
                    d[dictionary['Tablename']].append(dictionary[k1])
            if(k2 in dictionary.keys()):
                if(type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i])
                        d[dictionary['Tablename']].append(dictionary[k2][i])
                else:
                    u.add(dictionary[k2])
                    d[dictionary['Tablename']].append(dictionary[k2])
                    
            if(k1 not in dictionary.keys() and k2 not in dictionary.keys()):
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"]["Motto"],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Location(T,N,fake=False,sel=0):
    ul,uc = set([]),set([])
    dl,dc = {},{}
    k = "Location"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                dc[dictionary['Tablename']] = []
                dl[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    r = " ".join(dictionary[k]).replace("\ufeff","")
                    c = re.findall("[A-Za-z]+.[:].+",r)
                    p = re.findall("[A-Za-z,.][A-Za-z,.]+",r)
                    if(not c):
                        p = " ".join(p)
                        dc[dictionary['Tablename']].append(None)
                    else:
                        p = " ".join(p[:-1])[:-1]
                        uc.add(c[0])
                        dc[dictionary['Tablename']].append(c[0])
                    ul.add(p)
                    dl[dictionary['Tablename']].append(p)

                else:
                    r = dictionary[k].replace("\ufeff","")
                    c = re.findall("[A-Za-z]+.[:].+",r)
                    p = re.findall("[A-Za-z,.][A-Za-z,.]+",r)
                    if(not c):
                        p = " ".join(p)
                        dc[dictionary['Tablename']].append(None)
                    else:
                        p = " ".join(p[:-1])[:-1]
                        uc.add(c[0])
                        dc[dictionary['Tablename']].append(c[0])
                    ul.add(p)
                    dl[dictionary['Tablename']].append(p)
                    
            else:
                dc[dictionary['Tablename']] = []
                dc[dictionary['Tablename']].append(None)
                dl[dictionary['Tablename']] = []
                dl[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(dc[T[it]])<2):
                sel = 1
            dc = FakeDICT(T,N,uc,dc,it,sel)
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(dl[T[it]])<2):
                sel = 1
            dl = FakeDICT(T,N,ul,dl,it,sel)
    
    return list(uc),list(ul),dl,dc


def get_Nickname(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Nickname"
    for n in range(37):
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
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Campus(T,N,fake=False,sel=0):
    u1 = set([])
    u2 = set([])
    d1 = {}
    d2 = {}
    k = "Campus"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d1[dictionary['Tablename']] = []
                d2[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    r = ",".join(dictionary[k]).replace("\xa0"," ")
                    a = re.findall("[0-9][0-9,.]+.[A-Za-z2]+",r)
                    b = re.findall("[A-Za-z]+urban",r)
                    if(len(a)!=0):
                        for i in range(2):
                            d1[dictionary['Tablename']].append(a[i])
                            u1.add(a[i])
                    if(len(b) != 0):
                        for i in b:
                            d2[dictionary['Tablename']].append(i.lower())
                            u2.add(i.lower())
                else:
                    r = dictionary[k].replace("\xa0"," ")
                    a = re.findall("[0-9][0-9,.]+.[A-Za-z2]+",r)
                    b = re.findall("[A-Za-z]+rban",r)
                    if(len(a)!=0):
                        l = min(len(a),2)
                        for i in range(l):
                            d1[dictionary['Tablename']].append(a[i])
                            u1.add(a[i])
                    if(len(b) != 0):
                        for i in b:
                            d2[dictionary['Tablename']].append(i.lower())
                            u2.add(i.lower())
                if(len(d2[dictionary['Tablename']])<1):
                    d2[dictionary['Tablename']].append(None)
                if(len(d1[dictionary['Tablename']])<1):
                    d1[dictionary['Tablename']].append(None)
        
            else:
                d1[dictionary['Tablename']] = []
                d1[dictionary['Tablename']].append(None)
                d2[dictionary['Tablename']] = []
                d2[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d1[T[it]])<2):
                sel = 1
            d1 = FakeDICT(T,N,u1,d1,it,sel)
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d2[T[it]])<2):
                sel = 1
            if(len(d2[T[it]])==1):
                d2 = FakeDICT(T,N,u2,d2,it,1)
            elif(len(d2[T[it]])==0):
                d2[T[it]].append(None)
                d2 = FakeDICT(T,N,u2,d2,it,0)
            else:
                d2 = FakeDICT(T,N,u2,d2,it,2)
            
    return list(u1),list(u2),d1,d2


def get_Colors(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Colors"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace(",","").replace("\xa0","").replace("and",",").lower())
                        d[dictionary['Tablename']].append(dictionary[k][i].replace(",","").replace("\xa0","").replace("and",",").lower()) 
                else:
                    
                    r = dictionary[k].replace(",","").replace("\xa0","").replace("and",",").lower()
                    for i in r.split(","):
                        u.add(i.strip())
                        d[dictionary['Tablename']].append(i.strip())

                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Students(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Students"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                r = dictionary[k]
                n = re.findall("[0-9,]+",r)[0]
                u.add(n.replace(",",""))
                d[dictionary['Tablename']].append(n.replace(",",""))
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Academic_staff(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Academic staff"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    r = " ".join(dictionary[k])
                    n = re.findall("[0-9,]+",r)[0]
                    u.add(n.replace(",",""))
                    d[dictionary['Tablename']].append(n.replace(",",""))

                else:
                    r = dictionary[k]
                    n = re.findall("[0-9,]+",r)[0]
                    u.add(n.replace(",",""))
                    d[dictionary['Tablename']].append(n.replace(",",""))

                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Administrative_staff(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Administrative staff"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    r = " ".join(dictionary[k])
                    n = re.findall("[0-9,]+",r)[0]
                    u.add(n.replace(",",""))
                    d[dictionary['Tablename']].append(n.replace(",",""))

                else:
                    r = dictionary[k]
                    n = re.findall("[0-9,]+",r)[0]
                    u.add(n.replace(",",""))
                    d[dictionary['Tablename']].append(n.replace(",",""))

                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_President(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "President"
    for n in range(37):
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
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Endowment(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Endowment"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                r = dictionary[k]
                m = re.findall("\$[0-9.]+.[a-z]illion",r)
                if(not m):
                    d[dictionary['Tablename']].append(dictionary[k])
                else:
                    u.add(m[0])
                    d[dictionary['Tablename']].append(m[0])
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Mascot(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Mascot"
    for n in range(37):
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
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Provost(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Provost"
    for n in range(37):
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
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Sporting_affiliations(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Sporting affiliations"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k].replace("\xa0"," "))
                    d[dictionary['Tablename']].append(dictionary[k].replace("\xa0"," "))
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Academic_affiliations(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Academic affiliations"
    for n in range(37):
        if(int(table_index[n][1:]) <=2800 ):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if(k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if(type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k].replace("\xa0"," "))
                    d[dictionary['Tablename']].append(dictionary[k].replace("\xa0"," "))
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d


def get_Former_names(T,N,fake=False,sel=0):
    u = set([])
    d = {}
    k = "Former names"
    for n in range(37):
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
                        u.add(dictionary[k].split(",")[i].replace("\xa0"," ").strip())
                        d[dictionary['Tablename']].append(dictionary[k].split(",")[i].replace("\xa0"," ").strip())
                    
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if(fake):
        for it in range(37): # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["University"][k.replace(" ","_")],1)[0]
            if(sel==2 and len(d[T[it]])<2):
                sel = 1
            d = FakeDICT(T,N,u,d,it,sel)
        
    return list(u),d

# Extract all data :

def get_Data(fake=False):
    
    Extracted_data = {}
    Keys=["Website","Type","Established","Undergraduates","Postgraduates","Motto","Location"
      ,"Nickname","Campus","Colors","Students","Academic_staff","Administrative_staff","President","Endowment","Mascot"
      ,"Provost","Sporting_affiliations","Academic_affiliations","Former_names"]
    for k in Keys:
        Extracted_data[k]=[]
        for l in eval("get_"+k)(T,N,fake):
            Extracted_data[k].append(l)
            
    return Extracted_data

# Sentence generator :

def WebsiteSent(tb,dn,F,it,tval=True,prem=False):
    dom = F[2]
    di = F[1]
    univ = F[0]
    syn = [" university"," college"]
    udom = ["in","edu","com","co","uk"]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None and dom[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" is this"+random.sample(syn,1)[0]+"'s website",
                    "This"+random.sample(syn,1)[0]+" has a website named "+All,
                    All+" is "+Nm+"'s website"]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None and dom[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The"+random.sample(syn,1)[0]+" "+Nm+" has the website "+All )
                ts.append( "The website has domain name "+random.sample(dom[tb[it]],1)[0] )
                ts.append( "Information about the faculty or student could be found at "+All )
                ts.append( "You can see the faculty or student profile of university "+Nm+" at "+All )
                ts.append( "Admission info about the college could be found at "+All )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ND = random.sample(list(set(udom)-set(dom[tb[it]])),1)
                All = ','.join(NT)
                ts.append( "The"+random.sample(syn,1)[0]+" "+Nm+" has the website "+All )
                ts.append( "The website has domain name "+random.sample(ND,1)[0] )
                ts.append( "Information about the faculty or student could be found at "+All )
                ts.append( "You can see the faculty or student profile of university "+Nm+" at "+All )
                ts.append( "Admission info about the college could be found at "+All )
                
        else:
            ts.append(None)
            
        return ts


def TypeSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" are the types of this university"
                  , "The university is of "+All+" type"]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is a "+",".join(random.sample(di[tb[it]],random.randint(1,length)))+" university" )
                if(re.findall("public",All)):
                    ts.append( Nm+" is a state-funded university" )
                else:
                    ts.append( Nm+" is not a state-funded university" )
                if(re.findall("private",All)):
                    ts.append( Nm+" is a self-funded university" )
                else:
                    ts.append( Nm+" is not a self-funded university" )
                ts.append( Nm+" belongs to "+str(length)+" categories" )
                ts.append( "This university belongs to more than "+str(random.randint(0,length-1))+" categories" )
                ts.append( "This university belongs to less than "+str(random.randint(length+1,length+5))+" categories" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(2,4))
                nlen = len(NT)
                All = ','.join(NT)
                ts.append( Nm+" is a "+",".join(random.sample(NT,random.randint(1,nlen)))+" university" )
                if(re.findall("private",All)):
                    ts.append( Nm+" is a state-funded university" )
                else:
                    ts.append( Nm+" is not a state-funded university" )
                if(re.findall("public",All)):
                    ts.append( Nm+" is a self-funded university" )
                else:
                    ts.append( Nm+" is not a self-funded university" )
                ts.append( Nm+" belongs to "+str(random.randint(length+1,length+5))+" categories" )
                ts.append( "This university belongs to less than "+str(random.randint(1,length))+" categories" )
                ts.append( "This university belongs to more than "+str(random.randint(length,length+5))+" categories" )
                
        else:
            ts.append(None)
            
        return ts


def EstablishedSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" founded "," formed "]
    jub = {25:" Silver ",40:" Ruby ",50:" Gold ",60:" Diamond ",65:" Sapphire ",70:" Platinum ",75:" Palladium "
           ,100:" Centennial ",125:" Quasquicentennial ",150:" Sesquicentennial ",175:" Dodransbicentennial ",200:" Bicentennial "}
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The university was established in "+All
                  , All+" is when this university was established"
                  , Nm+" was established in "+All ]
        else:
            ps1=[None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            year = int(di[tb[it]][0])
            length = len(di[tb[it]])
            if(tval):
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"in "+str(year) )
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"before "+str(random.randint(year+10,2020)) )
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"after "+str(random.randint(year-100,year-10)) )
                ts.append( Nm+" is "+str(2020-year)+' year old university' )
                ts.append( "The founding stone of the university was laid in "+str(year))
                for i in jub.keys():
                    if(year+i<=2020):
                        ts.append(Nm+" celebrated it's "+jub[i]+"jubilee on "+str(year+i))
                    else:
                        ts.append(Nm+" will celebrate it's "+jub[i]+"jubilee on "+str(year+i))
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"in "+NT[0] )
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"after "+str(random.randint(year+10,2020)) )
                ts.append( Nm+" was"+random.sample(syn,1)[0]+"before "+str(random.randint(year-100,year-10)) )
                ts.append( Nm+" is "+str(2020-int(NT[0]))+' year old university' )
                ts.append( "The founding stone of the university was laid in "+NT[0])
                year = int(NT[0])
                for i in jub.keys():
                    if(year+i<=2020):
                        ts.append(Nm+" celebrated it's "+jub[i]+"jubilee on "+str(year+i))
                    else:
                        ts.append(Nm+" will celebrate it's "+jub[i]+"jubilee on "+str(year+i))
                
                
        else:
            ts.append(None)
            
        return ts


def UndergraduatesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ 'There are '+di[tb[it]][0]+' undergraduate students in '+Nm ]
        else:
            ps1=[None]
            
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            num = int(di[tb[it]][0])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( str(num)+" bachelor students studied from this university" )
                ts.append( str(num)+" students are enrolled in the bachelor's program" )
                ts.append( "There are "+str(num)+" undergraduate students on campus every year" )
                ts.append( "There are more than "+str(random.randint(num-80,num-50))+" undergraduate students on campus every year" )
                ts.append( "There are less than "+str(random.randint(num+50,num+100))+" undergraduate students on campus every year" )
                ts.append( Nm+" is expected to graduate "+str(num)+" bachelor students" )
                ts.append( str(num)+" undergraduates study at "+Nm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts.append( NT[0]+" bachelor students studied from this university" )
                ts.append( NT[0]+" students are enrolled in the bachelor's program" )
                ts.append( "There are "+NT[0]+" undergraduate students on campus every year" )
                ts.append( "There are less than "+str(random.randint(num-80,num-50))+" undergraduate students on campus every year" )
                ts.append( "There are more than "+str(random.randint(num+50,num+100))+" undergraduate students on campus every year" )
                ts.append( Nm+" is expected to graduate "+NT[0]+" bachelor students" )
                ts.append( NT[0]+" undergraduates study at "+Nm )
                
                
        else:
            ts.append(None)
            
        return ts


def PostgraduatesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ 'There are '+di[tb[it]][0]+' postgraduate students in '+Nm ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            num = int(di[tb[it]][0])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( str(num)+" P.G. students studied from this university" )
                ts.append( str(num)+" students are enrolled in the postgraduate program" )
                ts.append( "There are "+str(num)+" P.G. students on campus every year" )
                ts.append( "There are more than "+str(random.randint(num-80,num-50))+" postgraduate students on campus every year" )
                ts.append( "There are less than "+str(random.randint(num+50,num+100))+" postgraduate students on campus every year" )
                ts.append( Nm+" is expected to graduate "+str(num)+" P.G. students" )
                ts.append( str(num)+" postgraduates study at "+Nm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts.append( NT[0]+" P.G. students studied from this university" )
                ts.append( NT[0]+" students are enrolled in the postgraduate program" )
                ts.append( "There are "+NT[0]+" postgraduate students on campus every year" )
                ts.append( "There are less than "+str(random.randint(num-80,num-50))+" postgraduate students on campus every year" )
                ts.append( "There are more than "+str(random.randint(num+50,num+100))+" postgraduate students on campus every year" )
                ts.append( Nm+" is expected to graduate "+NT[0]+" P.G. students" )
                ts.append( NT[0]+" postgraduates study at "+Nm )
                
                
        else:
            ts.append(None)
            
        return ts


def MottoSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" is the motto of "+Nm
                  , Nm+" has "+All+" as their motto"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( random.sample(di[tb[it]],1)[0]+" are the words the university "+random.sample(["lives by ","believes in "],1)[0] )
                ts.append( random.sample(di[tb[it]],1)[0]+" is the "+random.sample(["slogan ","apopthegm ","platitude "],1)[0]+"of "+Nm )
                ts.append( Nm+random.sample(["stand by ","believe in "],1)[0]+random.sample(di[tb[it]],1)[0] )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                ts.append( random.sample(NT,1)[0]+" are the words the university "+random.sample(["lives by ","believes in "],1)[0] )
                ts.append( random.sample(NT,1)[0]+" is the "+random.sample(["slogan ","apopthegm ","platitude "],1)[0]+"of "+Nm )
                ts.append( Nm+random.sample(["stand by ","believe in "],1)[0]+random.sample(NT,1)[0] )
                
        else:
            ts.append(None)
            
        return ts


def LocationSent(tb,dn,F,it,tval=True,prem=False):
    diP = F[2]
    diC = F[3]
    univP = F[1]
    univC = F[0]
    syn = [" at "," located at "," situated at "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(diC[tb[it]][0] != None or diP[tb[it]][0] != None ):
            if(diC[tb[it]][0] != None and diP[tb[it]][0] != None):
                All = ','.join(diC[tb[it]]+diP[tb[it]])
            elif(diC[tb[it]][0] != None):
                All = ','.join(diC[tb[it]])
            else:
                All = ','.join(diP[tb[it]])
            ps1 = [ "The location of this university is "+All
                  , All+" is the location of this university" ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(diP[tb[it]][0] != None or diC[tb[it]][0] != None):
            if(tval):
                if(diP[tb[it]][0]!=None):
                    ts.append( Nm+" is"+random.sample(syn,1)[0]+diP[tb[it]][0] )
                    ts.append( Nm+" is"+random.sample(syn,1)[0]+random.sample(diP[tb[it]][0].split(",")[1:],1)[0] )
                if(diC[tb[it]][0]!=None):
                    ts.append( "The coordinates of "+Nm+" is "+diC[tb[it]][0])
            else:
                if(diP[tb[it]][0]!=None):
                    Np = random.sample(list(set(univP)-set(diP[tb[it]])),1)[0]
                    ts.append( Nm+" is"+random.sample(syn,1)[0]+Np )
                    ts.append( Nm+" is"+random.sample(syn,1)[0]+random.sample(Np.split(","),1)[0] )
                if(diC[tb[it]][0]!=None):
                    Nc = random.sample(list(set(univC)-set(diC[tb[it]][0])),1)
                    ts.append( "The coordinates of "+Nm+" is "+Nc[0])
                
        else:
            ts.append(None)
            
        return ts


def NicknameSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The nicknames of the students from this university are "+All
                  , All+" are the nicknames given to the students of "+Nm ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( 'The students of '+Nm+" university are called "+random.sample(di[tb[it]],1)[0] )
                ts.append( random.sample(di[tb[it]],1)[0]+" is graduated from "+Nm )
                ts.append( "Students from "+Nm+" is known as "+random.sample(di[tb[it]],1)[0] )
                ts.append( "Another name for students of "+Nm+" university is "+random.sample(di[tb[it]],1)[0] )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                ts.append( 'The students of '+Nm+" university are called "+random.sample(di[tb[it]],1)[0] )
                ts.append( random.sample(di[tb[it]],1)[0]+" is graduated from "+Nm )
                ts.append( "Students from "+Nm+" is known as "+random.sample(di[tb[it]],1)[0] )
                ts.append( "Another name for students of "+Nm+" university is "+random.sample(di[tb[it]],1)[0] )
                
        else:
            ts.append(None)
            
        return ts


def CampusSent(tb,dn,F,it,tval=True,prem=False):
    diU = F[3]
    diA = F[2]
    univU = F[1]
    univA = F[0]
    syn = [" occupies "," take in "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(diA[tb[it]][0] != None):
            All = ','.join(diA[tb[it]])
            if(len(diU[tb[it]])!=0 and diU[tb[it]][0]!=None):
                ps1 = [ "The campus of university is "+All+" ("+diU[tb[it]][0]+")"
                      , All+" ("+diU[tb[it]][0]+")"+" is the campus of this university" ]
            else:
                ps1 = [ "The campus of university is "+All
                      , All+" is the campus of this university" ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if( len(diA[tb[it]])>0 and diA[tb[it]][0] != None):
            if(tval):
                ts.append( "The size of "+Nm+" is "+random.sample(diA[tb[it]],1)[0] )
                ts.append( Nm+" is spread in "+random.sample(diA[tb[it]],1)[0] )
                ts.append( Nm+" has an area of "+random.sample(diA[tb[it]],1)[0] )
                ts.append( Nm+random.sample(syn,1)[0]+random.sample(diA[tb[it]],1)[0]+" area" )
                if(len(diU[tb[it]]) != 0 and diU[tb[it]][0] != None ):
                    ts.append( Nm+" is realized in "+diU[tb[it]][0] )
                    ts.append( Nm+" is located in "+diU[tb[it]][0] )
                l = random.sample(diA[tb[it]],1)[0].replace(",","").split(" ")
                n = int(math.ceil(float(l[0])))
                ts.append(Nm+" is less than "+str(random.randint(n+1,n+4))+" "+l[1] )
                ts.append(Nm+" is more than "+str(random.randint(0,n-1))+" "+l[1] )
                
            else:
                NT = random.sample(list(set(univA)-set(diA[tb[it]])),random.randint(1,2))
                
                ts.append( "The size of "+Nm+" is "+random.sample(NT,1)[0] )
                ts.append( Nm+" is spread in "+random.sample(NT,1)[0] )
                ts.append( Nm+" has an area of "+random.sample(NT,1)[0] )
                ts.append( Nm+random.sample(syn,1)[0]+random.sample(NT,1)[0]+" area" )
                if(len(diU[tb[it]]) != 0 and diU[tb[it]][0] != None and len(diU[tb[it]])<2):
                    ts.append( Nm+" is realized in "+random.sample(list(set(univU)-set(diU[tb[it]])),1)[0] )
                    ts.append( Nm+" is located in "+random.sample(list(set(univU)-set(diU[tb[it]])),1)[0] )
                l = random.sample(diA[tb[it]],1)[0].replace(",","").split(" ")
                n = int(math.ceil(float(l[0])))
                ts.append(Nm+" is more than "+str(random.randint(n+1,n+4))+" "+l[1] )
                ts.append(Nm+" is less than "+str(random.randint(0,n-1))+" "+l[1] )
                
        else:
            ts.append(None)
            
        return ts


def ColorsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The colors of this university are "+All
                  , All+" are the colors of this university" ]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( random.sample(di[tb[it]],1)[0]+" is the school color of "+Nm )
                ts.append( random.sample(di[tb[it]],1)[0]+" is one of the school colors of this university" )
                ts.append( random.sample(di[tb[it]],1)[0]+" can be seen at lot of place at "+Nm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,2))
                ts.append( random.sample(NT,1)[0]+" is the school color of "+Nm )
                ts.append( random.sample(NT,1)[0]+" is one of the school colors of this university" )
                ts.append( random.sample(NT,1)[0]+" can be seen at lot of place at "+Nm )
                
        else:
            ts.append(None)
            
        return ts


def StudentsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ 'There are '+di[tb[it]][0]+' students in '+Nm ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            length = len(di[tb[it]])
            num = int(di[tb[it]][0])
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( str(num)+" students studied from this university" )
                ts.append( str(num)+" students are enrolled in "+Nm )
                ts.append( "There are "+str(num)+" students on campus every year" )
                ts.append( "There are more than "+str(random.randint(num-80,num-50))+" students on campus every year" )
                ts.append( "There are less than "+str(random.randint(num+50,num+100))+" students on campus every year" )
                ts.append( Nm+" is expected to graduate "+str(num)+" students" )
                ts.append( str(num)+" stdents study at "+Nm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts.append( NT[0]+" students studied from this university" )
                ts.append( NT[0]+" students are enrolled in "+Nm )
                ts.append( "There are "+NT[0]+" students on campus every year" )
                ts.append( "There are less than "+str(random.randint(num-80,num-50))+" students on campus every year" )
                ts.append( "There are more than "+str(random.randint(num+50,num+100))+" students on campus every year" )
                ts.append( Nm+" is expected to graduate "+NT[0]+" students" )
                ts.append( NT[0]+" students study at "+Nm )
                
                
        else:
            ts.append(None)
            
        return ts


def Academic_staffSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" academic staff are at "+Nm
                  , Nm+" has "+All+" academic staff" ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "There are "+All+" full time employees in the university" )
                ts.append( Nm+" employees "+All+" people" )
                ts.append( All+" people  assist in the day to day activities at "+Nm )
                ts.append( All+" people work at "+Nm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts.append( "There are "+NT[0]+" full time employees in the university" )
                ts.append( Nm+" employees "+NT[0]+" people" )
                ts.append( NT[0]+" people  assist in the day to day activities at "+Nm )
                ts.append( NT[0]+" people work at "+Nm )
                
        else:
            ts.append(None)
            
        return ts


def Administrative_staffSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" administrative staff are at "+Nm
                  , Nm+" has "+All+" administrative staff" ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "There are "+All+" full time employees in the university" )
                ts.append( Nm+" employees "+All+" people" )
                ts.append( All+" people  assist in the day to day activities at "+Nm )
                ts.append( All+" people work at "+Nm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)
                ts.append( "There are "+NT[0]+" full time employees in the university" )
                ts.append( Nm+" employees "+NT[0]+" people" )
                ts.append( NT[0]+" people  assist in the day to day activities at "+Nm )
                ts.append( NT[0]+" people work at "+Nm )
                
        else:
            ts.append(None)
            
        return ts


def PresidentSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" important "," sensitive "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" is the president of this university"
                  , "The president of this university is "+All ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( All+" is the head of the institution" )
                ts.append( All+" heads "+Nm+" university" )
                ts.append( All+" is the highest governing body of the university" )
                ts.append( All+" makes the most "+random.sample(syn,1)[0]+" decision of the institution" )
                ts.append( All+" is responsible for the university" )
                ts.append( All+" is the administrator of the university" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( NT+" is the head of the institution" )
                ts.append( NT+" heads "+Nm+" university" )
                ts.append( NT+" is the highest governing body of the university" )
                ts.append( NT+" makes the most "+random.sample(syn,1)[0]+" decision of the institution" )
                ts.append( NT+" is responsible for the university" )
                ts.append( NT+" is the administrator of the university" )
                
        else:
            ts.append(None)
            
        return ts


def EndowmentSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" received "," was gifted "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The university was endowed "+All
                   ,All+" was endowed to "+Nm ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            m = float(re.findall("[0-9.]+",di[tb[it]][0])[0])
            mm = re.findall("[mb]illion",di[tb[it]][0])[0]
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( "The market financial value of the university is "+All )
                ts.append( "The university was gifted "+All )
                ts.append( "The university "+Nm+random.sample(syn,1)[0]+All+" in donation" )
                ts.append( Nm+random.sample(syn,1)[0]+"more than "+"$"+ str(m-random.randint(1,min(int(m),4)))+" "+mm )
                ts.append( Nm+random.sample(syn,1)[0]+"less than "+"$"+ str(m+random.randint(1,2))+" "+mm )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( "The market financial value of the university is "+NT )
                ts.append( "The university was gifted "+NT )
                ts.append( "The university "+Nm+random.sample(syn,1)[0]+NT+" in donation" )
                ts.append( Nm+random.sample(syn,1)[0]+"more than "+"$"+ str(m-random.randint(1,min(int(m),4)))+" "+mm )
                ts.append( Nm+random.sample(syn,1)[0]+"less than "+"$"+ str(m+random.randint(1,2))+" "+mm )
                
        else:
            ts.append(None)
            
        return ts


def MascotSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" symbol "," token "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The mascot of this university is "+All
                  , All+" is the mascot of "+Nm]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( All+" represent the "+Nm )
                ts.append( All+" is the"+random.sample(syn,1)[0]+"of "+Nm )
                ts.append( "You can see the symbol "+All+" in every important event of "+Nm)
                ts.append( All+" is the symbol of pride for "+Nm )
                ts.append( "Students are dressed as "+All+" for "+Nm+" games" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( NT+" represent the "+Nm )
                ts.append( NT+" is the"+random.sample(syn,1)[0]+"of "+Nm )
                ts.append( "You can see the symbol "+NT+" in every important event of "+Nm)
                ts.append( NT+" is the symbol of pride for "+Nm )
                ts.append( "Students are dressed as "+NT+" for "+Nm+" games" )
                
        else:
            ts.append(None)
            
        return ts


def ProvostSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" important "," sensitive "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ All+" is the second in head after the president of this university"
                  , "The second in head after the president of this university is "+All ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( All+" is second to the head of the institution" )
                ts.append( All+" is the second highest governing body of the university" )
                ts.append( All+" makes the most "+random.sample(syn,1)[0]+" decision of the institution" )
                ts.append( All+" is responsible for the university" )
                ts.append( All+" is the administrator of the university" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( NT+" is second to the head of the institution" )
                ts.append( NT+" is the second highest governing body of the university" )
                ts.append( NT+" makes the most "+random.sample(syn,1)[0]+" decision of the institution" )
                ts.append( NT+" is responsible for the university" )
                ts.append( NT+" is the administrator of the university" )
                
        else:
            ts.append(None)
            
        return ts


def Sporting_affiliationsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" affiliated to "," associated with "," allied with "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" has "+All+" sport affiliations"
                  , "The sport affiliations of "+Nm+" is "+All ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is"+random.sample(syn,1)[0]+All+" in sports" )
                ts.append( "Sports body of the university "+Nm+" is connected to "+All )
                ts.append( All+" regulates the sports of "+Nm )
                
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( Nm+" is"+random.sample(syn,1)[0]+NT+" in sports" )
                ts.append( "Sports body of the university "+Nm+" is connected to "+NT )
                ts.append( NT+" regulates the sports of "+Nm )
                
        else:
            ts.append(None)
            
        return ts


def Academic_affiliationsSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    syn = [" affiliated to "," associated with "," allied with "]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ Nm+" has "+All+" academic affiliations"
                  , "The academic affiliations of "+Nm+" is "+All ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                All = ','.join(di[tb[it]])
                ts.append( Nm+" is"+random.sample(syn,1)[0]+All+" in academics" )
                ts.append( "Academic body of the university "+Nm+" is connected to "+All )
                ts.append( All+" regulates the academics of "+Nm )
                
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),1)[0]
                ts.append( Nm+" is"+random.sample(syn,1)[0]+NT+" in academics" )
                ts.append( "Academic body of the university "+Nm+" is connected to "+NT )
                ts.append( NT+" regulates the academics of "+Nm )
                
        else:
            ts.append(None)
            
        return ts


def Former_namesSent(tb,dn,F,it,tval=True,prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if(prem):
        if(di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [ "The former name of "+Nm+" was "+All
                  , Nm+" was formerly known as "+All ]
        else:
            ps1=[None]
        return ps1
    else:
        ts = []
        if(di[tb[it]][0] != None):
            if(tval):
                p = random.sample(di[tb[it]],1)[0]
                ts.append( "The past name of "+Nm+" is "+p )
                ts.append( Nm+" was also known by "+p+" in the past" )
                ts.append( Nm+" was previously called as "+p )
                ts.append( p+" changed it's name to "+Nm )
                ts.append( "At some point in time student's used to study at "+p )
                ts.append( Nm+" used to be called "+p+" before" )
                ts.append( p+" was another name for "+Nm+" before" )
                
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])),random.randint(1,4))
                p = random.sample(NT,1)[0]
                ts.append( "The past name of "+Nm+" is "+p )
                ts.append( Nm+" was also known by "+p+" in the past" )
                ts.append( Nm+" was previously called as "+p )
                ts.append( p+" changed it's name to "+Nm )
                ts.append( "At some point in time student's used to study at "+p )
                ts.append( Nm+" used to be called "+p+" before" )
                ts.append( p+" was another name for "+Nm+" before" )
                
        else:
            ts.append(None)
            
        return ts

# 1st multi-row templates
def multi_row1(tb,dn,F,it,tval=True):
    Ug,G = F["Undergraduates"]
    Up,P = F["Postgraduates"]
    Us,S = F["Students"]
    Uc,C = F["Academic_staff"]
    Ud,D = F["Administrative_staff"]
    
    ns = -1 # number of students
    if(G[tb[it]][0]!=None and P[tb[it]][0]!=None):
        ns = int(G[tb[it]][0])+int(P[tb[it]][0])
    elif(S[tb[it]][0]!=None):
        ns = int(S[tb[it]][0])
        
    nst = -1 # number of staff
    if(C[tb[it]][0]!=None and D[tb[it]][0]!=None):
        nst = int(C[tb[it]][0])+int(D[tb[it]][0])
    
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(ns != -1):
            if(S[tb[it]][0]!=None):
                ts["Students"] = []
                ts["Students"].append( "There are "+str(ns)+" students in "+Nm )
            else:
                ts["Undergraduates,Postgraduates"] = []
                ts["Undergraduates,Postgraduates"].append( "There are "+str(ns)+" students in "+Nm )
        if(nst != -1 and ns != -1):
            if(S[tb[it]][0]!=None):
                ts["Students,Academic_staff,Administrative_staff"] = []
                ts["Students,Academic_staff,Administrative_staff"].append( str(nst)+" employees manage "+str(ns)+" students" )
            else:
                ts["Undergraduates,Postgraduates,Academic_staff,Administrative_staff"] = []
                ts["Undergraduates,Postgraduates,Academic_staff,Administrative_staff"].append( str(nst)+" employees manage "+str(ns)+" students" )
                
    else:
        if(ns != -1):
            if(S[tb[it]][0]!=None):
                ts["Students"] = []
                ts["Students"].append( "There are "+str(random.randint(ns+10,ns+1000))+" students in "+Nm )
            else:
                ts["Undergraduates,Postgraduates"] = []
                ts["Undergraduates,Postgraduates"].append( "There are "+str(random.randint(ns+10,ns+1000))+" students in "+Nm )
                
        if(nst != -1 and ns != -1):
            if(S[tb[it]][0]!=None):
                ts["Students,Academic_staff,Administrative_staff"] = []
                ts["Students,Academic_staff,Administrative_staff"].append( str(random.randint(nst+10,nst+1000))+" employees manage "+str(random.randint(ns+10,ns+1000))+" students" )
            else:
                ts["Undergraduates,Postgraduates,Academic_staff,Administrative_staff"] = []
                ts["Undergraduates,Postgraduates,Academic_staff,Administrative_staff"].append( str(random.randint(nst+10,nst+1000))+" employees manage "+str(random.randint(ns+10,ns+1000))+" students" ) 
        
    return ts

# 2nd multi-row templates
def multi_row2(tb,dn,F,it,tval=True):
    Um,M = F["Mascot"]
    Un,N = F["Nickname"]
    Upr,Pr = F["President"]
    Upv,Pv = F["Provost"]
    
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if(M[tb[it]][0] != None and N[tb[it]][0] != None):
            ts["Mascot,Nickname"] = []
            Al1 = ",".join(random.sample(M[tb[it]],1))
            Al2 = ",".join(random.sample(N[tb[it]],1))
            ts["Mascot,Nickname"].append( Al1+" is the mascot for the "+Al2 )
        if(Pr[tb[it]][0] != None and Pv[tb[it]][0] != None):
            ts["President,Provost"] = []
            Al1 = ",".join(random.sample(Pr[tb[it]],1))
            Al2 = ",".join(random.sample(Pv[tb[it]],1))
            ts["President,Provost"].append( Al1+" and "+Al2+" are the main administrative figure heads of the university" )
        
        
    else:
        if(M[tb[it]][0] != None and N[tb[it]][0] != None):
            ts["Mascot,Nickname"] = []
            Al1 = ",".join(random.sample(list(set(Um)-set(M[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Un)-set(N[tb[it]])),1))
            ts["Mascot,Nickname"].append( Al1+" is the mascot for the "+Al2 )
        if(Pr[tb[it]][0] != None and Pv[tb[it]][0] != None):
            ts["President,Provost"] = []
            Al1 = ",".join(random.sample(list(set(Upr)-set(Pr[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Upv)-set(Pv[tb[it]])),1))
            ts["President,Provost"].append( Al1+" and "+Al2+" are the main administrative figure heads of the university" )
        
    return ts

# 3rd multi-row templates
def multi_row3(tb,dn,F,it,tval=True):
    Um,M = F["Motto"]
    Us,S = F["Sporting_affiliations"]
    Ua,A = F["Academic_affiliations"]
    
    ME = []
    MOt = []
    if(M[tb[it]][0]!=None):
        for i in M[tb[it]]:
            if(re.findall("latin",i) or re.findall("sankrit",i) or len(re.findall("[A-za-z]",i)) == 0):
                MOt.append(i)
            else:
                ME.append(i)
        
    Nm = dn[tb[it]][0]
    ts = {}
    if(tval):
        if( len(ME) != 0 and len(MOt) != 0 ):
            ts["Motto"] = []
            Al1 = ",".join(random.sample(ME,1))
            Al2 = ",".join(random.sample(MOt,1))
            ts["Motto"].append( "English of the motto "+Al2+" of the university is "+Al1 )
        if(S[tb[it]][0] != None and A[tb[it]][0] != None):
            ts["Sporting_affiliations,Academic_affiliations"] = []
            Al1 = ",".join(random.sample(S[tb[it]],1))
            Al2 = ",".join(random.sample(A[tb[it]],1))
            ts["Sporting_affiliations,Academic_affiliations"].append( "Affiliations of the university are "+Al1+", "+Al2 )
        
    else:
        if( len(ME) != 0 and len(MOt) != 0 ):
            ts["Motto"] = []
            Al1 = ",".join(random.sample(list(set(Um)-set(ME)),1))
            Al2 = ",".join(random.sample(list(set(Um)-set(MOt)),1))
            ts["Motto"].append( "English of the motto "+Al2+" of the university is "+Al1 )
        if(A[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Sporting_affiliations,Academic_affiliations"] = []
            Al1 = ",".join(random.sample(list(set(Ua)-set(A[tb[it]])),1))
            Al2 = ",".join(random.sample(list(set(Us)-set(S[tb[it]])),1))
            ts["Sporting_affiliations,Academic_affiliations"].append( "Affiliations of the university are "+Al1+", "+Al2 )
        
    return ts