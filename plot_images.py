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
step = sys.argv[2]

def masking():
    #----------------------------------------------Brains----------------------------------------------
    images=[]

    for img in sorted(os.listdir(dataDir)):
        #if ("crop" in img):
        if img.endswith('.nii') and not("mask" in img) and not(img == "recon.nii"):
            size=[nib.load(f"{dataDir}/{img}").get_fdata()][0].shape[2]
            images.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size/3)]])
            images.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size/2)]])
            try:
                images.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size-5)]])
            except IndexError:
                images.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size-1)]])

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
            try:
                masks.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size-5)]])
            except IndexError:
                masks.extend([nib.load(f"{dataDir}/{img}").get_fdata()[:,:,int(size-1)]])

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

def QA():
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

def recon():
    #----------------------------------------------Reconstruction----------------------------------------------
    recon=[]

    for img in sorted(os.listdir(dataDir + "/Best_Images_crop/recon")):
        if (img == "recon.nii"):
            size=[nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()][0].shape[2]
            recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,:,int(size/3)]])
            recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,:,int(size/2)]])
            try:
                recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,:,int(size-20)]])
            except IndexError:
                recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,:,int(size-5)]])
            size=[nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()][0].shape[1]
            recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,int(size/3),:]])
            recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,int(size/2),:]])
            try:
                recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,int(size-20),:]])
            except IndexError:
                recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[:,int(size-5),:]])
            size=[nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()][0].shape[0]
            recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[int(size/3),:,:]])
            recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[int(size/2),:,:]])
            try:
                recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[int(size-20),:,:]])
            except IndexError:
                recon.extend([nib.load(f"{dataDir}/Best_Images_crop/recon/{img}").get_fdata()[int(size-5),:,:]])
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

if __name__ == '__main__':
    if (step == "masking"):
        masking()
    elif (step == "QA"):
        QA()
    elif (step == "recon"):
        recon()

