#!/usr/bin/env bash


##Possible calls to script: make_archives.sh PN PV | make_archives.sh --make-mesh | make_archives PN PV --make-mesh | make_archives.sh 
#Handle every case correctly:
#Looks sort of ugly so far....
MAKE_MESH=false
while [ ! $# -eq 0 ]
do 
     case "$1" in
          --make-mesh)
               MAKE_MESH=true
               shift

     esac
               PN=$1
               shift
               PV=$2
               shift
               :


if [ -z "$PV" ]; then
     PV=9999
fi
if [ -z "$PN" ]; then
     PN="mouse-brain-atlas"
fi
P="${PN}-${PV}"
PHD="${PN}HD-${PV}"

mkdir ${P}
mkdir ${PHD}
cp FAIRUSE-AND-CITATION ${P}
cp FAIRUSE-AND-CITATION ${PHD}
pushd ${P}
     bash ../ambmc.sh || exit 1
     mv ambmc_15micron.nii ../${PHD}
     mv lambmc_15micron.nii ../${PHD}
     cp ambmc_COPYING ../${PHD}
     cp ambmc_README ../${PHD}
     bash ../dsurqec.sh || exit 1
     bash ../get_abi_atlases.sh || exit 1
     python ../nrrd_to_nifti.py || exit 1
     bash ../ants_reg.sh || exit 1     
     rm abi_10_average.nii.gz 
     rm abi_10_annotation.nii.gz
     mv abi_15_average.nii.gz ../${PHD}
     mv abi_15_annotation.nii.gz ../${PHD}
     if [$MAKE_MESH]; then
          bash ../ambmc2dsurqec.sh
          mv ambmc2dsurqec_15micron.nii.gz ../{$PHD}
popd
tar cfJ "${P}.tar.xz" ${P}
tar cfJ "${PHD}.tar.xz" ${PHD}
