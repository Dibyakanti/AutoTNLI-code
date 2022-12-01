##########################################################
# Data Preprocessing for RoBERTa Base and Albert Base 	 #
##########################################################

import torch
import json
from pytorch_transformers import RobertaTokenizer
from transformers import AlbertTokenizer
import argparse
from utils import get_BERT_vector,get_ALBERT_large_vector,get_ALBERT_base_vector,get_BERTbase_vector
import pickle
import time, os, sys

def preprocess_config(parser):
	parser.add_argument('--max_len', default= 512, type=int)
	parser.add_argument('--data_dir', default="../../data/", type=str)
	parser.add_argument('--in_dir', default="./autotnli_splits",type=str)
	parser.add_argument('--out_dir',default="./autotnli_splits/processed",type=str)
	parser.add_argument('--single_sentence', default=0,type=int)
	parser.add_argument('--splits',default=["train","dev","test_alpha1","test_alpha2","test_alpha3"],  action='store', type=str, nargs='*')
	parser.add_argument('--model',default="Roberta", type=str)
	return parser


def load_sentences(file, header=True, single_sentence=False):
	rows = []
	with open(file, encoding="ISO-8859-1") as f:
		for line in f:
			if header:
				header = False
				continue
			blocks = line.strip().split('\t')
			
			lab = int(blocks[-1])
			if single_sentence:
				sample = {'uid': int(blocks[0]), 'hypothesis': blocks[4], 'label': lab}
			else:
				sample = {'uid': int(blocks[0]), 'premise': blocks[3], 'hypothesis': blocks[4], 'label': lab}
			rows.append(sample)
	return rows


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser = preprocess_config(parser)
	args = vars(parser.parse_args())

	data = {}
	for split in args["splits"]:
		data[split] = load_sentences(args['data_dir']+args['in_dir']+"/"+split+".tsv",
									single_sentence=args['single_sentence'])
		print("{} {} samples loaded".format(len(data[split]),split))

	if args['single_sentence']:
		folder_name = args['data_dir']+args['out_dir']+"_hypo"
	else:
		folder_name = args['data_dir']+args['out_dir']

	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)
	elif len(os.listdir(folder_name)) != 0:
		char = input("""\nThere are existing files in your save directory.\nThis may overwrite data if a split name coincides with a file name. Do you wish to continue? [y/n]: """)
		if char != "y" and char !="Y":
			exit()


	for split in args["splits"]:
		data_dict = {}
		i=0
		for pt_dict in data[split]:
			i+=1
			if args['single_sentence']:
				if(args['model']=="Roberta"):
					enc, amask, segments = get_BERT_vector(pt_dict['hypothesis'],single_sentence=True)
				elif(args['model']=="Albert"):
					enc, amask, segments = get_ALBERT_base_vector(pt_dict['hypothesis'],single_sentence=True)
			else:
				if(args['model']=="Roberta"):
					enc, amask, segments = get_BERT_vector(pt_dict['premise'],pt_dict['hypothesis'])
				elif(args['model']=="Albert"):
					enc, amask, segments = get_ALBERT_base_vector(pt_dict['premise'],pt_dict['hypothesis'])
					
			if len(data_dict.keys())==0:
				data_dict['uid'] = [int(pt_dict['uid'])]
				data_dict['encodings'] = [enc]
				data_dict['attention_mask'] = [amask]
				data_dict['segments'] = [segments]
				data_dict['labels']   = [pt_dict['label']]
			else:
				data_dict['uid'].append(int(pt_dict['uid']))
				data_dict['encodings'].append(enc)
				data_dict['attention_mask'].append(amask)
				data_dict['segments'].append(segments)
				data_dict['labels'].append(pt_dict['label'])
			
			if i%100 == 0:
				print("{} examples processed".format(i))

		print("{} processing done.".format(split))

		output = open(folder_name+"/"+split+".pkl", 'wb')
		pickle.dump(data_dict, output)
		output.close()

	print("Preprocessing Finished")











