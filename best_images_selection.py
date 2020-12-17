#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import csv
import fnmatch
import sys
import errno

'''
Developed by: Ivan Legorreta
Contact information: ilegorreta@outlook.com
'''

dataDir = sys.argv[1]
threshold = float(sys.argv[2])

try:
	os.mkdir("%s/Best_Images" %dataDir)
	print("Directory 'Best_Images' created")
except OSError as e:
	if e.errno == errno.EEXIST:
		sys.exit("Directory 'Best_Images' already exists. Please remove it before running this script")
	else:
        	raise

'''
Quality Assesment is performed with cropped images, whereas reconstruction is performed with normal images
'''

#Read CSV file
with open('%s/predictions.csv' %dataDir, "r") as file: #Change 'csv_prueba.csv' to the correspondant file name where predict.py saves the results of the prediction  
	reader = csv.DictReader(file)
	cont = 0
	for row in reader:
		score = float(row["Average"]) #Reading QC score and cast it to float
		if score >= threshold: #Experiment with different tresholds
			name = row["Name"] #Get Image name
			name = name.replace("_crop", '') #Removing 'crop' from image name.
			pos = name.find('.nii')
			name2 = name[:pos] + ".{:0.2f}".format(score) + name[pos:]
			shutil.copy2(name, "%s/Best_Images/%s" %(dataDir,name2)) #Copying the image into Best_Images directory while renaming it to include score 
			cont += 1
	print("%s images copied into 'Best_Images' directory" %cont)
