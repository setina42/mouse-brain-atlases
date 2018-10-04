import sys
from glob import glob
import skimage
from skimage import measure
import vtk
import nibabel
import numpy

path = os.path.abspath('.')
file = glob(path + 'ambmc2dsurqec_15micron_masked.nii*')

#Load nifti
img= nibabel.load(file)
img_data = img.get_fdata()

#Create Mesh
verts, faces, normals, values = measure.marching_cubes_lewiner(img_data)

thefile = open(glob(path + 'ambmc2dsurqec_15micron_masked.obj')
		)
for item in verts:
	thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()

#This seems only necessary for SurfIce, but does not work with for example mayavi
faces=faces +1

#Stolen form stackoverflow :) https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python
thefile = open(glob(path + 'ambmc2dsurqec_15micron_masked_SurfIce.obj')
		)
for item in verts:
	thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()

