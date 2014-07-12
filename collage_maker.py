#!/usr/bin/env python
#-*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import os
import random
from PIL import Image
from optparse import OptionParser

def make_collage(images, filename, width, init_height):
	"""
	Make a collage images from `images` and save to `filename`.
	"""
	if not images:
		print 'No images for collage found!'
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
		if any(map(lambda x: len(x[1]) <= 1, coefs_lines)):
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
		print 'Height of collage could not be 0!'
		return False

	collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
	# put images to the collage
	y = 0
	for coef, imgs_line in coefs_lines:
		if imgs_line:
			x = 0
			for img_path in imgs_line:
				img = Image.open(img_path)
				# if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster
				k = (init_height / coef) / img.size[1]
				if k > 1:
					img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)					
				else:
					img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
				if collage_image:
					collage_image.paste(img, (int(x), int(y)))
				x += img.size[0] + margin_size
			y += int(init_height / coef) + margin_size
	collage_image.save(filename)
	return True

def main():
	# prepare options parser
	options = OptionParser(usage='%prog [options]', description='Photo collage maker')
	options.add_option('-f', '--folder', dest='folder', help='folder with images (*.jpg, *.jpeg)', default='.')
	options.add_option('-o', '--output', dest='output', help='output collage image filename', default='collage.png')
	options.add_option('-w', '--width', dest='width', type='int', help='resulting collage image width')
	options.add_option('-i', '--init_height', dest='init_height', type='int', help='initial height for resize the images')
	options.add_option('-s', '--shuffle', action='store_true', dest='shuffle', help='enable images shuffle', default=False)

	opts, args = options.parse_args()
	if not opts.width or not opts.init_height:
		options.print_help()
		return

	# get images
	images = filter(lambda x: os.path.splitext(x)[1].lower() in ['.jpg', '.jpeg'], os.listdir(opts.folder))
	if not images:
		print 'No images for making collage! Please select other directory with images!'
		return

	# shuffle images if needed
	if opts.shuffle:
		random.shuffle(images)
	
	print 'making collage...'
	res = make_collage(images, opts.output, opts.width, opts.init_height)
	if not res:
		print 'making collage failed!'
		return
	print 'collage done!'

if __name__ == '__main__':
	main()
