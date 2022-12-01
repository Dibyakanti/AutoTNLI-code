##########################
# Utility functions      #
##########################

import torch
import time
import sys
from transformers import AlbertModel
from pytorch_transformers import RobertaTokenizer, BertTokenizer
from transformers import AlbertTokenizer
import numpy as np
import json

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
tokenizer_bert = BertTokenizer.from_pretrained('bert-base-cased')
tokenizer_albert = AlbertTokenizer.from_pretrained('albert-base-v2')
tokenizer_albert_large = AlbertTokenizer.from_pretrained('albert-large-v2')


def _truncate_seq_pair(tokens_a, max_length):
    """Truncates a sequence pair in place to the maximum length.
    Copyed from https://github.com/huggingface/pytorch-pretrained-BERT
    """
    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a)
        if total_length <= max_length:
            break
        tokens_a.pop()


def get_BERT_vector(sent1, sent2=None, max_sent1_len=400, max_sent2_len=100, single_sentence=False):
    # Preparing attention mask so no attention is given to
    # padded tokens for sentence 1
    attention_mask_sent1 = [1]*(max_sent1_len+2)

    sent1_encoding = tokenizer.encode("<s>" + sent1)

    _truncate_seq_pair(sent1_encoding, max_sent1_len+1)

    attention_mask_sent1[len(sent1_encoding):max_sent1_len +
                         1] = [0]*(max_sent1_len-len(sent1_encoding)+1)
    sent1_encoding.extend([tokenizer.encode("<pad>")[0]]
                          * (max_sent1_len-len(sent1_encoding)+1))
    sent1_encoding.extend(tokenizer.encode("</s>"))

    # Preparing attention mask so no attention is given tokens
    # padded tokens for sentence 2
    if not single_sentence:
        attention_mask_sent2 = [1]*(max_sent2_len+2)

        sent2_encoding = tokenizer.encode("</s>"+sent2)

        attention_mask_sent2[len(
            sent2_encoding):max_sent2_len+1] = [0]*(max_sent2_len-len(sent2_encoding)+1)
        sent2_encoding.extend([tokenizer.encode("<pad>")[0]]
                              * (max_sent2_len-len(sent2_encoding)+1))
        sent2_encoding.extend(tokenizer.encode("</s>"))
    else:
        attention_mask_sent2 = [0]*(max_sent2_len+2)
        sent2_encoding = [tokenizer.encode("<pad>")[0]]*(max_sent2_len+2)

    # Fixing segment ids
    segments = [0]*(max_sent1_len+2)
    if not single_sentence:
        segments.extend([1]*(max_sent2_len+2))
    else:
        segments.extend([0]*(max_sent2_len+2))

    sentences_encoding = sent1_encoding
    attention_mask = attention_mask_sent1

    sentences_encoding.extend(sent2_encoding)
    attention_mask.extend(attention_mask_sent2)

    return sentences_encoding, attention_mask, segments


def get_ALBERT_large_vector(sent1, sent2=None, max_sent1_len=400, max_sent2_len=100, single_sentence=False):
    # Preparing attention mask so no attention is given to
    # padded tokens for sentence 1
    attention_mask_sent1 = [1]*(max_sent1_len+2)

    sent1_encoding = tokenizer_albert_large.encode("[CLS] " + sent1)

    _truncate_seq_pair(sent1_encoding, max_sent1_len+1)

    attention_mask_sent1[len(sent1_encoding):max_sent1_len +
                         1] = [0]*(max_sent1_len-len(sent1_encoding)+1)
    sent1_encoding.extend([tokenizer_albert_large.encode(
        "[PAD]")[0]]*(max_sent1_len-len(sent1_encoding)+1))
    sent1_encoding.extend([tokenizer_albert_large.encode("[SEP]")[0]])

    # Preparing attention mask so no attention is given tokens
    # padded tokens for sentence 2
    if not single_sentence:
        attention_mask_sent2 = [1]*(max_sent2_len+1)

        sent2_encoding = tokenizer_albert_large.encode(sent2)

        attention_mask_sent2[len(sent2_encoding):max_sent2_len] = [
            0]*(max_sent2_len-len(sent2_encoding))
        sent2_encoding.extend([tokenizer_albert_large.encode(
            "[PAD]")[0]]*(max_sent2_len-len(sent2_encoding)))
        sent2_encoding.extend([tokenizer_albert_large.encode("[SEP]")[0]])
    else:
        attention_mask_sent2 = [0]*(max_sent2_len+1)
        sent2_encoding = [tokenizer_albert_large.encode("[PAD]")[
            0]]*(max_sent2_len+1)

    # Fixing segment ids
    segments = [0]*(max_sent1_len+2)
    if not single_sentence:
        segments.extend([1]*(max_sent2_len+1))
    else:
        segments.extend([0]*(max_sent2_len+1))

    sentences_encoding = sent1_encoding
    attention_mask = attention_mask_sent1

    sentences_encoding.extend(sent2_encoding)
    attention_mask.extend(attention_mask_sent2)

    return sentences_encoding, attention_mask, segments


def get_ALBERT_base_vector(sent1, sent2=None, max_sent1_len=400, max_sent2_len=100, single_sentence=False):
    # Preparing attention mask so no attention is given to
    # padded tokens for sentence 1
    attention_mask_sent1 = [1]*(max_sent1_len+2)

    sent1_encoding = tokenizer_albert.encode("[CLS] " + sent1)

    _truncate_seq_pair(sent1_encoding, max_sent1_len+1)

    attention_mask_sent1[len(sent1_encoding):max_sent1_len +
                         1] = [0]*(max_sent1_len-len(sent1_encoding)+1)
    sent1_encoding.extend([tokenizer_albert.encode(
        "[PAD]")[0]]*(max_sent1_len-len(sent1_encoding)+1))
    sent1_encoding.extend([tokenizer_albert.encode("[SEP]")[0]])

    # Preparing attention mask so no attention is given tokens
    # padded tokens for sentence 2
    if not single_sentence:
        attention_mask_sent2 = [1]*(max_sent2_len+1)

        sent2_encoding = tokenizer_albert.encode(sent2)

        attention_mask_sent2[len(sent2_encoding):max_sent2_len] = [
            0]*(max_sent2_len-len(sent2_encoding))
        sent2_encoding.extend([tokenizer_albert.encode(
            "[PAD]")[0]]*(max_sent2_len-len(sent2_encoding)))
        sent2_encoding.extend([tokenizer_albert.encode("[SEP]")[0]])
    else:
        attention_mask_sent2 = [0]*(max_sent2_len+1)
        sent2_encoding = [tokenizer_albert.encode(
            "[PAD]")[0]]*(max_sent2_len+1)

    # Fixing segment ids
    segments = [0]*(max_sent1_len+2)
    if not single_sentence:
        segments.extend([1]*(max_sent2_len+1))
    else:
        segments.extend([0]*(max_sent2_len+1))

    sentences_encoding = sent1_encoding
    attention_mask = attention_mask_sent1

    sentences_encoding.extend(sent2_encoding)
    attention_mask.extend(attention_mask_sent2)

    return sentences_encoding, attention_mask, segments


def get_BERTbase_vector(sent1, sent2=None, max_sent1_len=400, max_sent2_len=100, single_sentence=False):
    # Preparing attention mask so no attention is given to
    # padded tokens for sentence 1
    attention_mask_sent1 = [1]*(max_sent1_len+2)

    sent1_encoding = tokenizer_bert.encode("[CLS] " + sent1)

    _truncate_seq_pair(sent1_encoding, max_sent1_len+1)

    attention_mask_sent1[len(sent1_encoding):max_sent1_len +
                         1] = [0]*(max_sent1_len-len(sent1_encoding)+1)
    sent1_encoding.extend([tokenizer_bert.encode("[PAD]")[0]]
                          * (max_sent1_len-len(sent1_encoding)+1))
    sent1_encoding.extend(tokenizer_bert.encode("[SEP]"))

    # Preparing attention mask so no attention is given tokens
    # padded tokens for sentence 2
    if not single_sentence:
        attention_mask_sent2 = [1]*(max_sent2_len+1)

        sent2_encoding = tokenizer_bert.encode(sent2)

        attention_mask_sent2[len(sent2_encoding):max_sent2_len] = [
            0]*(max_sent2_len-len(sent2_encoding))
        sent2_encoding.extend([tokenizer_bert.encode(
            "[PAD]")[0]]*(max_sent2_len-len(sent2_encoding)))
        sent2_encoding.extend(tokenizer_bert.encode("[SEP]"))
    else:
        attention_mask_sent2 = [0]*(max_sent2_len+1)
        sent2_encoding = [tokenizer_bert.encode("[PAD]")[0]]*(max_sent2_len+1)

    # Fixing segment ids
    segments = [0]*(max_sent1_len+2)
    if not single_sentence:
        segments.extend([1]*(max_sent2_len+1))
    else:
        segments.extend([0]*(max_sent2_len+1))

    sentences_encoding = sent1_encoding
    attention_mask = attention_mask_sent1

    sentences_encoding.extend(sent2_encoding)
    attention_mask.extend(attention_mask_sent2)

    return sentences_encoding, attention_mask, segments


def two_stage_aggregate(args):
	for dataset in args["eval_splits"]:
		f = open(args["save_dir"]+args["save_folder"]+"first_stage/"+str(dataset)+'.json',)
		first_part_json = json.load(f)
		f.close()

		f = open(args["save_dir"]+args["save_folder"]+"second_stage/"+str(dataset)+'.json',)
		second_part_json = json.load(f)
		f.close()

		first_part_json['pred']
		predictions_2_step = []

		for i in range(len(first_part_json['pred'])):
			if (first_part_json['pred'][i] == 1):
				predictions_2_step.append(1)
			elif (second_part_json['pred'][i] == 0):
				predictions_2_step.append(0)
			else:
				predictions_2_step.append(2)

		accuracy = np.sum(np.equal(predictions_2_step, second_part_json['gold']))/len(predictions_2_step)
		print(dataset, " : ", accuracy)

		return None
