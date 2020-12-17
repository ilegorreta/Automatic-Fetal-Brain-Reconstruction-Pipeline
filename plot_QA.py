#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Developed by: Ivan Legorreta
Contact information: ilegorreta@outlook.com
'''

import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
from PIL import Image 
import numpy as np
import matplotlib.gridspec as gridspec

dataDir = sys.argv[1]

#----------------------------------------------QA----------------------------------------------
images=[]
scores=[]
for img in sorted(os.listdir(dataDir + "/Best_Images_crop/")):
    if img.endswith('.nii') and ("-mm-" in img):
        score = img[-8:-4]
        scores.append(score)
        size=[nib.load(f"{dataDir}/Best_Images_crop/{img}").get_fdata()][0].shape[2]
        images.extend([nib.load(f"{dataDir}/Best_Images_crop/{img}").get_fdata()[:,:,int(size/2)]])
        size=[nib.load(f"{dataDir}/Best_Images_crop/{img}").get_fdata()][0].shape[1]
        images.extend([nib.load(f"{dataDir}/Best_Images_crop/{img}").get_fdata()[:,int(size/2),:]])
        size=[nib.load(f"{dataDir}/Best_Images_crop/{img}").get_fdata()][0].shape[0]
        images.extend([nib.load(f"{dataDir}/Best_Images_crop/{img}").get_fdata()[int(size/2),:,:]])

#Set properties of images  
plt.rcParams['figure.facecolor'] = 'black'
plt.style.use('dark_background')
fig=plt.figure(figsize=(25, 15))
rows =int(round((len(images)/3)/2.0))
columns = 2
outer = gridspec.GridSpec((rows+1), columns, wspace=0.2, hspace=0.1)
count = 1
if ((len(images)/3) % 2) == 0:
    limit = rows*columns
else:
    limit = (rows*columns) - 1

for i in range(limit):
    inner = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[i], wspace=0.1, hspace=0.1)
    ax = plt.Subplot(fig, outer[i])
    ax.set_title("QA Score: %s" %scores[i], fontsize=40)
    ax.axis("off")
    fig.add_subplot(ax)

    for j in range(3):
        fig.add_subplot(inner[j])
        plt.imshow(np.squeeze(np.asarray(images[count-1])), cmap='gray',interpolation='nearest')
        plt.axis("off")
        count += 1

plt.savefig(dataDir + "/Validation_images/qa.png", dpi=300)
