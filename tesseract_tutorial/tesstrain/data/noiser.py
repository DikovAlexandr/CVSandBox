import os
import cv2
import numpy as np
import random

input_folder = 'Literaturnaya-ground-truth'

output_folder = 'Literaturnaya-ground-truth_noise'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def add_realistic_noise(image):
    row, col, ch = image.shape
    gauss = np.random.normal(0, 200, (row, col, ch))
    noisy = np.clip(image + gauss, 0, 255)
    
    return noisy.astype(np.uint8)

def sp_noise(image, prob = 0.1):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

for filename in os.listdir(input_folder):
    if filename.endswith('.tif'):
        img = cv2.imread(os.path.join(input_folder, filename))
        noisy_img = add_realistic_noise(img)
        noisy_img = sp_noise(noisy_img)
        gray_image = cv2.cvtColor(noisy_img, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, binary_image)

print("Done", output_folder)