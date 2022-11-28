from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random
import math
import sys
import time
import json
import multiprocessing
from multiprocessing.pool import ThreadPool
import argparse

from Album import *
import Person
import Movie
import Book
import FoodnDrinks
import Organization
import Paint
import Festival
import SportsnEvents
import University
import City
from util import *
from util import _append

# !pip install dateparser
# !pip install pendulum

if './' not in sys.path:
    sys.path.append('./')


def config(parser):
    parser.add_argument('--store_json', default=False, type=bool)
    return parser


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    album_tables = [0, 7, 10, 13, 28, 42, 44, 55, 65, 69, 72, 80, 93, 102, 106, 112, 114, 115, 117, 157, 166, 170, 179, 235, 307, 326, 330, 347, 352, 369, 376, 379, 389, 417, 419, 424, 428, 432, 441, 443, 445, 451, 462, 465, 469, 479, 480, 501, 509, 520, 546, 562, 585, 587, 592, 600, 611, 612, 614, 671, 676, 679, 682, 685, 691, 699, 700, 703, 709, 720, 721, 723, 742, 743, 755, 771, 785, 800, 801, 805, 811, 818, 819, 824, 826, 834, 838, 852, 854, 860, 863, 886, 902, 907, 909, 920, 935, 942, 945, 955, 965, 976, 978, 980, 989, 1024, 1025, 1030, 1043,
                    1061, 1066, 1072, 1077, 1101, 1103, 1115, 1124, 1128, 1136, 1153, 1157, 1161, 1169, 1196, 1206, 1209, 1223, 1231, 1235, 1243, 1264, 1270, 1282, 1283, 1316, 1320, 1467, 1478, 1547, 1589, 1714, 1739, 1742, 1744, 1747, 1749, 1750, 1757, 1764, 1766, 1769, 1778, 1788, 1793, 1802, 1803, 1817, 1820, 1823, 1824, 1831, 1834, 1846, 1848, 1853, 1867, 1870, 1871, 1872, 1879, 1897, 1899, 1900, 1913, 1930, 1934, 1940, 1949, 1952, 1953, 1960, 1963, 1966, 1968, 1970, 1971, 1975, 1984, 1986, 1987, 1998, 2000, 2005, 2017, 2022, 2026, 2027, 2031, 2033, 2034]
    table_list = []
    for i in album_tables:
        table_list.append("T"+str(i))
    tables_list = []
    global_lists, global_info, fake_adverse_list = {}, {}, {}
    outputFile = open('results_onefake.txt', "w+")

    fp = open("../wiki_data/all_jsons.json", "r")
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

    new_dicts = []
    for i in range(0, len(tables_list)):
        dictionary = tables_list[i]
        preprocesStudio(dictionary, global_lists)
        try:
            dictionary = constriants(dictionary)
        except Exception as e:
            print("error in constraints: ", e)
            continue
        new_dicts.append(dictionary)
        num_of_fake_per_table = 5  # change this to change number of fake tables
        for index in range(0, num_of_fake_per_table):
            new_dict = table_generator(
                dictionary, global_lists, global_info, index)
            try:
                new_dict = constriants(new_dict)
            except Exception as e:
                print("error in constraints: ", e)
                continue
            new_dicts.append(new_dict)

    for i in range(0, len(new_dicts)):
        dictionary = new_dicts[i]
        generate_fake_lists(dictionary, fake_adverse_list, global_info)

    for i in range(0, len(new_dicts)):
        splitDateRange(new_dicts[i])
        preprocessDate(new_dicts[i])


    table = []
    premises = []
    hypothesis = []
    label = []
    premises_used = []
    json_name = []
    for i in range(0, len(new_dicts)):
        dictionary = new_dicts[i]
        for key, value in dictionary.items():
            print(str(key) + ":" + str(value.val) + str(value.tag) + "\n")

        table_name = (dictionary["Tablename"].val).split("_")[-1]

        # get json
        json_table = get_json(dictionary)

        final_result = {}
    #   producer
        print("Producer")
        final_result["Producer"] = []
        final_result["Producer"] = commonRules(
            dictionary, fake_adverse_list[table_name], 1)

    #   genre
        print("Genre")
        final_result["Genre"] = []
        final_result["Genre"] = commonRules(
            dictionary, fake_adverse_list[table_name], 2)

    #   label
        print("Label")
        final_result["Label"] = []
        final_result["Label"] = commonRules(
            dictionary, fake_adverse_list[table_name], 3)

    #   studio
        print("Studio")
        final_result["Studio"] = []
        final_result["Studio"] = commonRules(
            dictionary, fake_adverse_list[table_name], 4)

    #   length rules
        print("Length")
        final_result["Length"] = []
        final_result["Length"] = lengthRules(dictionary)

    #   date rules
        print("date_rules")
        temp_length = dateRules(dictionary)
        for t_l in temp_length:
            if t_l in final_result:
                for x in temp_length[t_l]:
                    final_result[t_l].append(x)
            else:
                final_result[t_l] = []
                final_result[t_l] = temp_length[t_l]

    #     if final_result:
        for key in final_result:
            for statement in final_result[key]:
                truth_val = statement.split()[-1].strip()
                length = len(statement.split())
                statement = " ".join((statement.split()[:length - 1])).strip()
                if truth_val == "True":
                    truth_val = 1
                else:
                    truth_val = 0
                table_name_entry = dictionary["Tablename"].val
                table_names_list = table_name_entry.split("_")
                table.append(table_names_list[0])
                # create premises    import time

                json_name.append(table_names_list[1])
                json_sent = []
                for key_ in json_table:
                    # extra if and elif statement for neutral statements
                    if type(key) == tuple and key_ not in key:
                        json_sent.append(json_table[key_][0])
                    elif key_ != key:
                        json_sent.append(json_table[key_][0])
                json_sentences = ". ".join(json_sent)
                premises.append(json_sentences)

                hypothesis.append(statement)
                dict_prem = {}
                if type(key) == tuple:
                    for key_ in key:
                        dict_prem[key_] = []
                        dict_prem[key_] = json_table[key_]

                else:
                    dict_prem[key] = []
                    dict_prem[key] = json_table[key]
                premises_used.append(dict_prem)
                label.append(str(truth_val))

    df = pd.DataFrame({"table": table, "premises": premises, "hypothesis": hypothesis,
                       "label": label, "key & premises_used": premises_used, "json_name": json_name})
    df.to_csv("../autotnli_data/Album"+".csv", sep="\t")

    # get all json in a folder
    if(args['store_json']==True):
        for i in range(len(new_dicts)):
            single_table = new_dicts[i]
            for key in single_table:
                single_table[key] = single_table[key].val
            with open("../autotnli_data/json/"+single_table["Tablename"]+".json", "w") as fp:
                json.dump(single_table, fp)
