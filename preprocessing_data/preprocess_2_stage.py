import argparse
import pandas as pd
import numpy as np
import math
import copy
import random
import ast
import json


def config(parser):
    parser.add_argument('--cutoff', default=30, type=int)
    parser.add_argument('--relevant_rows', default=False, type=bool)
    parser.add_argument('--root', default="../autotnli_data/", type=str)
    parser.add_argument('--keep_addr', default="../splits/", type=str)
    parser.add_argument('--category_list', default=["Book", "City", "Festival", "FoodnDrinks", "Movie",
                        "Organization", "Paint", "Person", "SportsnEvents", "University"],  action='store', type=str, nargs='*')
    parser.add_argument('--table_list', default=[
                        "T0", "_F1", "_F2", "_F3", "_F4", "_F5"],  action='store', type=str, nargs='*')
    return parser


def preprocess_data(root, keep_addr, category_list, table_list, cutoff=30, relevant_rows=False):

    names = []
    for i in category_list:
        for j in table_list:
            names.append(i+j)

    train = []

    for name in names:
        df = pd.read_csv(root+name+".tsv", sep="\t")

        num = cutoff if len(df.json_name.unique()) > cutoff else len(
            df.json_name.unique())  # for entail and non-entail # 30,200
        list_of_tables = random.sample(list(df.json_name.unique()), num)
        for t in list_of_tables:
            s1 = df[df.json_name == t].sample(frac=1)
            train.append(s1)

    train_set = pd.concat(train, ignore_index=True).drop(
        columns=["Unnamed: 0", "Unnamed: 0.1"])

    for x in range(len(train_set.label)):  # correct the labels
        if (train_set.label[x] == 1 or train_set.label[x] == "E"):
            train_set.label[x] = 0
        else:
            train_set.label[x] = 1

    if (relevant_rows):  # make a list of premises with only the relevant rows
        train_relevant_premises = []
        for used_premises in train_set["key & premises_used"]:
            dictionary = ast.literal_eval(used_premises)
            temp_premises = []
            for key in dictionary.keys():
                temp_premises.append(random.sample(dictionary[key], 1)[0])
            train_relevant_premises.append(". ".join(temp_premises) + ". ")

        train_set_mod = pd.DataFrame({"table": train_set.table, "json_name": train_set.json_name,
                                     "premise": train_relevant_premises, "hypothesis": train_set.hypothesis, "label": train_set.label})

    else:
        train_set_mod = pd.DataFrame({"table": train_set.table, "json_name": train_set.json_name,
                                     "premise": train_set.premises, "hypothesis": train_set.hypothesis, "label": train_set.label})

    train_set_mod = train_set_mod.sample(frac=1).reset_index(drop=True)
    dev_set_mod = train_set_mod.sample(frac=0.1).reset_index(drop=True)
    test_set_mod = train_set_mod.sample(frac=0.01).reset_index(drop=True)

    ''' only infotabs training and Auto-TNLI testing data '''
    # test_set_mod_alpha1 = train_set_mod.sample(frac=1).reset_index(drop=True) # both real and counterfactual
    # test_set_mod_alpha2 = train_set_mod[train_set_mod.json_name.str.contains("T0")].sample(frac=1).reset_index(drop=True) # only real
    # test_set_mod_alpha3 = train_set_mod[train_set_mod.json_name.str.contains("_F")].sample(frac=1).reset_index(drop=True) # only counterfactual

    train_set_mod.to_csv(keep_addr+"train.tsv", sep="\t", index_label="index")
    dev_set_mod.to_csv(keep_addr+"dev.tsv", sep="\t", index_label="index")
    test_set_mod.to_csv(keep_addr+"test_alpha1.tsv",
                        sep="\t", index_label="index")

    return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    root = args['root']
    keep_addr = args['keep_addr']
    category_list = args['category_list']
    table_list = args['table_list']
    cutoff = args['cutoff']
    relevant_rows = args['relevant_rows']

    preprocess_data(root, keep_addr, category_list,
                    table_list, cutoff, relevant_rows)
