# install library 
#
# py -m pip install matplotlib
# https://www.tutorialspoint.com/how-to-install-matplotlib-in-python

#Import Libraries

import argparse
import os
import random
from PIL import Image
import matplotlib.pyplot as plt
Image.MAX_IMAGE_PIXELS = None

def photo2pixelart(image, i_size, o_name):
    """
    image: path to image file
    i_size: size of the small image eg:(8,8)
    o_name: Output path/name.ext
    """    
    #read file
    img=Image.open(image)

    #convert to small image
    small_img=img.resize(i_size,Image.BILINEAR)

    #resize to output size
    res=small_img.resize(img.size, Image.NEAREST)

    #Save output image
    filename= o_name
    res.save(filename)
    print(f'     Saving image as: {o_name}')

def pixelate_folder_images(images, reduction):
    """
    images: Array of images
    reduction: % of quality reduction
    """    
    images_list = images[:]

    while images_list:
            # get first image and resize to `init_height`
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            w, h = img.size

            print('---------------------------------------------------------')
            print(f'Pixelating Image : {img_path}')
            print(f'     This is image Width: {w}')
            print(f'     This is image Height: {h}')
            print(f'     This is thumbnail Width: {w*reduction}')
            print(f'     This is thumbnail Height: {h*reduction}')

            photo2pixelart(img_path,
                        (int(w*reduction),int(h*reduction)), 
                        img_path.replace('Input','Output')
                        .replace('.png','-pix.png')
                        .replace('.jpg','-pix.jpg')
                        .replace('.jpeg','-pix.jpeg')
                        )

def main():
    # prepare argument parser
    parse = argparse.ArgumentParser(description='Folder Pixelator')    
    parse.add_argument('-f', '--folder', dest='folder', help='folder with images (*.jpg, *.jpeg, *.png)', default='.')
    parse.add_argument('-r', '--reduction', dest='reduction', type=float, help='Percentage of quality reduction', default='0.025')
   
    args = parse.parse_args()
    if not args.folder:
        parse.print_help()
        exit(1)

    # get images
    files = [os.path.join(args.folder, fn) for fn in os.listdir(args.folder)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    if not images:
        print('No images for making collage! Please select other directory with images!')
        exit(1)
    
    pixelate_folder_images(images, args.reduction)

if __name__ == '__main__':
    main()

# folder_pixelator.py -f .\Images\Input\ -r 0.025