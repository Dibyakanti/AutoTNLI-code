import argparse
import pandas as pd
import numpy as np
import math
import copy
import random
import ast
import json
import os


def config(parser):
    parser.add_argument('--stage', default=2, type=int)
    parser.add_argument('--in_dir', default="../autotnli_data/", type=str)
    parser.add_argument('--out_dir', default="../splits/random/", type=str)
    parser.add_argument('--few_shot', default=False, type=bool)
    return parser


def preprocess_infotabs_data(in_dir, out_dir , stage, few_shot=False):

    if (stage == 1):
        print("Stage-1 data")
        for name in ["dev","test_alpha1","test_alpha2","test_alpha3","train"]:
            df = pd.read_csv(in_dir+name+".tsv", sep="\t", index_col="index")

            # first part for using only two labels while training  initial labels 0-E,1-N,2-C
            df["label"].replace({0: 0, 1: 1, 2: 0}, inplace=True)

            if (few_shot and name=="train"):
                table_list = list(df.table_id.unique())
                list_25 = random.sample(table_list, int(0.25*len(table_list)))
                list_20 = random.sample(list_25, int(0.80*len(list_25)))
                list_15 = random.sample(list_20, int(0.75*len(list_20)))
                list_10 = random.sample(list_15, int(0.6666*len(list_15)))
                list_5 = random.sample(list_10, int(0.50*len(list_10)))
                df_25, df_20, df_15, df_10, df_5 = df[df.table_id.isin(list_25)], df[df.table_id.isin(
                    list_20)], df[df.table_id.isin(list_15)], df[df.table_id.isin(list_10)], df[df.table_id.isin(list_5)]
                df_5.to_csv(out_dir+"train_5"+".tsv",
                            sep="\t", index_label="index")
                df_10.to_csv(out_dir+"train_10"+".tsv",
                            sep="\t", index_label="index")
                df_15.to_csv(out_dir+"train_15"+".tsv",
                            sep="\t", index_label="index")
                df_20.to_csv(out_dir+"train_20"+".tsv",
                            sep="\t", index_label="index")
                df_25.to_csv(out_dir+"train_25"+".tsv",
                            sep="\t", index_label="index")
            else:
                df.to_csv(out_dir+name+".tsv",sep="\t",index_label="index")

    elif (stage == 2):
        print("Stage-2 data")
        for name in ["dev","test_alpha1","test_alpha2","test_alpha3","train"]:
            df = pd.read_csv(in_dir+name+".tsv", sep="\t", index_col="index")

            df = df[df.label != 1].reset_index(drop=True)  # second part
            # second part for using only two labels while training  initial labels 0-E,1-N,2-C
            df["label"].replace({0: 0, 2: 1}, inplace=True)

            if (few_shot):
                table_list = list(df.table_id.unique())
                list_25 = random.sample(table_list, int(0.25*len(table_list)))
                list_20 = random.sample(list_25, int(0.80*len(list_25)))
                list_15 = random.sample(list_20, int(0.75*len(list_20)))
                list_10 = random.sample(list_15, int(0.6666*len(list_15)))
                list_5 = random.sample(list_10, int(0.50*len(list_10)))
                df_25, df_20, df_15, df_10, df_5 = df[df.table_id.isin(list_25)], df[df.table_id.isin(
                    list_20)], df[df.table_id.isin(list_15)], df[df.table_id.isin(list_10)], df[df.table_id.isin(list_5)]
                df_5.to_csv(out_dir+"train_5"+".tsv",
                            sep="\t", index_label="index")
                df_10.to_csv(out_dir+"train_10"+".tsv",
                            sep="\t", index_label="index")
                df_15.to_csv(out_dir+"train_15"+".tsv",
                            sep="\t", index_label="index")
                df_20.to_csv(out_dir+"train_20"+".tsv",
                            sep="\t", index_label="index")
                df_25.to_csv(out_dir+"train_25"+".tsv",
                            sep="\t", index_label="index")
            else:
                df.to_csv(out_dir+name+".tsv",sep="\t",index_label="index")

    else:
         print("Stage can only be 1 or 2")   

    return None


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    in_dir = args['in_dir']
    out_dir = args['out_dir']
    stage = args['stage']
    few_shot = args['few_shot']

    preprocess_infotabs_data(in_dir, out_dir, stage, few_shot)