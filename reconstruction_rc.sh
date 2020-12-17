#!/bin/bash

#Developed by: Ivan Legorreta
#Contact information: ilegorreta@outlook.com

cd $1
cd Best_Images_crop

appDirTBB="/neuro/arch/Linux64/packages/irtk/build-tbb-rc/bin"
#appDirTBB="/neuro/labs/grantlab/research/Fetal_MRI/IRTK/build/bin/"
imageDir=$(pwd)
transformDir=""

TIMESTAMP=`date "+%m-%d-%Y - %Hhr:%Mmin:%Sseg"`

IMAGES=$(ls *.nii)

declare -A array

for IMAGE in $IMAGES
do
	position=$(awk -F"." '{print NF-1}' <<< "${IMAGE}")
	score=$(echo $IMAGE | cut -d'.' -f $position)
	if [ "$score" = "00" ]
	then
		score="9999"
	fi
	array[$IMAGE]=$score
done


KEYS=$(
for KEY in ${!array[@]}; do
  echo "${array[$KEY]}:::$KEY"
done | sort -rn | awk -F::: '{print $2}'
)

array2=()
for val in $KEYS; do
	array2+=($val)
done

if [ $2 == 2 ]
then
	TEMP2=${array2[0]}
	array2[0]=${array2[1]}
	array2[1]=$TEMP2
elif [ $2 == 3 ]
then
	TEMP2=${array2[0]}
	array2[0]=${array2[2]}
	array2[2]=$TEMP2
fi

IMAGESCOUNT=${#array2[@]}
IMAGES_NAMES=$''
IMAGES2=$''
IDS=$''
ONES=$''
THICKNESS=$''

for i in "${array2[@]}"
do
	IMAGES_NAMES+=$imageDir'/'$i' '
	IDS+='id '
	ONES+='1 '
	TEMP=$(echo ${i:0:3})
	THICKNESS+=$TEMP
	THICKNESS+=' '
	IMAGES2+=$i' '
done

echo Reconstruction order: 
echo $IMAGES2 at $TIMESTAMP >> $"reconstruction_order.txt"
echo >> $"reconstruction_order.txt"

mkdir recon
cd recon

$appDirTBB/reconstruction recon.nii $IMAGESCOUNT $IMAGES_NAMES $IDS -thickness $THICKNESS -debug -packages $ONES
#$appDirTBB/reconstruction recon.nii $IMAGESCOUNT $IMAGES_NAMES -thickness $THICKNESS -debug -packages $ONES
