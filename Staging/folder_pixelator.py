# install library
#
# py -m pip install matplotlib
# https://www.tutorialspoint.com/how-to-install-matplotlib-in-python

#Import Libraries
from PIL import Image
#import matplotlib as mpl
import matplotlib.pyplot as plt
Image.MAX_IMAGE_PIXELS = None

def photo2pixelart(image, i_size, o_name):
    """
    image: path to image file
    i_size: size of the small image eg:(8,8)
    o_size: output size eg:(10000,10000)
    o_name: Output path/name.ext
    """
    #read file
    img=Image.open(image)

    #convert to small image
    small_img=img.resize(i_size,Image.BILINEAR)

    #resize to output size
    res=small_img.resize(img.size, Image.NEAREST)

    #Save output image
    #filename=f'./Images/Output/mario_{i_size[0]}x{i_size[1]}.png' # original code
    filename= o_name
    res.save(filename)

    #Display images side by side
    plt.figure(figsize=(16,10))
    #original image
    plt.subplot(1,2,1)
    plt.title('Original image', size=18)
    plt.imshow(img)   #display image
    plt.axis('off')   #hide axis
    #pixel art
    plt.subplot(1,2,2)
    plt.title(f'Pixel Art {i_size[0]}x{i_size[1]}', size=18)
    plt.imshow(res)
    plt.axis('off')
    plt.show()

def main():
    #8x8
    #photo2pixelart(image='./Images/Output/1024CartoonCollage-8x8.png',i_size=(160,160),
    #              o_name='./Images/Output/Pixelated/1024CartoonCollage-8x8-Pixelated.png')
    #16x16
    #photo2pixelart(image='./Images/Output/1024CartoonCollage-16x16.png',i_size=(325,325),
    #              o_name='./Images/Output/Pixelated/1024CartoonCollage-16x16-Pixelated.png')
    #32x32
    photo2pixelart(image='./Images/Output/1024CartoonCollage-32x32.png',i_size=(648,648),
                  o_name='./Images/Output/Pixelated/1024CartoonCollage-32x32-Pixelated.png')
    
    
    #photo2pixelart(image='mario.jpg',i_size=(80,80)) #original code

if __name__ == '__main__':
    main()