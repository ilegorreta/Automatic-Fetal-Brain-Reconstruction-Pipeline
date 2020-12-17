#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Developed by: Ivan Legorreta
Contact information: ilegorreta@outlook.com
'''

import os
import sys

dataDir = sys.argv[1]

def crop_image(input_name, output_name):
	import numpy as np
	import nibabel as nib

	nim = nib.load(f"{dataDir}/{input_name}")
	image = nim.get_data()
	if np.mean(image) == 0:
		print(input_name,'\t Passed')
		return 0

	# Detect the bounding box of the foreground
	idx = np.nonzero(image > 0)
	x1, x2 = idx[0].min(), idx[0].max()
	y1, y2 = idx[1].min(), idx[1].max()
	z1, z2 = idx[2].min(), idx[2].max()

	# Crop the image
	image = image[x1:x2, y1:y2, z1:z2]

	affine = nim.affine
	affine[:3, 3] = np.dot(affine, np.array([x1, y1, z1, 1]))[:3]
	nim2 = nib.Nifti1Image(image, affine)
	nib.save(nim2, f"{dataDir}/{output_name}")
	return image

if __name__ == '__main__':
	for img in sorted(os.listdir(dataDir)):
		if img.endswith('.nii') and ("-mm-" in img):
			#print(img)
			pos = img.find('.nii')
			img_crop = img[:pos] + "_crop" + img[pos:]
			#print(img_crop)
			crop_image(img, img_crop)
	print("Images cropped successfully")
