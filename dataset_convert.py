from PIL import Image
import os

def crop_images_to_minimum_size(input_folder):
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    min_width = float('inf')
    min_height = float('inf')

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        image = Image.open(image_path)
        width, height = image.size
        min_width = min(min_width, width)
        min_height = min(min_height, height)

    min_width = int(min_width)
    min_height = int(min_height)

    # Обрезаем все изображения до минимальных размеров
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)
        image = Image.open(image_path)
        width, height = image.size
        image = image.crop(((width - min_width)/2, (height - min_height)/2, (width - min_width)/2 + min_width, (height - min_height)/2 + min_height))
        image.save(image_path)

    print(f"New size: {min_width}x{min_height}")

input_folder = os.path.join(os.getcwd(), "train")
image_files = os.listdir(input_folder)

crop_images_to_minimum_size(input_folder)

for i, image_file in enumerate(image_files):
    input_image_path = os.path.join(input_folder, image_file)
    img = Image.open(input_image_path)

    # img = crop_to_a4_ratio(img)
    img = img.convert("L")

    if image_file != f"{i + 1:06d}.jpg":
        new_filename = f"{i + 1:06d}.jpg"
        img.save(os.path.join(input_folder, new_filename))
        os.remove(input_image_path)

print("Conver ready")