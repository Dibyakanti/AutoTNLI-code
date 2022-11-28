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
    parser.add_argument('--interval',  default=1000, type=int)
    parser.add_argument('--category', default="Person", type=str)
    parser.add_argument('--store_json', default=False, type=bool)
#     parser.add_argument('--category_list', default=["Person","Album"],  action='store', type=str, nargs='*')
    return parser


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    interval = int(args['interval'])
    p = ThreadPool()

    for tag in np.arange(0, category_table_count[str(args['category'])], interval):
        fake_n = "_CF"
        premises = []
        hypothesis = []
        label = []
        json_name = []
        table = []
        premises_used = []

        for i in [args['category']]:
            N, T = getattr(eval(i), "get_Table_Title")()

            # getting all the extracted data at once in a dictionary
            Extracted_Data = getattr(eval(i), "get_Data")(fake=True)

            for j in range(tag, min(tag+interval, category_table_count[i])):
                start = time.time()

                # save as json
                if(args['store_json']==True):
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
                                    to_be_json.append(",".join(dct[T[j]][::-1]))
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
