import os
import re
import random
import pathlib
import subprocess
import pytesseract

'''
TESSDATA_PREFIX=../tesseract/tessdata make training MODEL_NAME=Literaturnaya START_MODEL=rus TESSDATA=../tesseract/tessdata MAX_ITERATIONS=100
'''

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['PATH'] += r';C:\Program Files\Tesseract-OCR'

training_text_file = 'langdata/rus/rus.training_text'

lines = []

with open(training_text_file, 'r', encoding='utf-8') as input_file:
    for line in input_file.readlines():
        lines.append(line.strip())

output_directory = 'Multiline_dataset'

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

random.shuffle(lines)

count = 2000

lines = lines[:count]

line_count = 0
for line in lines:
    num_lines = random.randint(1, 4)
    multi_line_text = re.sub(r' ', '\n', line, num_lines)

    training_text_file_name = pathlib.Path(training_text_file).stem
    print (training_text_file_name)
    line_training_text = os.path.join(output_directory, f'{training_text_file_name}_{line_count}.gt.txt')

    with open(line_training_text, 'w', encoding='utf-8') as output_file:
        output_file.writelines([multi_line_text])

    file_base_name = f'rus_{line_count}'

    subprocess.run([
        'text2image',
        '--font=Literaturnaya', # Literaturnaya
        f'--text={line_training_text}',
        f'--outputbase={output_directory}/{file_base_name}',
        '--max_pages=1',
        '--degrade_image=true',
        '--strip_unrenderable_words',
        '--leading=10',
        '--xsize=1000',
        '--ysize=200',
        '--margin=10',
        '--ptsize=6',
        '--char_spacing=0.0',
        '--exposure=0',
        '--unicharset_file=langdata/rus.unicharset'
    ])

    line_count += 1
