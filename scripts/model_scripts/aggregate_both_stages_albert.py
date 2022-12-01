import torch
import torch.nn as nn
import torch.optim as optim
from pytorch_transformers import RobertaTokenizer, RobertaForSequenceClassification, RobertaModel, BertModel
from torch.utils.data import TensorDataset, DataLoader
import argparse
import pickle
import time
import json
from feedforward import FeedForward
from tqdm import tqdm
import os
from utils import two_stage_aggregate

def config(parser):
    parser.add_argument('--in_dir_first_stage',  default="./splits/", type=str)
    parser.add_argument('--in_dir_second_stage',  default="./splits/", type=str)
    parser.add_argument('--eval_splits', default=["train", "dev", "test_alpha1"],  action='store', type=str, nargs='*')
    return parser


def test_data(args):
    # result_dir = "../results/"+args['in_dir'].split("/")[-2]+"-"+args['model_dir'].split("/")[-2]
    result_dir = args["save_dir"]+args["save_folder"]

    if args['embed_size'] == 768:
        model = RobertaModel.from_pretrained('roberta-base').cuda()
    else:
        model = RobertaModel.from_pretrained('roberta-large').cuda()

    if args['parallel']:
        model = nn.DataParallel(model)

    classifier = FeedForward(args['embed_size'], int(
        args['embed_size']/2), args['nooflabels']).cuda()

    checkpoint = torch.load(args['model_dir']+args['model_name'])
    model.load_state_dict(checkpoint['model_state_dict'])
    classifier.load_state_dict(checkpoint['classifier_state_dict'])

    for split in args["eval_splits"]:
        try:
            data_file = open(args['in_dir']+split+".pkl", 'rb')
            data = pickle.load(data_file)
            # print(len(data['encodings']))
            acc, gold, pred = test(model, classifier, data, args)
            print("{} accuracy: {}".format(split, acc))

            results = {"accuracy": acc,
                       "gold": gold,
                       "pred": pred}

            if args['save_enable'] != 0:
                if not os.path.isdir(result_dir):
                    os.mkdir(result_dir)
                with open(result_dir+"/predict_"+split+".json", 'w') as fp:
                    json.dump(results, fp)

        except FileNotFoundError:
            print("{}.pkl file doesn't exist".format(split))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser = config(parser)
    args = vars(parser.parse_args())

    two_stage_aggregate(args)