#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Developed by: Ivan Legorreta
Contact information: ilegorreta@outlook.com
'''

import os
import subprocess
import math
import nibabel as nib
import numpy as np
from numpy import zeros

#dataDir = os.getcwd()
op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/dist/alignment_updated", shell=True)
os.chdir("segmentation")
op = subprocess.call("flirt -in Recon_final.nii.gz -ref /neuro/labs/grantlab/research/HyukJin_MRI/Fetal_template/template-31/template-31.nii -out recon_to31.nii -omat recon_to31.xfm", shell=True)
op = subprocess.call("~/arch/Linux64/packages/ANTs/current/bin/N4BiasFieldCorrection -i recon_to31.nii.gz -o recon_to31_nuc.nii", shell=True)
op = subprocess.call("/neuro/labs/grantlab/users/jinwoo.hong/work/codes/fetal_cp_seg2 -input recon_to31_nuc.nii -output .", shell=True)







