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
    parser.add_argument('--in_dir', default="../../data/infotabs_data/test/processed/", type=str)
    parser.add_argument('--nooflabels', default=2, type=int)
    parser.add_argument('--save_dir', default="../../data/results/", type=str)
    parser.add_argument('--save_folder', default="./", type=str)
    parser.add_argument('--model_dir', default="../../models_saved/", type=str)
    parser.add_argument('--model_name', default="model_4_0.301", type=str)
    parser.add_argument('--mode', default="train", type=str)
    parser.add_argument('--embed_size', default=768, type=int)
    parser.add_argument('--save_enable', default=0, type=int)
    parser.add_argument('--eval_splits', default=["train", "dev", "test_alpha1"],  action='store', type=str, nargs='*')
    parser.add_argument('--seed', default=13, type=int)
    parser.add_argument('--parallel', default=0, type=int)
    parser.add_argument('--inoculate', default=False, type=bool)
    parser.add_argument('--load', default=False, type=bool)
    parser.add_argument('--learning_rate', default=1e-4, type=float)
    parser.add_argument('--store_best', default=False, type=bool)
    parser.add_argument('--dev_file', default="dev", type=str)
    parser.add_argument('--train_file', default="train", type=str)
    parser.add_argument('--eval_splits', default=["train", "dev", "test_alpha1"],  action='store', type=str, nargs='*')
    return parser


def test_data_two_stage(args):
    result_dir = args["save_dir"]+args["save_folder"] + ("first_stage/" if stage == 1 else "second_stage/")

    if args['embed_size'] == 768:
        model = AlbertModel.from_pretrained('albert-base-v2').cuda()
    else:
        model = AlbertModel.from_pretrained('albert-large-v2').cuda()

    if args['parallel']:
        model = nn.DataParallel(model)

    classifier = FeedForward(args['embed_size'], int(
        args['embed_size']/2), args['nooflabels']).cuda()

    checkpoint = torch.load(args['model_dir']  + ("first_stage/" if stage == 1 else "second_stage/") + args['model_name'])
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

    test_data_two_stage(args, stage=1)
    test_data_two_stage(args, stage=2)

    two_stage_aggregate(args)