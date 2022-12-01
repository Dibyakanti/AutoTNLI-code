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
    category_map[category_map.category.isin(['Festival'])].table_id)


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(
        open(tablesFolder + '/' + filename, encoding="utf8"), 'html.parser')
    keys = []
    keys = [i.text.replace("\xa0", " ")
            for i in soup.find('tr').find_all('th')]
    if (soup.find('caption')):
        keys.insert(0, soup.find('caption').text)
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
    for n in range(35):
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


def get_Type(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Type"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")
                                  [i].strip().strip("."))
                            d[dictionary['Tablename']].append(
                                dictionary[k].split(",")[i].strip().strip("."))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Observed_by(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Observed by"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")
                                  [i].strip().strip("."))
                            d[dictionary['Tablename']].append(
                                dictionary[k].split(",")[i].strip().strip("."))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Frequency(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Frequency"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")
                                  [i].strip().strip("."))
                            d[dictionary['Tablename']].append(
                                dictionary[k].split(",")[i].strip().strip("."))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Celebrations(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Celebrations"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")
                                  [i].strip().strip("."))
                            d[dictionary['Tablename']].append(
                                dictionary[k].split(",")[i].strip().strip("."))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Significance(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Significance"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            if (len(dictionary[k][i]) > 0):
                                u.add(dictionary[k][i])
                                d[dictionary['Tablename']].append(
                                    dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")
                                  [i].strip().strip("."))
                            d[dictionary['Tablename']].append(
                                dictionary[k].split(",")[i].strip().strip("."))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Observances(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Observances"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")
                                  [i].strip().strip("."))
                            d[dictionary['Tablename']].append(
                                dictionary[k].split(",")[i].strip().strip("."))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Date(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Date"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i].replace("\xa0", " "))
                            d[dictionary['Tablename']].append(
                                dictionary[k][i].replace("\xa0", " "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")[
                                  i].strip().strip(".").replace("\xa0", " "))
                            d[dictionary['Tablename']].append(dictionary[k].split(
                                ",")[i].strip().strip(".").replace("\xa0", " "))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Related_to(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Related to"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")
                                  [i].strip().strip("."))
                            d[dictionary['Tablename']].append(
                                dictionary[k].split(",")[i].strip().strip("."))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Also_called(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Also called"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i].replace("\xa0", " "))
                            d[dictionary['Tablename']].append(
                                dictionary[k][i].replace("\xa0", " "))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")[
                                  i].strip().strip(".").replace("\xa0", " "))
                            d[dictionary['Tablename']].append(dictionary[k].split(
                                ",")[i].strip().strip(".").replace("\xa0", " "))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Official_name(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Official name"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i].replace("\u200e", ""))
                            d[dictionary['Tablename']].append(
                                dictionary[k][i].replace("\u200e", ""))
                else:
                    for i in range(len(dictionary[k].split(","))):
                        if (len(dictionary[k].split(",")[i]) > 0):
                            u.add(dictionary[k].split(",")[i].strip().strip(
                                ".").replace("\u200e", ""))
                            d[dictionary['Tablename']].append(dictionary[k].split(
                                ",")[i].strip().strip(".").replace("\u200e", ""))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Begins(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Begins"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k].strip())
                    d[dictionary['Tablename']].append(dictionary[k].strip())

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_Ends(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "Ends"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i])
                            d[dictionary['Tablename']].append(dictionary[k][i])
                else:
                    u.add(dictionary[k].strip())
                    d[dictionary['Tablename']].append(dictionary[k].strip())

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_2021_date(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "2021 date"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i].replace("\xa0", " "))
                            d[dictionary['Tablename']].append(
                                dictionary[k][i].replace("\xa0", " "))
                else:
                    u.add(dictionary[k].strip().replace("\xa0", " "))
                    d[dictionary['Tablename']].append(
                        dictionary[k].strip().replace("\xa0", " "))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_2020_date(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "2020 date"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i].replace("\xa0", " "))
                            d[dictionary['Tablename']].append(
                                dictionary[k][i].replace("\xa0", " "))
                else:
                    u.add(dictionary[k].strip().replace("\xa0", " "))
                    d[dictionary['Tablename']].append(
                        dictionary[k].strip().replace("\xa0", " "))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_2019_date(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "2019 date"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i].replace("\xa0", " "))
                            d[dictionary['Tablename']].append(
                                dictionary[k][i].replace("\xa0", " "))
                else:
                    u.add(dictionary[k].strip().replace("\xa0", " "))
                    d[dictionary['Tablename']].append(
                        dictionary[k].strip().replace("\xa0", " "))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d


def get_2018_date(T, N, fake=False, sel=0):
    u = set([])
    d = {}
    k = "2018 date"
    for n in range(35):
        if (int(table_index[n][1:]) <= 2800):
            dictionary = parseFile(table_index[n]+".html", tablesFolder)
            if (k in dictionary.keys()):
                d[dictionary['Tablename']] = []
                if (type(dictionary[k]) == list):
                    for i in range(len(dictionary[k])):
                        if (len(dictionary[k][i]) > 0):
                            u.add(dictionary[k][i].replace("\xa0", " "))
                            d[dictionary['Tablename']].append(
                                dictionary[k][i].replace("\xa0", " "))
                else:
                    u.add(dictionary[k].strip().replace("\xa0", " "))
                    d[dictionary['Tablename']].append(
                        dictionary[k].strip().replace("\xa0", " "))

            else:
                d[dictionary['Tablename']] = []
                d[dictionary['Tablename']].append(None)
    if (fake):
        for it in range(35):  # for getting all the fakes in one go
            sel = random.sample(
                FakeDICT_helper["Festival"][k.replace(" ", "_")], 1)[0]
            if (sel == 2 and len(d[T[it]]) < 2):
                sel = 1
            d = FakeDICT(T, N, u, d, it, sel)

    return list(u), d

# Extract all data :


def get_Data(fake=False):

    Extracted_data = {}
    Keys = ["Type", "Observed_by", "Frequency", "Celebrations", "Significance", "Observances", "Date", "Related_to",
            "Also_called", "Official_name", "Begins", "Ends", "2021_date", "2020_date", "2019_date", "2018_date"]
    for k in Keys:
        Extracted_data[k] = []
        for l in eval("get_"+k)(T, N, fake):
            Extracted_data[k].append(l)

    return Extracted_data

# Sentence generator :


def TypeSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    length = len(di[tb[it]])
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [Nm+" is of "+All+" type", All +
                   (" are" if length > 1 else " is")+" the type(s) "+Nm+" festival"]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" is a "+All+" festival")
                ts.append("This festival is of more than " +
                          str(random.randint(0, length-1))+" characteristics")
                ts.append("This festival is of less than " +
                          str(random.randint(length+1, length+5))+" characteristics")
                ts.append(
                    Nm+" is a "+random.sample(di[tb[it]], 1)[0]+" festival")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" is a "+All+" festival")
                ts.append("This festival is of less than " +
                          str(random.randint(0, length-1))+" characteristics")
                ts.append("This festival is of more than " +
                          str(random.randint(length+1, length+5))+" characteristics")
                ts.append(Nm+" is a "+random.sample(NT, 1)[0]+" festival")
        else:
            ts.append(None)

        return ts


def Observed_bySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The festival is observed by " +
                   All, All+" observe "+Nm+" festival"]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" is celebrated by "+All)
                ts.append(Nm+" is celebrated by more than " +
                          str(random.randint(0, length-1))+" groups")
                ts.append(Nm+" is celebrated by less than " +
                          str(random.randint(length+1, length+5))+" groups")
                ts.append(Nm+" is celebrated by " +
                          ("single" if length == 1 else "multiple")+" groups")
                ts.append(Nm+" celebrate " +
                          random.sample(di[tb[it]], 1)[0]+" festival")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" is celebrated by "+All)
                ts.append(Nm+" is celebrated by more than " +
                          str(random.randint(0, length-1))+" groups")
                ts.append(Nm+" is celebrated by less than " +
                          str(random.randint(length+1, length+5))+" groups")
                ts.append(Nm+" is celebrated by " +
                          ("single" if length == 1 else "multiple")+" groups")
                ts.append(Nm+" celebrate "+random.sample(NT, 1)[0]+" festival")

        else:
            ts.append(None)

        return ts


def FrequencySent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The frequency of this festival is "+All,
                   All+" is the frequency of this festival"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" is a "+All+" festival")
                if (re.findall("annual", All)):
                    ts.append(Nm+" is celebrated "+All+"ly")

            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)
                All = ','.join(NT)
                ts.append(Nm+" is a "+All+" festival")
                if (re.findall("annual", All)):
                    syn = [" every day", " every month",
                           " weekly", " every Sunday", " bimonthly"]
                    ts.append(Nm+" is celebrated"+random.sample(syn, 1)[0])

        else:
            ts.append(None)

        return ts


def CelebrationsSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The festival involves celebrating "+All,
                   All+" are the celebrations of this festival"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append("The festival involves " +
                          random.sample(di[tb[it]], 1)[0])
                ts.append("The festival involves more than " +
                          str(random.randint(0, length-1))+" rituals")
                ts.append("The festival involves less than " +
                          str(random.randint(length+1, length+5))+" rituals")
                ts.append("There are "+str(length)+" rituals in this festival")
                ts.append(Nm+" is celebrated by "+All)

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append("The festival involves "+random.sample(NT, 1)[0])
                ts.append("The festival involves less than " +
                          str(random.randint(0, length))+" rituals")
                ts.append("The festival involves more than " +
                          str(random.randint(length+1, length+5))+" rituals")
                ts.append("There are "+str(random.randint(length +
                          1, length+5))+" rituals in this festival")
                ts.append(Nm+" is celebrated by "+All)

        else:
            ts.append(None)

        return ts


def SignificanceSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The significance of "+Nm+" festival are "+All, All+" are the significance of the " +
                   Nm+" festival", "Because of "+All+" the festival "+Nm+" is observed"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append("The festival is celebrated because "+All)
                ts.append("The festival "+Nm+" is celebrated to acknowledge " +
                          random.sample(di[tb[it]], 1)[0])
                ts.append("The festival is celebrated to mark "+All)
                ts.append("The festival is observed because of " +
                          random.sample(di[tb[it]], 1)[0])
                ts.append("The festival "+Nm +
                          " is celebrated due to "+str(length)+" reasons")
                ts.append("The festival is celebrated because of more than " +
                          str(random.randint(0, length-1))+" reasons")
                ts.append("The festival is celebrated because of less than " +
                          str(random.randint(length+1, length+5))+" reasons")
                ts.append("The festival is celebrated because of " +
                          ("single reason" if length == 1 else "multiple reasons"))

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append("The festival is celebrated because "+All)
                ts.append(
                    "The festival "+Nm+" is celebrated to acknowledge "+random.sample(NT, 1)[0])
                ts.append("The festival is celebrated to mark "+All)
                ts.append("The festival is observed because of " +
                          random.sample(NT, 1)[0])
                ts.append("The festival "+Nm+" is celebrated due to " +
                          str(random.randint(length+1, length+6))+" reasons")
                ts.append("The festival is celebrated because of less than " +
                          str(random.randint(0, length))+" reasons")
                ts.append("The festival is celebrated because of more than " +
                          str(random.randint(length, length+5))+" reasons")
                ts.append("The festival is celebrated because of " +
                          ("single reason" if length != 1 else "multiple reasons"))

        else:
            ts.append(None)

        return ts


def ObservancesSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" rituals are observed in this festival",
                   All+" are the observances in "+Nm]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" is celebrated by " +
                          random.sample(di[tb[it]], 1)[0])
                ts.append(All+" are observed in "+Nm)
                ts.append(Nm+" is celebrated by more than " +
                          str(random.randint(0, length-1))+" rituals")
                ts.append(Nm+" is celebrated by less than " +
                          str(random.randint(length+1, length+5))+" rituals")
                ts.append(Nm+" is observed by celebrating " +
                          ("single ritual" if length == 1 else "multiple rituals"))

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" is celebrated by "+random.sample(NT, 1)[0])
                ts.append(All+" are observed in "+Nm)
                ts.append(Nm+" is celebrated by less than " +
                          str(random.randint(0, length))+" rituals")
                ts.append(Nm+" is celebrated by more than " +
                          str(random.randint(length, length+5))+" rituals")
                ts.append(Nm+" is observed by celebrating " +
                          ("single ritual" if length != 1 else "multiple rituals"))

        else:
            ts.append(None)

        return ts


def DateSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [All+" is when "+Nm+" is celebrated",
                   "On "+All+", "+Nm+" is celebrated"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append("The festival is celebrated on " +
                          ",".join(random.sample(di[tb[it]], random.randint(1, length))))

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append("The festival is celebrated on " +
                          ",".join(random.sample(NT, random.randint(1, len(NT)))))

        else:
            ts.append(None)

        return ts


def Related_toSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [Nm+" is related to "+All, All+" is related to "+Nm]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(
                    Nm+" is similar to "+",".join(random.sample(di[tb[it]], random.randint(1, length))))
                ts.append(random.sample(di[tb[it]], 1)[0]+" is similar to "+Nm)
                ts.append("The festival is similar to " +
                          ",".join(random.sample(di[tb[it]], random.randint(1, length))))
                ts.append(Nm+" is celebrated in line with " +
                          ",".join(random.sample(di[tb[it]], random.randint(1, length))))
                ts.append(Nm+" is similar to more than " +
                          str(random.randint(0, length-1))+" festivals")
                ts.append(Nm+" is similar to less than " +
                          str(random.randint(length+1, length+5))+" festivals")
                ts.append(
                    Nm+" is similar to "+("single festival" if length == 1 else "multiple festivals"))
                ts.append(
                    Nm+" and "+random.sample(di[tb[it]], 1)[0]+" are similar")
                ts.append("Following festivals "+All +
                          " are similar to each other")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 4))
                All = ','.join(NT)
                ts.append(Nm+" is similar to " +
                          ",".join(random.sample(NT, random.randint(1, len(NT)))))
                ts.append(random.sample(NT, 1)[0]+" is similar to "+Nm)
                ts.append("The festival is similar to " +
                          ",".join(random.sample(NT, random.randint(1, len(NT)))))
                ts.append(Nm+" is celebrated in line with " +
                          ",".join(random.sample(NT, random.randint(1, len(NT)))))
                ts.append(Nm+" is similar to less than " +
                          str(random.randint(0, length))+" festivals")
                ts.append(Nm+" is similar to more than " +
                          str(random.randint(length, length+5))+" festivals")
                ts.append(
                    Nm+" is similar to "+("single festival" if length != 1 else "multiple festivals"))
                ts.append(Nm+" and "+random.sample(NT, 1)[0]+" are similar")
                ts.append("Following festivals "+All +
                          " are similar to each other")

        else:
            ts.append(None)

        return ts


def Also_calledSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [Nm+" is also called "+All, All+" is also called "+Nm]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append("The festival is also called as "+All)
                ts.append("There is at least one more name of "+Nm+" festival")
                ts.append(Nm+" is also known as " +
                          ",".join(random.sample(di[tb[it]], random.randint(1, length))))
                syn = [" alternate ", " other name "]
                ts.append(Nm+" is the"+random.sample(syn, 1)[0]+"of "+",".join(
                    random.sample(di[tb[it]], random.randint(1, length))))
                ts.append(Nm+" is known by more than " +
                          str(random.randint(0, length-1))+" names")
                ts.append(Nm+" is known by less than " +
                          str(random.randint(length+1, length+5))+" names")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 4))
                All = ','.join(NT)
                ts.append("The festival is also called as "+All)
                ts.append("There is at least one more name of "+Nm+" festival")
                ts.append(Nm+" is also known as " +
                          ",".join(random.sample(NT, random.randint(1, len(NT)))))
                syn = [" alternate ", " other name "]
                ts.append(Nm+" is the"+random.sample(syn, 1)[0]+"of "+",".join(
                    random.sample(di[tb[it]], random.randint(1, length))))
                ts.append(Nm+" is known by less than " +
                          str(random.randint(0, length))+" names")
                ts.append(Nm+" is known by more than " +
                          str(random.randint(length, length+5))+" names")
        else:
            ts.append(None)

        return ts


def Official_nameSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The official name of the festival "+Nm+" is " +
                   All, "The common name of the festival "+All+" is "+Nm]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(All+" is the primary name of the festival")
                ts.append(Nm+" is also known by "+All)
                ts.append(All+" is also known by "+Nm)
                syn = [" alternate ", " other name "]
                ts.append(Nm+" is the"+random.sample(syn, 1)[0]+"of "+All)
                ts.append("The festival "+Nm+" is also called as "+All)
                ts.append("There is at least one more name of " +
                          random.sample([Nm, All], 1)[0]+" festival")
                ts.append("The common name of "+All+" is "+Nm)

            else:
                NT = random.sample(list(set(univ)-set(di[tb[it]])), 1)
                All = ','.join(NT)
                ts.append(All+" is the primary name of the festival")
                ts.append(Nm+" is also known by "+All)
                ts.append(All+" is also known by "+Nm)
                syn = [" alternate ", " other name "]
                ts.append(Nm+" is the"+random.sample(syn, 1)[0]+"of "+All)
                ts.append("The festival "+Nm+" is also called as "+All)
                ts.append("There is at least one more name of " +
                          random.sample([All], 1)[0]+" festival")
                ts.append("The common name of "+All+" is "+Nm)

        else:
            ts.append(None)

        return ts


def BeginsSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    syn = [" start", " initiate"]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [Nm+" begins on "+All, All+" is when the festival begins"]
        else:
            ps1 = [None]
        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" is"+random.sample(syn, 1)[0]+"ed on "+All)
                ts.append(Nm+random.sample(syn, 1)[0]+"s at "+All)

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" is"+random.sample(syn, 1)[0]+"ed on "+All)
                ts.append(Nm+random.sample(syn, 1)[0]+"s at "+All)

        else:
            ts.append(None)

        return ts


def EndsSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    syn = [" goes on ", " runs "]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = [Nm+" ends on "+All, All+" is when this festival ends "]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+random.sample(syn, 1)[0]+"till "+All)

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+random.sample(syn, 1)[0]+"till "+All)

        else:
            ts.append(None)

        return ts


# give the year to use it for example 21,20,19,18
def _2021_dateSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The 2021 date of the festival was " +
                   All, Nm+" 2021 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" was celebrated on "+All+" in "+str(2021))
                ts.append(
                    Nm+" was celebrated on different date in different year")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" was celebrated on "+All+" in "+str(2021))
                ts.append(
                    Nm+" was celebrated on different date in different year")

        else:
            ts.append(None)

        return ts


def _2020_dateSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The 2020 date of the festival was " +
                   All, Nm+" 2020 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" was celebrated on "+All+" in "+str(2020))
                ts.append(
                    Nm+" was celebrated on different date in different year")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" was celebrated on "+All+" in "+str(2020))
                ts.append(
                    Nm+" was celebrated on different date in different year")

        else:
            ts.append(None)

        return ts


def _2019_dateSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The 2019 date of the festival was " +
                   All, Nm+" 2019 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" was celebrated on "+All+" in "+str(2019))
                ts.append(
                    Nm+" was celebrated on different date in different year")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" was celebrated on "+All+" in "+str(2019))
                ts.append(
                    Nm+" was celebrated on different date in different year")

        else:
            ts.append(None)

        return ts


def _2018_dateSent(tb, dn, F, it, tval=True, prem=False):
    di = F[1]
    univ = F[0]
    Nm = dn[tb[it]][0]
    if (prem):
        if (di[tb[it]][0] != None):
            All = ','.join(di[tb[it]])
            ps1 = ["The 2018 date of the festival was " +
                   All, Nm+" 2018 date was "+All]
        else:
            ps1 = [None]

        return ps1
    else:
        ts = []
        if (di[tb[it]][0] != None):
            length = len(di[tb[it]])
            if (tval):
                All = ','.join(di[tb[it]])
                ts.append(Nm+" was celebrated on "+All+" in "+str(2018))
                ts.append(
                    Nm+" was celebrated on different date in different year")

            else:
                NT = random.sample(
                    list(set(univ)-set(di[tb[it]])), random.randint(1, 3))
                All = ','.join(NT)
                ts.append(Nm+" was celebrated on "+All+" in "+str(2018))
                ts.append(
                    Nm+" was celebrated on different date in different year")

        else:
            ts.append(None)

        return ts


# 1st multi-row templates
def multi_row1(tb, dn, F, it, tval=True):

    Nm = dn[tb[it]][0]

    def Y1_2(t1, t2, tval):

        f1 = F[str(t1)+"_date"]
        f2 = F[str(t2)+"_date"]
        u1, y1 = f1
        u2, y2 = f2
        if (y1[tb[it]][0] != None and y2[tb[it]][0] != None):
            if (tval):
                Al1 = ",".join(y1[tb[it]])
                Al2 = ",".join(y2[tb[it]])
            else:
                n1 = random.sample(list(set(u1)-set(y1[tb[it]])), 1)
                n2 = random.sample(list(set(u2)-set(y2[tb[it]])), 1)
                Al1 = ",".join(n1)
                Al2 = ",".join(n2)

            return (Nm+" was celebrated on "+Al1+" in "+str(t1)+" and on "+Al2+" in "+str(t2))
        else:

            return None

    ts = {}
    if (tval):
        for i in [2018, 2019, 2020]:
            for j in [2019, 2020, 2021]:
                if (Y1_2(i, j, tval) != None and i != j):
                    ts[str(i)+"_date"+","+str(j)+"_date"] = []
                    ts[str(i)+"_date"+","+str(j) +
                       "_date"].append(Y1_2(i, j, tval))

    else:
        for i in [2018, 2019, 2020]:
            for j in [2019, 2020, 2021]:
                if (Y1_2(i, j, tval) != None and i != j):
                    ts[str(i)+"_date"+","+str(j)+"_date"] = []
                    ts[str(i)+"_date"+","+str(j) +
                       "_date"].append(Y1_2(i, j, tval))

    return ts


# 2nd multi-row templates
def multi_row2(tb, dn, F, it, tval=True):
    Uo, O = F["Official_name"]
    Ua, A = F["Also_called"]

    ts = {}
    if (tval):
        if (O[tb[it]][0] != None and A[tb[it]][0] != None):
            ts["Official_name,Also_called"] = []
            Al1 = ",".join(random.sample(O[tb[it]], 1))
            Al2 = ",".join(random.sample(A[tb[it]], 1))
            ts["Official_name,Also_called"].append(Al1+" is also called "+Al2)
            ts["Official_name,Also_called"].append(
                Al2+" is a common name of "+Al1)

    else:
        if (O[tb[it]][0] != None and A[tb[it]][0] != None):
            ts["Official_name,Also_called"] = []
            Al1 = ",".join(random.sample(list(set(Uo)-set(O[tb[it]])), 1))
            Al2 = ",".join(random.sample(list(set(Ua)-set(O[tb[it]])), 1))
            ts["Official_name,Also_called"].append(Al1+" is also called "+Al2)
            ts["Official_name,Also_called"].append(
                Al2+" is a common name of "+Al1)

    return ts


# 3rd multi-row templates
def multi_row3(tb, dn, F, it, tval=True):
    Uo, O = F["Observances"]
    Us, S = F["Significance"]
    Uc, C = F["Celebrations"]

    Nm = dn[tb[it]][0]
    ts = {}
    if (tval):
        if (O[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Observances,Significance"] = []
            Al1 = ",".join(random.sample(O[tb[it]], 1))
            Al2 = ",".join(random.sample(S[tb[it]], 1))
            ts["Observances,Significance"].append(
                Al1+" is observed to signify "+Al2)
            ts["Observances,Significance"].append(Al2+" is signified by "+Al1)

        if (C[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Celebrations,Significance"] = []
            Al1 = ",".join(random.sample(C[tb[it]], 1))
            Al2 = ",".join(random.sample(S[tb[it]], 1))
            ts["Celebrations,Significance"].append(
                Al1+" is celebrated to signify "+Al2)
            ts["Celebrations,Significance"].append(Al2+" is signified by "+Al1)

    else:
        if (O[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Observances,Significance"] = []
            Al1 = ",".join(random.sample(list(set(Uo)-set(O[tb[it]])), 1))
            Al2 = ",".join(random.sample(list(set(Us)-set(S[tb[it]])), 1))
            ts["Observances,Significance"].append(
                Al1+" is observed to signify "+Al2)
            ts["Observances,Significance"].append(Al2+" is signified by "+Al1)

        if (C[tb[it]][0] != None and S[tb[it]][0] != None):
            ts["Celebrations,Significance"] = []
            Al1 = ",".join(random.sample(list(set(Uo)-set(O[tb[it]])), 1))
            Al2 = ",".join(random.sample(list(set(Us)-set(S[tb[it]])), 1))
            ts["Celebrations,Significance"].append(
                Al1+" is celebrated to signify "+Al2)
            ts["Celebrations,Significance"].append(Al2+" is signified by "+Al1)

    return ts
