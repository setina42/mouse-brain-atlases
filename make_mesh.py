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

#Load nifti
img= nibabel.load(file)
img_data = img.get_fdata()
img2=nibabel.load("ambmc2dsurqec_internalmask.nii.gz")
mask = img2.get_fdata()

#To ensure marching cube algorithm does not extract inner surface, replace all inner structures with 
#uniform mean value
mean_value= numpy.mean(img_data[numpy.nonzero(img_data)])
mean_value=floor(mean_value)
img_data[numpy.nonzero(mask)]=mean_value

print("masking done")

#Conserve the affine information in the mesh
affine = img.affine
M = affine[:3, :3]
abc = affine[:3, 3]

def f(i, j, k):
   """ Return X, Y, Z coordinates for i, j, k """
   return M.dot([i, j, k]) + abc

#Create Mesh
verts, faces, normals, values = measure.marching_cubes_lewiner(img_data)
print("Marching Cube done")

#Write .obj file
thefile = open(path + '/ambmc2dsurqec_15micron_surfacemesh_0.obj','w')
for item in verts:
	transformed = f(item[0],item[1],item[2])
	thefile.write("v {0} {1} {2}\n".format(transformed[0],transformed[1],transformed[2]))
print("Meshfile 1 written 30%")
for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
print("Meshfile 1 written 60%")
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()



#Necessary for use of meshfile with SurfIce/Blender. Marching cube outputs  verts starting from 0, while other software consider verts starting at 1. 
faces=faces +1


thefile = open(path + '/ambmc2dsurqec_15micron_surfacemesh_1.obj','w')
for item in verts:
	transformed = f(item[0],item[1],item[2])
	thefile.write("v {0} {1} {2}\n".format(transformed[0],transformed[1],transformed[2]))
print("Meshfile 2 written 30%")
for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
print("Meshfile 2 written 60%")
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()

