import os
from os import replace
import logging

# loggin feature
logging.basicConfig(level = logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler = logging.FileHandler('file_rename.log')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

#Global Variables
files_folder = '.\\Images\\01scanned\\'
text_to_change ='1024CartoonCollage'
new_text ='CryptoCartoonPerceptions'

def change_name_of_files(files):

    count = 0
    for file_path in files:
        new_file_name = file_path.replace(text_to_change,new_text)
        logger.info(f"    Renaming file #{count} from : {file_path} to {new_file_name}")
        os.rename(file_path, new_file_name)

def main():
    logger.info(f"Renaming Files in folder {files_folder}")
    logger.info(f"File Name portion to be removed: {text_to_change}")
    logger.info(f"File Name portion to be added: {new_text}")
    
    # get images
    files = [os.path.join(files_folder, fn) for fn in os.listdir(files_folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        logger.error('No images found,  Please select other directory with images!')
        exit(1)

    change_name_of_files(images)
    

if __name__ == '__main__':
    main()