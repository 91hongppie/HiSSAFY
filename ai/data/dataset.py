import tensorflow as tf
from data import text_preprocess
from config import config
import string
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img


# dataset 생성
def image_path(file_path):
   if file_path[:2] == '..':
      file_path = file_path[1:]
   with open(file_path, 'r', encoding='utf-8') as f:
      lines = f.readlines()


# dataset 생성
# img_path = image_path('../datasets/captions.csv')
# caption = text_preprocess.tokenizer_load()
def dataset_create(img_path, caption):
    dataset = tf.data.Dataset.from_tensor_slices((img_path, caption))
    img_captions = []
    for next_element in dataset:
        img_captions.append(next_element)

   for elem in img_captions:
      images = elem[0].numpy()[1:]

      image = Image.open(images)
      image = img_to_array(image)
      image = image.astype('float32') / 255

      # plt.figure()
      # plt.title(elem[1].numpy())
      # plt.imshow(image, cmap='gray')
      # plt.show()



    # print(img_captions)
    return img_captions


# dataset_create(img_path, caption)
