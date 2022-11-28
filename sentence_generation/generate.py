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


# def config(parser):
#     parser.add_argument('--epochs',  default=10, type=int)
#     parser.add_argument('--batch_size',  default=4, type=int)
#     # parser.add_argument('--in_dir', default="./../../temp/processed/parapremise/", type=str)
#     parser.add_argument('--nooflabels', default=3, type=int)
#     # parser.add_argument('--save_dir', default="./../../temp/models", type=str)
#     parser.add_argument('--save_folder', default="parapremise/", type=str)
#     # parser.add_argument('--model_dir',default="./../../temp/models/parapremise/",type=str)
#     parser.add_argument('--model_name', default="model_4_0.301", type=str)
#     parser.add_argument('--mode', default="train", type=str)
#     parser.add_argument('--embed_size', default=768, type=int)
#     parser.add_argument('--save_enable', default=0, type=int)
#     parser.add_argument('--eval_splits', default=["train", "dev", "test_alpha1"],  action='store', type=str, nargs='*')
#     parser.add_argument('--seed', default=13, type=int)
#     parser.add_argument('--parallel', default=0, type=int)
#     # parser.add_argument('--multi_gpu_on', action='store_true')   # use for multi gpu training (not needed)

#     return parser

def config(parser):
    parser.add_argument('--interval',  default=50, type=int)
    parser.add_argument('--category', default=None, type=str)
#     parser.add_argument('--eval_splits', default=["train", "dev", "test_alpha1"],  action='store', type=str, nargs='*')

    return parser


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    interval = int(args['interval'])
    p = ThreadPool()
    for tag in np.arange(0, 200, interval):
        premises = []
        hypothesis = []
        label = []
        json_name = []
        table = []
        premises_used = []

        for i in ["City"]:
            N, T = getattr(eval(i), "get_Table_Title")()

            # getting all the extracted data at once in a dictionary
            Extracted_Data = getattr(eval(i), "get_Data")()

            for j in range(tag, min(tag+interval, category_table_count[i])):
                start = time.time()
                premise = []
                count = 0  # keep count of the number of premises to be generated
                key_premises = {}
                k_range = len(Dict[i]) if i != "Person" else len(Dict[i+"1"])

                # for k_index in range(len(Dict[i+"1"])):
                #   k = Dict[i+"2"][k_index]
                #   k1 = Dict[i+"1"][k_index]

                for k_index in range(k_range):
                    k = Dict[i][k_index] if i != "Person" else Dict[i+"2"][k_index]
                    # D = Extracted_Data[k1]
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
                if(j%10):
                    print("{} : {}".format(j,(time.time()-start)/60))
        df = pd.DataFrame({"table": table, "premises": premises, "hypothesis": hypothesis,
                           "label": label, "key & premises_used": premises_used, "json_name": json_name})
        df.to_csv("/content/drive/MyDrive/psn/"+i.split("_")
                  [0].lower()+"_T0_"+str(int(tag/interval))+".tsv", sep="\t")
        del df
