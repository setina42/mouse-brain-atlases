#!/usr/bin/env bash

echo arrived

CUT=false
MASK=false
BOUNDARY=false

while getopts ':i:t:bcs:a:d:m:' flag; do
        case "${flag}" in

                i)
                        IMAGE_NAME="$OPTARG"
                        ;;
                  
                t)      TRESHHOLD="$OPTARG"
                        ;;
                b)
                        BOUNDARY=true
                        ;;

                c)
                        CUT=true
                        ;;
                s)
                        SIZE="$OPTARG"
                        ;;
                a)
                        AXIS="$OPTARG"
                        ;;
                d)
                        DIRECTION="$OPTARG"
                        ;;
                m)  
                        MASK=true
                        MASK_FILE="$OPTARG"
                        ;;
        esac
done


if $MASK; then
        NAME=($(echo $MASK_FILE | tr "." "\n"))
        PREFIX=${NAME[0]}
        echo $PREFIX
        SUFFIX=_mask.nii.gz
        MASK_NAME=$PREFIX$SUFFIX
        echo $MASK_FILE 
        echo $MASK_NAME
        fslmaths $MASK_FILE -thr 10 -bin $MASK_NAME

else
        NAME=$((echo $IMAGE_NAME | tr "." "\n"))
        PREFIX=${NAME[0]}
        SUFFIX=_mask.nii.gz
        MASK_NAME=$PREFIX$SUFFIX
        fslmaths $IMAGE_NAME -thr 10 -bin $MASK_NAME
fi

echo mask created

NAME_M=($(echo $MASK_NAME | tr "." "\n"))
PREFIX_M=${NAME_M[0]}
SUFFIX_M=_smoothed.nii.gz
SMOOTHED_MASK=$PREFIX_M$SUFFIX_M

echo $MASK_NAME
echo $SMOOTHED_MASK

#smooth one mask 
SmoothImage 3 $MASK_NAME 6 $SMOOTHED_MASK

#make mesh using marching cube. 
echo mask smoothed

if $CUT; then
        NAME_C=$((echo $IMAGE_NAME | tr "." "\n"))
        PREFIX_C=${NAME_C[0]}
        SUFFIX_c="_cut.nii.gz"
        OUTPUTFILE=$PREFIX_C$SUFFIX_C
        echo $OUTPUTFILE
        if $BOUNDARY; then
                python -c "import make_mesh; make_mesh.cut_img_mas(\"$IMAGE_NAME\",\"$OUTPUTFILE\",$SIZE,$AXIS,$DIRECTION,\"$MASK_NAME\")"
                IMAGE_NAME=$OUTPUTFILE
        else
                        python -c "import make_mesh; make_mesh.cut_img_mas(\"$IMAGE_NAME\",\"$OUTPUTFILE\",$SIZE,$AXIS,$DIRECTION)"
                IMAGE_NAME=$OUTPUTFILE
        fi
        echo Image cut
        

fi
python make_mesh.py -i $IMAGE_NAME -m $SMOOTHED_MASK -t $TRESHHOLD

echo mesh created
#cleanUP
