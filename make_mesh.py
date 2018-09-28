import sys
from glob import import glob
import skimage
from skimage import import measure
import vtk
import nibabel
import numpy


#Load nifti
img= nibabel.load("C:\\Users\\tinas\\Desktop\\Sync\\Rec\\abi_50_average.nii.gz")
img_data = img.get_fdata()


#img_data[img_data>5] = 20;
            

#Create Mesh  TODO: How to select a good value for the isosurface?? 10 yields more or less good results, but unsafe
verts, faces, normals, values = measure.marching_cubes_lewiner(img_data,10)
faces=faces +1

#Stolen form stackoverflow :) https://stackoverflow.com/questions/48844778/create-a-obj-file-from-3d-array-in-python
thefile = open("C:\\Users\\tinas\\Desktop\\Sync\\Rec\\test.obj", 'w')
for item in verts:
	thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in normals:
	thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
for item in faces:
	thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))  
thefile.close()

