import os
import shutil
import random

source_folder = os.path.join(os.getcwd(), "source")
test_folder = os.path.join(os.getcwd(), "test")
val_folder = os.path.join(os.getcwd(), "val")
test_ratio = 0.8

os.makedirs(test_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)

files = os.listdir(source_folder)
random.shuffle(files)

split_index = int(len(files) * test_ratio)

test_files = files[:split_index]
val_files = files[split_index:]

for file in test_files:
    source_path = os.path.join(source_folder, file)
    destination_path = os.path.join(test_folder, file)
    shutil.move(source_path, destination_path)

for file in val_files:
    source_path = os.path.join(source_folder, file)
    destination_path = os.path.join(val_folder, file)
    shutil.move(source_path, destination_path)

print("Completed")