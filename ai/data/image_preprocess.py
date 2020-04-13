import os, sys
import csv, string
import numpy as np
# from config import config
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img


def image_path(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        image_name = []
        for idx, line in enumerate(lines):
            if idx == 0: continue
            img_name, comment_number, img_caption = line.split('|')
            image_name.append(f'./datasets/images/{img_name.strip().strip(string.punctuation)}')
    return image_name


def resize():
    with open('./datasets/captions.csv', 'r', encoding='utf8') as f:
        fieldnames = ['image_name', 'comment_number', 'comment']
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter='|')
        for idx, row in enumerate(reader):
            if row['image_name'] == 'image_name':
                continue
            if idx % 5 == 1:
                img_name = row['image_name'].split('|')[0]
                img = Image.open(f'./datasets/images/{img_name}')
                resize_image = img.resize((256, 256))
                resize_image.save(f'./datasets/images/{img_name}', quality=95)
    return


def standardization():
    with open('./datasets/captions.csv', 'r', encoding='utf8') as f:
        fieldnames = ['image_name', 'comment_number', 'comment']
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter='|')
        for idx, row in enumerate(reader):
            if row['image_name'] == 'image_name':
                continue
            if row['image_name']:
                img_name = row['image_name'].split('|')[0]
                img = Image.open(f'./datasets/images/{img_name}')
                break
    converted_image = np.array(img)
    standard_image = np.array(converted_image)
    for x in range(len(converted_image)):
        standard_image[x] = (converted_image[x] - np.mean(converted_image)) / np.std(converted_image)
    
    return standard_image


def convert(image, label):
  image = tf.image.convert_image_dtype(image, tf.float32) # Cast and normalize the image to [0,1]
  return image, label

def augment(image,label):
  image,label = convert(image, label)
  image = tf.image.convert_image_dtype(image, tf.float32) # Cast and normalize the image to [0,1]
  image = tf.image.resize_with_crop_or_pad(image, 34, 34) # Add 6 pixels of padding
  image = tf.image.random_crop(image, size=[28, 28, 1]) # Random crop back to 28x28
  image = tf.image.random_brightness(image, max_delta=0.5) # Random brightness

  return image,label



def image_augmentation(image):
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

    x = img_to_array(image)
    x = x.reshape((1,) + x.shape)

    for batch in datagen.flow(x, batch_size=1, save_to_dir='./datasets/aug_image', save_prefix='aug', save_format='jpeg'):
        aug_img = batch
        return aug_img

# iii = Image.open(f'../datasets/images/36979.jpg')
# ima = image_augmentation(iii)
# images = ima.astype('float32') / 255.
# print(images)
# plt.figure()
# plt.imshow(images[0], cmap=plt.cm.gray)
# plt.colorbar()
# plt.grid(False)
# plt.show()



# def rotate(x: tf.Tensor) -> tf.Tensor:
#     img = tf.image.rot90(image, tf.random.uniform(shape=[], minval=0, maxval=4, dtype=tf.float32))
#     # img = image.rotate(90)
#     img.imshow()
#     img.show()

# image = Image.open(f'../datasets/images/36979.jpg')
# rotate(image)

# # Req. 3-1	이미지 경로 및 캡션 불러오기
# def get_path_caption(config):
#     img_paths_captions = [[], [[], []]]

#     with open(config.caption_file_path, 'r', encoding='utf8') as f:
#         lines = f.readlines()        
#         for idx, line in enumerate(lines):
#             if idx == 0: continue            
#             img_name, comment_number, img_caption = line.split('|')
#             img_paths_captions[0].append(f'{config.img_path}{img_name.strip(string.punctuation)}')
#             img_paths_captions[1][0].append(comment_number.strip())
#             img_paths_captions[1][1].append(img_caption.strip().strip(string.punctuation))

#     return img_paths_captions


# # Req. 3-2	전체 데이터셋을 분리해 저장하기
# def dataset_split_save(img_paths, captions):
#     N = len(img_paths)
#     samples = np.random.randint(0, N, N // 3)
#     with open('./datasets/training.csv', 'w', newline='', encoding='utf8') as td:
#         with open('./datasets/validate.csv', 'w', newline='', encoding='utf8') as vd:
#             tw = csv.writer(td, delimiter='|')
#             vw = csv.writer(vd, delimiter='|')

#             for i in range(N):
#                 if i not in samples:
#                     tw.writerow([img_paths[i], captions[0][i], captions[1][i]])
#                 else:
#                     vw.writerow([img_paths[i], captions[0][i], captions[1][i]])
    
#     return './datasets/training.csv', './datasets/validate.csv'


# # Req. 3-3	저장된 데이터셋 불러오기
# def get_data_file(dataset):
#     img_paths_captions = [[], [[], []]]
#     with open(dataset, 'r', encoding='utf8') as f:
#         lines = f.readlines()
#         for line in lines:
#             path, comment_number, caption = line.split('|')
#             img_paths_captions[0].append(path)
#             img_paths_captions[1][0].append(comment_number.strip())
#             img_paths_captions[1][1].append(caption.strip())

#     return img_paths_captions


# # Req. 3-4	데이터 샘플링
# def sampling_data(paths, caps, portions):
#     img_paths_captions = [[], [[], []]]
#     N = len(paths)
#     samples = np.random.randint(0, N, portions)
    
#     for i in range(N):
#         if i not in samples: continue
#         img_paths_captions[0].append(paths[i])
#         img_paths_captions[1][0].append(caps[0][i])
#         img_paths_captions[1][1].append(caps[1][i])
    
#     return img_paths_captions
