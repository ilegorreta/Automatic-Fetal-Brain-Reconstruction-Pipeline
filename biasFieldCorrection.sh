#!/bin/bash

#Developed by: Ivan Legorreta
#Contact information: ilegorreta@outlook.com

cd $1

IMAGES=$(ls -I '*mask*')

for IMAGE in $IMAGES
do
	if [ "$IMAGE" == "mri_pipeline.py" ]; then
		continue
        elif [ "$IMAGE" == "init_pipeline.py" ]; then
		continue
	elif [ "$IMAGE" == "output.log" ]; then
		continue
	elif [ "$IMAGE" == "warnings.log" ]; then
		continue
        elif [ "$IMAGE" == "skipped.txt" ]; then
		continue
	else
		if [[ -f mask_$IMAGE ]]; then
			mri_mask ${IMAGE} mask_${IMAGE} brain_${IMAGE}
			~/arch/Linux64/packages/ANTs/current/bin/N4BiasFieldCorrection -d 3 -o corrected_${IMAGE} -i brain_${IMAGE} -s 3 -c [400x400x400,0.00]
			if [[ -f corrected_${IMAGE} ]]; then
				SIZE=$(mri_info corrected_${IMAGE} | awk '/voxel sizes:/ {print $5}')
				mv corrected_${IMAGE} ${SIZE}-mm-${IMAGE}
			else
				echo $IMAGE >> bfc_failed_images.log
			fi
		fi	
	fi
done
