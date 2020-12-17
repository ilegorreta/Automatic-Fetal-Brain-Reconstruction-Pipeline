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

#----------------------------------------------Brains----------------------------------------------
images=[]

for img in sorted(os.listdir(dataDir)):
    #if ("crop" in img):
    if img.endswith('.nii') and not("mask" in img) and not(img == "recon.nii"):
        size=[nib.load(f"{dataDir}/{img}").get_fdata()][0].shape[2]
        images.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size/3)]])
        images.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size/2)]])
        images.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size-5)]])

#Set properties of images  
plt.rcParams['figure.facecolor'] = 'black'
plt.style.use('dark_background')
fig=plt.figure(figsize=(25, 15))
rows =int(round((len(images)/3)/2.0))
columns = 2
outer = gridspec.GridSpec(rows, columns, wspace=0.2, hspace=0.1)
count = 1
if ((len(images)/3) % 2) == 0:
    limit = rows*columns
else:
    limit = (rows*columns) - 1

for i in range(limit):
    inner = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[i], wspace=0.1, hspace=0.1)

    for j in range(3):
        fig.add_subplot(inner[j])
        plt.imshow(np.squeeze(np.asarray(images[count-1])), cmap='gray',interpolation='nearest')
        plt.axis('off')
        count += 1

plt.savefig(dataDir + '/Validation_images/images.png', dpi=300)

#----------------------------------------------Masks----------------------------------------------
masks=[]

for img in sorted(os.listdir(dataDir)):
    if img.endswith('.nii') and ("mask" in img):
        size=[nib.load(f"{dataDir}/{img}").get_fdata()][0].shape[2]
        masks.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size/3)]])
        masks.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size/2)]])
        masks.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size-5)]])

#Set properties of images  
plt.rcParams['figure.facecolor'] = 'black'
plt.style.use('dark_background')
fig=plt.figure(figsize=(25, 15))
rows =int(round((len(masks)/3)/2.0))
columns = 2
outer = gridspec.GridSpec(rows, columns, wspace=0.2, hspace=0.1)
count = 1
if ((len(masks)/3) % 2) == 0:
    limit = rows*columns
else:
    limit = (rows*columns) - 1

for i in range(limit):
    inner = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[i], wspace=0.1, hspace=0.1)

    for j in range(3):
        fig.add_subplot(inner[j])
        plt.imshow(np.squeeze(np.asarray(masks[count-1])), cmap='gray',interpolation='nearest')
        plt.axis('off')
        count += 1

plt.savefig(dataDir + '/Validation_images/masks.png', dpi=300)

#----------------------------------------------Trasposition----------------------------------------------
overlay = Image.open(dataDir + '/Validation_images/images.png')
base = Image.open(dataDir + '/Validation_images/masks.png')
    
bands = list(overlay.split())
if len(bands) == 4:
    # Assuming alpha is the last band
    bands[3] = bands[3].point(lambda x: x*0.6)
    
overlay = Image.merge(overlay.mode, bands) 
   
base.paste(overlay, (0, 0), overlay)
base.save(dataDir + '/Validation_images/transposition.png')
