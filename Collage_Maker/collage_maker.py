# -*- coding: utf-8 -*-
"""
Collage maker - tool to create picture collages
Author: Delimitry 
"""

import argparse
import os
import random
from PIL import Image


def make_collage(images, filename, width, init_height):
    """
    Make a collage image with a width equal to `width` from `images` and save to `filename`.
    """
    if not images:
        print('No images for collage found!')
        return False

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
            img = img.resize((800,800),Image.BILINEAR)
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
                img = img.resize((800,800),Image.BILINEAR)
                '''
                # if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                '''
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size
    collage_image.save(filename)
    return True


def main():
    # prepare argument parser
    parse = argparse.ArgumentParser(description='Photo collage maker')
    parse.add_argument('-f', '--folder', dest='folder', help='folder with images (*.jpg, *.jpeg, *.png)', default='.')
    parse.add_argument('-of', '--outputFolder', dest='outputFolder', help='output collages image folder', default='./Images/Output/')
    #parse.add_argument('-w', '--width', dest='width', type=int, help='resulting collage image width')
    #parse.add_argument('-i', '--init_height', dest='init_height', type=int, help='initial height for resize the images')
    parse.add_argument('-s', '--shuffle', action='store_true', dest='shuffle', help='enable images shuffle')
    parse.add_argument('-d', '--dimmention', dest='dimmention', help='collage dimmention 2x2,4x4,8x8,16x16,32x32')

    args = parse.parse_args()
    #if not args.width or not args.init_height:
    if not args.folder or not args.dimmention:
        parse.print_help()
        exit(1)

    # get images
    files = [os.path.join(args.folder, fn) for fn in os.listdir(args.folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        print('No images for making collage! Please select other directory with images!')
        exit(1)

    # shuffle images if needed
    if args.shuffle:
        random.shuffle(images)

    collage_items = []
    counter = 1
    collageNumber = 1

    if args.dimmention == '2x2':
        print('Making collage 2x2 collages...')

        for singleImage in images:
            collage_items.append(singleImage)
            if counter == 4:
                make_collage(collage_items, args.outputFolder + f'1024CartoonCollage-2x2-{collageNumber}.png' , 1600, 800)
                collageNumber = collageNumber + 1
                collage_items = []
                counter = 0
            counter = counter + 1
    
    elif args.dimmention == '4x4':
        print('Making collage 4x4 collages...')
    
        for singleImage in images:
            collage_items.append(singleImage)
            if counter == 16:
                make_collage(collage_items, args.outputFolder + f'1024CartoonCollage-4x4-{collageNumber}.png' , 3200, 800)
                collageNumber = collageNumber + 1
                collage_items = []
                counter = 0
            counter = counter + 1

    elif args.dimmention == '8x8':
        print('Making collage 8x8 collages...')
        
        for singleImage in images:
            collage_items.append(singleImage)
            if counter == 64:
                make_collage(collage_items, args.outputFolder + f'1024CartoonCollage-8x8-{collageNumber}.png' , 6400, 800)
                collageNumber = collageNumber + 1
                collage_items = []
                counter = 0
            counter = counter + 1
        
    elif args.dimmention == '16x16':
        print('Making collage 16x16 collages...')

        for singleImage in images:
            collage_items.append(singleImage)
            if counter == 256:
                make_collage(collage_items, args.outputFolder + f'1024CartoonCollage-16x16-{collageNumber}.png' , 12800, 800)
                collageNumber = collageNumber + 1
                collage_items = []
                counter = 0
            counter = counter + 1

    elif args.dimmention == '32x32':
        print('Making collage 32x32 collages...')

        for singleImage in images:
            collage_items.append(singleImage)
            if counter == 1024:
                make_collage(collage_items, args.outputFolder + f'1024CartoonCollage-32x32-{collageNumber}.png' , 25600, 800)
                collageNumber = collageNumber + 1
                collage_items = []
                counter = 0
            counter = counter + 1
    else:    
        print('Error providing collage dimmention, it shoud be: 2x2 or 4x4 or 8x8 or 16x16 or 32x32')


# collage_maker.py -f .\Images\Input\8x8  -d 8x8



if __name__ == '__main__':
    main()
