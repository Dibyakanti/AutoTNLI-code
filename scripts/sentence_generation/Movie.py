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
    category_map[category_map.category.isin(['Movie'])].table_id)


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(
        open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys = [i.text for i in soup.find('tr').find_all('th')]
    vals = []
    for x in soup.find_all():
        if len(x.get_text(strip=True)) == 0:
            x.extract()
    for i in soup.find('tr').find_all('td'):
        result = [val.text.strip().replace("\n", "").replace("\t", "")
                  for val in i.find_all('li')]
        if not result:
            if (i.find('br')):
                for x in i.findAll('br'):
                    x.replace_with(',')
                result = i.text.split(',')
            elif "â€“" in i.text:
                result = [val.strip().replace("\n", "").replace("\t", "")
                          for val in i.text.split("â€“")]
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
    for n in range(200):
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


def get_Directed_by(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Directed by"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Directed by" in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary['Directed by']) == list):
                    for i in range(len(dictionary['Directed by'])):
                        u.add(dictionary['Directed by'][i])
                        d[dictionary['Tablename']].append(
                            dictionary['Directed by'][i])
                else:
                    u.add(dictionary['Directed by'])
                    d[dictionary['Tablename']].append(
                        dictionary['Directed by'])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Produced_by(T, N, fake=False, sel=0):
    u = set([])
    p = {}
    k = "Produced by"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Produced by" in dictionary.keys()):
                p[dictionary['Tablename']] = []
                if (type(dictionary['Produced by']) == list):
                    for i in range(len(dictionary['Produced by'])):
                        u.add(dictionary['Produced by'][i])
                        p[dictionary['Tablename']].append(
                            dictionary['Produced by'][i])
                else:
                    u.add(dictionary['Produced by'])
                    p[dictionary['Tablename']].append(
                        dictionary['Produced by'])

            else:
                p[dictionary['Tablename']] = []
                p[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(p[T[it]]) < 2):
                sel = 1
            p = FakeDICT(T, N, u, p, it, sel)

    return list(u), p


def get_Screenplay_by(T, N, fake=False, sel=0):
    u = set([])
    p = {}
    k = "Screenplay by"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Screenplay by" in dictionary.keys()):
                p[dictionary['Tablename']] = []
                if (type(dictionary['Screenplay by']) == list):
                    for i in range(len(dictionary['Screenplay by'])):
                        u.add(dictionary['Screenplay by'][i])
                        p[dictionary['Tablename']].append(
                            dictionary['Screenplay by'][i])
                else:
                    u.add(dictionary['Screenplay by'])
                    p[dictionary['Tablename']].append(
                        dictionary['Screenplay by'])

            else:
                p[dictionary['Tablename']] = []
                p[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(p[T[it]]) < 2):
                sel = 1
            p = FakeDICT(T, N, u, p, it, sel)

    return list(u), p


def get_Based_on(T, N, fake=False, sel=0):
    u = set([])
    b = {}
    k = "Based on"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Based on" in dictionary.keys()):
                b[dictionary['Tablename']] = []
                if (type(dictionary['Based on']) == list):
                    for i in range(len(dictionary['Based on'])):
                        u.add(dictionary['Based on'][i])
                        b[dictionary['Tablename']].append(
                            dictionary['Based on'][i])
                else:
                    u.add(dictionary['Based on'])
                    b[dictionary['Tablename']].append(dictionary['Based on'])

            else:
                b[dictionary['Tablename']] = []
                b[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(b[T[it]]) < 2):
                sel = 1
            b = FakeDICT(T, N, u, b, it, sel)

    return list(u), b


def get_Starring(T, N, fake=False, sel=0):
    u = set([])
    s = {}
    k = "Starring"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Starring" in dictionary.keys()):
                s[dictionary['Tablename']] = []
                if (type(dictionary['Starring']) == list):
                    for i in range(len(dictionary['Starring'])):
                        u.add(dictionary['Starring'][i])
                        s[dictionary['Tablename']].append(
                            dictionary['Starring'][i])
                else:
                    u.add(dictionary['Starring'])
                    s[dictionary['Tablename']].append(dictionary['Starring'])

            else:
                s[dictionary['Tablename']] = []
                s[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(s[T[it]]) < 2):
                sel = 1
            s = FakeDICT(T, N, u, s, it, sel)

    return list(u), s


def get_Music_by(T, N, fake=False, sel=0):
    u = set([])
    m = {}
    k = "Music by"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Music by" in dictionary.keys()):
                m[dictionary['Tablename']] = []
                if (type(dictionary['Music by']) == list):
                    for i in range(len(dictionary['Music by'])):
                        u.add(dictionary['Music by'][i])
                        m[dictionary['Tablename']].append(
                            dictionary['Music by'][i])
                else:
                    u.add(dictionary['Music by'])
                    m[dictionary['Tablename']].append(dictionary['Music by'])

            else:
                m[dictionary['Tablename']] = []
                m[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(m[T[it]]) < 2):
                sel = 1
            m = FakeDICT(T, N, u, m, it, sel)

    return list(u), m


def get_Cinematography(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Cinematography"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Cinematography" in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary['Cinematography']) == list):
                    for i in range(len(dictionary['Cinematography'])):
                        u.add(dictionary['Cinematography'][i])
                        d[dictionary['Tablename']].append(
                            dictionary['Cinematography'][i])
                else:
                    u.add(dictionary['Cinematography'])
                    d[dictionary['Tablename']].append(
                        dictionary['Cinematography'])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Edited_by(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Edited by"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if ("Edited by" in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary['Edited by']) == list):
                    for i in range(len(dictionary['Edited by'])):
                        u.add(dictionary['Edited by'][i])
                        d[dictionary['Tablename']].append(
                            dictionary['Edited by'][i])
                else:
                    u.add(dictionary['Edited by'])
                    d[dictionary['Tablename']].append(dictionary['Edited by'])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Productioncompany(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Productioncompany "
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Distributed_by(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Distributed by"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Release_date(T, N, fake=False, sel=0):
    ud = set([])
    up = set([])
    d, p = {}, {}
    k = "Release date"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                p[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        s = dictionary[k][i].replace('\xa0', ' ')
                        ss = s.split('(')
                        if (len(ss) > 2 and len(re.findall("[0-9]", ss[2])) == 0):
                            pp = ss[2].replace(')', '').strip()
                            ud.add("(".join(ss[0:2]))
                            up.add(pp)
                            d[dictionary['Tablename']].append(
                                "(".join(ss[0:2]))
                            p[dictionary['Tablename']].append(pp)
                        elif (len(ss) > 1):
                            ud.add("(".join(ss[0:2]))
                            d[dictionary['Tablename']].append(
                                "(".join(ss[0:2]))
                            p[dictionary['Tablename']] = []
                            p[dictionary['Tablename']].append(None)
                        else:
                            d[dictionary['Tablename']].append(None)
                            p[dictionary['Tablename']].append(None)
                else:
                    d[dictionary['Tablename']].append(None)
                    p[dictionary['Tablename']].append(None)

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
                p[dictionary['Tablename']] = []
                p[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, ud, d, it, sel)
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(p[T[it]]) < 2):
                sel = 1
            p = FakeDICT(T, N, up, p, it, sel)

    return list(ud), list(up), d, p


def get_Running_time(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Running time"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Country(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Country"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Language(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Language"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(dictionary[k])

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Budget(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Budget"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i].replace('\xa0', ' '))
                        d[dictionary['Tablename']].append(
                            dictionary[k][i].replace('\xa0', ' '))
                else:
                    u.add(dictionary[k].replace('\xa0', ' '))
                    d[dictionary['Tablename']].append(
                        dictionary[k].replace('\xa0', ' '))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Box_office(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Box office"
    for n in range(200):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        u.add(dictionary[k][i])
                        d[dictionary['Tablename']].append(
                            dictionary[k][i].replace("\xa0", " "))
                else:
                    u.add(dictionary[k])
                    d[dictionary['Tablename']].append(
                        dictionary[k].replace("\xa0", " "))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(200):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Movie"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d

# Extract all data :


def get_Data(fake=False):

    Extracted_data = {}
    Keys = ["Directed_by", "Produced_by", "Screenplay_by", "Starring", "Music_by", "Cinematography", "Edited_by",
            "Productioncompany", "Distributed_by", "Release_date", "Running_time", "Country", "Language", "Budget", "Box_office"]
    for k in Keys:
        Extracted_data[k] = []
        for l in eval("get_"+k)(T, N, fake):
            Extracted_data[k].append(l)

    return Extracted_data

# Sentence generator :


def Directed_bySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" directed the movie named "+dn[tb[it]][0], "The movie named "+dn[tb[it]][0] +
                   " was directed by "+All, All+" were the directors in the movie named "+dn[tb[it]][0]]
        else:
            ps1 = [None]
        return ps1

    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = [dn[tb[it]][0] + " was directed by " + All, dn[tb[it]][0] + " was made by " + random.sample(di[tb[it]], 1)[0], dn[tb[it]][0] + " was directed by " + str(len(di[tb[it]])) + " director(s)", dn[tb[it]][0] + " was directed by more than " + str(
                    random.randint(0, len(di[tb[it]])-1)) + " director(s)", dn[tb[it]][0] + " was directed by less than " + str(random.randint(len(di[tb[it]])+1, len(di[tb[it]]) + 5))+" director(s)"]
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts1 = [dn[tb[it]][0] + " was directed by " + All, dn[tb[it]][0] + " was made by " + random.sample(NT, 1)[0], dn[tb[it]][0] + " was directed by " + str(len(di[tb[it]])+3) + " director(s)", dn[tb[it]][0] + " was directed by less than " + str(
                    random.randint(0, len(di[tb[it]])-1)) + " director(s)", dn[tb[it]][0] + " was directed by more than " + str(random.randint(len(di[tb[it]])+1, len(di[tb[it]]) + 5)) + " director(s)"]
        else:
            ts1 = [None]
        return ts1


def Produced_bySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" produced this movie", "The movie named "+dn[tb[it]][0] +
                   " was produced by "+All, All+" were the producers in this movie"]
        else:
            ps1 = [None]
        return ps1

    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = dn[tb[it]][0] + " was produced by " + All
                ts2 = dn[tb[it]][0] + " was produced by " + \
                    str(len(di[tb[it]])) + " producer(s)"
                ts3 = dn[tb[it]][0] + " was produced by more than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " producer(s)"
                ts4 = dn[tb[it]][0] + " was produced by less than " + \
                    str(random.randint(
                        len(di[tb[it]])+1, len(di[tb[it]]) + 5)) + " producer(s)"

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts1 = dn[tb[it]][0] + " was produced by " + All
                ts2 = dn[tb[it]][0] + " was produced by " + \
                    str(len(di[tb[it]])+2) + " producer(s)"
                ts3 = dn[tb[it]][0] + " was produced by less than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " producer(s)"
                ts4 = dn[tb[it]][0] + " was produced by more than " + \
                    str(random.randint(
                        len(di[tb[it]])+1, len(di[tb[it]]) + 5)) + " producer(s)"

            return [ts1, ts2, ts3, ts4]
        else:
            return [None]


def Screenplay_bySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" wrote the script in this movie", All+" wrote the script in " +
                   dn[tb[it]][0], "The script in " + dn[tb[it]][0] + " was written by "+All]
        else:
            ps1 = [None]
        return ps1

    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = "The script was written by " + All

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 5))
                All = ','.join(NT)
                ts1 = "The script was written by " + All

            return [ts1]
        else:
            return [None]


def StarringSent(tb, dn, F, it, tval=True, prem=False):  # a bit goofed
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" were the actors who played a role in "+dn[tb[it]][0],
                   "In this movie the acting was done by "+All, "The actors in this movie were "+All]
        else:
            ps1 = [None]

        return ps1

    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = All + " played roles in this movie"
                ts2 = str(len(di[tb[it]])) + \
                    " people played a role in this movie"
                ts3 = "There were more than " + \
                    str(random.randint(
                        0, len(di[tb[it]])-1)) + " stars in this movie"
                ts4 = random.sample(di[tb[it]], 1)[0] + \
                    " was a part of this movie"
                ts5 = random.sample(di[tb[it]], 1)[0] + " did the movie"
                ts6 = random.sample(di[tb[it]], 1)[0] + " signed for the movie"
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 5))
                All = ','.join(NT)
                ts1 = All + " played roles in this movie"
                ts2 = str(len(di[tb[it]])+2) + \
                    " people played a role in this movie"
                ts3 = "There were more than " + \
                    str(random.randint(
                        len(di[tb[it]])+1, len(di[tb[it]])+4)) + " stars in this movie"
                ts4 = random.sample(NT, 1)[0] + " was a part of this movie"
                ts5 = random.sample(NT, 1)[0] + " did the movie"
                ts6 = random.sample(NT, 1)[0] + " signed for the movie"

            return [ts1, ts2, ts3, ts4, ts5, ts6]
        else:
            return [None]


def Music_bySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" composed the music in this movie", "In "+dn[tb[it]][0]+","+All +
                   "composed the music", "Music composers "+All+" worked in the making of this film"]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = "Music was composed by "+All
                ts2 = "Music was composed by more than " + \
                    str(random.randint(0, len(di[tb[it]])-1))+" composers"
                ts3 = "Music was composed by less than " + \
                    str(random.randint(
                        len(di[tb[it]])+1, len(di[tb[it]])+5))+" composers"
                ts4 = random.sample(di[tb[it]], 1)[0] + \
                    " was a composer of the movie"
                ts5 = random.sample(di[tb[it]], 1)[0] + \
                    " created the music for this movie"
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts1 = "Music was composed by " + All
                ts2 = "Music was composed by less than " + \
                    str(random.randint(0, len(di[tb[it]])-1))+" composers"
                ts3 = "Music was composed by more than " + \
                    str(random.randint(
                        len(di[tb[it]])+1, len(di[tb[it]])+5))+" composers"
                ts4 = random.sample(NT, 1)[0]+" was a composer of the movie"
                ts5 = random.sample(NT, 1)[0] + \
                    " created the music for this movie"
            return [ts1, ts2, ts3, ts4, ts5]
        else:
            return [None]


def CinematographySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The cinematographer of "+dn[tb[it]][0]+" was "+All,
                   "In "+dn[tb[it]][0]+" the cinematography was done by "+All]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                ts1 = random.sample(di[tb[it]], 1)[
                    0] + " was a cinematographer in the making of this movie"
                ts2 = "There were " + \
                    str(len(di[tb[it]])) + \
                    " cinematographers involved in the making of this movie"
                ts3 = "There were more than " + \
                    str(random.randint(0, len(
                        di[tb[it]])-1)) + " cinematographers involved in the making of this movie"
                ts4 = "There were less than " + str(random.randint(len(di[tb[it]])+1, len(
                    di[tb[it]])+5)) + " cinematographers involved in the making of this movie"
                ts5 = random.sample(di[tb[it]], 1)[0] + \
                    " knows how to make motion pictures"
                ts6 = random.sample(di[tb[it]], 1)[
                    0]+" knows the art of making motion pictures"
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 2))
                ts1 = random.sample(
                    NT, 1)[0] + " was a cinematographer in the making of this movie"
                ts2 = "There were " + \
                    str(len(di[tb[it]])+2) + \
                    " cinematographers involved in the making of this movie"
                ts3 = "There were less than " + \
                    str(random.randint(0, len(
                        di[tb[it]])-1)) + " cinematographers involved in the making of this movie"
                ts4 = "There were more than " + str(random.randint(len(di[tb[it]])+1, len(
                    di[tb[it]])+5)) + " cinematographers involved in the making of this movie"
                ts5 = random.sample(NT, 1)[0] + \
                    " knows how to make motion pictures"
                ts6 = random.sample(
                    NT, 1)[0]+" knows the art of making motion pictures"
            return [ts1, ts2, ts3, ts4, ts5, ts6]
        else:
            return [None]


def Edited_bySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" edited the movie named "+dn[tb[it]][0], "The movie named "+dn[tb[it]]
                   [0]+" was edited by "+All, All+" were the editors in the movie named "+dn[tb[it]][0]]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = "The movie was edited by " + All
                ts2 = "The movie was edited by " + \
                    str(len(di[tb[it]])) + " editors"
                ts3 = "The movie was edited by more than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " editors"
                ts4 = "The movie was edited by less than " + \
                    str(random.randint(
                        len(di[tb[it]])+1, len(di[tb[it]])+5)) + " editors"
                ts5 = "The movie was cut and paste by " + \
                    random.sample(di[tb[it]], 1)[0]
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 4))
                All = ','.join(NT)
                ts1 = "The movie was edited by " + All
                ts2 = "The movie was edited by " + \
                    str(len(di[tb[it]])+2) + " editors"
                ts3 = "The movie was edited by less than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " editors"
                ts4 = "The movie was edited by more than " + \
                    str(random.randint(
                        len(di[tb[it]])+1, len(di[tb[it]])+5)) + " editors"
                ts5 = "The movie was cut and paste by "+random.sample(NT, 1)[0]
            return [ts1, ts2, ts3, ts4, ts5]
        else:
            return [None]


def ProductioncompanySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The movie named "+All+" was produced by "+dn[tb[it]][0]+" company", All+" company produced the movie named " +
                   dn[tb[it]][0], "The movie named "+dn[tb[it]][0]+" was produced by "+All+" organization"]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = "The movie was produced by " + All
                ts2 = "The movie was produced by " + \
                    str(len(di[tb[it]])) + " producers"
                ts3 = "The movie was funded by " + \
                    random.sample(di[tb[it]], 1)[0]
                ts4 = random.sample(di[tb[it]], 1)[0] + \
                    " company produced the film"
                ts5 = "The movie was produced by more than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " producers"
                ts6 = "The movie was produced by less than " + \
                    str(random.randint(len(di[tb[it]])+1,
                        len(di[tb[it]])+5)) + " producers"
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 4))
                All = ','.join(NT)
                ts1 = "The movie was produced by " + All
                ts2 = "The movie was produced by " + \
                    str(len(di[tb[it]])+2) + " producers"
                ts3 = "The movie was funded by " + random.sample(NT, 1)[0]
                ts4 = random.sample(NT, 1)[0] + " company produced the film"
                ts5 = "The movie was produced by less than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " producers"
                ts6 = "The movie was produced by more than " + \
                    str(random.randint(len(di[tb[it]])+1,
                        len(di[tb[it]])+5)) + " producers"

            return [ts1, ts2, ts3, ts4, ts5, ts6]
        else:
            return [None]


def Distributed_bySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" distributed this movie", "The movie named "+dn[tb[it]][0] +
                   " was distributed by "+All, All+" were the distributors in this movie"]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = "The movie was distributed by " + All
                ts2 = str(len(di[tb[it]])) + " distributors released the film"
                ts3 = random.sample(di[tb[it]], 1)[0] + \
                    " distributor released the film"
                ts4 = "The movie was distributed by more than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " distributors"
                ts5 = "The movie was distributed by less than " + \
                    str(random.randint(len(di[tb[it]])+1,
                        len(di[tb[it]])+5)) + " distributors"
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 4))
                All = ','.join(NT)
                ts1 = "The movie was distributed by " + All
                ts2 = str(len(di[tb[it]])+random.randint(1, 3)
                          ) + " distributors released the film"
                ts3 = random.sample(NT, 1)[0]+" distributor released the film"
                ts4 = "The movie was distributed by less than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " distributors"
                ts5 = "The movie was distributed by more than " + \
                    str(random.randint(len(di[tb[it]])+1,
                        len(di[tb[it]])+5)) + " distributors"

            return [ts1, ts2, ts3, ts4, ts5]
        else:
            return [None]


def Release_dateSent(tb, dn, F, it, tval=True, prem=False):
    d = F[2]
    p = F[3]
    univ = F[0]
    p_univ = F[1]

    def get_d(s):

        ss = s.split('(')
        d = ss[1].replace(')', '').strip().split('-')

        return d

    if (prem):
        if (d[tb[it]][0] != None and len(d[tb[it]][0].split("(")) > 1):
            if (p[tb[it]][0] != None and len(d[tb[it]]) == len(p[tb[it]])):
                All = []
                for i in range(len(d[tb[it]])):
                    All.append(d[tb[it]][i]+"("+p[tb[it]][i]+")")
                All = ",".join(All)
            else:
                All = ",".join(d[tb[it]])
            ps1 = ["The release date of the movie was "+All,
                   "The movie named "+dn[tb[it]][0]+" was released on "+All]
        else:
            ps1 = [None]
        return ps1

    else:
        if (d[tb[it]][0] != None and len(d[tb[it]][0].split("(")) > 1):
            length = len(d[tb[it]])
            i = random.randint(0, length-1)
            s = d[tb[it]][i]
            dt = get_d(s)
            ss = s.split('(')
            date = ss[0].strip()
            ts = []
            if (tval):
                if (len(d[tb[it]]) == len(p[tb[it]]) and p[tb[it]][i] != None):
                    place = p[tb[it]][i]
                    ts.append(dn[tb[it]][0] +
                              " was released on " + date + " in " + place)
                    ts.append("The movie was released in "+place)
                    ts.append("The movie was screened at "+place)
                    if (len(d[tb[it]]) > 2):
                        # two places where the movie was released
                        p1 = random.randint(0, len(d[tb[it]])-2)
                        p2 = random.randint(p1, len(d[tb[it]])-1)
                        # month and year of release of the 2 places
                        d1 = 0
                        d2 = 0
                        if (len(get_d(d[tb[it]][p1])) > 2 and len(get_d(d[tb[it]][p2])) > 2):
                            d1 = int(get_d(d[tb[it]][p1])[2])
                            d2 = int(get_d(d[tb[it]][p2])[2])
                        if (len(get_d(d[tb[it]][p1])) > 1 and len(get_d(d[tb[it]][p2])) > 1):
                            m1 = int(get_d(d[tb[it]][p1])[1])
                            m2 = int(get_d(d[tb[it]][p2])[1])
                        y1 = int(get_d(d[tb[it]][p1])[0])
                        y2 = int(get_d(d[tb[it]][p2])[0])
                        m = str(abs(y2-y1)*12 + abs(m2 - m1))
                        if (y2 > y1 or (y2 == y1 and m2 > m1) or (y2 == y1 and m2 == m1 and d2 > d1)):
                            ts.append("The movie was released in " +
                                      p[tb[it]][p1]+" before "+p[tb[it]][p2])
                            ts.append(
                                "The movie was released in "+p[tb[it]][p1]+","+m+" months before "+p[tb[it]][p2])
                            ts.append(
                                "The movie was released in "+p[tb[it]][p2]+","+m+" months after "+p[tb[it]][p1])
                        else:
                            ts.append("The movie was released in " +
                                      p[tb[it]][p2]+" before "+p[tb[it]][p1])
                            ts.append(
                                "The movie was released in "+p[tb[it]][p2]+","+m+" months before "+p[tb[it]][p1])
                            ts.append(
                                "The movie was released in "+p[tb[it]][p1]+","+m+" months after "+p[tb[it]][p2])
                else:
                    ts.append(dn[tb[it]][0] + " was released on " + date)
                # year
                y = get_d(s)[0]
                ts.append("The movie was released in " + y)
                ts.append(dn[tb[it]][0] +
                          " was released before " + str(int(dt[0])+5))
                ts.append("The movie came on " + date)
                ts.append("In year "+y+", the movie was released")
                if (len(dt) > 2):
                    day = datetime.date(int(dt[0]), int(
                        dt[1]), int(dt[2])).weekday()
                    ts.append(dn[tb[it]][0] +
                              " was released on a " + str(day_of_week[day]))

            else:
                plist = p[tb[it]]
                s = random.sample(d[tb[it]], 1)[0]
                ns = random.sample(list(set(univ)-set(d[tb[it]])), 1)[0]
                nss = ns.split('(')
                ndate = nss[0].strip()
                if (len(d[tb[it]]) == len(p[tb[it]]) and p[tb[it]][0] != None):
                    nplace = random.sample(list(set(p_univ)-set(plist)), 1)[0]
                    ts.append(dn[tb[it]][0] + " was released on " +
                              ndate + " in " + nplace)
                    ts.append("The movie was released in "+nplace)
                    ts.append("The movie was screened at "+nplace)
                    if (len(d[tb[it]]) > 2):
                        # two places where the movie was released
                        p1 = random.randint(0, len(d[tb[it]])-2)
                        p2 = random.randint(p1, len(d[tb[it]])-1)
                        # month and year of release of the 2 places
                        d1 = 0
                        d2 = 0
                        if (len(get_d(d[tb[it]][p1])) > 2 and len(get_d(d[tb[it]][p2])) > 2):
                            d1 = int(get_d(d[tb[it]][p1])[2])
                            d2 = int(get_d(d[tb[it]][p2])[2])
                        if (len(get_d(d[tb[it]][p1])) > 1 and len(get_d(d[tb[it]][p2])) > 1):
                            m1 = int(get_d(d[tb[it]][p1])[1])
                            m2 = int(get_d(d[tb[it]][p2])[1])
                        y1 = int(get_d(d[tb[it]][p1])[0])
                        y2 = int(get_d(d[tb[it]][p2])[0])
                        m = abs(y2-y1)*12 + abs(m2 - m1)
                        if (y2 > y1 or (y2 == y1 and m2 > m1) or (y2 == y1 and m2 == m1 and d2 > d1)):
                            ts.append("The movie was released in " +
                                      p[tb[it]][p2]+" before "+p[tb[it]][p1])
                            ts.append("The movie was released in "+p[tb[it]][p1]+","+str(
                                random.randint(m+1, m+5))+" months after "+p[tb[it]][p2])
                            ts.append("The movie was released in "+p[tb[it]][p2]+","+str(
                                random.randint(m+1, m+5))+" months before "+p[tb[it]][p1])
                        else:
                            ts.append("The movie was released in " +
                                      p[tb[it]][p1]+" before "+p[tb[it]][p2])
                            ts.append("The movie was released in "+p[tb[it]][p2]+","+str(
                                random.randint(m+1, m+5))+" months after "+p[tb[it]][p1])
                            ts.append("The movie was released in "+p[tb[it]][p1]+","+str(
                                random.randint(m+1, m+5))+" months before "+p[tb[it]][p2])
                else:
                    ts.append(dn[tb[it]][0] + " was released on " + ndate)
                # year
                y = int(get_d(s)[0])
                ts.append("The movie was released in " +
                          str(y + random.randint(3, 5)))
                ts.append(dn[tb[it]][0] +
                          " was released before " + str(int(dt[0])-5))
                if (len(dt) > 2):
                    day = datetime.date(int(dt[0]), int(
                        dt[1]), int(dt[2])).weekday()
                    ts.append(dn[tb[it]][0] + " was released on a " +
                              str(day_of_week[(day+2) % 7]))
                ts.append("The movie came on " + ndate)
                ts.append("In year "+str(y + random.randint(3, 5)) +
                          ", the movie was released")

            return ts
        else:
            return [None]


def Running_timeSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            m = re.findall("[0-9]+", di[tb[it]][0])[0]
            ps1 = ["The running time of the movie was "+m+" minutes",
                   "The movie named "+dn[tb[it]][0]+" had a running time of "+m+" minutes"]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                # minutes
                m = re.findall("[0-9]+", di[tb[it]][0])[0]
                ts1 = dn[tb[it]][0] + " runs for " + di[tb[it]][0]
                ts2 = "The movie is  " + m + " minutes long"
                ts3 = 'The movie runs for more than ' + \
                    str(int(m)-random.randint(10, 40)) + " minutes"
                ts4 = 'The movie runs for less than ' + \
                    str(int(m)+random.randint(10, 40)) + " minutes"
            else:
                m = int(re.findall("[0-9]+", di[tb[it]][0])[0])
                ts1 = dn[tb[it]][0] + " runs for " + \
                    str(random.randint(m+1, m+30)) + " minutes"
                ts2 = "The movie is  " + \
                    str(random.randint(m+1, m+30)) + " minutes long"
                ts3 = 'The movie runs for less than ' + \
                    str(int(m)-random.randint(10, 40)) + " minutes"
                ts4 = 'The movie runs for more than ' + \
                    str(int(m)+random.randint(10, 40)) + " minutes"

            return [ts1, ts2, ts3, ts4]
        else:
            return [None]


def CountrySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The production country of the movie was "+All, All +
                   " were the countries in which the production was done", "The production of the movie was done in "+All]
        else:
            ps1 = [None]

        return ps1

    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = dn[tb[it]][0] + " was produced in " + All
                ts2 = "The movie was released in " + \
                    str(len(di[tb[it]])) + ' countries'
                ts3 = "This was produced in more than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " countries"
                ts4 = "This was produced in less than " + \
                    str(random.randint(len(di[tb[it]])+1,
                        len(di[tb[it]])+3)) + " countries"
                ts5 = "This film is an " + \
                    random.sample(di[tb[it]], 1)[0]+" film"
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 2))
                All = ','.join(NT)
                ts1 = dn[tb[it]][0] + " was produced in " + All
                ts2 = "The movie was released in " + \
                    str(len(di[tb[it]])+3) + ' countries'
                ts3 = "This was produced in less than " + \
                    str(random.randint(0, len(di[tb[it]])-1)) + " countries"
                ts4 = "This was produced in more than " + \
                    str(random.randint(len(di[tb[it]])+1,
                        len(di[tb[it]])+3)) + " countries"
                ts5 = "This film is an "+random.sample(NT, 1)[0]+" film"
            return [ts1, ts2, ts3, ts4, ts5]
        else:
            return [None]


def LanguageSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["It is in "+All, All +
                   " are the languages in which it was released"]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts1 = dn[tb[it]][0] + " was released in " + All
                ts2 = dn[tb[it]][0] + " was released in more than " + \
                    str(random.randint(0, len(di[tb[it]])-1))
                ts3 = dn[tb[it]][0] + " was released in less than " + \
                    str(random.randint(len(di[tb[it]])+1, len(di[tb[it]])+5))
                ts4 = "The movie was in "+random.sample(di[tb[it]], 1)[0]
            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 2))
                All = ','.join(NT)
                ts1 = dn[tb[it]][0] + " was released in " + All
                ts2 = dn[tb[it]][0] + " was released in less than " + \
                    str(random.randint(0, len(di[tb[it]])-1))
                ts3 = dn[tb[it]][0] + " was released in more than " + \
                    str(random.randint(len(di[tb[it]])+1, len(di[tb[it]])+5))
                ts4 = "The movie was in "+random.sample(NT, 1)[0]
            return [ts1, ts2, ts3, ts4]
        else:
            return [None]


def BudgetSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" was the budget of this film",
                   All+" was used to make this film"]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                m = re.findall("[0-9.,]+", di[tb[it]][-1].replace(",", ""))[0]
                ts1 = "The movies's budget is " + All
                ts2 = "The movie was made using " + All
                ts3 = All + " was used to make the movie"
                ts4 = "The movie was made within "+All
                ts5 = All + " dollars were invested in the movie"
                ts6 = All + " was the budget of this play"
                ts7 = "The movie's budget is more than $" + \
                    str(random.randint(int(float(m)/3), int(float(m)/1.5)))
                ts8 = "The movie's budget is less than $" + \
                    str(random.randint(int(float(m)*1.5), int(float(m)*2)))
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)
                All = ','.join(NT)
                m = re.findall("[0-9.,]+", di[tb[it]][0].replace(",", ""))[0]
                ts1 = "The movies's budget is " + All
                ts2 = "The movie was made using " + All
                ts3 = All + " was used to make the movie"
                ts4 = "The movie was made within "+All
                ts5 = All + " dollars were invested in the movie"
                ts6 = All + " was the budget of this play"
                ts7 = "The movie's budget is less than $" + \
                    str(random.randint(int(float(m)/3), int(float(m)/1.5)))
                ts8 = "The movie's budget is more than $" + \
                    str(random.randint(int(float(m)*1.5), int(float(m)*2)))

            return [ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8]
        else:
            return [None]


def Box_officeSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ['The box office collection of the movie was ' +
                   All, "It collected "+All+" in box office"]
        else:
            ps1 = [None]
        return ps1
    else:
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                m = re.findall("[0-9][0-9.,]*", di[tb[it]][-1])[0]
                m = m.replace(",", "")
                ts1 = "The movies' box office collection is " + All
                ts2 = "The movies' box office collection is more than $" + \
                    str(random.randint(int(float(m)/3), int(float(m)/2)))
                ts3 = "The movies' box office collection is less than $" + \
                    str(random.randint(int(float(m)*1.5), int(float(m)*2)))
                ts4 = "The movies' revenue is more than $" + \
                    str(random.randint(int(float(m)/3), int(float(m)/2)))
                ts5 = "The movies' revenue is less than $" + \
                    str(random.randint(int(float(m)*1.5), int(float(m)*2)))
                ts6 = "The movie collected " + All
                ts7 = "The movie made " + All
                ts8 = "The gross revenue accrued by the film in its theatrical run is "+All
                ts9 = "The gross revenue of this film was "+All
            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)
                All = ','.join(NT)
                m = re.findall("[0-9][0-9.,]*", di[tb[it]][0])[0]
                m = m.replace(",", "")
                ts1 = "The movies's box office collection is " + All
                ts2 = "The movies' box office collection is less than $" + \
                    str(random.randint(int(float(m)/3), int(float(m)/1.5)))
                ts3 = "The movies' box office collection is more than $" + \
                    str(random.randint(int(float(m)*1.5), int(float(m)*2)))
                ts4 = "The movies' revenue is less than $" + \
                    str(random.randint(int(float(m)/3), int(float(m)/1.5)))
                ts5 = "The movies' revenue is more than $" + \
                    str(random.randint(int(float(m)*1.5), int(float(m)*2)))
                ts6 = "The movie collected " + All
                ts7 = "The movie made " + All
                ts8 = "The gross revenue accrued by the film in its theatrical run is "+All
                ts9 = "The gross revenue of this film was "+All

            return [ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9]
        else:
            return [None]

# 1st multi-row templates


def multi_row1(tb, dn, F, it, tval=True):
    Ud, D = F["Directed_by"]  # Director
    Up, P = F["Produced_by"]  # Producer
    Usp, Sp = F["Screenplay_by"]  # Screen-play by
    Usr, Sr = F["Starring"]  # Starring
    Ued, Ed = F["Edited_by"]  # Edited by
    Um, M = F["Music_by"]  # Music by
    Uc, C = F["Cinematography"]  # Cinematography

    ts = {}

    if (tval):
        if (D[tb[it]][0] != None and P[tb[it]][0] != None):
            ts["Directed_by,Produced_by"] = []
            Al1 = ",".join(D[tb[it]])
            Al2 = ",".join(P[tb[it]])
            ts["Directed_by,Produced_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and produced by "+Al2)
        if (D[tb[it]][0] != None and Sp[tb[it]][0] != None):
            ts["Directed_by,Screenplay_by"] = []
            Al1 = ",".join(D[tb[it]])
            Al2 = ",".join(Sp[tb[it]])
            ts["Directed_by,Screenplay_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and script was written by "+Al2)
        if (D[tb[it]][0] != None and Sr[tb[it]][0] != None):
            ts["Directed_by,Starring"] = []
            Al1 = ",".join(D[tb[it]])
            Al2 = ",".join(Sr[tb[it]])
            ts["Directed_by,Starring"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and starred by "+Al2)
        if (D[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Directed_by,Edited_by"] = []
            Al1 = ",".join(D[tb[it]])
            Al2 = ",".join(Ed[tb[it]])
            ts["Directed_by,Edited_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and edited by "+Al2)
        if (D[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Directed_by,Music_by"] = []
            Al1 = ",".join(D[tb[it]])
            Al2 = ",".join(M[tb[it]])
            ts["Directed_by,Music_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and music was composed by "+Al2)
        if (D[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Directed_by,Cinematography"] = []
            Al1 = ",".join(D[tb[it]])
            Al2 = ",".join(C[tb[it]])
            ts["Directed_by,Cinematography"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and cinematography by "+Al2)

        if (P[tb[it]][0] != None and Sp[tb[it]][0] != None):
            ts["Produced_by,Screenplay_by"] = []
            Al1 = ",".join(P[tb[it]])
            Al2 = ",".join(Sp[tb[it]])
            ts["Produced_by,Screenplay_by"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and script was written by "+Al2)
        if (P[tb[it]][0] != None and Sr[tb[it]][0] != None):
            ts["Produced_by,Starring"] = []
            Al1 = ",".join(P[tb[it]])
            Al2 = ",".join(Sr[tb[it]])
            ts["Produced_by,Starring"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and starred by "+Al2)
        if (P[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Produced_by,Edited_by"] = []
            Al1 = ",".join(P[tb[it]])
            Al2 = ",".join(Ed[tb[it]])
            ts["Produced_by,Edited_by"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and edited by "+Al2)
        if (P[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Produced_by,Music_by"] = []
            Al1 = ",".join(P[tb[it]])
            Al2 = ",".join(M[tb[it]])
            ts["Produced_by,Music_by"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and music was composed by "+Al2)
        if (P[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Produced_by,Cinematography"] = []
            Al1 = ",".join(P[tb[it]])
            Al2 = ",".join(C[tb[it]])
            ts["Produced_by,Cinematography"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and cinematography "+Al2)

        if (Sp[tb[it]][0] != None and Sr[tb[it]][0] != None):
            ts["Screenplay_by,Starring"] = []
            Al1 = ",".join(Sp[tb[it]])
            Al2 = ",".join(Sr[tb[it]])
            ts["Screenplay_by,Starring"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and starred by "+Al2)
        if (Sp[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Screenplay_by,Edited_by"] = []
            Al1 = ",".join(Sp[tb[it]])
            Al2 = ",".join(Ed[tb[it]])
            ts["Screenplay_by,Edited_by"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and edited by "+Al2)
        if (Sp[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Screenplay_by,Music_by"] = []
            Al1 = ",".join(Sp[tb[it]])
            Al2 = ",".join(M[tb[it]])
            ts["Screenplay_by,Music_by"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and music was composed by "+Al2)
        if (Sp[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Screenplay_by,Cinematography"] = []
            Al1 = ",".join(Sp[tb[it]])
            Al2 = ",".join(C[tb[it]])
            ts["Screenplay_by,Cinematography"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and cinematography by "+Al2)

        if (Sr[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Starring,Edited_by"] = []
            Al1 = ",".join(Sr[tb[it]])
            Al2 = ",".join(Ed[tb[it]])
            ts["Starring,Edited_by"].append(
                dn[tb[it]][0]+" was starred by "+Al1+" and edited by "+Al2)
        if (Sr[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Starring,Music_by"] = []
            Al1 = ",".join(Sr[tb[it]])
            Al2 = ",".join(M[tb[it]])
            ts["Starring,Music_by"].append(
                dn[tb[it]][0]+" was starred by "+Al1+" and music was composed by "+Al2)
        if (Sr[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Starring,Cinematography"] = []
            Al1 = ",".join(Sr[tb[it]])
            Al2 = ",".join(C[tb[it]])
            ts["Starring,Cinematography"].append(
                dn[tb[it]][0]+" was starred by "+Al1+" and cinematography by "+Al2)

        if (Ed[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Edited_by,Music_by"] = []
            Al1 = ",".join(Ed[tb[it]])
            Al2 = ",".join(M[tb[it]])
            ts["Edited_by,Music_by"].append(
                dn[tb[it]][0]+" was edited by "+Al1+" and music was composed by "+Al2)
        if (Ed[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Edited_by,Cinematography"] = []
            Al1 = ",".join(Ed[tb[it]])
            Al2 = ",".join(C[tb[it]])
            ts["Edited_by,Cinematography"].append(
                dn[tb[it]][0]+" was edited by "+Al1+" and cinematography by "+Al2)

        if (M[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Music_by,Cinematography"] = []
            Al1 = ",".join(M[tb[it]])
            Al2 = ",".join(C[tb[it]])
            ts["Music_by,Cinematography"].append(
                dn[tb[it]][0]+" music was composed by "+Al1+" and cinematography by "+Al2)

    else:
        if (D[tb[it]][0] != None and P[tb[it]][0] != None):
            ts["Directed_by,Produced_by"] = []
            NT1 = random.sample(
                list(set(Ud)-set(D[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Up)-set(P[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Directed_by,Produced_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and produced by "+Al2)
        if (D[tb[it]][0] != None and Sp[tb[it]][0] != None):
            ts["Directed_by,Screenplay_by"] = []
            NT1 = random.sample(
                list(set(Ud)-set(D[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Usp)-set(Sp[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Directed_by,Screenplay_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and script was written by "+Al2)
        if (D[tb[it]][0] != None and Sr[tb[it]][0] != None):
            ts["Directed_by,Starring"] = []
            NT1 = random.sample(
                list(set(Ud)-set(D[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Usr)-set(Sr[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Directed_by,Starring"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and starred by "+Al2)
        if (D[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Directed_by,Edited_by"] = []
            NT1 = random.sample(
                list(set(Ud)-set(D[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Ued)-set(Ed[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Directed_by,Edited_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and edited by "+Al2)
        if (D[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Directed_by,Music_by"] = []
            NT1 = random.sample(
                list(set(Ud)-set(D[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Um)-set(M[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Directed_by,Music_by"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and music was composed by "+Al2)
        if (D[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Directed_by,Cinematography"] = []
            NT1 = random.sample(
                list(set(Ud)-set(D[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Uc)-set(C[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Directed_by,Cinematography"].append(
                dn[tb[it]][0]+" was directed by "+Al1+" and cinematography by "+Al2)

        if (P[tb[it]][0] != None and Sp[tb[it]][0] != None):
            ts["Produced_by,Screenplay_by"] = []
            NT1 = random.sample(
                list(set(Up)-set(P[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Usp)-set(Sp[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Produced_by,Screenplay_by"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and script was written by "+Al2)
        if (P[tb[it]][0] != None and Sr[tb[it]][0] != None):
            ts["Produced_by,Starring"] = []
            NT1 = random.sample(
                list(set(Up)-set(P[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Usr)-set(Sr[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Produced_by,Starring"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and starred by "+Al2)
        if (P[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Produced_by,Edited_by"] = []
            NT1 = random.sample(
                list(set(Up)-set(P[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Ued)-set(Ed[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Produced_by,Edited_by"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and edited by "+Al2)
        if (P[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Produced_by,Music_by"] = []
            NT1 = random.sample(
                list(set(Up)-set(P[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Um)-set(M[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Produced_by,Music_by"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and music was composed by "+Al2)
        if (P[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Produced_by,Cinematography"] = []
            NT1 = random.sample(
                list(set(Up)-set(P[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Uc)-set(C[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Produced_by,Cinematography"].append(
                dn[tb[it]][0]+" was produced by "+Al1+" and cinematography "+Al2)

        if (Sp[tb[it]][0] != None and Sr[tb[it]][0] != None):
            ts["Screenplay_by,Starring"] = []
            NT1 = random.sample(
                list(set(Usp)-set(Sp[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Usr)-set(Sr[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Screenplay_by,Starring"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and starred by "+Al2)
        if (Sp[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Screenplay_by,Edited_by"] = []
            NT1 = random.sample(
                list(set(Usp)-set(Sp[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Ued)-set(Ed[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Screenplay_by,Edited_by"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and edited by "+Al2)
        if (Sp[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Screenplay_by,Music_by"] = []
            NT1 = random.sample(
                list(set(Usp)-set(Sp[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Um)-set(M[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Screenplay_by,Music_by"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and music was composed by "+Al2)
        if (Sp[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Screenplay_by,Cinematography"] = []
            NT1 = random.sample(
                list(set(Usp)-set(Sp[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Uc)-set(C[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Screenplay_by,Cinematography"].append(
                dn[tb[it]][0]+" was script was written by "+Al1+" and cinematography by "+Al2)

        if (Sr[tb[it]][0] != None and Ed[tb[it]][0] != None):
            ts["Starring,Edited_by"] = []
            NT1 = random.sample(
                list(set(Usr)-set(Sr[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Ued)-set(Ed[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Starring,Edited_by"].append(
                dn[tb[it]][0]+" was starred by "+Al1+" and edited by "+Al2)
        if (Sr[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Starring,Music_by"] = []
            NT1 = random.sample(
                list(set(Usr)-set(Sr[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Um)-set(M[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Starring,Music_by"].append(
                dn[tb[it]][0]+" was starred by "+Al1+" and music was composed by "+Al2)
        if (Sr[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Starring,Cinematography"] = []
            NT1 = random.sample(
                list(set(Usr)-set(Sr[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Uc)-set(C[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Starring,Cinematography"].append(
                dn[tb[it]][0]+" was starred by "+Al1+" and cinematography by "+Al2)

        if (Ed[tb[it]][0] != None and M[tb[it]][0] != None):
            ts["Edited_by,Music_by"] = []
            NT1 = random.sample(
                list(set(Ued)-set(Ed[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Um)-set(M[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Edited_by,Music_by"].append(
                dn[tb[it]][0]+" was edited by "+Al1+" and music was composed by "+Al2)
        if (Ed[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Edited_by,Cinematography"] = []
            NT1 = random.sample(
                list(set(Ued)-set(Ed[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Uc)-set(C[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Edited_by,Cinematography"].append(
                dn[tb[it]][0]+" was edited by "+Al1+" and cinematography by "+Al2)

        if (M[tb[it]][0] != None and C[tb[it]][0] != None):
            ts["Music_by,Cinematography"] = []
            NT1 = random.sample(
                list(set(Um)-set(M[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Uc)-set(C[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(NT1)
            Al2 = ",".join(NT2)
            ts["Music_by,Cinematography"].append(
                dn[tb[it]][0]+" music was composed by "+Al1+" and cinematography by "+Al2)

    return ts

# 2nd multi-row templates


def multi_row2(tb, dn, F, it, tval=True):
    Upc, Pc = F["Productioncompany"]  # Production company
    Udb, Db = F["Distributed_by"]  # Distributed by

    ts = {}

    if (tval):
        if (Pc[tb[it]][0] != None and Db[tb[it]][0] != None):
            ts["Productioncompany,Distributed_by"] = []
            Al1 = ",".join(Pc[tb[it]])
            Al2 = ",".join(Db[tb[it]])
            ts["Productioncompany,Distributed_by"].append(
                Al1+" produced  "+dn[tb[it]][0]+" and was distributed by "+Al2)
    else:
        if (Pc[tb[it]][0] != None and Db[tb[it]][0] != None):
            ts["Productioncompany,Distributed_by"] = []
            NT1 = random.sample(
                list(set(Upc)-set(Pc[tb[it]])), random.randint(1, 2))
            NT2 = random.sample(
                list(set(Udb)-set(Db[tb[it]])), random.randint(1, 2))
            Al1 = ",".join(Pc[tb[it]])
            Al2 = ",".join(NT2)
            ts["Productioncompany,Distributed_by"].append(
                Al1+" produced  "+dn[tb[it]][0]+" and was distributed by "+Al2)

    return ts

# 3rd multi-row templates


def multi_row3(tb, dn, F, it, tval=True):
    Ubud, Bud = F['Budget']  # Budget
    Ubo, Bo = F["Box_office"]  # Box office

    ts = {}
    if (Bud[tb[it]][0] != None and Bo[tb[it]][0] != None):
        ts["Budget,Box_office"] = []
        mbud = float(re.findall("[0-9][0-9.,]*",
                     Bud[tb[it]][-1].replace(",", ""))[0])
        mbo = re.findall("[0-9][0-9.,]*", Bo[tb[it]][-1])[0]
        mbo = float(mbo.replace(",", ""))
        if (tval):
            if (mbud > mbo):
                syn = [" flop", " loss"]
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" was a "+random.sample(syn, 1)[0])
                ts["Budget,Box_office"].append(
                    "This movie had negative earning")
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" lossed "+str(mbud-mbo)+" million")
            else:
                syn = [" hit", " profit"]
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" was a "+random.sample(syn, 1)[0])
                ts["Budget,Box_office"].append(
                    "This movie had positive earning")
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" gained "+str(mbo-mbud)+" million")
        else:
            if (mbud < mbo):
                syn = [" flop", " loss"]
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" was a "+random.sample(syn, 1)[0])
                ts["Budget,Box_office"].append(
                    "This movie had negative earning")
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" lossed "+str(mbo-mbud)+" million")
            else:
                syn = [" hit", " profit"]
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" was a "+random.sample(syn, 1)[0])
                ts["Budget,Box_office"].append(
                    "This movie had positive earning")
                ts["Budget,Box_office"].append(
                    dn[tb[it]][0]+" gained "+str(mbud-mbo)+" million")

    return ts
