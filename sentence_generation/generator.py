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

if './' not in sys.path:
    sys.path.append('./')

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


def config(parser):
    parser.add_argument('--interval',  default=1000, type=int)
    parser.add_argument('--counterfactuals',  default=0, type=int)
    parser.add_argument('--store_json', default=False, type=bool)
    # parser.add_argument('--category', default="Person", type=str)
    parser.add_argument('--category_list', default=["Book", "City", "Festival", "FoodnDrinks", "Movie",
                        "Organization", "Paint", "Person", "SportsnEvents", "University"],  action='store', type=str, nargs='*')
    return parser


def generate(category, args):
    i = category

    interval = int(args['interval'])
    p = ThreadPool()

    N, T = getattr(eval(i), "get_Table_Title")()
    # getting all the extracted data at once in a dictionary
    Extracted_Data = getattr(eval(i), "get_Data")()

    for tag in np.arange(0, category_table_count[i], interval):
        premises = []
        hypothesis = []
        label = []
        json_name = []
        table = []
        premises_used = []

        for j in range(tag, min(tag+interval, category_table_count[i])):
            start = time.time()

            premise = []
            count = 0  # keep count of the number of premises to be generated
            key_premises = {}
            k_range = len(Dict[i]) if i != "Person" else len(Dict[i+"1"])

            for k_index in range(k_range):
                k = Dict[i][k_index] if i != "Person" else Dict[i+"2"][k_index]
                D = Extracted_Data[k] if i != "Person" else Extracted_Data[Dict[i+"1"][k_index]]
                # stores all possible premises for all the functions
                if (len(get_True(i, D, k, j)) > 0):
                    key_premises[k] = get_premises(i, D, k, j)
                    # make the true statements
                    for s in get_True(i, D, k, j):
                        temp = {}
                        temp[k] = []
                        ts = key_premises[k]
                        random.shuffle(ts)
                        temp[k] = ts[:]
                        hypothesis, label, table, json_name, premises_used = p.starmap(_append, [(
                            hypothesis, s), (label, "E"), (table, T[j]), (json_name, T[j]), (premises_used, temp)])
                        count = count+1  # count later on to be used for making premises
                    # make the false statements
                    for s in get_False(i, D, k, j):
                        temp = {}
                        ts = key_premises[k]
                        random.shuffle(ts)
                        temp[k] = ts[:]
                        hypothesis, label, table, json_name, premises_used = p.starmap(_append, [(
                            hypothesis, s), (label, "N"), (table, T[j]), (json_name, T[j]), (premises_used, temp)])
                        count = count+1

            # generate the multi_rows
            for multi_n in range(1, multi_row_count[i]+1):
                multi_True = getattr(
                    eval(i), "multi_row"+str(multi_n))(T, N, Extracted_Data, j, True)
                multi_False = getattr(
                    eval(i), "multi_row"+str(multi_n))(T, N, Extracted_Data, j, False)
                for m_key in multi_True.keys():
                    for m_t in multi_True[m_key]:
                        temp_prem = {}
                        for prem_key in m_key.split(","):
                            temp_prem[prem_key] = []
                            ts = key_premises[prem_key]
                            random.shuffle(ts)
                            temp_prem[prem_key] = ts[:]
                        hypothesis, label, table, json_name, premises_used = p.starmap(_append, [(
                            hypothesis, m_t), (label, "E"), (table, T[j]), (json_name, T[j]), (premises_used, temp_prem)])
                        count = count+1

                    for m_f in multi_False[m_key]:
                        temp_prem = {}
                        for prem_key in m_key.split(","):
                            temp_prem[prem_key] = []
                            ts = key_premises[prem_key]
                            random.shuffle(ts)
                            temp_prem[prem_key] = ts[:]
                        hypothesis, label, table, json_name, premises_used = p.starmap(_append, [(
                            hypothesis, m_f), (label, "N"), (table, T[j]), (json_name, T[j]), (premises_used, temp_prem)])
                        count = count+1

            # generate the premises
            for pi in range(count):
                ss = []
                for key in key_premises.keys():
                    if key in premises_used[-(count-pi)].keys():
                        ss.append(premises_used[-(count-pi)][key][0])
                    else:
                        ss.append(random.sample(key_premises[key], 1)[0])
                random.shuffle(ss)
                premises.append(" . ".join(ss))
            if (j % 10):
                print("{} : {}".format(j, (time.time()-start)/60))
    df = pd.DataFrame({"table": table, "premises": premises, "hypothesis": hypothesis,
                       "label": label, "key & premises_used": premises_used, "json_name": json_name})
    df.to_csv("../autotnli_data"+i.split("_")
              [0].lower()+"_T0_"+str(int(tag/interval))+".tsv", sep="\t")
    del df

    return None


def generate_counterfactual(category, counterfactuals_temp, args):
    i = category

    interval = int(args['interval'])
    p = ThreadPool()

    N, T = getattr(eval(i), "get_Table_Title")()
    # getting all the extracted data at once in a dictionary
    Extracted_Data = getattr(eval(i), "get_Data")(fake=True)

    for tag in np.arange(0, category_table_count[i], interval):
        fake_n = "_CF"+str(counterfactuals_temp)
        premises = []
        hypothesis = []
        label = []
        json_name = []
        table = []
        premises_used = []

        for j in range(tag, min(tag+interval, category_table_count[i])):
            start = time.time()

            # save as json
            if (args['store_json'] == True):
                json_file = {}
                json_file["title"] = N[T[j]]
                for kjson in set(Extracted_Data.keys()):
                    if (kjson == "BDA"):
                        to_be_json = []
                        df = Extracted_Data["BDA"][0]
                        dct = Extracted_Data["BDA"][1]
                        to_be_json.append(
                            str(df["Born_D"][j])+" "+df["Born_M"][j]+","+str(df["Born_Y"][j]))
                        if (dct[T[j]][0] != None):
                            to_be_json.append(",".join(dct[T[j]][::-1]))
                        json_file["Born"] = [",".join(to_be_json)]
                        if (df.isna().Died_Y[j] == False):
                            to_be_json = []
                            dct = Extracted_Data["BDA"][2]
                            to_be_json.append(
                                str(df["Died_D"][j])+" "+df["Died_M"][j]+","+str(df["Died_Y"][j]))
                            if (dct[T[j]][0] != None):
                                to_be_json.append(
                                    ",".join(dct[T[j]][::-1]))
                            json_file["Died"] = [",".join(to_be_json)]
                        if (df.isna().Age[j] == False):
                            json_file["Age"] = [df.Age[j]]
                    else:
                        to_be_json = []
                        for parser in Extracted_Data[kjson]:
                            if (type(parser) == dict and parser[T[j]][0] != None):
                                for temp_parser in parser[T[j]]:
                                    if (len(str(temp_parser)) > 3 or type(temp_parser) == int):
                                        to_be_json.append(str(temp_parser))
                        if (len(to_be_json) > 0):
                            json_file[kjson.replace("_", " ")] = [
                                ', '.join(to_be_json)]
                with open("../autotnli_data/json/"+T[j]+fake_n+".json", "w") as fp:
                    json.dump(json_file, fp)

            premise = []
            count = 0  # count the number of premises to be generated
            key_premises = {}
            k_range = len(Dict[i]) if i != "Person" else len(Dict[i+"1"])

            for k_index in range(k_range):
                k = Dict[i][k_index] if i != "Person" else Dict[i+"2"][k_index]
                D = Extracted_Data[k] if i != "Person" else Extracted_Data[Dict[i+"1"][k_index]]
                # stores all possible premises for all the functions
                if (len(get_True(i, D, k, j)) > 0):
                    key_premises[k] = get_premises(i, D, k, j)
                    # make the true statements
                    for s in get_True(i, D, k, j):
                        temp = {}
                        temp[k] = []
                        ts = key_premises[k]
                        random.shuffle(ts)
                        temp[k] = ts[:]
                        p.starmap(_append, [(hypothesis, s), (label, "E"), (
                            table, T[j]), (json_name, T[j]+fake_n), (premises_used, temp)])
                        count = count+1  # count later on to be used for making premises
                    # make the false statements
                    for s in get_False(i, D, k, j):
                        temp = {}
                        ts = key_premises[k]
                        random.shuffle(ts)
                        temp[k] = ts[:]
                        p.starmap(_append, [(hypothesis, s), (label, "N"), (
                            table, T[j]), (json_name, T[j]+fake_n), (premises_used, temp)])

                        count = count+1

            # generate the multi_rows
            for multi_n in range(1, multi_row_count[i]+1):
                multi_True = getattr(
                    eval(i), "multi_row"+str(multi_n))(T, N, Extracted_Data, j, True)
                multi_False = getattr(
                    eval(i), "multi_row"+str(multi_n))(T, N, Extracted_Data, j, False)
                for m_key in multi_True.keys():
                    for m_t in multi_True[m_key]:
                        temp_prem = {}
                        for prem_key in m_key.split(","):
                            temp_prem[prem_key] = []
                            ts = key_premises[prem_key]
                            random.shuffle(ts)
                            temp_prem[prem_key] = ts[:]
                        p.starmap(_append, [(hypothesis, m_t), (label, "E"), (table, T[j]), (
                            json_name, T[j]+fake_n), (premises_used, temp_prem)])
                        count = count+1

                    for m_f in multi_False[m_key]:
                        temp_prem = {}
                        for prem_key in m_key.split(","):
                            temp_prem[prem_key] = []
                            ts = key_premises[prem_key]
                            random.shuffle(ts)
                            temp_prem[prem_key] = ts[:]
                        p.starmap(_append, [(hypothesis, m_f), (label, "N"), (table, T[j]), (
                            json_name, T[j]+fake_n), (premises_used, temp_prem)])
                        count = count+1

            # generate the premises
            for pi in range(count):
                ss = []
                for key in key_premises.keys():
                    if key in premises_used[-(count-pi)].keys():
                        ss.append(premises_used[-(count-pi)][key][0])
                    else:
                        ss.append(random.sample(key_premises[key], 1)[0])
                random.shuffle(ss)
                premises.append(" . ".join(ss))
            if (j % 10):
                print("{} : {}".format(j, (time.time()-start)/60))
    df = pd.DataFrame({"table": table, "premises": premises, "hypothesis": hypothesis,
                       "label": label, "key & premises_used": premises_used, "json_name": json_name})
    df.to_csv("../autotnli_data"+i.split("_")
              [0].lower()+fake_n+"_"+str(int(tag/interval))+".tsv", sep="\t")
    del df

    return None


def generate_album(args):

    album_tables = [0, 7, 10, 13, 28, 42, 44, 55, 65, 69, 72, 80, 93, 102, 106, 112, 114, 115, 117, 157, 166, 170, 179, 235, 307, 326, 330, 347, 352, 369, 376, 379, 389, 417, 419, 424, 428, 432, 441, 443, 445, 451, 462, 465, 469, 479, 480, 501, 509, 520, 546, 562, 585, 587, 592, 600, 611, 612, 614, 671, 676, 679, 682, 685, 691, 699, 700, 703, 709, 720, 721, 723, 742, 743, 755, 771, 785, 800, 801, 805, 811, 818, 819, 824, 826, 834, 838, 852, 854, 860, 863, 886, 902, 907, 909, 920, 935, 942, 945, 955, 965, 976, 978, 980, 989, 1024, 1025, 1030, 1043,
                    1061, 1066, 1072, 1077, 1101, 1103, 1115, 1124, 1128, 1136, 1153, 1157, 1161, 1169, 1196, 1206, 1209, 1223, 1231, 1235, 1243, 1264, 1270, 1282, 1283, 1316, 1320, 1467, 1478, 1547, 1589, 1714, 1739, 1742, 1744, 1747, 1749, 1750, 1757, 1764, 1766, 1769, 1778, 1788, 1793, 1802, 1803, 1817, 1820, 1823, 1824, 1831, 1834, 1846, 1848, 1853, 1867, 1870, 1871, 1872, 1879, 1897, 1899, 1900, 1913, 1930, 1934, 1940, 1949, 1952, 1953, 1960, 1963, 1966, 1968, 1970, 1971, 1975, 1984, 1986, 1987, 1998, 2000, 2005, 2017, 2022, 2026, 2027, 2031, 2033, 2034]
    table_list = []
    for i in album_tables:
        table_list.append("T"+str(i))
    tables_list = []
    global_lists, global_info, fake_adverse_list = {}, {}, {}

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
        # change this to change number of fake tables
        num_of_fake_per_table = args['counterfactuals']
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
                # create premises

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
    if (args['store_json'] == True):
        for i in range(len(new_dicts)):
            single_table = new_dicts[i]
            for key in single_table:
                single_table[key] = single_table[key].val
            with open("../autotnli_data/json/"+single_table["Tablename"]+".json", "w") as fp:
                json.dump(single_table, fp)

    return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    for Category in args['category_list']:
        if Category != "Album":
            generate(Category, args)

            for counterfactuals_temp in range(int(args['counterfactuals'])):
                generate_counterfactual(Category, counterfactuals_temp+1, args)
        else:
            generate_album(args)
