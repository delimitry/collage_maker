import os
from os import replace
import logging
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import (
    GaussianBlur
    )

# loggin feature
logging.basicConfig(level = logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler = logging.FileHandler('filters.log')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

#Global Variables
input_folder = '.\\Images\\test\\'
output_folder = '.\\Images\\test\\out\\'

variant_value1 = 2
variant_value2 = 10
variant_value3 = 20
variant_value4 = 40
variant_value5 = 50
def change_name_of_files(images):

    count = 0
    for img_path in images:
        count = count + 1
        img = Image.open(img_path)
        #variant 1
        #filtered_image = img.filter(GaussianBlur(radius=variant_value1))
        #filtered_image.save(img_path.replace(input_folder, output_folder).replace('.jpg','-variant'+str(variant_value1)+'.jpg'))
        #variant 2
        #filtered_image = img.filter(GaussianBlur(radius=variant_value2))
        #filtered_image.save(img_path.replace(input_folder, output_folder).replace('.jpg','-variant'+str(variant_value2)+'.jpg'))
        #variant 3
        filtered_image = img.filter(GaussianBlur(radius=variant_value3))
        filtered_image.save(img_path.replace(input_folder, output_folder).replace('.jpg','-variant'+str(variant_value3)+'.jpg'))
        #variant 4
        #filtered_image = img.filter(GaussianBlur(radius=variant_value4))
        #filtered_image.save(img_path.replace(input_folder, output_folder).replace('.jpg','-variant'+str(variant_value4)+'.jpg'))
        #variant 5
        #filtered_image = img.filter(GaussianBlur(radius=variant_value5))
        #filtered_image.save(img_path.replace(input_folder, output_folder).replace('.jpg','-variant'+str(variant_value5)+'.jpg'))
        
        logger.info(f"    Applying filter to image # {count}")
        

def main():
    logger.info(f"Renaming Files in folder {input_folder}")
    
    
    # get images
    files = [os.path.join(input_folder, fn) for fn in os.listdir(input_folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        logger.error('No images found,  Please select other directory with images!')
        exit(1)

    change_name_of_files(images)
    

if __name__ == '__main__':
    main()


    # more info at https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/ImageFilter.html
    