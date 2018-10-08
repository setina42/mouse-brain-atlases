#!/bin/bash

STANDALONE=$1

#Standalone: Need to download atlas and transform beforehand
if [ -n "${STANDALONE}" ]; then
        
	bash dsurqec.sh
	bash ambmc.sh
fi
	# Resize
ResampleImage 3 dsurqec_40micron_masked.nii _dsurqec_15micron_masked.nii 0.015x0.015x0.015 size=1 spacing=0 4
SmoothImage 3 _dsurqec_15micron_masked.nii 0.4 dsurqec_15micron_masked.nii
fslorient -copyqform2sform dsurqec_15micron_masked.nii


#Run AntsRegisatr
antsAI -d 3 -v \
        --transform Rigid[ 0.5 ] \
        --metric MI[dsurqec_15micron_masked.nii,ambmc_15micron.nii, 1, 64, Random, 0.1 ] \
        exit 1


# Registration call
antsRegistration \
	--float 1 \
	--collapse-output-transforms 1 \
	--dimensionality 3 \
	--initial-moving-transform [dsurqec_15micron_masked.nii,ambmc_15micron.nii, 1 ] \
	--initialize-transforms-per-stage 0 --interpolation Linear --output [ ambmc2dsurqec_, ambmc2dsurqec_15micron.nii ] \
	--interpolation Linear \
	\
	--transform Rigid[ 0.5 ] \
	--metric MI[dsurqec_15micron_masked.nii,ambmc_15micron.nii, 1, 64, Random, 0.1 ] \
	--convergence [ 400x400x400x200, 1e-9, 10 ] \
	--smoothing-sigmas 3.0x2.0x1.0x0.0vox \
	--shrink-factors 10x4x2x1 \
	--use-estimate-learning-rate-once 0 \
	--use-histogram-matching 1 \
	\
	--transform Affine[ 0.1 ]\
	--metric MI[dsurqec_15micron_masked.nii,ambmc_15micron.nii, 1, 64, Regular, 0.1 ] \
	--convergence [ 400x200, 1e-10, 10 ] \
	--smoothing-sigmas 1.0x0.0vox \
	--shrink-factors 2x1 \
	--use-estimate-learning-rate-once 0 \
	--use-histogram-matching 1 \
	\
	--transform SyN[0.25,3,0] \
	--metric CC[dsurqec_15micron_masked.nii,ambmc_15micron.nii,1,4] \
	--convergence [100x70x50,1e-6,10] \
	--shrink-factors 8x4x2 \
	--smoothing-sigmas 3x2x1vox \
	\
	--winsorize-image-intensities [ 0.05, 0.95 ] \
	--write-composite-transform 1 \
	--verbose

fslorient -copyqform2sform ambmc2dsurqec_15micron.nii

#Apply mask
#fslmaths 'ambmc2dsurqec_15micron.nii' -mas 'dsurqec_15micron_mask.nii' 'ambmc2dsurqec_15micron_masked.nii'
#This is a bad idea. Dont use the resampled mask, but resample the masked image and make a new mask out of it. This can then be applied to amb,c2dsurqec. The resulting mesh is much smoother
         

fslmaths dsurqec_15micron_masked.nii -thr 10 -bin dsurqec_15micron_mask_fromresampledfile.nii
fslmaths 'ambmc2dsurqec_15micron.nii.gz' -mas 'dsurqec_15micron_mask_fromresampledfile.nii.gz' 'ambmc2dsurqec_15micron_masked.nii.gz'


#Make mesh file of transformed atlas
python make_mesh.py


