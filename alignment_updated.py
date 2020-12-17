#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:30:31 2020

@author: maria.hernandez
"""

#Todas slides 3 planos python (elige la que tenga mayor cc 
#para cada slide)

#def alignment():
import os
import math
import nibabel as nib
import numpy as np
from numpy import zeros
       
path=os.getcwd()
if not os.path.exists('./alignment'):
    os.makedirs('alignment')
    
if not os.path.exists('./segmentation'):
    os.makedirs('segmentation')
    
os.system('cp recon/recon.nii alignment')
os.chdir(os.getenv("HOME"))

if not os.path.exists('./templates'):
    os.system('cp -R /neuro/labs/grantlab/users/maria.hernandez/Trial/templates ~')

os.chdir(path)
os.chdir('alignment')

os.system(\
'flirt -in ~/templates/template-23/template-23.nii -ref recon.nii \
-out Temp-Recon-7dof-23.nii -omat Temp-Recon-7dof-23.xfm -dof 7; \
flirt -in ~/templates/template-23/csf-23.nii -ref recon.nii \
-out csf-aligned23.nii -init Temp-Recon-7dof-23.xfm -applyxfm; \
flirt -in ~/templates/template-24/template-24.nii -ref recon.nii \
-out Temp-Recon-7dof-24.nii -omat Temp-Recon-7dof-24.xfm -dof 7; \
flirt -in ~/templates/template-24/csf-24.nii -ref recon.nii \
-out csf-aligned24.nii -init Temp-Recon-7dof-24.xfm -applyxfm; \
flirt -in ~/templates/template-25/template-25.nii -ref recon.nii \
-out Temp-Recon-7dof-25.nii -omat Temp-Recon-7dof-25.xfm -dof 7; \
flirt -in ~/templates/template-25/csf-25.nii -ref recon.nii \
-out csf-aligned25.nii -init Temp-Recon-7dof-25.xfm -applyxfm; \
flirt -in ~/templates/template-26/template-26.nii -ref recon.nii \
-out Temp-Recon-7dof-26.nii -omat Temp-Recon-7dof-26.xfm -dof 7; \
flirt -in ~/templates/template-26/csf-26.nii -ref recon.nii \
-out csf-aligned26.nii -init Temp-Recon-7dof-26.xfm -applyxfm; \
flirt -in ~/templates/template-27/template-27.nii -ref recon.nii \
-out Temp-Recon-7dof-27.nii -omat Temp-Recon-7dof-27.xfm -dof 7; \
flirt -in ~/templates/template-27/csf-27.nii -ref recon.nii \
-out csf-aligned27.nii -init Temp-Recon-7dof-27.xfm -applyxfm; \
flirt -in ~/templates/template-28/template-28.nii -ref recon.nii \
-out Temp-Recon-7dof-28.nii -omat Temp-Recon-7dof-28.xfm -dof 7; \
flirt -in ~/templates/template-28/csf-28.nii -ref recon.nii \
-out csf-aligned28.nii -init Temp-Recon-7dof-28.xfm -applyxfm; \
flirt -in ~/templates/template-29/template-29.nii -ref recon.nii \
-out Temp-Recon-7dof-29.nii -omat Temp-Recon-7dof-29.xfm -dof 7; \
flirt -in ~/templates/template-29/csf-29.nii -ref recon.nii \
-out csf-aligned29.nii -init Temp-Recon-7dof-29.xfm -applyxfm; \
flirt -in ~/templates/template-30/template-30.nii -ref recon.nii \
-out Temp-Recon-7dof-30.nii -omat Temp-Recon-7dof-30.xfm -dof 7; \
flirt -in ~/templates/template-30/csf-30.nii -ref recon.nii \
-out csf-aligned30.nii -init Temp-Recon-7dof-30.xfm -applyxfm; \
flirt -in ~/templates/template-31/template-31.nii -ref recon.nii \
-out Temp-Recon-7dof-31.nii -omat Temp-Recon-7dof-31.xfm -dof 7; \
flirt -in ~/templates/template-31/csf-31.nii -ref recon.nii \
-out csf-aligned31.nii -init Temp-Recon-7dof-31.xfm -applyxfm; \
flirt -in ~/templates/template-32/template-32.nii -ref recon.nii \
-out Temp-Recon-7dof-32.nii -omat Temp-Recon-7dof-32.xfm -dof 7; \
flirt -in ~/templates/template-32/csf-32.nii -ref recon.nii \
-out csf-aligned32.nii -init Temp-Recon-7dof-32.xfm -applyxfm;')

recon = nib.load('recon.nii') # Load reconstruction image 
size=recon.get_fdata().shape # Get the dimensions of the volume 

meas = [0,0,0]
beginning=[0,0,0]

for i in range (0, 3):
    beginning[i]=int(round(size[i]/10.0))
    temp=size[i]-beginning[i]
    meas[i]=temp-beginning[i]
    
    if (i==0):
        dimensions=zeros([size[1],size[2]])
        coronal= dict.fromkeys(range(0, meas[i]),dimensions)
    if (i==1):
        dimensions=zeros([size[0],size[2]])
        sagital= dict.fromkeys(range(0, meas[i]),dimensions)
    if (i==2):
        dimensions=zeros([size[0],size[1]])
        axial= dict.fromkeys(range(0, meas[i]),dimensions)

ccl= meas[0]+meas[1]+meas[2]

im = {'corrcoef':zeros([1,ccl*10]), 'greatest':zeros([1,ccl]), 'template':zeros([1,ccl])}

for i in range (0, meas[0]): #Gets the number of slides choosen
    a= beginning[0]+i #Starts in the slide selected as beginning and ends passing the one selected as end
    coronal[i]=np.uint8(np.squeeze(recon.get_fdata()[a,:,:])/4)  #Get the slide of the reconstruction image.

for i in range (0, meas[1]):    
    a= beginning[1]+i #Starts in the slide selected as beginning and ends passing the one selected as end
    sagital[i]=np.uint8(np.squeeze(recon.get_fdata()[:,a,:])/4)  #Get the slide of the reconstruction image.

for i in range (0, meas[2]):    
    a= beginning[2]+i #Starts in the slide selected as beginning and ends passing the one selected as end
    axial[i]=np.uint8(np.squeeze(recon.get_fdata()[:,:,a])/4)  #Get the slide of the reconstruction image.
            
number=22 #Stablishes the base to number the templates

def mean2(value):
    mean2value=np.sum(value)/np.size(value)
    return mean2value

def corr2(R, T):
    R=R-mean2(R)
    T=T-mean2(T)
    corr=((R*T).sum())/(math.sqrt((R*R).sum()*(T*T).sum()))
    return corr
   
for i in range (0,10): #Says that the process will repeat for the 10 templates
    number=number+1 #The first template will be 23
    volume='csf-aligned%d.nii.gz' %number #Construct the name of the template volume that will be loaded
    volume=nib.load(volume) #Load the template volume
    meascor=(meas[0]*i)
    meassag=(meas[1]*i)+(meas[0]*9)
    measax=(meas[2]*i)+(meas[0]*9)+(meas[1]*9)
    
    for j in range (0,ccl):
        if (j<meas[0]):
            t=meascor+j #Define the position in which the results will be stored\
            a=beginning[0]+j; #Select the slide that will be taken
            slide=volume.get_fdata()[a,:,:] #Loads the slide
            
        if (j>=meas[0] and j<(meas[0]+meas[1])):
            t=meassag+j #Define the position in which the results will be stored\
            a=beginning[0]+j-meas[0]; #Select the slide that will be taken
            slide=volume.get_fdata()[:,a,:] #Loads the slide
        
        if (j>=(meas[0]+meas[1])):
            t=measax+j #Define the position in which the results will be stored\
            a=beginning[0]+j-meas[0]-meas[1]; #Select the slide that will be taken
            slide=volume.get_fdata()[:,:,a] #Loads the slide    
            
       #normalize the slide
        slide=np.uint8(256*(slide-slide.min())/(slide.max()-slide.min()))
       
        index=np.nonzero(slide) #get the positions of the non zero values 
        csfi=slide[np.nonzero(slide)] #get the values of the no zero values
      
        temp=csfi.shape #gets the number of non zero values 
        temp=temp[0]
        reconi=[]
        
        if (j<meas[0]):
            for n in range (0,temp): #get the same indexes of the recon image
                slide=coronal[j].item(index[0][n],index[1][n])
                reconi.append(slide)
                          
        if (j>=meas[0] and j<(meas[0]+meas[1])):
            for n in range (0,temp): #get the same indexes of the recon image
                jj=j-meas[0]
                slide=sagital[jj].item(index[0][n],index[1][n])
                reconi.append(slide)
                
        if (j>=(meas[0]+meas[1])):
            for n in range (0,temp): #get the same indexes of the recon image
                jj=j-meas[0]-meas[1]
                slide=axial[jj].item(index[0][n],index[1][n])
                reconi.append(slide)
                
        im['corrcoef'][0,t]=corr2(reconi, csfi)
     
    a=0
         
for a in range (0,ccl):
    im['greatest'][0,a]=-5
        
    for i in range (0,10):
        if (a<meas[0]):
            j=(meas[0]*i)+a
                            
        if (a>=meas[0] and a<(meas[1]+meas[0]) ):
            j=(meas[1]*i)+(meas[0]*9)+a
            
        if (a>=(meas[1]+meas[0])):    
            j=(meas[2]*i)+(meas[0]*9)+(meas[1]*9)+a            
            
        if im['corrcoef'][0,j]>im['greatest'][0,a]:
            im['greatest'][0,a]=im['corrcoef'][0,j]
            im['template'][0,a]=i+23

t=im['template']
t=t[0]
a=t.tolist()
j=im['greatest']
jj=max(j[0])-((max(j[0]))/2.5)

for i in range (0,ccl):
    if (j[0][i]>jj):
        a.append(im['template'][0,i])

n=np.histogram(t,bins=[23,24,25,26,27,28,29,30,31,32,33])
temp=np.argsort(n[0])[::-1]    
tempi=temp+23
temp=tempi[0]

os.environ['temp']=str(temp)
   
os.system('convert_xfm -omat InvAligned-$temp.xfm -inverse Temp-Recon-7dof-$temp.xfm')

os.system('flirt -in recon.nii -ref ~/templates/template-$temp/template-$temp.nii \
-out InvAligned-$temp.nii.gz -init InvAligned-$temp.xfm -applyxfm')

os.chdir(path)
 
os.system('cp alignment/InvAligned-$temp.nii.gz segmentation')
os.system('cp alignment/InvAligned-$temp.xfm segmentation')

os.chdir('segmentation')

os.system('mv InvAligned-$temp.nii.gz Recon_final.nii.gz')
os.system('mv InvAligned-$temp.xfm Recon_final.xfm')








