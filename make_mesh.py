import sys
from glob import glob
import skimage
from skimage import measure
import nibabel
import numpy
import os

path = os.path.abspath('.')
file = path + '/ambmc2dsurqec_15micron_masked.nii.gz'

#Load nifti
img= nibabel.load(file)
img_data = img.get_fdata()

#Extract affine transformation to use on vertices
affine = img.affine
M = affine[:3, :3]
abc = affine[:3, 3]

def f(i, j, k):
   """ Return X, Y, Z coordinates for i, j, k """
   return M.dot([i, j, k]) + abc

#Create Mesh
##Figure out automatic treshhold or parameterize
verts, faces, normals, values = measure.marching_cubes_lewiner(img_data)

thefile = open(path + '/ambmc2dsurqec_15micron_masked.obj','w')

for item in verts:
	transformed = f(item[0],item[1],item[2])
	thefile.write("v {0} {1} {2}\n".format(transformed[0],transformed[1],transformed[2]))

for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()

#This seems only necessary for SurfIce/Blender, but does not work with for example mayavi
faces=faces +1


thefile = open(path + '/ambmc2dsurqec_15micron_masked_SurfIce.obj','w')
for item in verts:
	transformed = f(item[0],item[1],item[2])
	thefile.write("v {0} {1} {2}\n".format(transformed[0],transformed[1],transformed[2]))

for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()

