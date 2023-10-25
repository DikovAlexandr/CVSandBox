import os
import random
from PIL import Image
import pandas as pd

input_folder = "Multiline_dataset"
output_folder = "result"

validation_percent = 20

train_folder = os.path.join(output_folder, 'train')
val_folder = os.path.join(output_folder, 'val')

for folder in [train_folder, val_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

train_data = {'filename': [], 'words': []}
val_data = {'filename': [], 'words': []}

for filename in os.listdir(input_folder):
    if filename.endswith('.tif'):
        image_path = os.path.join(input_folder, filename)
        text_file_path = os.path.join(input_folder, filename.replace('.tif', '.gt.txt'))

        if os.path.exists(text_file_path):
            with Image.open(image_path) as img:
                img = img.resize((img.width // 2, img.height // 2))

                random_num = random.randint(1, 100)
                output_path = os.path.join(
                    train_folder if random_num > validation_percent else val_folder,
                    filename.replace('.tif', '.jpg'))
                img.save(output_path, 'JPEG')

                data = train_data if random_num > validation_percent else val_data
                data['filename'].append(filename.replace('.tif', '.jpg'))

                with open(text_file_path, 'r', encoding='utf-8') as text_file:
                    text = text_file.read()
                    data['words'].append(text)

train_df = pd.DataFrame(train_data)
val_df = pd.DataFrame(val_data)
csv_filename = 'result/labels.csv'

train_csv_filename = 'result/train_labels.csv'
val_csv_filename = 'result/val_labels.csv'

train_csv_filename = 'result/train_labels.csv'
val_csv_filename = 'result/val_labels.csv'
train_df.to_csv(train_csv_filename, index=False, encoding='utf-8')
val_df.to_csv(val_csv_filename, index=False, encoding='utf-8')

print(f"Images in {output_folder}.")
print(f"Labels in {csv_filename}.")