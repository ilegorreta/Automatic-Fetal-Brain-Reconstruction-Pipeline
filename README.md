# Automatic Fetal Brain Reconstruction Pipeline
## Developed by Iván Legorreta
### Contact information: ilegorreta@outlook.com

The aim of this project was to develop a workflow pipeline containing multiple processing tools towards reconstructing fetal brain MRIs. Developed using Python3 and bash scripts.

This pipeline will call and execute several MRI processing tools, as shown in the next figure:
![Reconstruction Pipeline Diagram](https://github.com/ilegorreta/Automatic-Fetal-Brain-Reconstruction-Pipeline/blob/main/reconstruction_pipeline.png)

### Requirements
* Linux OS
* FreeSurfer Environment

### Running the Pipeline

Once you are inside FreeSurfer Environment, you will need to execute pipeline's binary file with the following command:
```python
/neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/dist/mri_pipeline_v2
```
---
Moreover, you can append additional parameters at the end of the line while executing the script. These are known as command line arguments. They are completely optional, but can be useful to modify script’s behavior. Here is the list of the available arguments:

* **-td [value]** OR **--target_dir [value]** : String value. Set absolute path to the target directory where the images are located. Default value is current working directory.

* **-sf [value]** OR **--start_from [value]** : Integer value. To set from which processing step should the pipeline start from. Here are the options (expressed in actual sequential order within the pipeline):
1. Masking
1. Masks Renaming
1. Masking Validation Image
1. Brain Extraction and Bias Field Correction
1. Cropping Process
1. Quality Assessment
1. Best Images Selection
1. Quality Assessment Validation Image
1. Reconstruction
1. Reconstruction Validation Image

**Note**: You will need to type the number of the chosen processing step, not the name.

* **-th [value]** OR **--threshold [value]** : Float value. Set threshold for selecting best images after quality assessment. Must be a decimal number between 0 and 1. Default value: 0.4

* **-ti [value]** OR **--target_image [value]** : Integer value. Set target image for reconstruction. By default, highest scored image (1) will be used as target, but you can set this value to 2 or 3, in order to use second or third best image as target, respectively.

* **-r [value]** OR **--rc [value]** : Boolean value. Set to ‘True’ only if you are running the script within rc cluster (*rc-twice* or *rc-golden*). Value is NOT case sensitive. Default: ‘False’.

* **-h** OR **--help** : To display this set of instructions on Linux terminal.

### File Structure within Target Directory
During execution, the script will create additional files and sub-directories within target directory, and it is important to understand the information within them.

#### Directory Outline
```bash
.
└── Subject_data/
    ├── Best_Images_crop/
    │   ├── recon/
    │   │   └── recon.nii
    │   └── reconstruction_order.txt
    ├── bfc_failed_images.log
    ├── output.log
    ├── predictions.csv
    ├── skipped.txt
    ├── Validation_images/
    │   ├── images.png
    │   ├── masks.png
    │   ├── qa.png
    │   ├── recon.png
    │   └── transposition.png
    └── warnings.log

```
#### File Description
* **output.log**: Contains the <u>standard output</u> of each processing step.
* **warnings.log**: Contains the <u>standard error</u> of each processing step.
* **skipped.txt**: Indicates which images were not correctly processed during <u>brain masking tool</u>. These are excluded for following process.
* **bfc_failed_images.log**: Indicates which images were <u>not</u> correctly processed during <u>bias field correction tool</u>. They are excluded for following process.
* **predictions.csv**: Contains the quality assessment prediction scores for each image.
* **Best_Images_crop**: This <u>directory</u> contains the images that surpass the exclusion threshold and are the ones that are going to be used for reconstruction.
    * **reconstruction_order.txt**: Indicates the order of the images used for reconstruction. The script will automatically order the images in descending order, based on QA scores.
    * **recon**: This directory contains the resultant files of the reconstruction, most importantly, recon.nii file.
    * **recon.nii**: File containing volume's reconstruction  
* **Validation_images**:  This <u>directory</u> contains the validation images of each processing step, including:
    * **images.png**: Original images snapshots.
    * **masks.png**: Brain masking snapshots
    * **transposition.png**: Transposition of brain image with corresponding mask snapshots.
    * **qa.png**: Brain extraction and scores of quality assessment, snapshots.
    * **recon.png**: Reconstruction snapshots.

---
---
Please feel free to reach me if you have any question or want to know further details.

> By ilegorreta
