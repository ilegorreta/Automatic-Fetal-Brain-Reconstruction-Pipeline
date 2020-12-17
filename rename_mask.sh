#!/bin/bash

#Developed by: Ivan Legorreta
#Contact information: ilegorreta@outlook.com

cd $1

MASKS=$(ls *_mask.nii)

for MASK in $MASKS
do
	TEMP=${MASK/_mask/}	
	mv $MASK mask_${TEMP}
done
