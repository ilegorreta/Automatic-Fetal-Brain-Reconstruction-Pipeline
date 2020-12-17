#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description="Automatic Pipeline script")
parser.add_argument("-th", "--threshold", help = "Set Threshold (Default: 0.4)", required = False, default = 0.4)
parser.add_argument("-tar", "--target", help = "Set target image. Default: 1 (Image with highest score)", required = False, default = 1)
parser.add_argument("-r", "--rc", help = "Set to 'True' when running script in rc server", required = False, default = "False")
argument = parser.parse_args()
threshold = str(argument.threshold)
target = str(argument.target)
rc = str(argument.rc)

warnings = open("warnings.log", 'a')
os.system("cp /neuro/labs/grantlab/research/ivan_gonzalez/Documents/recon_pipeline/mri_pipeline.py .")
subprocess.call(['/bin/bash', '-i', '-c', "ss;. neuro-fs stable && conda activate deep_learning && python mri_pipeline.py -th %s -tar %s -r %s" %(threshold,target,rc)], stderr=warnings)
