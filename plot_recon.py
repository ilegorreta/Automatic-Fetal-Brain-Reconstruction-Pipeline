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

#----------------------------------------------Reconstruction----------------------------------------------
recon=[]

for img in sorted(os.listdir(dataDir + "/Best_Images_crop/recon")):
    if (img == "recon.nii"):
        size=[nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()][0].shape[2]
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,:,int(size/3)]])
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,:,int(size/2)]])
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,:,int(size-20)]])
        size=[nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()][0].shape[1]
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,int(size/3),:]])
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,int(size/2),:]])
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,int(size-20),:]])
        size=[nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()][0].shape[0]
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[int(size/3),:,:]])
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[int(size/2),:,:]])
        recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[int(size-20),:,:]])
        break

#Set properties of images  
plt.rcParams['figure.facecolor'] = 'black'
plt.style.use('dark_background')
fig=plt.figure(figsize=(25, 15))
rows =3
columns = 3

for i in range(1,len(recon)+1):
    fig.add_subplot(rows, columns, i)
    plt.imshow(np.squeeze(np.asarray(recon[i-1])), cmap='gray',interpolation='nearest')
    plt.axis('off')

plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
plt.savefig(dataDir + "/Validation_images/recon.png", dpi=300)
