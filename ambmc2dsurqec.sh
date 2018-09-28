#!/bin/bash

PN=$1
PV=$2
if [ -z "$PV" ]; then
        PV=9999
fi
if [ -z "$PN" ]; then
        PN="ambmc2dsurqec"
fi
P="${PN}-${PV}"
mkdir ${P}
pushd ${P}
          

        wget http://repo.mouseimaging.ca/repo/DSURQE_40micron_nifti/DSURQE_40micron_average.nii
        wget http://repo.mouseimaging.ca/repo/DSURQE_40micron_nifti/DSURQE_40micron_mask.nii

        # Set origin to Paxinos Bregma
        mv DSURQE_40micron_average.nii dsurqec_40micron.nii
        fslorient -setsform 0.04 0 0 -6.27 0 0.04 0 -10.6 0 0 0.04 -7.88 0 0 0 1 dsurqec_40micron.nii
        fslorient -copysform2qform dsurqec_40micron.nii
        mv DSURQE_40micron_mask.nii dsurqec_40micron_mask.nii
        fslorient -setsform 0.04 0 0 -6.27 0 0.04 0 -10.6 0 0 0.04 -7.88 0 0 0 1 dsurqec_40micron_mask.nii
        fslorient -copysform2qform dsurqec_40micron_mask.nii

        # Resize
        ResampleImage 3 dsurqec_40micron.nii dsurqec_15micron.nii 0.015x0.015x0.015 size=1 spacing=0 4
        fslorient -copyqform2sform dsurqec_15micron.nii
        ResampleImage 3 dsurqec_40micron_mask.nii dsurqec_15micron_mask.nii 0.015x0.015x0.015 size=1 spacing=0 1
        fslorient -copyqform2sform dsurqec_15micron_mask.nii

        # Apply Masks
        fslmaths 'dsurqec_15micron.nii' -mas 'dsurqec_15micron_mask.nii' 'dsurqec_15micron_masked.nii'

        # Cleanup
        rm dsurqec_40micron.nii
        rm dsurqec_40micron_mask.nii
        rm dsurqec_15micron.nii
        rm dsurqec_15micron_mask.nii
        

        # Download Upstream Template
        wget http://imaging.org.au/uploads/AMBMC/ambmc-c57bl6-model-symmet_v0.8-nii.tar.gz
        tar xvzf ambmc-c57bl6-model-symmet_v0.8-nii.tar.gz
        cp ambmc-c57bl6-model-symmet_v0.8-nii/ambmc-c57bl6-model-symmet_v0.8.nii _ambmc_15micron.nii

        # Make RAS
        fslswapdim _ambmc_15micron.nii x -y z ambmc_15micron.nii
        fslorient -setsform 0.015 0 0 5.094 0 0.015 0 9.8355 0 0 0.015 -3.726 0 0 0 1 ambmc_15micron.nii.gz
        fslorient -copysform2qform ambmc_15micron.nii.gz

        # Cleanup
        rm -rf ambmc-c57bl6-model-symmet_v0.8-nii*
        rm -rf _*ambmc*nii*
popd
