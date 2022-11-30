import pandas as pd
import numpy as np
import math
import copy
import random
import ast
import json
import os
from util import *


def preprocess_category_split(in_dir, out_dir, category_list, table_list, post_cross_category=False):

    train = []
    dev = []
    test = []

    if (post_cross_category):  # split 2
        train_split = ["book", "paint",
                       "sportsnevents", "foodndrinks", "album"]
        dev_split = ["person", "city", "movie"]
    else:  # split 1
        train_split = ["person", "city", "movie"]
        dev_split = ["album", "festival", "paint", "organization"]

    for i in category_list:
        for j in table_list:
            name = i+j
            df = pd.read_csv(in_dir+name+".tsv", sep="\t")

            n = 15 if (i in dev_split) else (60 if (i in train_split) else 40)
            num = n if len(df.json_name.unique()) > n else len(
                df.json_name.unique())
            list_of_tables = random.sample(list(df.json_name.unique()), num)
            for t in list_of_tables:
                s1 = df[df.json_name == t].sample(frac=1)
                if (i in train_split):
                    train.append(s1)
                elif (i in dev_split):
                    dev.append(s1)
                else:
                    test.append(s1)

    train_set = pd.concat(train, ignore_index=True)
    dev_set = pd.concat(dev, ignore_index=True)
    test_set = pd.concat(test, ignore_index=True)

    # correct the labels
    for x in range(len(train_set.label)):
        if (train_set.label[x] == 1 or train_set.label[x] == "E"):
            train_set.label[x] = 0
        else:
            train_set.label[x] = 1

    for x in range(len(dev_set.label)):
        if (dev_set.label[x] == 1 or dev_set.label[x] == "E"):
            dev_set.label[x] = 0
        else:
            dev_set.label[x] = 1

    for x in range(len(test_set.label)):
        if (test_set.label[x] == 1 or test_set.label[x] == "E"):
            test_set.label[x] = 0
        else:
            test_set.label[x] = 1

    train_set_mod = pd.DataFrame({"table": train_set.table, "json_name": train_set.json_name,
                                  "premise": train_set.premises, "hypothesis": train_set.hypothesis, "label": train_set.label})
    dev_set_mod = pd.DataFrame({"table": dev_set.table, "json_name": dev_set.json_name,
                                "premise": dev_set.premises, "hypothesis": dev_set.hypothesis, "label": dev_set.label})
    test_set_mod = pd.DataFrame({"table": test_set.table, "json_name": test_set.json_name,
                                "premise": test_set.premises, "hypothesis": test_set.hypothesis, "label": test_set.label})

    train_set_mod = train_set_mod.sample(frac=1).reset_index(drop=True)
    dev_set_mod = dev_set_mod.sample(frac=1).reset_index(drop=True)
    test_set_mod = test_set_mod.sample(frac=1).reset_index(drop=True)

    # make sure to have different out_dir for separate splits
    if not os.path.exists(out_dir):  # ../splits/split1 for split1
        os.makedirs(out_dir)

    train_set_mod.to_csv(out_dir+"train.tsv", sep="\t", index_label="index")
    dev_set_mod.to_csv(out_dir+"dev.tsv", sep="\t", index_label="index")
    test_set_mod.to_csv(out_dir+"test_alpha1.tsv",
                        sep="\t", index_label="index")

    return None


def preprocess_key_split(in_dir, out_dir, category_list, table_list, metadata_path, use_metadata=False):

    train = []
    dev = []
    test = []

    for i in category_list:
        all_keys = set([])
        for j in table_list:
            name = i+j
            df = pd.read_csv(in_dir+name+".tsv", sep="\t")
            if (j == "_T0"):
                for l in df["key & premises_used"]:
                    for key in ast.literal_eval(l).keys():
                        all_keys.add(key)
                if (use_metadata):
                    with open(metadata_path+"metadata.json", "r") as read_it:
                        data = json.load(read_it)
                    train_key = data["train_keys"]
                    dev_key = data["dev_keys"]
                    test_key = data["test_keys"]
                else:
                    train_key = random.sample(all_keys, int(0.5*len(all_keys)))
                    dev_key = random.sample(
                        (all_keys-set(train_key)), int(0.2*len(all_keys)))
                    test_key = (all_keys-set(train_key))-set(dev_key)
            num = 30 if len(df.json_name.unique()) > 30 else len(
                df.json_name.unique())
            list_of_tables = random.sample(list(df.json_name.unique()), num)
            for t in list_of_tables:
                s1 = df[df.json_name == t].sample(frac=1).reset_index()
                for index in range(len(s1)):
                    k = set(ast.literal_eval(
                        s1[s1.index == index]["key & premises_used"][index]).keys())
                    if (k.issubset(train_key)):
                        train.append(s1[s1.index == index])
                    elif (k.issubset(dev_key)):
                        dev.append(s1[s1.index == index])
                    elif (k.issubset(test_key)):
                        test.append(s1[s1.index == index])
                    else:
                        ind = random.sample(range(3), 1)
                        if (ind == 0):
                            train.append(s1[s1.index == index])
                        elif (ind == 1):
                            dev.append(s1[s1.index == index])
                        else:
                            test.append(s1[s1.index == index])

    train_set = pd.concat(train, ignore_index=True)
    dev_set = pd.concat(dev, ignore_index=True)
    test_set = pd.concat(test, ignore_index=True)

    # correct the labels
    for x in range(len(train_set.label)):
        if (train_set.label[x] == 1 or train_set.label[x] == "E"):
            train_set.label[x] = 0
        else:
            train_set.label[x] = 1

    for x in range(len(dev_set.label)):
        if (dev_set.label[x] == 1 or dev_set.label[x] == "E"):
            dev_set.label[x] = 0
        else:
            dev_set.label[x] = 1

    for x in range(len(test_set.label)):
        if (test_set.label[x] == 1 or test_set.label[x] == "E"):
            test_set.label[x] = 0
        else:
            test_set.label[x] = 1

    train_set_mod = pd.DataFrame({"table": train_set.table, "json_name": train_set.json_name,
                                  "premise": train_set.premises, "hypothesis": train_set.hypothesis, "label": train_set.label})
    dev_set_mod = pd.DataFrame({"table": dev_set.table, "json_name": dev_set.json_name,
                                "premise": dev_set.premises, "hypothesis": dev_set.hypothesis, "label": dev_set.label})
    test_set_mod = pd.DataFrame({"table": test_set.table, "json_name": test_set.json_name,
                                "premise": test_set.premises, "hypothesis": test_set.hypothesis, "label": test_set.label})

    train_set_mod = train_set_mod.sample(frac=1).reset_index(drop=True)
    dev_set_mod = dev_set_mod.sample(frac=1).reset_index(drop=True)
    test_set_mod = test_set_mod.sample(frac=1).reset_index(drop=True)

    # make sure to have different out_dir for separate splits
    if not os.path.exists(out_dir):  # ../splits/split1 for split1
        os.makedirs(out_dir)

    train_set_mod.to_csv(out_dir+"train.tsv", sep="\t", index_label="index")
    dev_set_mod.to_csv(out_dir+"dev.tsv", sep="\t", index_label="index")
    test_set_mod.to_csv(out_dir+"test_alpha1.tsv",
                        sep="\t", index_label="index")

    # store the keys used in train-dev-test in a json file
    metadata_dict = {"train_keys": train_key,
                     "dev_keys": dev_key, "test_keys": test_key}
    out_file = open(out_dir+"metadata.json", "w")
    json.dump(metadata_dict, out_file)
    out_file.close()
