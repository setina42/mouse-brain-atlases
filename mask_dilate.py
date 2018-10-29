import sys
from glob import glob
import skimage
from skimage import measure
import nibabel
import numpy
import os
import scipy

path = os.path.abspath('.')
file = path + '/ambmc2dsurqec_mask.nii.gz'

#Load nifti
img= nibabel.load(file)
mask = img.get_fdata()
new_header=img.header.copy()

#Create two internal masks of different size from the original and save as nifti
mask_eroded = scipy.ndimage.morphology.binary_erosion(mask,iterations=10)
mask_nifti=nibabel.Nifti1Image(mask_eroded,None,header=new_header)
nibabel.save(mask_nifti,"ambmc2dsurqec_mask_eroded10.nii.gz")

mask_eroded = scipy.ndimage.morphology.binary_erosion(mask,iterations=6)
mask_nifti=nibabel.Nifti1Image(mask_eroded,None,header=new_header)
nibabel.save(mask_nifti,"ambmc2dsurqec_mask_eroded6.nii.gz")

