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
    global dataDir; dataDir = os.getcwd()
    global output; output = open("output.log", 'a')
    global warnings; warnings = open("warnings.log", 'a')
    parser = argparse.ArgumentParser(description="Automatic Pipeline script")
    parser.add_argument("-th", "--threshold", help = "Set Threshold (Default: 0.4)", required = False, default = 0.4)
    parser.add_argument("-tar", "--target", help = "Set target image. Default: 1 (Image with highest score)", required = False, default = 1)
    parser.add_argument("-r", "--rc", help = "Set to 'True' when running script in rc server", required = False, default = "False")
    argument = parser.parse_args()
    global threshold; threshold = str(argument.threshold)
    global target; target = str(argument.target)
    global rc; rc = argument.rc; rc = rc.lower()
    try:
        os.mkdir("Validation_images")
    except FileExistsError as e:
        pass
    print("\nStarting MRI Reconstruction Pipeline")
    separate()

def masking():
    spinner = yaspin(text="Creating brain masks", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call("/neuro/users/jinwoo.hong/github_work/masking_tool/dist/18.04/brain_mask '%s' '%s'" %("--target-dir", dataDir), stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Masking", spinner)
    separate()

def rename():
    spinner = yaspin(text="Renaming masks", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/rename_mask.sh '%s'" %(dataDir), stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Renaming masks", spinner)
    separate()

def validation_image(step):
    spinner = yaspin(text="Creating '%s' validation image" %(step), side="right", spinner="arc", color="green")
    spinner.start() 
    op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/plot_'%s'.py '%s'" %(step,dataDir), stdout=output, stderr=warnings, shell=True)
    error_handler(op, "%s validation image" %(step), spinner)
    separate()

def brainExtraction_BFC():
    spinner = yaspin(text="Performing Brain Extraction and Bias Field Correction", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/biasFieldCorrection.sh '%s'" %(dataDir), stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Brain Extraction and BFC", spinner)
    separate()

def crop():
    spinner = yaspin(text="Cropping images", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/crop.py '%s'" %(dataDir), stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Cropping", spinner)
    separate()

def QA():
    spinner = yaspin(text="Assessing image quality", side="right", spinner="arc", color="green")
    spinner.start()
    op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/dist/predict_resnet '%s'" %(dataDir), stdout=output, stderr=warnings, shell=True)
    error_handler(op, "QA", spinner)
    separate()

def bestImagesSelection():
    spinner = yaspin(text="Creating and populating Best_Images Directory", side="right", spinner="arc", color="green")
    spinner.start()
    try:
        os.mkdir("Best_Images_crop")
    except FileExistsError as e:
        sys.exit("Directory 'Best_Images_crop' already exists. Please remove it before running this script")
    op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/best_images_selection_crop.py '%s' '%s'" %(dataDir, threshold), stdout=output, stderr=warnings, shell=True)
    error_handler(op, "Best_Images_Selection", spinner)
    separate()

def reconstruction():
    if (rc == "true"):
        op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/reconstruction_rc.sh '%s' '%s'" %(dataDir, target), shell=True)
    else:
        op = subprocess.call("/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/reconstruction.sh '%s' '%s'" %(dataDir, target), shell=True)
    separate()
    spinner = yaspin(text="Reconstruction finished", side="right", spinner="arc", color="green")
    spinner.start()
    spinner.ok("✔")
    separate()

if __name__ == '__main__':
    pipeline_init()
    masking()
    rename()
    validation_image("masking")
    brainExtraction_BFC()
    crop()
    QA()
    bestImagesSelection()
    validation_image("QA")
    reconstruction()
    validation_image("recon")
    print("Reconstruction pipeline finish successfully!\n")
