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
        folder00   = data['folders']['00']
        folder01   = data['folders']['01']
        folder02   = data['folders']['02']
        folder03   = data['folders']['03']
        folder04   = data['folders']['04']
        shufle     = data['collageCreation']['shufle']  # Global variable to specify if images needs to be shufled
        reduction  = data['Pixelation']['reduction']    # Global variable to specify thubmnail size to create pixelated image
        outputSize = data['Pixelation']['outputSize']   # Global variable to specify the final output size of the pixelated image
        new_size   = data['ImageResize']['new_size'] # (800,800)
        name_2x2  = data['collageCreation']['name_2x2']
        name_4x4  = data['collageCreation']['name_4x4']
        name_8x8  = data['collageCreation']['name_8x8']
        name_16x16  = data['collageCreation']['name_16x16']
        name_32x32  = data['collageCreation']['name_32x32']        
        overlay_opacity  = data['overlays']['overlay_opacity']
        overlay_1x1  = data['overlays']['overlay_1x1']
        overlay_2x2  = data['overlays']['overlay_2x2']
        overlay_4x4  = data['overlays']['overlay_4x4']
        overlay_8x8  = data['overlays']['overlay_8x8']
        overlay_16x16  = data['overlays']['overlay_16x16']
        overlay_32x32  = data['overlays']['overlay_32x32']

def standarize_scanned_image_sizes():
    '''
    This function will standarize the size of all scanned images to be 800x800
    '''
    input_folder = folder01
    output_folder = folder02
    
    logger.info(f'Resizing Scanned Images to {new_size} ...')
    
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

def make_single_collage(dimenssion, collageNumber, images, filename, width, init_height):
    """
    Make a collage image with a width equal to `width` from `images` and save to `filename`.
    """

    margin_size = 2
    # run until a suitable arrangement of images is found
    while True:
        # copy images to images_list
        images_list = images[:]
        coefs_lines = []
        images_line = []
        x = 0
        while images_list:
            # get first image and resize to `init_height`
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, init_height))
            # when `x` will go beyond the `width`, start the next line
            if x > width:
                coefs_lines.append((float(x) / width, images_line))
                images_line = []
                x = 0
            x += img.size[0] + margin_size
            images_line.append(img_path)
        # finally add the last line with images
        coefs_lines.append((float(x) / width, images_line))

        # compact the lines, by reducing the `init_height`, if any with one or less images
        if len(coefs_lines) <= 1:
            break
        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
            # reduce `init_height`
            init_height -= 10
        else:
            break

    # get output height
    out_height = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            out_height += int(init_height / coef) + margin_size
    if not out_height:
        print('Height of collage could not be 0!')
        return False

    collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
    # put images to the collage
    y = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            x = 0
            for img_path in imgs_line:
                img = Image.open(img_path)
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size
    collage_image.save(filename)    
    logger.info(f"    Creating {dimenssion} Collage #{collageNumber}: {filename}")
    return True

def create_all_collages():
    '''
    This process will create new collage images using the images that were resized/standarized 
    and store them under the folder of images to be pixelated
    '''
    input_folder = folder02
    output_folder = folder02
    width_2x2 = new_size[0] * 2
    width_4x4 = new_size[0] * 4
    width_8x8 = new_size[0] * 8
    width_16x16 = new_size[0] * 16
    width_32x32 = new_size[0] * 32
    nxn_height  = new_size[1]

    logger.info('Creating Collages....')

    # get images
    files = [os.path.join(input_folder, fn) for fn in os.listdir(input_folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        logger.error('No images found,  Please select other directory with images!')
        exit(1)
    
    # Create 2x2 Collages
    if shufle:
        random.shuffle(images)
        print('true')
    collage_items = []
    counter = 1
    collageNumber = 1

    logger.info('Creating 2x2 Collages')
    for singleImage in images:
        collage_items.append(singleImage)
        if counter == 4:
            make_single_collage('2x2', collageNumber, collage_items, output_folder + f'{name_2x2}-{collageNumber}.png' , width_2x2, nxn_height)
            collageNumber = collageNumber + 1
            collage_items = []
            counter = 0
        counter = counter + 1

    # Create 4x4 Collages    
    if shufle:
        random.shuffle(images)
    collage_items = []
    counter = 1
    collageNumber = 1

    logger.info('Creating 4x4 Collages')
    for singleImage in images:
        collage_items.append(singleImage)
        if counter == 16:
            make_single_collage('4x4', collageNumber, collage_items, output_folder + f'{name_4x4}-{collageNumber}.png' , width_4x4, nxn_height)
            collageNumber = collageNumber + 1
            collage_items = []
            counter = 0
        counter = counter + 1

    # Create 8x8 Collages
    if shufle:
        random.shuffle(images)
    collage_items = []
    counter = 1
    collageNumber = 1

    logger.info('Creating 8x8 Collages')
    for singleImage in images:
        collage_items.append(singleImage)
        if counter == 64:
            make_single_collage('8x8', collageNumber, collage_items, output_folder + f'{name_8x8}-{collageNumber}.png' , width_8x8, nxn_height)
            collageNumber = collageNumber + 1
            collage_items = []
            counter = 0
        counter = counter + 1
    
    # Create 16x16 Collages
    if shufle:
        random.shuffle(images)
    collage_items = []
    counter = 1
    collageNumber = 1

    logger.info('Creating 16x16 Collages')
    for singleImage in images:
        collage_items.append(singleImage)
        if counter == 256:
            make_single_collage('16x16', collageNumber, collage_items, output_folder + f'{name_16x16}-{collageNumber}.png' , width_16x16, nxn_height)
            collageNumber = collageNumber + 1
            collage_items = []
            counter = 0
        counter = counter + 1

    # Create 32x32 Collages
    if shufle:
        random.shuffle(images)
    collage_items = []
    counter = 1
    collageNumber = 1

    logger.info('Creating Big Mama!')
    for singleImage in images:
        collage_items.append(singleImage)
        if counter == 1024:
            make_single_collage('32x32', collageNumber, collage_items, output_folder + f'{name_32x32}-{collageNumber}.png' , width_32x32, nxn_height)
            collageNumber = collageNumber + 1
            collage_items = []
            counter = 0
        counter = counter + 1

def photo2pixelart(image, i_size, o_name, o_size):
    """
    image: path to image file
    i_size: size of the small image eg:(8,8)
    o_name: Output path/name.ext
    o_size: percentage of image output size
    """    
    #read file
    img=Image.open(image)

    #convert to small image
    small_img=img.resize(i_size,Image.BILINEAR)

    #resize to output size
    res=small_img.resize(o_size, Image.NEAREST)

    #Save output image
    filename= o_name
    res.save(filename)
    logger.info(f'         Saving image as: {o_name}')

def pixelate_all_images():
    '''
    This function will pixelate all images inside an specific folder and save them into a different one
    '''
    input_folder = folder02
    output_folder = folder03
    
    logger.info(f'Pixelating all images in folder: {input_folder}')
    # get images
    files = [os.path.join(input_folder, fn) for fn in os.listdir(input_folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        logger.error('No images found,  Please select other directory with images!')
        exit(1)
    
    #pixelate_folder_images(images, args.reduction, args.output)

    images_list = images[:]

    counter = 1
    while images_list:
            # get first image and resize to `init_height`
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            w, h = img.size
            
            logger.info(f'    Pixelating Image #{counter}: {img_path}')
            logger.info(f'         Original W: {w}px | Thumbnail W: {int(w*reduction)}px | Output W: {int(w*outputSize)}px ')
            logger.info(f'         Original H: {h}px | Thumbnail H: {int(h*reduction)}px | Output H: {int(h*outputSize)}px ')

            photo2pixelart(img_path,
                        (int(w*reduction),int(h*reduction)), 
                        img_path.replace(input_folder, output_folder)
                        .replace('.png','-pixelated.png')
                        .replace('.jpg','-pixelated.jpg')
                        .replace('.jpeg','-pixelated.jpeg'),
                        (int(w*outputSize),int(h*outputSize))
                        )
        
            counter = counter + 1

def watermark_addition():
    '''
    This function will add a watermark into each image
    '''
    overlays_folder = folder00
    input_folder = folder03
    output_folder = folder04
    singleItemSize = new_size[0] * outputSize
    logger.info('This is: wattermark_addition')

    # get images
    files = [os.path.join(input_folder, fn) for fn in os.listdir(input_folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        logger.error('No images found,  Please select other directory with images!')
        exit(1)

    watermark_1x1 = Image.open(overlays_folder + overlay_1x1)
    watermark_2x2 = Image.open(overlays_folder + overlay_2x2)
    watermark_4x4 = Image.open(overlays_folder + overlay_4x4)
    #watermark_8x8 = Image.open(overlays_folder + overlay_8x8)
    #watermark_16x16 = Image.open(overlays_folder + overlay_16x16)
    #watermark_32x32 = Image.open(overlays_folder + overlay_32x32)

    watermark_1x1 = watermark_1x1.convert("RGBA")
    watermark_2x2 = watermark_2x2.convert("RGBA")
    watermark_4x4 = watermark_4x4.convert("RGBA")
    #watermark_8x8 = watermark_8x8.convert("RGBA")
    #watermark_16x16 = watermark_16x16.convert("RGBA")
    #watermark_32x32 = watermark_32x32.convert("RGBA")

    count = 0
    for img_path in images:
        # pending to add logic to know the overlay to be used depending on the image size.
        background = Image.open(img_path)
        background = background.convert("RGBA")

        count = count + 1
        
        # 1x1 Images
        if background.size[0] == singleItemSize:
            logger.info(f"    Adding 1x1 Watermark to image #{count}: {img_path}")
            new_img = Image.blend(background, watermark_1x1, overlay_opacity)

        # 2x2 Images
        elif background.size[0] == singleItemSize * 2:
            logger.info(f"    Adding 2x2 Watermark to image #{count}: {img_path}")
            new_img = Image.blend(background, watermark_2x2, overlay_opacity)
        
        # 4x4 Images
        elif background.size[0] == singleItemSize * 4:
            logger.info(f"    Adding 4x4 Watermark to image #{count}: {img_path}")
            new_img = Image.blend(background, watermark_4x4, overlay_opacity)
        '''
        # 8x8 Images
        elif background.size[0] == singleItemSize * 8:
            logger.info(f"    Adding 8x8 Watermark to image #{count}: {img_path}")
            new_img = Image.blend(background, watermark_8x8, overlay_opacity)

        # 16x16 Images
        elif background.size[0] == singleItemSize * 16:
            logger.info(f"    Adding 16x16 Watermark to image #{count}: {img_path}")
            new_img = Image.blend(background, watermark_16x16, overlay_opacity)
        
        # 32x32 Images
        elif background.size[0] == singleItemSize * 32:
            logger.info(f"    Adding 32x32 Watermark to image #{count}: {img_path}")
            new_img = Image.blend(background, watermark_32x32,overlay_opacity)
        '''
        new_img.save(img_path.replace(input_folder, output_folder),"PNG")

def main():
    
    logger.info('Starting Crypto Cartoon Perceptions Automation Process...')
    standarize_scanned_image_sizes()
    create_all_collages()
    pixelate_all_images()
    watermark_addition()
    logger.info('El brete se completO, Cual inter?????')
    logger.info('------------------------------------')

if __name__ == '__main__':
    main()