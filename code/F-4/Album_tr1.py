#!/usr/bin/env python
# coding: utf-8

# In[62]:


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import math
import sys
import json


if './' not in sys.path:
    sys.path.append('./')


# In[63]:


# from Album import *
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
import spacy
import random
import datetime
from dateutil.parser import parse
import dateparser
import calendar
from math import ceil
import numpy as np
import json
import pendulum

nlp = spacy.load("en_core_web_sm")


def readInputFile(filename):
    colnames=['TABLE', 'CATEGORY']
    df = pd.read_csv(filename, sep='\t', names = colnames)
    return df

def getCategoryTables(df, categoryName):
    isCategory = df['CATEGORY'] == categoryName
    filtered = df[isCategory == True]
    return filtered['TABLE'].tolist()


def parseFile(filename, tablesFolder):
    soup = BeautifulSoup(open(tablesFolder + '/' + filename), 'html.parser')
    keys =[i.text for i in soup.find('tr').find_all('th')]
    vals = []
    for i in soup.find('tr').find_all('td'):
        result = [val.text.strip().replace("\n", "").replace("\t", "") for val in i.find_all('li')]
        if not result:
            if "â€“" in i.text:
                result = [val.strip().replace("\n", "").replace("\t", "") for val in i.text.split("â€“")]
            elif "â€”" in i.text:
                result = [val.strip().replace("\n", "").replace("\t", "") for val in i.text.split("â€”")]
            else:
                result = i.text.strip().replace("\n", "").replace("\t", "")
        vals.append(result)
    title = keys[0]
    dictionary = dict(zip(keys[1:], vals))
    dictionary["Title"] = title
    dictionary["Tablename"] = filename.split(".")[0]
    return dictionary


class Value:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.tag = None
        doc = nlp(str(val))
        self.original = None
        self.adverse = None
        for entity in doc.ents:
            self.tag = entity.label_
            break
        if key == "Tablename": self.tag = "ID"


def reformDict(dictionary):
    for key, val in dictionary.items():
        dictionary[key] = Value(key, val)
    return dictionary


def generateRandom(start, end):
    return random.randint(start, end)
    

def getDate(val):
    months = {
        "January":1,
        "February":2,
        "March":3,
        "April":4,
        "May":5,
        "June":6,
        "July":7,
        "August":8,
        "September":9,
        "October":10,
        "November":11,
        "December ":12
    }


    result = None
    #if multiple values
    if type(val) == list:
        #date of format 18 October 2011(18 - 10 - 11)
        if "(" in val[0]:
            val = val[0].split("(")[0]
        #dates of format("october 2100, march 2018")
        else:
            val = val[-1]
    #date of format 18 October 2011 ( 18 - 10 - 11)
    elif "(" in val:
        val = val.split("(")[0].strip()    
    try:
        # to ignore values like 15, 
        if len(val) > 2:
            #parses into date time format
            datetime_obj = dateparser.parse(val, settings={'STRICT_PARSING': True})
            splits = (str(datetime_obj).split()[0]).split("-")
            day, month, year = splits[2], splits[1], splits[0]
            result = (day, month, year)
    except:
        result = None
    
    if len(val) == 4 and int(val) > 1500:
        result = None
    
    if not result:
        #1. Month Year
        splits = val.split()
        if len(splits) == 2 and splits[0].replace(",","").strip() in months.keys() and int(splits[1]) > 1500:
            month, year = splits[0].replace(",","").strip(), splits[1]
            result = ((None, months[month], year))
        # Year
        elif len(splits) == 1 and int(splits[0]) > 1500:
            year = splits[0]
            result = (None, None, year)
    return result
    

def preprocessDate(dictionary):
    months_list = set()
    years_list = set()
    days_list = set()
    for k, v in dictionary.items():
        if v.tag == "DATE": 
            if k == "Recorded":
                date_start = getDate(v.val[0])
                date_ended = getDate(v.val[1])
                v.original = [date_start, date_ended]
                if date_start:
                    if date_start[0]: days_list.add(date_start[0])
                    if date_start[1]: months_list.add(date_start[1])
                    if date_start[2]: years_list.add(date_start[2])
                if date_ended:
                    if date_ended[0]: days_list.add(date_ended[0])
                    if date_ended[1]: months_list.add(date_ended[1])
                    if date_ended[2]: years_list.add(date_ended[2])
            else:
                result = getDate(v.val)
                if result:
                    v.original = result
                    if result[0] :days_list.add(result[0])
                    if result[1]: months_list.add(result[1])
                    if result[2]: years_list.add(result[2])
    
    for k, v in dictionary.items():
        
        if v.tag == "DATE" and v.original: 
            days_start_adverse, month_start_adverse, year_start_adverse = set(), set(), set()
            days_ended_adverse, month_ended_adverse, year_ended_adverse = set(), set(), set()
            if k == "Recorded":
                date_start = v.original[0]
                date_ended = v.original[1]
                for day in days_list:
                    if day != date_start[0]: days_start_adverse.add(day)
                    if day != date_start[0]: days_ended_adverse.add(day)
                for month in months_list:
                    if month != date_start[1]: month_start_adverse.add(month)
                    if month != date_start[1]: month_ended_adverse.add(month)
                for year in years_list:
                    if year != date_start[2]: year_start_adverse.add(year)
                    if year != date_start[2]: year_ended_adverse.add(year)
                v.adverse = [[days_start_adverse, month_start_adverse, year_start_adverse],
                             [days_ended_adverse, month_ended_adverse, year_ended_adverse]]
            else:
                days_adv, months_adv, years_adv = set(), set(), set()
                for day in days_list:
                    if day != v.original[0]:
                        days_adv.add(day)
                for month in months_list:
                    if month != v.original[1]:
                        months_adv.add(month)
                for year in years_list:
                    if year != v.original[2]:
                        years_adv.add(year)
                v.adverse = [days_adv, months_adv, years_adv]


def albumDateOuputGenerator(name, key, indicator, func_keyword, data, truth_value):
    '''
    indicator: 1 - > day based, 2-> leap year, 3-> odd/even, 4-> dateBased, 5-> ecentury, 6-> orderBased, 7-> weekMonth
    '''
    if not data: data.append("X")
    template = {
        1: str(data[0]),
        2: "a " + str(data[0]) + " year.",
        3: "an " + str(data[0]) + " day.",
        5: str(data[0]) + "th century."
    }
    if indicator == 4:
        if len(data) == 3: template[4] = str(data[0]) + " of " + str(data[1]) + " in " + str(data[2]) + "."
        elif len(data) == 2: template[4]= str(data[0]) + " in " + str(data[1]) + "."
        else: template[4] = str(data[0]) + "."
    elif indicator == 6:
        if len(data) == 3: template[6] = data[0] + " " + getMonth(int(data[1])) + ", " + data[2] + "."
        elif len(data) == 2: template[6]= getMonth(int(data[0])) + ", " + data[1] + "."
        else: template[6] = data[0] + "."
        result = []    
        if key == "recording started":
            result.append("The recording of the album started " + " " + func_keyword + " " + template[indicator] + " " + truth_value)
        elif key == "recording ended":
            result.append("The recording of the album ended " + " " + func_keyword + " " + template[indicator] + " " + truth_value)
        return result   
    elif indicator == 7:
        template[7] = data[0] + " week of " + data[1] + " in " + data[2]
    
#     prefixes = ["It was ", "The album was ", "The album \"" +name + "\" was "]
    prefixes = ["The album \"" +name + "\" was "]
    result = []
    for prefix in prefixes:
        # print (prefix + key + " " + func_keyword + " " + template[indicator] + " " + truth_value)
        result.append(prefix + key + " " + func_keyword + " " + template[indicator] + " " + truth_value)
    return result


def dayBasedSentenceGenerator(day, name, key):
    result = []
    days = []
    
    randomDay = generateRandom(0, 6)
    while randomDay == day:
        randomDay = generateRandom(0,6)
    days.append((calendar.day_name[randomDay], False))
    days.append((calendar.day_name[day], True))
    for day, truthVal in days:
        result = result + albumDateOuputGenerator(name, key.lower(), 1, "on", [day], str(truthVal))
    return result


def week_of_month(dt):
    if (dt.month < 10):
        month = "0"+str(dt.month)
    else:
        month = str(dt.month)
    if (dt.day < 10):
        day = "0"+str(dt.day)
    else:
        day = str(dt.day)  
    year = str(dt.year)
    curr_date = year + "-" + month + "-" + day
    week_number = pendulum.parse(curr_date).week_of_month
    if(week_number<0 or week_number>5):
        week_number = 5
    return week_number


def dayBased(value, name):
    date = " ".join(x for x in value.original)
    day = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    d = datetime.datetime.strptime(date, '%d %m %Y')
    return dayBasedSentenceGenerator(day, name, value.key)



def leapYear(value, name):
    leap, result = False, []
    if calendar.isleap(int(value.original[2])): leap = True
    key = value.key.lower()    
    result += albumDateOuputGenerator(name, key, 2, "in", ["leap"], str(leap))
    result += albumDateOuputGenerator(name, key, 2, "in", ["non leap"], str(not leap))
    return result



def oddEvenBased(value, name):
    even, result = False, []
    key = value.key.lower()
    if int(value.original[0]) % 2 == 0:
        even = True    
    result += albumDateOuputGenerator(name, key, 3, "on", ["even"], str(even))
    result += albumDateOuputGenerator(name, key, 3, "on", ["odd"], str(not even))
    return result


def getMonth(num):
    reverseMap = {
        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "November",
        12 : "December"
    }
    return reverseMap[num]


# In[20]:


def dateChange(value, name):
    day, month, year = value.original
    if month: month_str = getMonth(int(month))
    adv_days, adv_months, adv_years = value.adverse
    fake_days, fake_months, fake_years = [], [], []
    key = value.key.lower()
    result = []
    if day:
        if not adv_days:
            val = generateRandom(1, 31)
            while val == day:
                val = generateRandom(1, 31)
            fake_days.append(str(val))
        else:
            for day2 in adv_days:
                fake_days.append(day2)
        for fake_day in fake_days:  
            result += albumDateOuputGenerator(name, key, 4, "on", [fake_day, month_str, year], str(False))
        result += albumDateOuputGenerator(name, key, 4, "on", [day, month_str, year], str(True))
    if month:
        if not adv_months:
            val = generateRandom(1, 12)
            while val == month:
                val = generateRandom(1, 12)
            fake_months.append(val)
        else:
            for month_a in adv_months:
                fake_months.append(int(month_a))
            #month and day
        if day: 
            for fake_month in fake_months:
                fake_month_str = getMonth(fake_month)
                result += albumDateOuputGenerator(name, key, 4, "on", [ day, fake_month_str, year], str(False))
        #only month and not day - add true ones for this case
        else:
            for fake_month in fake_months:
                fake_month_str = getMonth(fake_month)
                result += albumDateOuputGenerator(name, key, 4, "in", [ fake_month_str, year], str(False))
            month_str = getMonth(int(month))
            result += albumDateOuputGenerator(name, key, 4, "in", [ month_str, year], str(True))
    if year:
        if not adv_years:
            val = generateRandom(int(year) - 5, int(year) + 5)
            while val == year:
                val = generateRandom(int(year) - 5, int(year) + 5)
            fake_years.append(val)
        else:
            for year_a in adv_years:
                fake_years.append(year_a)
            #if day and month both present
        if day and month:
            for fake_year in fake_years:
                result += albumDateOuputGenerator(name, key, 4, "in", [ day, month_str, fake_year], str(False))
            # if not day but month and year present
        elif not day and month:
            for fake_year in fake_years:
                result += albumDateOuputGenerator(name, key, 4, "in", [ month_str, fake_year], str(False))
        elif not day and not month:
            for fake_year in fake_years:
                result += albumDateOuputGenerator(name, key, 4, "in", [fake_year], str(False))
            result += albumDateOuputGenerator(name, key, 4, "in", [year], str(True))
    return result
   


# In[21]:


def centuryBased(value, name):
    
    result = []
    year = value.original[2]
    century = int(year[0] + year[1]) + 1
    fake_century = set()
    key = value.key.lower()
    if value.adverse[2]:
        for year_a in value.adverse[2]:
            fake_cent = int(year_a[0] + year_a[1]) + 1
            if fake_cent != century:
                fake_century.add(fake_cent)
    if len(fake_century) == 0:
        fake_cent = generateRandom(century-2, century + 2)
        while fake_cent == century:
            fake_cent = generateRandom(century-2, century+ 2)
        fake_century.add(fake_cent)
    for fake_cent in fake_century:
        result += albumDateOuputGenerator(name, key, 5, "in", [str(fake_cent)], str(False))
    result += albumDateOuputGenerator(name, key, 5, "in", [str(century)], str(True))            
    return result


# In[22]:


def orderBased(value, name, key, original_val, adverse_val):
    # print("Adverse val:", adverse_val)
    # print("original:", original_val)
    result = []
    day, month, year = original_val
    adv_days, adv_months, adv_years = adverse_val
    generation_set = {}
    if year:
        less_year, greater_year = None, None
        if adv_years:
            adv_year = int(adv_years.pop())
            if adv_year > int(year): greater_year = adv_year
            elif adv_year < int(year): less_year = adv_year
        if not less_year: less_year = generateRandom(int(year) - 5, int(year)-1)
        if not greater_year: greater_year = generateRandom(int(year) + 1, int(year)+5)  
        generation_set["Y"] = (less_year, greater_year) 
    if month:
        less_month, greater_month = None, None
        if adv_months:
            adv_month = int(adv_months.pop())
            if adv_month > int(month): greater_month = adv_month
            elif adv_month < int(month): less_month = adv_month
        if not less_month and int(month)!= 1: less_month = generateRandom(1, int(month)-1)
        if not greater_month and int(month)!= 12: greater_month = generateRandom(int(month) + 1, 12)  
        generation_set["M"] = (less_month, greater_month) 
    if day:
        less_day, greater_day = None, None
        if adv_days:
            adv_day = int(adv_days.pop())
            if adv_day > int(day): greater_day = adv_day
            elif adv_day < int(day): less_day = adv_day
        if not less_day and int(day)!= 1: less_day = generateRandom(1, int(day)-1)
        if not greater_day and int(day)!= 31: greater_day = generateRandom(int(day) + 1, 31)  
        generation_set["D"] = (less_day, greater_day) 
    
    keywords = ["before", "after"]
    truth_vals = [(True, False),(False,True)]
    # print("generated:", str(generation_set["D"][1]), month, year)
    if day and month and year:
        if generation_set["D"][1]:
            for index in range(0, len(keywords)):
                result += albumDateOuputGenerator(name, key, 6, keywords[index], [str(generation_set["D"][1]), month, year], str(truth_vals[index][0]))
        if generation_set["D"][0]:
            for index in range(0, len(keywords)):                                              
                result += albumDateOuputGenerator(name, key, 6, keywords[index], [str(generation_set["D"][0]), month, year], str(truth_vals[index][1]))
        if generation_set["M"][1]:
            for index in range(0, len(keywords)): 
                result += albumDateOuputGenerator(name, key, 6, keywords[index], [day, str(generation_set["M"][1]), year], str(truth_vals[index][0])) 
        if generation_set["M"][0]:
            for index in range(0, len(keywords)): 
                result += albumDateOuputGenerator(name, key, 6, keywords[index], [day, str(generation_set["M"][0]), year], str(truth_vals[index][1])) 
        for index in range(len(keywords)):
            result += albumDateOuputGenerator(name, key, 6, keywords[index], [day, month, str(generation_set["Y"][1])], str(truth_vals[index][0]))
            result += albumDateOuputGenerator(name, key, 6, keywords[index], [day, month, str(generation_set["Y"][0])], str(truth_vals[index][1]))
    elif month and year:
        if generation_set["M"][1]:
            for index in range(0, len(keywords)): 
                result += albumDateOuputGenerator(name, key, 6, keywords[index], [str(generation_set["M"][1]), year], str(truth_vals[index][0]))
        if generation_set["M"][0]:
            for index in range(0, len(keywords)): 
                result += albumDateOuputGenerator(name, key, 6, keywords[index], [str(generation_set["M"][0]), year], str(truth_vals[index][1]))
        for index in range(len(keywords)):
            result += albumDateOuputGenerator(name, key, 6, keywords[index], [month, str(generation_set["Y"][1])], str(truth_vals[index][0]))
            result += albumDateOuputGenerator(name, key, 6, keywords[index], [month, str(generation_set["Y"][0])], str(truth_vals[index][1]))
    elif year:
        for index in range(len(keywords)):
            result += albumDateOuputGenerator(name, key, 6, keywords[index], [str(generation_set["Y"][1])], str(truth_vals[index][0]))
            result += albumDateOuputGenerator(name, key, 6, keywords[index], [str(generation_set["Y"][0])], str(truth_vals[index][1]))
    return result


# In[23]:


def weekBased(value, name):
    result, key = [], value.key.lower()
    date = " ".join(x for x in value.original)
    day, month, year = value.original
    month = int(month)
    day = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    d = datetime.datetime.strptime(date, '%d %m %Y')
#     print(d)
    real_week = week_of_month(d)
    fake_week = generateRandom(1,5)
    while fake_week == real_week:
        fake_week = generateRandom(1,5)
    less_week, greater_week = None, None
    if real_week > 1:less_week = generateRandom(1,real_week-1)
    if real_week < 5:greater_week = generateRandom(real_week+1,5)    
    keywords = ["before", "after", "in"]
    truth_vals = [str(True), str(False)]
    suffix = {1: "st", 2:"nd", 3: "rd", 4: "th", 5: "th"}
    #in
    # print (real_week,fake_week)
#     print(real_week)
    result += albumDateOuputGenerator(name, key, 7, keywords[2], [str(fake_week) + suffix[fake_week], getMonth(month), str(year)], truth_vals[1])
    result += albumDateOuputGenerator(name, key, 7, keywords[2], [str(real_week) + suffix[real_week], getMonth(month), str(year)], truth_vals[0])
    if less_week:
        result += albumDateOuputGenerator(name, key, 7, keywords[0], [str(less_week) + suffix[less_week], getMonth(month), str(year)], truth_vals[1])
        result += albumDateOuputGenerator(name, key, 7, keywords[1], [str(less_week) + suffix[less_week], getMonth(month), str(year)], truth_vals[0])
    if greater_week:
        result += albumDateOuputGenerator(name, key, 7, keywords[0], [str(greater_week)+ suffix[greater_week], getMonth(month), str(year)], truth_vals[0])
        result += albumDateOuputGenerator(name, key, 7, keywords[1], [str(greater_week)+ suffix[greater_week], getMonth(month), str(year)], truth_vals[1])
    return result
    
    
    


# In[24]:


def dateRules(dictionary):
    name = None
    result = []
    for key, value in dictionary.items():
        if value.key == "Title": name = value.val
    date_recorded, date_released = None, None
    length_label, length_genre = None, None
    for key, value in dictionary.items():
        if key == "Label": length_label = len(value.val) if type(value.val) == list else 1
        if key == "Genre": length_genre = len(value.val) if type(value.val) == list else 1
        if value.tag == "DATE" and value.original and key == "Released":    
            date_released = value.original
            # print("Date rules for released")
            if all(value.original):
                # print("day based")
                result = result + dayBased(value,name) #day based
                # print("odd/even based")
                result = result + oddEvenBased(value, name) #odd even
#                 print(name);
                result = result + weekBased(value, name) # week based
            if value.original[2]:
                # print("leap year")
                result = result + leapYear(value, name) #leap year
                # print("century")
                result = result + centuryBased(value, name) #century based
            # print("datechange")
            result = result + dateChange(value, name) #day month year interchange
            # print("order based")
            result = result + orderBased(value.val, name, value.key.lower(), value.original, value.adverse) #orderbased
        if value.tag == "DATE" and value.original and key == "Recorded":
            # print("roder based recording started") 
            result = result + orderBased(value.val, name, "recording started", value.original[0], value.adverse[0])
            # print("roder based recording end")
            result = result + orderBased(value.val, name, "recording ended", value.original[1], value.adverse[1])
            # print("diff based")
            result = result + diffBased(value.original[0], value.original[1], name, type_t = "single")
            date_recorded = value.original[1]
    # print("diff based multi")
    result = result + diffBased(date_recorded, date_released, name, type_t = "multi")
    # print("multi label genre")
    # print (length_label, length_genre, name)
    if length_label and length_genre:
        result = result + multiRowLabelGenre(length_label, length_genre, name)
    return result


# In[25]:


def diffBasedOutputGenerator(data, name, truth_val, param):
    result = []
    if not data[0]: years_diff, months_diff = None, str(data[1])
    else: years_diff, months_diff = str(data[0]), str(data[1])
    truth_val = str(truth_val)
    if param == 1:
        if not years_diff:
            result.append("It took around" + months_diff + " months " + " for the album " + name + " to record." + "\t" + truth_val)
        else:
            result.append("It took around " + years_diff + " years, " + months_diff + " months " + " for the album " + name + " to record." + "\t" + truth_val)
            
    elif param == 2:
        if not years_diff:
            result.append("It took less than " + months_diff + " months " + " for the album " + name + " to record." + "\t" + truth_val)
        else: 
            result.append("It took less than " + years_diff + " years, " + months_diff + " months " + " for the album " + name + " to record." + "\t" + truth_val)
    if param == 3:
        if not years_diff:
            result.append("It took more than " + months_diff + " months " + " for the album " + name + " to record." + "\t" + truth_val) 
        else:
            result.append("It took more than " + years_diff + " years, " + months_diff + " months " + " for the album " + name + " to record." + "\t" + truth_val)
    return result


# In[26]:


def diffBasedMultiOutputGenerator(data, name, truth_val, param):
    result = []
    # print(data)
    if not data[0]: years_diff, months_diff = None, str(data[1])
    else: years_diff, months_diff = str(data[0]), str(data[1])
    truth_val = str(truth_val)
    if param == 1:
        if not years_diff:
            result.append("It took around " + months_diff + " months " + " for the album " + name + " to release after being recorded." + "\t" + truth_val)
        else:
            result.append("It took around " + years_diff + " years, " + months_diff + " months " + " for the album " + name + " to release after being recorded." + "\t" + truth_val)
    elif param == 2:
        if not years_diff:
            result.append("It took less than " + months_diff + " months " + " for the album " + name + " to release after being recorded." + "\t" + truth_val)
        else: 
            result.append("It took less than " + years_diff + " years, " + months_diff + " months " + " for the album " + name + " to release after being recorded." + "\t" + truth_val)
    if param == 3:
        if not years_diff:
            result.append("It took more than " + months_diff + " months " + " for the album " + name + " to release after being recorded." + "\t" + truth_val)
        else:
            result.append("It took more than " + years_diff + " years, " + months_diff + " months " + " for the album " + name + " to release after being recorded." + "\t" + truth_val)
            
    return result


# In[27]:


def diffBased(date1, date2, name, type_t):
    result = []
    date_start, date_ended = date1, date2
    years_diff, months_diff = dateDiff(date_start, date_ended)
    if type_t == "single":
        if years_diff == 0:
            result.append("The album was recorded within one year. \t True")
            result.append("The album was recorded in more than one year. \t False")
            result = result + diffBasedOutputGenerator([None, months_diff],name, True, 1)
            fake_month_diff = generateRandom(1, 12)
            while fake_month_diff == months_diff:
                fake_month_diff = generateRandom(1, 12)
            result = result + diffBasedOutputGenerator([None, fake_month_diff],name, False, 1)
            if months_diff > 2:
                fake_val_before = generateRandom(1 , months_diff - 2)
                result = result + diffBasedOutputGenerator([None, fake_val_before],name, False, 2)
                result = result + diffBasedOutputGenerator([None, fake_val_before],name, True, 3)
            if months_diff < 10:
                fake_val_after = generateRandom(months_diff + 2, 12)
                result = result + diffBasedOutputGenerator([None, fake_val_after],name, True, 2)
                result = result + diffBasedOutputGenerator([None, fake_val_after],name, False, 3)
            
        else:
            result.append("The album was recorded within one year. \tFalse")
            result.append("The album was recorded in more than one year. \tTrue")
            fake_diff_year = generateRandom(1, years_diff + 5)
            while fake_diff_year == years_diff:
                fake_diff_year = generateRandom(1, years_diff + 5)
            fake_month_diff = generateRandom(1, 12)
            while fake_month_diff == months_diff:
                fake_month_diff = generateRandom(1, 12)
            result = result + diffBasedOutputGenerator([years_diff, months_diff],name, True, 1)
            result = result + diffBasedOutputGenerator([fake_diff_year, months_diff],name, False, 1)
            result = result + diffBasedOutputGenerator([years_diff, fake_month_diff],name, False, 1)

            actual_val = years_diff * 12 + months_diff
            fake_val_before = generateRandom(actual_val - 12, actual_val - 1)
            fake_val_after = generateRandom(actual_val + 1, actual_val + 12)
            fake_years_before, fake_months_before = fake_val_before // 12, fake_val_before % 12
            fake_years_after, fake_months_after = fake_val_after // 12, fake_val_after % 12
            result = result + diffBasedOutputGenerator([fake_years_before, fake_months_before],name, False, 2)
            result = result + diffBasedOutputGenerator([fake_years_before,fake_months_before ],name, True, 3)
            result = result + diffBasedOutputGenerator([fake_years_after,fake_months_after],name, True, 2)
            result = result + diffBasedOutputGenerator([fake_years_after,fake_months_after],name, False, 3)
    else:
        if years_diff == 0:
            result.append("The album was released within one year after it was recorded. \t True")
            result.append("The album took more than one year to release after it was recorded. \t False")
            result = result + diffBasedMultiOutputGenerator([None, months_diff],name, True, 1)
            fake_month_diff = generateRandom(1, 12)
            while fake_month_diff == months_diff:
                fake_month_diff = generateRandom(1, 12)
            result = result + diffBasedMultiOutputGenerator([None, fake_month_diff],name, False, 1)
            if months_diff > 2:
                fake_val_before = generateRandom(1 , months_diff - 2)
                result = result + diffBasedMultiOutputGenerator([None, fake_val_before],name, False, 2)
                result = result + diffBasedMultiOutputGenerator([None, fake_val_before],name, True, 3)
            if months_diff < 10:
                fake_val_after = generateRandom(months_diff + 2, 12)
                result = result + diffBasedMultiOutputGenerator([None, fake_val_after],name, True, 2)
                result = result + diffBasedMultiOutputGenerator([None, fake_val_after],name, False, 3)
        else:
            result.append("The album took more than one year to release after it was recorded. \t True")
            result.append("The album was recorded in more than one year. \tTrue")
            fake_diff_year = generateRandom(1, years_diff + 5)
            while fake_diff_year == years_diff:
                fake_diff_year = generateRandom(1, years_diff + 5)
            fake_month_diff = generateRandom(1, 12)
            while fake_month_diff == months_diff:
                fake_month_diff = generateRandom(1, 12)
            result = result + diffBasedMultiOutputGenerator([years_diff, months_diff],name, True, 1)
            result = result + diffBasedMultiOutputGenerator([fake_diff_year, months_diff],name, False, 1)
            result = result + diffBasedMultiOutputGenerator([years_diff, fake_month_diff],name, False, 1)

            actual_val = years_diff * 12 + months_diff
            fake_val_before = generateRandom(actual_val - 12, actual_val - 1)
            fake_val_after = generateRandom(actual_val + 1, actual_val + 12)
            fake_years_before, fake_months_before = fake_val_before // 12, fake_val_before % 12
            fake_years_after, fake_months_after = fake_val_after // 12, fake_val_after % 12
            result = result + diffBasedMultiOutputGenerator([fake_years_before, fake_months_before],name, False, 2)
            result = result + diffBasedMultiOutputGenerator([fake_years_before,fake_months_before ],name, True, 3)
            result = result + diffBasedMultiOutputGenerator([fake_years_after,fake_months_after],name, True, 2)
            result = result + diffBasedMultiOutputGenerator([fake_years_after,fake_months_after],name, False, 3)
    return result


# In[28]:


def generate_global_lists(dictionary, global_lists, global_info):
    for key, value in dictionary.items():
        if global_lists.get(key): 
            if type(value.val) == list:
                global_info[key] = True
                global_lists[key] = global_lists[key].union(set(value.val))
            else:
                global_lists[key].add(value.val)
        else:
            if type(value.val) == list:
                global_info[key] = True
                global_lists[key] = set(x for x in value.val)
            else:
                global_info[key] = False
                global_lists[key] = set([value.val])



def generate_fake_lists(dictionary, fake_adverse_list, global_info):
    title = (dictionary["Tablename"].val).split("_")[-1]
    # print (title,dictionary["Tablename"].val)
    if fake_adverse_list.get(title):
        current_dic = fake_adverse_list[title]
    else:
        fake_adverse_list[title] = {}
        current_dic = fake_adverse_list[title]
    for key, value in dictionary.items():
        if current_dic.get(key): 
            if type(value.val) == list:
                global_info[key] = True
                current_dic[key] = current_dic[key].union(set(value.val))
            else:
                current_dic[key].add(value.val)
        else:
            if type(value.val) == list:
                global_info[key] = True
                current_dic[key] = set(x for x in value.val)
            else:
                global_info[key] = False
                current_dic[key] = set([value.val])
    fake_adverse_list[title] = current_dic


# In[58]:



def table_generator(dictionary, global_lists, global_info, iteration):
    new_dict = {}
    for key, value in dictionary.items():
        key_type = "list" if global_info[key] else "single"
#         new_dict[key]
#         if key_type == "list":
#         print("------------------------")
        if type(value.val) == list:
            new_value_list = []
            for list_entry in value.val:
                random_num = generateRandom(0,3)
#                 print("Random value1: ", random_num, dictionary["Tablename"].val)
                global_values = list(global_lists[key])
                index_random = generateRandom(0, len(global_values)-1)
                counter = 0
                while global_values[index_random] == list_entry and counter < 100000:
                    counter += 1
                    index_random = generateRandom(0, len(global_values)-1)
#                 print("RAndom for substitution :", index_random)
                new_value = global_values[index_random]
#                 print(key, "v:", value.val)
#                 print("list:", global_values)
#                 print("new:", new_value)
                
                # same val
                if random_num == 0:
                    new_value_list.append(list_entry)
                # substitute
                elif random_num == 1:
                    new_value_list.append(new_value)
                #addition
                elif random_num == 2:
                    new_value_list.append(list_entry)
                    new_value_list.append(new_value)
                #deletion   
                
            #empty list
            if not new_value_list:
                new_value_list = value.val
                    
            new_dict[key] = Value(key, list(set(new_value_list)))
        else:
            # if key_type == list
            #
            #

            random_num = generateRandom(0,1)
            #single value substitute
            global_values = list(global_lists[key])
            index_random = generateRandom(0, len(global_values)-1)
            counter = 0
            while global_values[index_random] == value.val and counter < 100000:
                index_random = generateRandom(0, len(global_values)-1)
                counter += 1
            new_value = global_values[index_random]
                
            if key == "Title":
#                 if random_num == 0:
                new_dict[key] = Value(key, value.val)
#                 else:
#                     new_dict[key] = Value(key, new_value)
            else:
                new_dict[key] = Value(key, new_value)
                
                
#         print("Old:", value.val)
#         print("New:", new_dict[key].val)
    
    new_value = "F" + str(iteration) + "_"  +  (dictionary["Tablename"].val).split("_")[-1]
    new_dict["Tablename"] = Value(key, new_value)
        
    return new_dict
                    


# In[30]:


def producerOutputGenerator(number, data, name, truth_val, param):
    data, truth_val = str(data), str(truth_val)
    if not number:
        return ["The album " + name + " was " + " produced by " + data +" . \t" + truth_val]
    if number:
        if param == 1:
            if data == "single": return ["The album " + name + " was produced by a " + data + " person.  \t" + truth_val]
            else: return ["The album " + name + " was produced by " + data + " people.  \t" + truth_val]
        if param == "less":
            return ["The album " + name + " was " + " produced by less than " + data + " person. \t" + truth_val]
        elif param == "more":
            return ["The album " + name + " was " + " produced by more than " + data + " person. \t" + truth_val]
        elif data == "1":
            return ["The album " + name + " was " + " produced by " + data + " person. \t" + truth_val]
        return ["The album " + name + " was " + " produced by " + data + " people.\t" + truth_val]



def studioOutputGenerator(numbased, data, name, truth_val, param):
    data, truth_val = str(data), str(truth_val)
    if not numbased:
        return ["The album " + name + " was recorded in " + data +" studio.  \t" + truth_val]
    else:
        if param == 1:
            if data == "single": return ["The album " + name + " was recoreded in a " + data + " studio.  \t" + truth_val]
            else: return ["The album " + name + " was recorded in " + data + " studios.  \t" + truth_val]
        if param == "less":
            return ["The album " + name + " was recorded in less than " + data + " studios. \t" + truth_val]
        elif param == "more":
            return ["The album " + name + " was recorded in more than " + data + " studios. \t" + truth_val]
        elif data == "1":
            return ["The album " + name + " was recorded in " + data + " studio. \t" + truth_val]
        return ["The album " + name + " was recorded in " + data + " studios.  \t" + truth_val]


# In[32]:


def genreOutputGenerator(numbased, data, name, truth_val, param):
    data, truth_val = str(data), str(truth_val)
    if not numbased:
        return ["The album " + name + " has songs of " + data +" genre.  \t" + truth_val]
    else:
        if param == 1:
            if data == "single": return ["The album " + name + " has " + data + " genre.  \t" + truth_val]
            else: return ["The album " + name + " has " + data + " genres.  \t" + truth_val]
        if param == "less":
            return ["The album " + name + " has less than " + data + " genres.  \t" + truth_val]
        elif param == "more":
            return ["The album " + name + " has more than " + data + " genres.  \t" + truth_val]
        elif data == "1":
            return ["The album " + name + " has " + data + " genre. \t" + truth_val]
        return ["The album " + name + " has " + data + " genres.  \t" + truth_val]


# In[33]:


def labelOutputGenerator(numbased, data, name, truth_val, param):
    data, truth_val = str(data), str(truth_val)
    if not numbased:                                                                                                                    
        return ["The album " + name + " is associated with the label " + data +".  \t" + truth_val]
    else:
        if param == 1:
            if data == "single": return ["The album " + name + " is associated with a " + data + " label.  \t" + truth_val]
            else: return ["The album " + name + " is associated with " + data + " labels.  \t" + truth_val]
        if param == "less":
            return ["The album " + name + " is associated with less than " + data + " labels.  \t" + truth_val]
        elif param == "more":
            return ["The album " + name + " is associated with more than " + data + " labels.  \t" + truth_val]
        elif data == "1":
            return ["The album " + name + " is associated with " + data + " label. \t" + truth_val]
        return ["The album " + name + " is associated with " + data + " labels. \t" + truth_val]


# In[34]:


def call_generator(function_name, arg1, arg2, arg3, arg4, arg5):
    return {
        'Producer': lambda: producerOutputGenerator(arg1, arg2, arg3, arg4, arg5),
        'Genre': lambda: genreOutputGenerator(arg1, arg2, arg3, arg4, arg5),
        'Label': lambda: labelOutputGenerator(arg1, arg2, arg3, arg4, arg5),
        'Studio': lambda: studioOutputGenerator(arg1, arg2, arg3, arg4, arg5)
    }[function_name]()


# In[35]:


def number_based_multiple(v, name, type_cat):
    result = []
    if type(v.val) == list:
        true_num = len(v.val)
    else:
        true_num = 1
    fake_num = generateRandom(true_num + 1, true_num + 5)
    result = result + call_generator(type_cat, True, fake_num, name, False, None)
    result = result + call_generator(type_cat, True, true_num, name, True, None)
    less_num = None
    
    if true_num == 1:
        result = result + call_generator(type_cat, True, "single", name, True, 1)
        result = result + call_generator(type_cat, True, "multiple", name, False, 1)                                                       
    else:
        result = result + call_generator(type_cat, True, "multiple", name, True, 1)
        result = result + call_generator(type_cat, True, "single", name, False, 1)
    
    if true_num > 1:
        less_num = generateRandom(1, true_num-1)
    greater_num = generateRandom(true_num + 1, true_num + 10)
    
    #less than
    if less_num:
        result = result + call_generator(type_cat, True, less_num, name, False, "less")
    result = result + call_generator(type_cat, True, greater_num, name, True, "less")
    
    #more than
    if less_num: 
        result = result + call_generator(type_cat, True, greater_num, name, False, "more")
    result = result + call_generator(type_cat, True, less_num, name, True, "more")
    return result


# In[36]:


def nameswap_multiple(global_list, v, name, type_cat):
    result = []
    true_list = v.val
    if type(true_list) == list and len(true_list)>1:
        true_val = true_list[generateRandom(0, len(true_list)-1)]
    else: true_val = v.val
    index = generateRandom(0,len(global_list)-1)
    if (set(true_list) != set(global_list)):
        while global_list[index] in true_list:
            index = generateRandom(0,len(global_list)-1)
        fake_val = global_list[index]
        result = result + call_generator(type_cat, False, fake_val, name, False, None)
    result = result + call_generator(type_cat, False, true_val, name, True, None)       
    return result
    


# In[37]:


def commonRules(dictionary, global_lists, num):
    rulesMap = {
        1: "Producer",
        2: "Genre",
        3: "Label",
        4: "Studio"
    }
    result, key = [], rulesMap[num]

    for k, v in dictionary.items():
        if k == "Title": name = v.val            
    for k, v in dictionary.items():
        if k == key:
            global_list = list(global_lists[key])
            #number based
            # print("number_based_multiple")
            result = result + number_based_multiple(v, name, rulesMap[num])
            #accross table substitutiontab
            # print("nameswap_multiple")
            result = result + nameswap_multiple(global_list, v, name, rulesMap[num])
    return result


# In[38]:


def lengthOutputGenerator(type_cat, data, truth_val, param, name):
    truth_val = str(truth_val)
    if type_cat == 1:
        if not param: 
            hours, mins = str(data[0]), str(data[1]) 
            return ("The album " + name + " is " + hours + " hours " + mins + " minutes long." + "\t" +truth_val)
        elif param == "more":
            hours= str(data[0])
            return ("The album " + name + " is longer than " + hours + " hours." + "\t" +truth_val)
        elif param == "less":
            hours= str(data[0])
            return ("The album " + name + " is shorter than " + hours + " hours." + "\t" +truth_val)
            


# In[39]:


def hoursBased(v, name):
    result = []
    if type(v.val) is list: return []
    hours, mins = v.val.split(":")[0], v.val.split(":")[1]
    if len(hours) == 2 and len(mins) == 2:
        hours, mins = int(hours), int(mins)
    else: return []
    if hours < 60:
        result.append(lengthOutputGenerator(1, [1],True, "less", name))
        result.append(lengthOutputGenerator(1, [1],False, "more", name))
        return result
    hours_new = hours // 60
    mins_rem = hours % 60
    
    hours_new_fake = generateRandom(hours_new+1, hours_new+4)
    mins_new = mins + mins_rem
    result.append(lengthOutputGenerator(1, [hours_new_fake, mins_new],False, None, name))
    if mins_new != 1:
        mins_new_fake = generateRandom(1, mins_new-1)
        result.append(lengthOutputGenerator(1, [hours_new, mins_new_fake],False, None, name))
        result.append(lengthOutputGenerator(1, [hours_new_fake, mins_new_fake],False, None, name))
    
    result.append(lengthOutputGenerator(1, [hours_new, mins_new],True, None, name))
    
    less_hours = None
    if hours_new > 1:
        less_hours = generateRandom(1, hours_new-1)
    greater_hours = generateRandom(hours_new + 1, hours_new + 5)
    
    # more than less True, 
    if less_hours: result.append(lengthOutputGenerator(1, [less_hours],True, "more", name))
    #more than greater False
    result.append(lengthOutputGenerator(1, [greater_hours],False, "more", name))
    #less than less False
    if less_hours: result.append(lengthOutputGenerator(1, [less_hours],False, "less", name))
    #less than greater True
    result.append(lengthOutputGenerator(1, [greater_hours],True, "less", name))
    return result
        

     


# In[40]:


def lengthRules(dictionary):
    result = []
    key = "Length"
    for k, v in dictionary.items():
        if k == "Title": name = v.val            
    for k, v in dictionary.items():
        if k == key:
            result = result + hoursBased(v, name)
    return result
    


# In[41]:


def preprocesStudio(dictionary, global_lists):
    result = []
    for key, value in dictionary.items():
        if value.key == "Title": name = value.val
    new_location = []
    for k, v in dictionary.items():
        if k == "Studio":
            #east and west coast

            #country from studio location
            for loc in v.val:
                origloc = loc
                loc = loc[loc.find("(")+1:loc.find(")")]
                try:
#                     location = geolocator.geocode(loc)
                    # print("before",loc, "after",location.address)
                    new_location += [origloc + " ("+location.address+") "]
                except:
                    new_location += [origloc]
            dictionary["Studio"] = Value("Studio", new_location)
    return 1


# In[42]:


def constriants(dictionary):
    recorded_date = str(dictionary["Recorded"].val).split("-")
    recorded_date_end = recorded_date[1]
    recorded_date_start = recorded_date[0]
    released_date = dictionary["Released"].val
    Dates = [recorded_date_start,recorded_date_end,released_date]
    # if any(v is None for v in [getDate(recorded_date_start),getDate(recorded_date_end),getDate(released_date)]):
    #     print (dictionary["Recorded"].val, released_date)
    #     print (getDate(recorded_date_start),getDate(recorded_date_end),getDate(released_date))
    d1, m1, y1 = getDate(recorded_date_start)
    d2, m2, y2 = getDate(recorded_date_end)
    d3, m3, y3 = getDate(released_date)
    date1 = int(y1 + m1 +d1)
    date2 = int(y2 +m2+d2)
    date3 = int(y3+m3+d3)
    dates  = [date1,date2,date3]
    sorted_index = np.argsort(dates)
    dictionary["Released"].val = Dates[sorted_index[2]]
    dictionary["Recorded"].val = Dates[sorted_index[0]] +" - "+ Dates[sorted_index[1]]
    return dictionary


# In[54]:


def splitDateRange(dictionary):
    for k, v  in dictionary.items():
        if k == "Released": v.tag = "DATE"
        if k == "Length": v.tag = "CARDINAL"
        if k == "Producer": v.tag = "PERSON"
        if k == "Label": v.tag = None
        if k == "Genre": v.tag = None
        if "-" in v.val and k == "Recorded":
            v.val = [x.strip() for x in v.val.split("-")]
            v.tag = "DATE"
            


# In[44]:


def dateDiff(date1, date2):
    year1, year2 = int(date1[2]), int(date2[2])
    month1, month2 = int(date1[1]), int(date2[1])
    day1, day2 = int(date1[0]), int(date2[0])
    diff = [day2-day1, month2-month1, year2-year1]
    
    year_diff = diff[2] * 12
    difference_months = year_diff + diff[1]
    
    year_diff = difference_months // 12
    difference_months = difference_months % 12
    
    if diff[0] < -15:
        difference_months -= 1
    elif diff[0] > 15:
        difference_months += 1
    
    return year_diff, difference_months
    
    


# In[45]:


def multiRowLabelGenre(length_label, length_genre, name):
    result = []
    greater_val, same, less_val =  None, False, None 
    if length_label > length_genre:
        greater_val, less_val = "labels", "genres"
        result.append("The album " + name + " is associated with more labels than it has genres. \t True")
        result.append("The album " + name + " is associated with less labels than it has genres. \t False")
    elif length_label == length_genre:
        same = True
        result.append("The album " + name + " is associated with the same number of labels as it has genres. \t True")
        result.append("The album " + name + " is associated with the same number of labels as it has genres. \t False")
#         result.append("The album " + name + " has same genres as the number of labels it is associated with. \t True")
#   result.append("The album " + name + " has same genres as the number of labels it is associated with. \t False")
    else:
        greater_val, less_val = "genres", "labels"
        result.append("The album " + name + " is associated with less labels than it has genres. \t True")
        result.append("The album " + name + " is associated with more labels than it has genres. \t False")
    
    if not same:
        diff = abs(length_label - length_genre)
        fake_diff = generateRandom(diff + 1, diff + 4)
        # print (diff,fake_diff)
        while fake_diff == diff:
            fake_diff = generateRandom(diff + 1, diff + 4)
        # print ("out of while fake diff :",fake_diff)
        if greater_val == "genres":
            result.append("The album " + name + " has " + str(diff) + " more genres than the labels it is assocatied with. \t True")
            result.append("The album " + name + " has " + str(fake_diff) + " more genres than the labels it is assocatied with. \t False")
        else:
            result.append("The album " + name + " is associated with " + str(diff) + " more labels than the genres it has. \t True")
            result.append("The album " + name + " is associated with " + str(fake_diff) + " more labels than the genres it has. \t False")
        fake_diff_after = str(generateRandom(diff + 1, diff + 4))
        result.append("The difference between the labels associated with the album " + name + " and the genres it has is more than " + fake_diff_after + ". \t False")
        result.append("The difference between the labels associated with the album " + name + " and the genres it has is less than " + fake_diff_after + ". \t True")
        if diff > 2: 
            fake_diff_before = str(generateRandom(diff - 2, diff - 1))
            result.append("The difference between the labels associated with the album " + name + " and the genres it has is more than " + fake_diff_before + ". \t True")
            result.append("The difference between the labels associated with the album " + name + " and the genres it has is less than " + fake_diff_before + ". \t False")
    # print(result)
    return result
    
    
def get_json(dictionary):
    '''
The album "_name" was released on _v1. The album "_name" was recorded from _v21-_v22. It was recorded in the studios _v31, _v32. It has the genres _v41, _v42. The album has length _v5. It is associated with label _v6. _v71, _v72 produced this album.
'''
    result = []
    print(dictionary["Title"].val)
    album = str(dictionary["Title"].val)
    if dictionary.get("Released"):
        v = dictionary.get("Released").val
        result.append("The album " + album + " was released on " + v)
    if dictionary.get("Recorded"):
        v = dictionary.get("Recorded").val
        result.append("The album " + album + " was recorded from " + v[0] + " to " + v[1])
    if dictionary.get("Studio"):
        v = dictionary.get("Studio").val
        if type(v) == list:
            studios = ", ".join(x for x in v)
            result.append("It was recorded in studios " + studios)
        else:
            result.append("It was recorded in studio " + v)
    if dictionary.get("Genre"):
        v = dictionary.get("Genre").val
        if type(v) == list:
            genres = ", ".join(x for x in v)
            result.append("It has genres " + genres)
        else:
            result.append("It has genre " + v)
    if dictionary.get("Length"):
        v = dictionary.get("Length").val
        result.append("It has length " + v)
    if dictionary.get("Label"):
        v = dictionary.get("Label").val
        if type(v) == list:
            labels = ", ".join(x for x in v)
            result.append("It is associated with the labels " + labels)
        else:
            result.append("It is associated with the label " + v)
    if dictionary.get("Producer"):
        v = dictionary.get("Producer").val
        producers = v
        if type(v) == list:
            producers = ", ".join(x for x in v)
        result.append(producers + " produced this album.")
    return ". ".join(result)


# In[64]:


# Catg = pd.read_csv("/content/drive/My Drive/Auto-TNLI/data/table_categories.tsv",sep="\t")
Catg = pd.read_csv("../../autotnlidatasetandcode/table_categories modified.tsv",sep="\t")
# Ptab = np.array(Catg[Catg.category.isin(['Person','Musician'])].table_id)
tablesFolderJ = "../files/json/"
# tablesFolderJ = "/content/drive/My Drive/Auto-TNLI/data/json/"


# In[65]:


table_list = set(Catg[Catg.category.isin(['Album'])].table_id.to_list())
tables_list = []
# tablesFolder = "../../autotnlidatasetandcode/tables"
global_lists, global_info, fake_adverse_list = {}, {}, {}
# outputFile = open('try_results.txt', "w+")
# outputFile2 = open('try_results_v2.txt', "w+")
# for i in range(len(table_list)):
#     tableFileName = table_list[i]
# #     dictionary = parseFile(tableFileName, tablesFolderJ)
# #     if "Title" in dicionary.keys():
# #     dictionary = reformDict(dictionary)
#     dictionary["Tablename"].val = "T" + "0" + "_" + dictionary["Tablename"].val
#     tables_list.append(dictionary)
#     generate_global_lists(dictionary, global_lists, global_info)

fp = open("all_jsons.json","r")
all_jsons = json.load(fp)
for jsonfile in all_jsons["all_json"]:
    jsonfile["Title"] = jsonfile["Title"][0]
    jsonfile["Released"] = jsonfile["Released"][0]
    jsonfile["Recorded"] = jsonfile["Recorded"][0]
    jsonfile["Length"] = jsonfile["Length"][0]
    jsonfile["Tablename"] = jsonfile["Tablename"][0]
    dictionary = reformDict(jsonfile)
    dictionary["Tablename"].val = "T"+"0"+"_"+dictionary["Tablename"].val
    tables_list.append(dictionary)
    generate_global_lists(dictionary, global_lists, global_info)


# In[66]:


tables_list = tables_list[:20]


# In[67]:


outputFile = open('results_onefake.txt', "w+")
new_dicts = []
# print (len(tables_list))
for i in range(0,len(tables_list)):
    dictionary = tables_list[i]
    preprocesStudio(dictionary, global_lists)
    try:
        dictionary = constriants(dictionary)
    except Exception as e:
        # print (dictionary["Tablename"].val)
        print("error in constraints: ",e)
        continue
    new_dicts.append(dictionary)
    num_of_fake_per_table = 2
    for index in range(0,num_of_fake_per_table):
        new_dict = table_generator(dictionary, global_lists, global_info, index)
        try:
            new_dict = constriants(new_dict)
        except Exception as e:
            # print (new_dict["Tablename"].val)
            print("error in constraints: ",e)
            continue
        new_dicts.append(new_dict)

for i in range(0,len(new_dicts)):
    dictionary = new_dicts[i]
    generate_fake_lists(dictionary,fake_adverse_list,global_info)

# for key,value in fake_adverse_list.items():
#     print (key,value)

# print(len(new_dicts))
# tables_list = tables_list + new_dicts
# tables_list = [tables_list[0]] + new_dicts
# print(len(tables_list))

for i in range(0, len(new_dicts)):
#     print("------------------ " + str(i) + "---------------------")
    splitDateRange(new_dicts[i])
    preprocessDate(new_dicts[i])  
    
# for i in range(0, len(new_dicts)):
#     dictionary = new_dicts[i]
#     for key, value in dictionary.items():
#         print( str(key) + ":" +  str(value.val) + str(value.tag) + "\n" )
# rules on all tables
serial_ctr = 1
for i in range(0, len(new_dicts)):    
    dictionary = new_dicts[i]
    final_result = []
#     for key, value in dictionary.items():
#         print( str(key) + ":" +  str(value.val) + str(value.tag) + "\n" )
    # outputFile.write("-------------------------- " + dictionary["Tablename"].val + "--------------------------\n")
    # for key, value in dictionary.items():
    #     outputFile.write( str(key) + ":" +  str(value.val) +  "\t  ( " + str(value.tag) + " ) \n" )
    # outputFile.write("---------Rules-----------\n")
    table_name = (dictionary["Tablename"].val).split("_")[-1]

    #get json
    json_table = get_json(dictionary)
    #length rules
#     print ("length_rules")
    final_result = final_result + lengthRules(dictionary) 
    #date rules
#     print ("dates_rules")
    final_result = final_result + dateRules(dictionary)
    #producer
#     print ("producer")
    final_result = final_result + commonRules(dictionary, fake_adverse_list[table_name], 1)
#     #label
#     print ("label")
    final_result = final_result + commonRules(dictionary, fake_adverse_list[table_name], 2)
#     #genre
#     print ("genre")
    final_result = final_result + commonRules(dictionary, fake_adverse_list[table_name], 3)
#     #studio
#     print ("studio")
    final_result = final_result + commonRules(dictionary, fake_adverse_list[table_name], 4)
    if final_result:
        for statement in final_result:
            truth_val = statement.split()[-1].strip()
            length = len(statement.split())
            statement = " ".join((statement.split()[:length -1])).strip()
            if truth_val == "True":
                truth_val = 1
            else:
                truth_val = 0
            table_name_entry = dictionary["Tablename"].val
            table_names_list = table_name_entry.split("_")
            outputFile.write(str(serial_ctr) + "\t" + table_names_list[0] + "\t" + table_names_list[1] + "\t" + json_table + "\t" + statement + "\t" + str(truth_val) + "\n")
            serial_ctr  += 1


# In[68]:


# dictionary["Released"].val


# In[69]:


# dictionary


# In[56]:


# pendulum.parse("2015-03-31").week_of_month


# In[ ]:




