#!/usr/bin/env bash


##Possible calls to script: make_archives.sh PN PV | make_archives.sh --make-mesh | make_archives PN PV --make-mesh | make_archives.sh 
#Handle every case correctly:
#Looks sort of ugly so far....
MAKE_MESH=false

if [ "$1" == "--make_mesh" ]; then
     MAKE_MESH=true
     PN=$2
     PV=$3

else 
     PN=$1
     PV=$2
     if [ "$3" == "--make_mesh" ]; then
          MAKE_MESH=true
     fi
fi

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
     bash ../abi.sh || exit 1
     bash ../abi2dsurqec_40micron.sh || exit 1     
     rm abi_10_average.nii.gz 
     rm abi_10_annotation.nii.gz
     mv abi_15_average.nii.gz ../${PHD}
     mv abi_15_annotation.nii.gz ../${PHD}
     if [ $MAKE_MESH ]; then
          bash ../ambmc2dsurqec.sh || exit 1
          mv ambmc2dsurqec_15micron.nii.gz ../{$PHD}
          mv ambmc2dsurqec_15micron.obj ../{PHD}
popd
tar cfJ "${P}.tar.xz" ${P}
tar cfJ "${PHD}.tar.xz" ${PHD}
