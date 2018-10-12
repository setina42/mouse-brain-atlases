
fslmaths ambmc2dsurqec_15micron_masked.nii.gz -thr 10 -bin ambmc2dsurqec_mask.nii.gz
echo "Mask made"
fslmaths ambmc2dsurqec_mask.nii.gz -kernel boxv3 11 11 11 -ero -bin ambmc2dsurqec_eroded_11.nii.gz
echo "Mask eroded by 11 11 11"
fslmaths ambmc2dsurqec_eroded_11.nii.gz -kernel boxv3 3 3 3 -ero -bin ambmc2dsurqec_eroded_11_3.nii.gz
fslmaths ambmc2dsurqec_eroded_11_3.nii.gz -kernel boxv3 3 3 3 -ero -bin ambmc2dsurqec_eroded_11_3_3.nii.gz
fslmaths ambmc2dsurqec_eroded_11_3_3.nii.gz -kernel boxv3 3 3 3 -ero -bin ambmc2dsurqec_internalmask.nii.gz
echo "Internal mask created"

rm ambmc2dsurqec_mask.nii.gz
rm ambmc2dsurqec_eroded_11_3_3.nii.gz
rm ambmc2dsurqec_eroded_11_3.nii.gz
rm ambmc2dsurqec_eroded_11.nii.gz
