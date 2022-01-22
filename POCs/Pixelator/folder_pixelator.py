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
    print(f'     Saving image as: {o_name}')

def pixelate_folder_images(images, reduction, outputSize):
    """
    images: Array of images
    reduction: % of quality reduction
    outputSize: % of image output size
    """    
    images_list = images[:]

    while images_list:
            # get first image and resize to `init_height`
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            w, h = img.size

            print('---------------------------------------------------------')
            print(f'Pixelating Image : {img_path}')
            print(f'     Original Width: {w}px | Thumbnail Width: {int(w*reduction)}px | Output Width: {int(w*outputSize)}px ')
            print(f'     Original Height: {h}px | Thumbnail Height: {int(h*reduction)}px | Output Height: {int(h*outputSize)}px ')

            photo2pixelart(img_path,
                        (int(w*reduction),int(h*reduction)), 
                        img_path.replace('Input','Output')
                        .replace('.png','-pix.png')
                        .replace('.jpg','-pix.jpg')
                        .replace('.jpeg','-pix.jpeg'),
                        (int(w*outputSize),int(h*outputSize))
                        )

def main():
    # prepare argument parser
    parse = argparse.ArgumentParser(description='Folder Pixelator')    
    parse.add_argument('-f', '--folder', dest='folder', help='folder with images (*.jpg, *.jpeg, *.png)', default='.')
    parse.add_argument('-r', '--reduction', dest='reduction', type=float, help='Percentage of quality reduction', default='0.025')
    parse.add_argument('-o', '--output', dest='output', type=float, help='Percentage of image output', default='0.5')
   
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
    
    pixelate_folder_images(images, args.reduction, args.output)

if __name__ == '__main__':
    main()

# folder_pixelator.py -f .\Images\Input\ -r 0.025 -o 0.5