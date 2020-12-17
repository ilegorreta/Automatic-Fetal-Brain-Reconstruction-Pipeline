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

#Read CSV file
with open(f"{dataDir}/predictions.csv", "r") as file: #Change 'csv_prueba.csv' to the correspondant file name where predict.py saves the results of the prediction  
	reader = csv.DictReader(file)
	cont = 0
	for row in reader:
		score = float(row["Average"]) #Reading QC score and cast it to float
		if score >= threshold: #Experiment with different tresholds
			name = row["Name"] #Get Image name
			#name = name.replace("_crop", '') #Removing 'crop' from image name.
			pos = name.find('.nii')
			name2 = name[:pos] + ".{:0.2f}".format(score) + name[pos:]
			shutil.copy2(f"{dataDir}/{name}", f"{dataDir}/Best_Images_crop/{name2}") #Copying the image into Best_Images directory while renaming it to include score 
			cont += 1
	print("%s images copied into 'Best_Images_crop' directory" %cont)
