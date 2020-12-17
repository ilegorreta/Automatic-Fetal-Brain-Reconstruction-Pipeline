#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Developed by: Ivan Legorreta
Contact information: ilegorreta@outlook.com
'''

import subprocess
import sys
import os
import argparse
from yaspin import yaspin

def error_handler(op, step, sp):
    if (op == 0):
        sp.ok("✔")
    else:
        sp.color = "red"
        sp.fail("x")
        sys.exit("Error during '%s' script. Check 'warnings.log' file for further details." %(step))    

def separate():
    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

def pipeline_init():
    sf_text = "Set from which processing step should the pipeline start from. Here are the options (expressed in actual sequential order within the pipeline):\n1) Masking\n2) Masks Renaming\n3) Masking Validation Image\n4) Brain Extraction and Bias Field Correction\n5) Cropping Process\n6) Quality Assessment\n7) Best Images Selection\n8) Quality Assessment Validation Image\n9) Reconstruction\n10) Reconstruction Validation Image"
    parser = argparse.ArgumentParser(description="Automatic Pipeline script")
    parser.add_argument("-td", "--target_dir", help = "Set target directory (the one containing subject MRIs). Default: Current dir", required=False, default="Current")
    parser.add_argument("-th", "--threshold", help = "Set Threshold (Default: 0.4)", required = False, default = 0.4)
    parser.add_argument("-ti", "--target_image", help = "Set target image. Default: 1 (Image with highest score)", required = False, default = 1)
    parser.add_argument("-r", "--rc", help = "Set to 'True' when running script in rc server", required = False, default = "False")
    parser.add_argument("-sf", "--start_from", help = sf_text , required = False, default = 1)
    argument = parser.parse_args()
    global dataDir; dataDir = str(argument.target_dir)
    global threshold; threshold = str(argument.threshold)
    global target_image; target_image = str(argument.target_image)
    global rc; rc = argument.rc; rc = rc.lower()
    global sf; sf = int(argument.start_from)
    if (dataDir == "Current"):
        dataDir = os.getcwd()
    global output; output = open(f"{dataDir}/output.log", 'a')
    global warnings; warnings = open(f"{dataDir}/warnings.log", 'a')
    try:
        os.mkdir(f"{dataDir}/Validation_images")
    except FileExistsError as e:
        pass
    print("\nStarting MRI Reconstruction Pipeline\n")
    print(f"Target Directory: {dataDir}\n")
    separate()

def masking():
    spinner = yaspin(text="Creating brain masks", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call(f"/neuro/users/jinwoo.hong/github_work/masking_tool/dist/18.04/brain_mask --target-dir {dataDir}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Masking", spinner)
    separate()

def rename():
    spinner = yaspin(text="Renaming masks", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/rename_mask.sh {dataDir}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Renaming masks", spinner)
    separate()

'''
def validation_image(step):
    spinner = yaspin(text=f"Creating {step} validation image", side="right", spinner="arc", color="green")
    spinner.start() 
    op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/plot_{step}.py {dataDir}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, f"{step} validation image", spinner)
    separate()
'''

def validation_image(step):
    spinner = yaspin(text=f"Creating {step} validation image", side="right", spinner="arc", color="green")
    spinner.start() 
    op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/plot_images.py {dataDir} {step}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, f"{step} validation image", spinner)
    separate()

def brainExtraction_BFC():
    spinner = yaspin(text="Performing Brain Extraction and Bias Field Correction", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/biasFieldCorrection.sh {dataDir}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Brain Extraction and BFC", spinner)
    separate()

def crop():
    spinner = yaspin(text="Cropping images", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/crop.py {dataDir}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Cropping", spinner)
    separate()

def QA():
    spinner = yaspin(text="Assessing image quality", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/dist/predict_resnet {dataDir}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, "QA", spinner)
    separate()

def bestImagesSelection():
    spinner = yaspin(text="Creating and populating 'Best_Images_crop' Directory", side="right", spinner="arc", color="green")
    spinner.start()
    try:
        os.mkdir(f"{dataDir}/Best_Images_crop")
    except FileExistsError as e:
        sys.exit(f"Directory 'Best_Images_crop' already exists at {dataDir}. Please remove it before running this script")
    op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/best_images_selection_crop.py {dataDir} {threshold}", stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Best_Images_Selection", spinner)
    separate()

def reconstruction():
    if (rc == "true"):
        op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/reconstruction_rc.sh {dataDir} {target_image}", shell=True)
    else:
        op = subprocess.call(f"/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/reconstruction.sh {dataDir} {target_image}", shell=True)
    separate()
    spinner = yaspin(text="Reconstruction finished", side="right", spinner="arc", color="green")
    spinner.start()
    spinner.ok("✔")
    separate()

if __name__ == '__main__':
    pipeline_init()
    if (isinstance(sf, int) == False):
        sys.exit("Error. Please select a valid 'Start From' option")
    if (sf < 1 or sf > 10):
        sys.exit("Error. Please select a valid 'Start From' option")
    if (sf == 1):
        masking()
    if (sf <= 2):
        rename()
    if (sf <= 3):
        validation_image("masking")
    if (sf <= 4):
        brainExtraction_BFC()
    if (sf <= 5):
        crop()
    if (sf <= 6):
        QA()
    if (sf <= 7):
        bestImagesSelection()
    if (sf <= 8):
        validation_image("QA")
    if (sf <= 9):
        reconstruction()
    if (sf <= 10):
        validation_image("recon")
    print("Reconstruction pipeline finish successfully!\n")
