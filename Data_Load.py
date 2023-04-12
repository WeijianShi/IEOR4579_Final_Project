import numpy as np
import pandas as pd
from Hashing import lst_gram
import args


def load_vocab():
    vocab = open(args.VOCAB_FILE, encoding='utf-8').readlines()
    slice2idx = {}
    idx2slice = {}
    cnt = 0
    for char in vocab:
        char = char.strip('\n')
        slice2idx[char] = cnt
        idx2slice[cnt] = char
        cnt += 1
    return slice2idx, idx2slice


def padding(text, maxlen=args.SENTENCE_MAXLEN):
    pad_text = []
    for sentence in text:

        pad_sentence = np.zeros(maxlen).astype('int64')  # build a all zero vector that matches the shape of text
        cnt = 0
        for index in sentence:
            pad_sentence[cnt] = index
            cnt += 1
            if cnt == maxlen:
                break
        pad_text.append(pad_sentence.tolist())
    return pad_text


def char_index(text_a, text_b):
    slice2idx, idx2slice = load_vocab()
    a_list, b_list = [], []

    # for each line (parsed into two sentences)in the file
    for a_sentence, b_sentence in zip(text_a, text_b):
        a, b = [], []

        # for each slice of the first sentence in each line
        for slice in lst_gram(a_sentence):

            if slice in slice2idx.keys():
                a.append(slice2idx[slice])
            else:
                a.append(1)  # for those not in the txt remark it as “UNK”
        # for each slice of the second sentence in each line
        for slice in lst_gram(b_sentence):
            if slice in slice2idx.keys():
                b.append(slice2idx[slice])
            else:
                b.append(1)

        a_list.append(a)
        b_list.append(b)

    a_list = padding(a_list)
    b_list = padding(b_list)

    return a_list, b_list


def load_char_data(filename):
    df = pd.read_csv(filename, sep='\t')
    text_a = df['#1 string'].values
    text_b = df['#2 string'].values
    label = df['quality'].values
    a_index, b_index = char_index(text_a, text_b)
    return np.array(a_index), np.array(b_index), np.array(label)
