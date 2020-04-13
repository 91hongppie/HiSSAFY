import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import re
import numpy as np
import os
import time
import json
from glob import glob
from PIL import Image
from config import config
from data.dataset_maker import image_path
from data.text_preprocess import tokenize, tokenizer_save, tokenizer_load
from data.dataset import dataset_create
from models.encoder import CNN_Encoder
from models.decoder import RNN_Decoder
from train import encoder, decoder, tokenizer, max_length, image_features_extract_model, img_name_val, evaluate, cap_val, plot_attention



# captions on the validation set
rid = np.random.randint(0, len(img_name_val))
image = img_name_val[rid]
real_caption = ' '.join([tokenizer.index_word[i] for i in cap_val[rid] if i not in [0]])
result, attention_plot = evaluate(image)
max_length = 50



print ('Real Caption:', real_caption)
print ('Prediction Caption:', ' '.join(result))
plot_attention(image, result, attention_plot)