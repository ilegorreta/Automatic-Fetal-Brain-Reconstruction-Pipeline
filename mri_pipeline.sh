#!/bin/bash

IMAGE_DIR=$(pwd)

echo "Starting MRI Reconstruction Pipeline"
echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# MASKING
echo "Creating brain masks..."
#/neuro/labs/grantlab/users/alejandro.valdes/projects/brain-masking-tool/dist/brain_mask --target-dir $IMAGE_DIR >> output.log
/neuro/users/jinwoo.hong/github_work/masking_tool/dist/18.04/brain_mask --target-dir $IMAGE_DIR >> output.log
echo "Masks created"

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# RENAMING
/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/rename_mask.sh $IMAGE_DIR
echo "Masks renamed"

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# Making Masking validation images
echo "Creating Masking validation image"
mkdir Validation_images
python /neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/plot_masking.py $IMAGE_DIR

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# Brain Extraction & BFC 
ss >> output.log;. neuro-fs stable >> output.log
echo "Performing Brain Extraction and Bias Field Correction..."
/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/biasFieldCorrection.sh $IMAGE_DIR 2>> warnings.log >> output.log
echo "Brain Extraction and Bias Field Correction completed"

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# CROPPING
echo "Cropping images..."
python /neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/crop.py $IMAGE_DIR 2>> warnings.log >> output.log
echo "Cropping process completed"

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# QA 
echo "Assessing image quality..."
conda activate deep_learning
python /neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/predict_resnet.py $IMAGE_DIR 2>> warnings.log >> output.log

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# Selection of best images
python /neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/best_images_selection_crop.py $IMAGE_DIR 0.4

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

#Making Best Images QA validation image
echo "Creating QA validation image"
python /neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/plot_QA.py $IMAGE_DIR

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

# Reconstruction
/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/reconstruction.sh $IMAGE_DIR 1

echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

#Making Reconstruction validation image
echo "Creating Reconstruction validation image"
python /neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/plot_recon.py $IMAGE_DIR
