from datetime import datetime
from tensorflow.keras.preprocessing import image
import os, csv, random
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

# Req. 2-2	세팅 값 저장
def save_config(config):	
	times = datetime.now().strftime('%Y%m%d_%H%M%S')

	with open(f'./conf.csv', 'a', encoding='utf8') as f:
		writer = csv.writer(f, delimiter='|')
		writer.writerow([times, config.caption_file_path, config.img_path])


# Req. 4-1	이미지와 캡션 시각화
def visualize_img_caption(img_paths, captions):
	for idx, img in enumerate(img_paths):
		img_load = image.load_img(img)
		img_tensor = image.img_to_array(img_load)
		img_tensor = np.expand_dims(img_tensor, axis=0)
		img_tensor.shape
		img_tensor /= 255.

		plt.title(captions[1][idx])
		plt.imshow(img_tensor[0])
		plt.show()
