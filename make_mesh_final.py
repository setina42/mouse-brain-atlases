import sys
from glob import glob
import skimage
from skimage import measure
import nibabel
import numpy
import os
from math import floor

path = os.path.abspath('.')
file = path + '/ambmc2dsurqec_15micron_masked.nii.gz'


#This scipt generates a surface mesh form nifit volume data using skimage's marching cube algorithm (isosurface extraction). Isosurface extraction can be tricky. If 0 as hard value is used as iso-surface, there will be staircase artifacts. If any other value is used, there will be many inner structures generated by marching cube due to similar intensity values in the inside of the brain.

#To avoid generating inner strucures and still getting a smooth mesh, a smoothing mask is used to replace all inner values below a chosen treshhold and create a smooth interior where values are to small.
#Then an overall mean value is chosen as isosurface-

#Create inner masks : One as size boundary and one that will be heavily smoothed.
path = os.path.abspath('.')
file = path + '/mask.nii.gz'

#Load nifti
img= nibabel.load(file)
mask = img.get_fdata()
new_header=img.header.copy()


mask_eroded = scipy.ndimage.morphology.binary_erosion(mask,iterations=10)
mask_nifti=nibabel.Nifti1Image(mask_eroded,None,header=new_header)
#mask_nifti=nibabel.Nifit1Image(mask_eroded, img.affine)
nibabel.save(mask_nifti,"eroded_python_10iteration.nii.gz")

mask_eroded = scipy.ndimage.morphology.binary_erosion(mask,iterations=12)
mask_nifti=nibabel.Nifti1Image(mask_eroded,None,header=new_header)
#mask_nifti=nibabel.Nifit1Image(mask_eroded, img.affine)
nibabel.save(mask_nifti,"eroded_python_12iteration.nii.gz")


#Load nifti-files: Original volume data as well as hard inner mask and smoothed inner mask
img= nibabel.load(file)
img_data = img.get_fdata()
origin = numpy.copy(img_data)

img2=nibabel.load("eroded_python_10iteration.nii.gz")
mask = img2.get_fdata()

img3=nibabel.load("eroded_python_6iteration_smooth10.nii.gz")
mask_smoothed = img3.get_fdata()

#In order to not distort size, take only smoothed values that lie wihtin the boundary of the bigger mask. Leave that step out maybe as well and also consider mask made with FSL
mask[numpy.nonzero(mask)] = mask_smoothed[numpy.nonzero(mask)]

mean_value= numpy.mean(img_data[numpy.nonzero(img_data)])
mean_value=floor(mean_value) 

#Fill in the holes within the nboundary of the eroded mask
img_data[(img_data > 0) & (mask == 1)] = mean_value


##Scale mask as to have smooth treshhold on both sides.

mask_min = numpy.min(mask[numpy.nonzero(mask)])

#Extract min from all values
mask[numpy.nonzero(mask)] = numpy.subtract(mask[numpy.nonzero(mask)],mask_min)

mask_min = numpy.min(mask[numpy.nonzero(mask)])

#Extract min from all values
mask[numpy.nonzero(mask)] = numpy.subtract(mask[numpy.nonzero(mask)],mask_min)


#To create a smooth inner data matrix that has the overall mean value as max value, calculate value needed to multiply with mask
substitute_value = float(mean_value) / float(numpy.max(mask))




img_data[numpy.nonzero(mask)]=numpy.multiply(mask[numpy.nonzero(mask)],substitute_value)

fin = numpy.fmax(img_data,origin)

#Extract affine transformation to use on vertices
affine = img.affine
M = affine[:3, :3]
abc = affine[:3, 3]

def f(i, j, k):
   """ Return X, Y, Z coordinates for i, j, k """
   return M.dot([i, j, k]) + abc

#Create Mesh
verts, faces, normals, values = measure.marching_cubes_lewiner(fin)
print("Marching Cube done")



thefile = open(path + '/ambmc2dsurqec_15micron_mesh_0.obj','w')
for item in verts:
	transformed = f(item[0],item[1],item[2])
	thefile.write("v {0} {1} {2}\n".format(transformed[0],transformed[1],transformed[2]))
print("File written 30%")
for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
print("File written 60%")
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()




#Necessary step for compatibility with Blender/SurfIce. marching Cube outputs faces starting at 0, while Blender/SurfIce consider them to start at 1.
faces=faces +1


thefile = open(path + '/ambmc2dsurqec_15micron_mesh_1.obj','w')
for item in verts:
	transformed = f(item[0],item[1],item[2])
	thefile.write("v {0} {1} {2}\n".format(transformed[0],transformed[1],transformed[2]))
print("File written 30%")
for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
print("File written 60%")
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()
