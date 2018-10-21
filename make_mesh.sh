#!/usr/bin/env bash

#Script to create mesh from volume data. 
#make mask
fslmaths ambmc2dsurqec_15micron_masked.nii.gz -thr 10 -bin ambmc2dsurqec_mask.nii.gz
echo "Mask made"

#create smaller, internal masks
python mask_erode.py

#smooth one mask heavily
SmoothImage 3 ambmc2dsurqec_mask_eroded6.nii.gz 10 ambmc2dsurqec_mask_eroded6_smoothed.nii.gz
rm ambmc2dsurqec_mask_eroded6.nii.gz

#make mesh using marching cube
python make_mesh.py

rm ambmc2dsurqec_mask_eroded6_smoothed.nii.gz
rm ambmc2dsurqec_mask_eroded10.nii.gz
rm ambmc2dsurqec_mask.nii.gz
