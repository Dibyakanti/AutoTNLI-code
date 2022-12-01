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


table_index = np.array(
    category_map[category_map.category.isin(['Painting'])].table_id)


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(
        open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys = [i.text for i in soup.find('tr').find_all('th')]
    vals = []
    for i in soup.find('tr').find_all('td'):
        if (i.parent.find('th')):
            result = [val.text.strip().replace("\n", "").replace("\t", "")
                      for val in i.find_all('li')]
            if not result:
                if (i.find('br')):
                    for x in i.findAll('br'):
                        x.replace_with(',')
                    result = i.text.split(',')
                if "â€“" in i.text:
                    result = [val.strip().replace("\n", "").replace("\t", "")
                              for val in i.text.split("â€“")]
                elif " to " in i.text:
                    result = [val.strip().replace("\n", "").replace("\t", "")
                              for val in i.text.split("to")]
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
    for n in range(132):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            tb.append(dictionary['Tablename'])
            if ("Title" in dictionary.keys()):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(dictionary['Title'])
            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    return d, tb


N, T = get_Table_Title()


def get_Artist(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Artist"
    for n in range(132):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in dictionary[k]:
                        if (not re.findall("[Aa]ttributed", i) and not re.findall("[Uu]nknown", i)):
                            u.add(i.strip())
                            d[dictionary['Tablename']].append(i.strip())
                else:
                    i = dictionary[k]
                    if (not re.findall("[Aa]ttributed", i) and not re.findall("[Uu]nknown", i)):
                        u.add(dictionary[k].strip())
                        d[dictionary['Tablename']].append(
                            dictionary[k].strip())
                    else:
                        d[dictionary['Tablename']].append(None)

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(132):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Paint"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Year(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Year"
    for n in range(132):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                r = re.findall("[0-9][0-9][0-9]+", dictionary[k])
                t = 0
                for s in r:
                    if (t != int(s)):
                        if (int(s) > 1000):
                            u.add(s)
                        d[dictionary['Tablename']].append(s)
                        t = int(s.strip())

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(132):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Paint"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Medium(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k1 = "Medium"
    k2 = "Type"
    for n in range(132):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k1 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k1]) == list):
                    for i in range(len(dictionary[k1])):
                        u.add(dictionary[k1][i].lower())
                        d[dictionary['Tablename']].append(
                            dictionary[k1][i].lower())
                else:
                    for i in range(len(dictionary[k1].split(","))):
                        u.add(dictionary[k1].split(",")[i].lower())
                        d[dictionary['Tablename']].append(
                            dictionary[k1].split(",")[i].lower())

            if (k2 in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k2]) == list):
                    for i in range(len(dictionary[k2])):
                        u.add(dictionary[k2][i].lower())
                        d[dictionary['Tablename']].append(
                            dictionary[k2][i].lower())
                else:
                    for i in range(len(dictionary[k2].split(","))):
                        u.add(dictionary[k2].split(",")[i].lower())
                        d[dictionary['Tablename']].append(
                            dictionary[k2].split(",")[i].lower())

            if (k1 not in dictionary.keys() and k2 not in dictionary.keys()):
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(132):  # for getting all the fakes in one go
            sel = random.sample(FakeDICT_helper["Paint"]["Medium"], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Dimensions(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Dimensions"
    for n in range(132):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                s = dictionary[k].replace('\xa0', '').replace('\u200b', '')
                r = re.findall("[0-9.]+", s)
                for ss in r:
                    u.add(float(ss.strip()))
                    d[dictionary['Tablename']].append(float(ss.strip()))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(132):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Paint"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel, subNone=False)

    return list(u), d


def get_Location(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Location"
    for n in range(132):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    u.add(",".join(dictionary[k]))
                    d[dictionary['Tablename']].append(",".join(dictionary[k]))
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(132):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Paint"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d

# Extract all data :


def get_Data(fake=False):

    Extracted_data = {}
    Keys = ["Artist", "Year", "Medium", "Dimensions", "Location"]
    for k in Keys:
        Extracted_data[k] = []
        for l in eval("get_"+k)(T, N, fake):
            Extracted_data[k].append(l)

    return Extracted_data

# Sentence generator :


def ArtistSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The artist of "+dn[tb[it]][0]+" was "+All, dn[tb[it]][0] +
                   " was painted by "+All, All+" made "+dn[tb[it]][0]+" painting"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(dn[tb[it]][0]+" was created by "+All)
                ts.append(All+" created this painting")
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)
                All = ','.join(NT)
                ts.append(dn[tb[it]][0]+" was created by "+All)
                ts.append(All+" created this painting")

        else:
            ts.append(None)

        return ts


def YearSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [dn[tb[it]][0]+" was painted in "+di[tb[it]][0],
                   "This was made in "+di[tb[it]][0], "This was painted in "+di[tb[it]][0]]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            y = int(di[tb[it]][0])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(dn[tb[it]][0] +
                          " was painted in the year "+di[tb[it]][0])
                ts.append(dn[tb[it]][0]+" was painted before " +
                          str(random.randint(y+20, y+100)))
                ts.append(dn[tb[it]][0]+" was painted after " +
                          str(random.randint(1000, y-30)))
                ts.append(dn[tb[it]][0]+" was painted in the " +
                          str(int(y/100)+1)+"th century")

            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)[0]
                ts.append(dn[tb[it]][0]+" was painted in the year "+NT)
                ts.append(dn[tb[it]][0]+" was painted after " +
                          str(random.randint(y+20, y+100)))
                ts.append(dn[tb[it]][0]+" was painted before " +
                          str(random.randint(1000, y-30)))
                ts.append(dn[tb[it]][0]+" was painted in the " +
                          str(int(y/100)-1)+"th century")

        else:
            ts.append(None)

        return ts


def MediumSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["It was made in "+All, All+" was the medium for this",
                   dn[tb[it]][0]+" was of "+All+" type"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(All+" was used as a medium for this painting")
                ts.append("The type of this painting is "+All)
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)
                All = ','.join(NT)
                ts.append(All+" was used as a medium for this painting")
                ts.append("The type of this painting is "+All)

        else:
            ts.append(None)

        return ts


def DimensionsSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            dd = di[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            ps1 = ["The dimensions are "+str(lc)+" cm by "+str(wc)+" cm and "+str(li)+" inch by "+str(wi)+" inch", "The painting "+dn[tb[it]][0]+" is "+str(lc)+" cm by "+str(
                wc)+" cm and "+str(li)+" inch by "+str(wi)+" inch", str(lc)+" cm by "+str(wc)+" cm and "+str(li)+" inch by "+str(wi)+" inch"+" is the size of the painting"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            dd = di[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            if (tval):
                ts.append("The painting is "+str(lc) +
                          " cm by "+str(wc)+" cm in size")
                ts.append("The painting is "+str(li) +
                          " inch by "+str(wi)+" inch in size")
                ts.append("The area is "+str(lc*wc)+" sq.cm")
                ts.append("The area is "+str(li*wi)+" sq.inch")
                ts.append("Length is "+str(lc-wc)+" cm more than width")
                ts.append("Length is "+str(li-wi)+" inch more than width")
                ts.append("The perimeter of the painting is " +
                          str(2*(lc+wc))+" cm")

            else:
                rnd = float(random.randint(3, 8))
                ts.append("The painting is "+str(lc+rnd) +
                          " cm by "+str(wc+rnd)+" cm in size")
                ts.append("The painting is "+str(wi) +
                          " inch by "+str(li)+" inch in size")
                ts.append("The area is "+str(lc*wi)+"sq.cm")
                ts.append("The area is "+str(li*wc)+"sq.inch")
                ts.append("Length is "+str(lc-wc+rnd)+"cm more than width")
                ts.append("Length is "+str(li-wi+2*rnd)+"inch more than width")
                ts.append("The perimeter of the painting is " +
                          str(2*rnd*(li+wi))+"inch")

        else:
            ts.append(None)

        return ts


def LocationSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [dn[tb[it]][0]+" is at "+All,
                   "The painting is at "+All, "It is located in "+All]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(dn[tb[it]][0]+" is now kept in the "+All)
                ts.append(All+" is the location of the painting")
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)
                All = ','.join(NT)
                ts.append(dn[tb[it]][0]+" is now kept in the "+All)
                ts.append(All+" is the location of the painting")

        else:
            ts.append(None)

        return ts


def multi_row1(tb, dn, F, it, tval=True):
    Ua, A = F["Artist"]
    Um, M = F["Medium"]
    Ul, L = F["Location"]

    ts = {}
    if (tval):
        if (A[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Artist,Medium"] = []
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(M[tb[it]])
            ts["Artist,Medium"].append(Al1+" used "+Al2+" medium for painting")
        if (A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = []
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(L[tb[it]])
            ts["Artist,Location"].append(Al1+"'s painting is located in "+Al2)
        if (A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = []
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(L[tb[it]])
            ts["Artist,Location"].append(
                "Atleast one of the painting by "+Al1+" is at "+Al2)

    else:
        if (A[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Artist,Medium"] = []
            NM = random.sample(list(set(Um)-set(M[tb[it]])), 1)
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(NM)
            ts["Artist,Medium"].append(Al1+" used "+Al2+" medium for painting")
        if (A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = []
            NA = random.sample(list(set(Ua)-set(A[tb[it]])), 1)
            Al1 = ",".join(NA)
            Al2 = ",".join(L[tb[it]])
            ts["Artist,Location"].append(Al1+"'s painting is located in "+Al2)
        if (A[tb[it]][0] != None and L[tb[it]][0] != None):
            ts["Artist,Location"] = []
            NL = random.sample(list(set(Ul)-set(L[tb[it]])), 1)
            Al1 = ",".join(A[tb[it]])
            Al2 = ",".join(NL)
            ts["Artist,Location"].append(
                "Atleast one of the painting by "+Al1+" is at "+Al2)

    return ts

# 1st multi-row templates


def multi_row2(tb, dn, F, it, tval=True):
    Ua, A = F["Artist"]
    Ud, D = F["Dimensions"]
    Uy, Y = F["Year"]

    ts = {}
    if (tval):
        if (A[tb[it]][0] != None and Y[tb[it]][0] != None):
            ts["Artist,Year"] = []
            Al1 = ",".join(A[tb[it]])
            year = int(Y[tb[it]][0])
            ts["Artist,Year"].append(
                dn[tb[it]][0]+" was created by "+Al1+" in the "+str(int(year/100)+1)+"th century")
            ts["Artist,Year"].append(
                Al1+" made a painting in "+str(int(year/100)+1)+"th century")
            syn = [" completed ", " started "]
            ts["Artist,Year"].append(
                Al1+random.sample(syn, 1)[0]+"this painting after "+str(random.randint(1000, year-40)))
        if (A[tb[it]][0] != None and D[tb[it]][0] != None):
            ts["Artist,Dimensions"] = []
            dd = D[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            Al1 = ",".join(A[tb[it]])
            ts["Artist,Dimensions"].append(
                Al1+"'s painting was "+str(lc)+" cm by "+str(wc)+" cm in size")
            ts["Artist,Dimensions"].append(
                Al1+"'s painting was "+str(li)+" cm by "+str(wi)+" cm in size")

    else:
        if (A[tb[it]][0] != None and Y[tb[it]][0] != None):
            ts["Artist,Year"] = []
            Al1 = ",".join(A[tb[it]])
            year = int(Y[tb[it]][0])
            ts["Artist,Year"].append(dn[tb[it]][0]+" was created by "+Al1 +
                                     " in the "+str(int(year/100)-random.randint(1, 3))+"th century")
            ts["Artist,Year"].append(
                Al1+" made a painting in "+str(int(year/100)-random.randint(1, 3))+"th century")
            syn = [" completed ", " started "]
            ts["Artist,Year"].append(
                Al1+random.sample(syn, 1)[0]+"this painting after "+str(random.randint(year+40, year+200)))
        if (A[tb[it]][0] != None and D[tb[it]][0] != None):
            ts["Artist,Dimensions"] = []
            dd = D[tb[it]]
            lc = dd[0] if dd[0] > dd[1] else dd[1]
            wc = dd[0] if dd[0] < dd[1] else dd[1]
            li = dd[2] if dd[2] > dd[3] else dd[3]
            wi = dd[2] if dd[2] < dd[3] else dd[3]
            Al1 = ",".join(A[tb[it]])
            rnd = float(random.randint(3, 8))
            ts["Artist,Dimensions"].append(
                Al1+"'s painting was "+str(lc+rnd)+" cm by "+str(wc-rnd)+" cm in size")
            ts["Artist,Dimensions"].append(
                Al1+"'s painting was "+str(li+rnd)+" inch by "+str(wi+rnd)+" inch in size")
    return ts
