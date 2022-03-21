'''
The process is as follows

1) Scan all images
2) Resize all single images to be 800x800
3) Create collages
4) Pixel images
5) Add water mark

'''
import argparse
import os
from os import replace
import os.path
import random
from PIL import Image
import matplotlib.pyplot as plt
from datetime import date
import time
import json
import argparse
import logging

Image.MAX_IMAGE_PIXELS = None

# loggin feature
logging.basicConfig(level = logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler = logging.FileHandler('main_log.log')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

#Reading global properties from json file
with open('settings.json') as f: # filename needs to be specefied
        data = json.load(f)
        folder01   = data['folders']['01']
        folder02   = data['folders']['02']
        new_size   = data['ImageResize']['new_size'] # (800,800)


def standarize_scanned_image_sizes():
    '''
    This function will standarize the size of all scanned images to be 800x800
    '''
    input_folder = folder01
    output_folder = folder02
    
    logger.info(f'Resizing Images on: {input_folder} to {new_size} ...')
    
    # get images
    files = [os.path.join(input_folder, fn) for fn in os.listdir(input_folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        logger.error('No images found,  Please select other directory with images!')
        exit(1)
    
    count = 0
    for img_path in images:
        count = count + 1
        logger.info(f"    Resizing image #{count}: {img_path}")
        img = Image.open(img_path)
        img = img.resize(new_size,Image.BILINEAR)
        img.save(img_path.replace(input_folder, output_folder))

def main():
    
    logger.info('Starting Image Resizing Process...')
    standarize_scanned_image_sizes()
    logger.info('------------------------------------')

if __name__ == '__main__':
    main()