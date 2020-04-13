import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
from config import config
import string
import numpy as np


# 텍스트 데이터 토큰화
def tokenize(file_path, max_words):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        sentences = []
        for idx, line in enumerate(lines):
            if idx == 0: continue            
            img_name, comment_number, img_caption = line.split('|')
            sentences.append(f'<start> {img_caption.strip().strip(string.punctuation)} <end> <pad>')
        # print(sentences)

    tokenizer = Tokenizer(num_words=max_words, oov_token="<unk>", filters='!"#$%&()*+.,-/:;=?@[]^_`{|}~ ')

    # 어휘 idx 구축
    tokenizer.fit_on_texts(sentences)

    seqs = tokenizer.texts_to_sequences(sentences)
    # print(f'seqs: {seqs}')

    one_hot_results = tokenizer.texts_to_matrix(sentences, mode='binary')
    # print(*one_hot_results)

    word_idx = tokenizer.word_index
    # print(word_idx)

    sequences = tf.keras.preprocessing.sequence.pad_sequences(seqs, padding='post', maxlen=30, value=word_idx['<pad>'])
    # print(sequences)
    print(f'Found {len(word_idx)} unique tokens')

    return sequences, tokenizer


# Tokenizer 저장 및 불러오기
def tokenizer_save(data):
    with open('token.pickle', 'wb') as f:
        try:
            pickle.dump(data, f)
            print('Successfully dumped')
            return 'Success'
        except:
            print('Dumping has failed')
            return 'Fail'


def tokenizer_load():
    with open('token.pickle', 'rb') as f:
        data = pickle.load(f)
    return data


# config.caption_file_path = '../datasets/captions.csv'
# file_path = config.caption_file_path
# max_words = 5000

# tokenizer_save(tokenize(file_path, max_words))
# print(tokenizer_load())
