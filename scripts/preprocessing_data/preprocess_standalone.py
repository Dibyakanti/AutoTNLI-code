import argparse
import ast
import copy
import json
import math
import os
import random
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from util import *


def config(parser):
    parser.add_argument('--train_complementary_test', default=False, type=bool)
    parser.add_argument('--post_cross_category', default=False, type=bool)
    parser.add_argument('--use_metadata', default=False, type=bool)
    parser.add_argument('--in_dir', default="../../data/autotnli_data/", type=str)
    parser.add_argument('--out_dir', default="../../data/autotnli/splits/random/", type=str)
    parser.add_argument('--metadata_path',
                        default="../../data/splits/", type=str)
    parser.add_argument('--category_list', default=["book", "city", "festival", "foodndrinks", "movie",
                        "organization", "paint", "person", "sportsnevents", "university"],  action='store', type=str, nargs='*')
    parser.add_argument('--table_list', default=[
                        "_T0", "_F1", "_F2", "_F3", "_F4", "_F5"],  action='store', type=str, nargs='*')
    parser.add_argument('--split_type', default="key", type=str)
    return parser


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

    return None


def preprocess_premise_split_util(index, df, table, univ, catg, complement=False):

    ignore_keys = set(["Metro", "City", "Urban"])

    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    add_words = {
        'album': [],
        "city": [],
        "person": ["married", "got", "sings", "worked", "age", "resting", "person", "kids", "labels"],
        "movie": ["done", "produced", "movie", "directed", "budget", "producers", "organization"],
        "book": ["used", "published", "genre"],
        "foodndrinks": ["variants", "ingredients", "type", "alcohol", "colors", "comes"],
        "organization": ["areas", "served", "type", "headquarters", "company's"],
        "paint": ["dimensions", "artist", "located", "painted", "medium", "size"],
        "sportsnevents": ["venue", "competitors"],
        "university": ["established", "endowed", "president", "motto"],
        "festival": ["common", "official", "name", "type", "begins", "called", "related", "observe", 'significance', "frequency", "type(s)"]}

    rem_words = {
        'album': [],
        "city": ["the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "into", "then", "i", "on"],
        "person": ["the", "of", "and", "in", "with", "against", "a", "his", "for", "or", "then", "her", "by", "as", "into", "under", "at", "all", "by", "from", "y", "me", 'ma'],
        "movie": ["the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "at", "from", "for", "don", "will", "i", "am", "me"],
        "book": ["the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "into", "then", "i", "on"],
        "foodndrinks": ["the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "from", "other", "on", "all"],
        "organization": ["the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "from", "other", "for", "more"],
        "paint": ["the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "from", "on", "as", "at", "an", "up", "am", "through", "i", "before"],
        "sportsnevents": ["the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "into", "then", "i", "on", "for", "do", "a", "is", "from", "at", "some", "all"],
        "university": ["are", "all", "the", "of", "and", "with", "against", "a", "his", "by", "or", "into", "then", "i", "on", "is", "let", "there", "be", "we", "she", "he", "our", "my", "for"],
        "festival": ["is", "each", "other", "no", "new", "once", "on", "every", "the", "of", "and", "in", "with", "against", "a", "his", "by", "or", "to", "at", "from", "for", "then", "same", "before", "that", "some", 'as', "than", "all", "after", "other", "because"]}

    rem_words_key_specific = {"Awards": [
        "on"], "Related_to": ["related"], "Type": ["are"]}
    add_words_key_specific = {"Main_ingredients": ["of"], "President": [
        "is"], "Location": ["is"], "Provost": ["the"], "Colors": ["are"]}

    extreme_keys = {
        'Urban': [], 'Metro': [], 'Elevation': ['is', 'elevation'], 'Density': ['density', 'is'], 'City': [], 'Highest_elevation': ['is', 'elevation'],
        'Demonym': ['is', 'demonym'], 'Incorporated': ['city', 'incorporated'], 'Location': ["located"], 'Government': ['government'], 'Lowest_elevation': ['is', 'elevation'], 'Mayor': ['mayor', 'is'],
        'Urban_density': ['urban', 'is'], 'Metro_density': ['metro', 'is'], 'Named_for': ['named', 'after'], "Labels": ['are', 'labels', 'which'], 'Spouse': ['was', 'married', 'to', 'got'], 'Parents': ['were', 'parents', 'of'], 'Occupation': ['worked', 'occupation', 'at', 'this', 'as'], 'Residence': ['residence', 'person', 'resided', 'at'],
        'Born': ['is', 'when', 'was', 'born'], 'Education': ['studied', 'where', 'person'], 'Institutions': ['are', 'worked', 'institutions'], 'Doctoral_students': ['were', 'doctoral', 'students'], 'Relatives': ['relatives', 'are', 'of'], 'Resting_place': ['resting', 'place', 'person'],
        'Conviction': ['charges', 'convicted', 'convicted'], 'Awards': ['won', 'was'], 'Instruments': ['played', 'were'], "Music_by": ["composed", "composers", "worked"], "Starring": ["movie", "acting", "actors", "role"], "Productioncompany": ["named", "produced", "was", "organization"], "Running_time": ["named", "running"], "Release_date": ["released", 'release'],
        "Cinematography": ["was", "done"], "Directed_by": ["director", "movie", "were"], "Edited_by": ["editors", "edited", "movie"], "Produced_by": ["was", "produced", "were", "producers"], "Screenplay_by": ["script", "written", "movie"], "Distributed_by": ["distributors", "were", "distributed", "was"],
        "Motto": ["has", "as", "their", "motto"], "Significance": ['are', "significance"], "Related_to": ["to"], "Date": ["is", "celebrated"], "Observances": ["are", "observances"], "Celebrations": ["involves", "celebrating"], "Observed_by": ["observe", "observed"]
    }

    words = (set(stopwords.words('english')) -
             set(rem_words[catg])) | set(add_words[catg])

    key_check = set([])
    premise = []
    extra_keys = set([])
    for prem in df[df.json_name == table]['key & premises_used']:
        Dict = ast.literal_eval(prem)
        for key in Dict:
            if (key in univ and key not in key_check):
                key_check.add(key)  # check if the key is seen
                i = 0
                for sent in Dict[key]:
                    set_words_1 = (
                        words - set(rem_words_key_specific[key]) if key in rem_words_key_specific else words)
                    set_words = (set_words_1 | set(
                        add_words_key_specific[key]) if key in add_words_key_specific else set_words_1)
                    if (key in extreme_keys):
                        set_words = extreme_keys[key]
                    if ((complement == False) and (" ".join([x.strip() for x in sent.split(" ") if x.strip().lower() in set_words]) == univ[key])):
                        premise.append(sent)
                        i += 1
                        break  # only take one in case of multiple matches
                    elif ((complement == True) and (" ".join([x.strip() for x in sent.split(" ") if x.strip().lower() in set_words]) != univ[key])):
                        premise.append(sent)
                        i += 1
                        break  # only take one in case of multiple matches
                if (i == 0 and complement == True):
                    premise.append(random.sample(Dict[key], 1)[0])
                    i += 1
                # checks
                if (i == 0):
                    print(key)
                    print(Dict[key])
                    print(univ[key])
                elif (i > 1):
                    # print(key, "MORE")
                    print(Dict[key])
                    print(univ[key])
                elif (i > 1):
                    extra_keys.add(key)

            elif (key not in key_check):
                set_words_1 = (
                    words - set(rem_words_key_specific[key]) if key in rem_words_key_specific else words)
                set_words = (set_words_1 | set(
                    add_words_key_specific[key]) if key in add_words_key_specific else set_words_1)
                if (key in extreme_keys):
                    set_words = extreme_keys[key]
                key_check.add(key)
                sent = Dict[key][index]  # index 0 for train in split-4
                univ[key] = " ".join([x.strip() for x in sent.split(
                    " ") if x.strip().lower() in set_words])
                premise.append(sent)

    try:
        if (len(key_check) != len(premise)):
            raise ValueError(" Error : The length of the premise is wrong !")
    except:
        print("STOP!")

    return premise


def preprocess_premise_split(in_dir, out_dir, category_list, table_list, train_complementary_test=False):

    train = []
    dev = []
    test = []

    train_no_para_premises = []
    dev_no_para_premises = []
    test_no_para_premises = []

    for i in category_list:
        univ = {}  # For keeping the template for each different paraphrase
        for j in table_list:
            name = i+j
            df = pd.read_csv(in_dir+name+".tsv", sep="\t")

            num = 30 if len(df.json_name.unique()) > 30 else len(
                df.json_name.unique())  # for entail and non-entail
            list_of_tables = random.sample(list(df.json_name.unique()), num)
            train_list_of_tables = random.sample(list_of_tables, int(0.5*num))
            dev_list_of_tables = random.sample(
                list(set(list_of_tables)-set(train_list_of_tables)), int(0.33*0.5*num))
            test_list_of_tables = list(
                set(list_of_tables)-set(train_list_of_tables)-set(dev_list_of_tables))

            for t in train_list_of_tables:
                s1 = df[df.json_name == t]
                train.append(s1)

                if (i != 'album'):
                    premise = preprocess_premise_split_util(
                        0, df, t, univ, i, False)
                    # make premises without paraphrasing
                    for count in range(len(df[df.json_name == t])):
                        train_no_para_premises.append(
                            ". ".join(random.sample(premise, len(premise))))
                else:
                    for prem in list(s1.premises):
                        train_no_para_premises.append(prem)

            for t in dev_list_of_tables:
                s2 = df[df.json_name == t]
                dev.append(s2)

                if (i != 'album'):
                    # 4-> False , 5 -> True
                    premise = preprocess_premise_split_util(
                        0, df, t, univ, i, train_complementary_test)
                    # make premises without paraphrasing
                    for count in range(len(df[df.json_name == t])):
                        dev_no_para_premises.append(
                            ". ".join(random.sample(premise, len(premise))))
                else:
                    for prem in list(s2.premises):
                        dev_no_para_premises.append(prem)

            for t in test_list_of_tables:
                s3 = df[df.json_name == t]
                test.append(s3)

                if (i != 'album'):
                    # 4-> False , 5 -> True
                    premise = preprocess_premise_split_util(
                        0, df, t, univ, i, train_complementary_test)
                    # make premises without paraphrasing
                    for count in range(len(df[df.json_name == t])):
                        test_no_para_premises.append(
                            ". ".join(random.sample(premise, len(premise))))
                else:
                    for prem in list(s3.premises):
                        test_no_para_premises.append(prem)

    # Concatenate each of the separate samples
    train_set = pd.concat(train, ignore_index=True)
    dev_set = pd.concat(dev, ignore_index=True)
    test_set = pd.concat(test, ignore_index=True)

    # Correct the labels
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

    # pre-process to make it similar to the format of infotabs
    train_set_mod = pd.DataFrame({"table": train_set.table, "json_name": train_set.json_name,
                                  "premise": train_no_para_premises, "hypothesis": train_set.hypothesis, "label": train_set.label})
    dev_set_mod = pd.DataFrame({"table": dev_set.table, "json_name": dev_set.json_name,
                                "premise": dev_no_para_premises, "hypothesis": dev_set.hypothesis, "label": dev_set.label})
    test_set_mod = pd.DataFrame({"table": test_set.table, "json_name": test_set.json_name,
                                "premise": test_no_para_premises, "hypothesis": test_set.hypothesis, "label": test_set.label})

    # extra step for reducing size if necessary
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


def entity_based_separation(entity_list, df, Entity_key):

    keys_set = set([])
    for entity in entity_list:
        for x in Entity_key[entity]:
            keys_set.add(x)

    length = len(df)
    rem_index = []
    for index in range(length):
        keys = list(ast.literal_eval(
            df[df.index == index]["key & premises_used"][index]).keys())
        if (len(set(keys) & keys_set) != len(keys)):
            rem_index.append(index)
    df = df.drop(df.index[rem_index])

    return df


def preprocess_entity_split(in_dir, out_dir, category_list, table_list):

    Entity_key = {
        "Person": ["Main_character", "Written_by", "Mayor", "Named_for", "President", "Provost", "Artist", "Key_people", "Founder", "Owner", "Directed_by", "Produced_by", "Screenplay_by", "Starring", "Music_by", "Cinematography", "Edited_by", "Spouse", "Children", "Genres", "Doctoral_students", "Relatives", "Parents"],
        "PersonType": ["Occupation"],
        "Skill": ["Industry", "Fields"],
        "Organization": ["Producer", "Label", "Publisher", "Government", "Sporting_affiliations", "Academic_affiliations", "Former_names", "Subsidiaries", "Predecessor", "Production_company", "Distributed_by", "Manufacturer", "Education", "Labels", "Institutions"],
        "Quantity": ["Length", "No_of_issues", "Elevation", "Metro", "Urban", "Highest_elevation", "Land", "Water", "City", "Demonym", "Lowest_elevation", "Density", "Metro_density", "Urban_density", "Frequency", "Undergraduates", "Postgraduates", "Campus", "Administrative_staff", "Academic_staff", "Endowment", "Dimensions", "Number_of_employees", "Running_time",
                     "Budget", "Box_office", "Alcohol_by_volume", "Competitors", "Teams", "No_of_events", "Age"],
        "DateTime": ["Released", "Recorded", "Schedule", "Publication_date", "Time_zone", "Incorporated", "Date", "Bgins", "Ends", '2021_date', '2020_date', '2019_date', '2018_date', "Established", "Year", "Founded", "Release_date", "Introduced", "Established", "Official_site", "Born", "Death", "Years_active"],
        "Location": ["Studio", "Province", "Location", "Area_code", "Postal_code", "Coordinates", "Headquarters", "Area_served", "Country", "Country_of_origin", "Venue", "Date", "Resting_place", "Residence"],
        "Other": ["Genre", "Format", "Type", "Observed_by", "Significance", "Observances", "Type", "Motto", "Nickname", "Colors", "Mascot", "Language", "Variants", "Color"],
        "Event": ["Celebrations", "Related_to", "Also_called", "Official_name", "Traded_as", "Conviction"],
        "URL": ["Website"],
        "Product": ["Medium", "Products", "Related_products", "Main_ingredients", "Awards", "Instruments"],
    }

    names = []
    for i in category_list:
        for j in table_list:
            names.append(i+j)

    train = []
    dev = []
    test = []

    for name in names:
        df = pd.read_csv(in_dir+name+".tsv", sep="\t")
        num = 500 if len(df.json_name.unique()) > 500 else len(
            df.json_name.unique())  # for entail and non-entail
        list_of_tables = random.sample(list(df.json_name.unique()), num)
        train_list_of_tables = random.sample(list_of_tables, int(0.5*num))
        dev_list_of_tables = random.sample(
            list(set(list_of_tables)-set(train_list_of_tables)), int(0.33*0.5*num))
        test_list_of_tables = list(
            set(list_of_tables)-set(train_list_of_tables)-set(dev_list_of_tables))
        for t in train_list_of_tables:
            s1 = df[df.json_name == t]
            train.append(s1)
        for t in dev_list_of_tables:
            s2 = df[df.json_name == t]
            dev.append(s2)
        for t in test_list_of_tables:
            s3 = df[df.json_name == t]
            test.append(s3)

    train_set = pd.concat(train, ignore_index=True)
    dev_set = pd.concat(dev, ignore_index=True)
    test_set = pd.concat(test, ignore_index=True)

    print("Creating train-test split done")

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

    print("Checked the labels")

    # check for ent
    train_entity_list = ["URL", "Event", "PersonType", "Skill", "Product"]
    train_set_ent = entity_based_separation(
        train_entity_list, train_set, Entity_key)
    dev_entity_list = ["Quantity", "Other", "Person"]
    dev_set_ent = entity_based_separation(dev_entity_list, dev_set, Entity_key)
    test_entity_list = ["DateTime", "Organization", "Location"]
    test_set_ent = entity_based_separation(
        test_entity_list, test_set, Entity_key)

    train_set_mod = pd.DataFrame({"table": train_set_ent.table, "json_name": train_set_ent.json_name,
                                  "premise": train_set_ent.premises, "hypothesis": train_set_ent.hypothesis, "label": train_set_ent.label})
    dev_set_mod = pd.DataFrame({"table": dev_set_ent.table, "json_name": dev_set_ent.json_name,
                                "premise": dev_set_ent.premises, "hypothesis": dev_set_ent.hypothesis, "label": dev_set_ent.label})
    test_set_mod = pd.DataFrame({"table": test_set_ent.table, "json_name": test_set_ent.json_name,
                                "premise": test_set_ent.premises, "hypothesis": test_set_ent.hypothesis, "label": test_set_ent.label})

    train_set_mod = train_set_mod.sample(frac=1).reset_index(drop=True)
    dev_set_mod = dev_set_mod.sample(frac=0.4).reset_index(drop=True)
    test_set_mod = test_set_mod.sample(frac=0.4).reset_index(drop=True)

    # make sure to have different out_dir for separate splits
    if not os.path.exists(out_dir):  # ../splits/split1 for split1
        os.makedirs(out_dir)

    train_set_mod.to_csv(out_dir+"train.tsv", sep="\t", index_label="index")
    dev_set_mod.to_csv(out_dir+"dev.tsv", sep="\t", index_label="index")
    test_set_mod.to_csv(out_dir+"test_alpha1.tsv",
                        sep="\t", index_label="index")

    return None


if __name__ == "__main__":

    nltk.download('stopwords')

    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    in_dir = args['in_dir']
    out_dir = args['out_dir']
    category_list = args['category_list']
    table_list = args['table_list']
    train_complementary_test = args['train_complementary_tes']
    post_cross_category = args['post_cross_category']
    use_metadata = args['use_metadata']
    metadata_path = args['metadata_path']
    split_type = args['split_type']

    if (args['split_type'] == "category"):
        preprocess_category_split(
            in_dir, out_dir, category_list, table_list, post_cross_category)
    elif (args['split_type'] == "key"):
        preprocess_key_split(in_dir, out_dir, category_list,
                             table_list, metadata_path, use_metadata)
    elif (args['split_type'] == "premise"):
        preprocess_premise_split(
            in_dir, out_dir, category_list, table_list, train_complementary_test)
    elif (args['split_type'] == "entity"):
        preprocess_entity_split(in_dir, out_dir, category_list, table_list)
