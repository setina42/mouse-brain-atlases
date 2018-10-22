import sys
from glob import glob
import skimage
from skimage import measure
import nibabel
import numpy
import os
from math import floor
import scipy
from subprocess import call
import argparse
#
def remove_inner_surface(img_data,mask,mask_smoothed,percentile=50):
	"""
	Function to replace inner data of the given volume with a smoothed, uniform masking to avoid generation of inner surface structures and staircase artifacts when using marching cube algorithm
	
	Input:
	img_data :input volume data to extract mesh from
	mask : inner internal mask acting as size boundary to smoothed mask
	mask_smoothed : smoothed internal mask
	percentile : determines values to be filled inside
	
	Returns:
	fin : manipulated data matrix to be used for marching cube
	iso_surface : corresponding iso surface value to use for marching cube
	"""
	#Keep original array
	origin = numpy.copy(img_data)

	#In order to not distort size, take only smoothed values that lie wihtin the boundary of the bigger mask. 
	mask[numpy.nonzero(mask)] = mask_smoothed[numpy.nonzero(mask)]
	
	#Determine inner replacement value
	percentile_value= numpy.percentile(img_data[numpy.nonzero(img_data)],percentile)
	percentile_value=floor(percentile_value)

	#Fill in the holes within the boundary of the eroded mask
	img_data[(img_data > 0) & (mask == 1)] = percentile_value
	print("percentile_value")
	print(percentile_value)
	
	#Scale mask as to have smooth treshhold on both sides.
	mask_min = numpy.min(mask[numpy.nonzero(mask)])
	mask[numpy.nonzero(mask)] = numpy.subtract(mask[numpy.nonzero(mask)],mask_min)
	mask_min = numpy.min(mask[numpy.nonzero(mask)])
	mask[numpy.nonzero(mask)] = numpy.subtract(mask[numpy.nonzero(mask)],mask_min)

	#To create a smooth inner data matrix that has the overall mean value as max value, calculate value needed to multiply with mask
	substitute_value = float(percentile_value) / float(numpy.max(mask))
	
	#Replace all inner values of the original data matrix with the smoothed mask multiplied by substitute
	img_data[numpy.nonzero(mask)]=numpy.multiply(mask[numpy.nonzero(mask)],substitute_value)

	#Choose the isosurface value slightly below the substitute value. This will ensure a singular mesh.
	iso_surface = float(percentile_value) / float(1.05)
	
	#The final data matrix consists of the maximum values in either the smoothed mask or the original. This ensures that either the original data will be taken or, in case
	#where the original data matrix will have too low intensities for marching cube to detect (i.e creating wholes in the mesh), the smoothed mask will be taken. 
	fin = numpy.fmax(img_data,origin)
	return(fin,iso_surface);



#Returns affine transformed coordinates (i,j,k) -> (x,y,z) Use to set correct coordinates and size for the mesh
def f(i, j, k, affine):
	M = affine[:3, :3]
	abc = affine[:3, 3]
	return M.dot([i, j, k]) + abc



#Writes an .obj file for the output of marching cube algorithm. Specify affine if needed in mesh. One = True for faces indexing starting at 1 as opposed to 0. Necessary for Blender/SurfIce
def write_obj(name,verts,faces,normals,values,affine=None,one=False):
	if (one) : faces=faces+1
	thefile = open(name,'w')
	if affine is not None:
		for item in verts:
			transformed = f(item[0],item[1],item[2],affine)
			thefile.write("v {0} {1} {2}\n".format(transformed[0],transformed[1],transformed[2]))
	else :
		for item in verts:
			thefile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
	print("File 1 written 30%")
	for item in normals:
		thefile.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
	print("File 2 written 60%")
	for item in faces:
		thefile.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(item[0],item[1],item[2]))
	thefile.close()

def main():

	parser = argparse.ArgumentParser(description="Create surface mesh form nifti-volume",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--file_prefix','-f',default='Mesh', type=str)
	parser.add_argument('--percentile','-p',default=50,type=int)
	args = parser.parse_args()

	path = os.path.abspath('.')
	path = path + '/'
	
	#Load necessary niftifiles: data volume, internal mask, intenal smoothed mask
	img= nibabel.load(path + 'ambmc2dsurqec_15micron_masked.nii.gz')
	img_data = img.get_fdata()
	origin = numpy.copy(img_data)

	img2=nibabel.load(path + "ambmc2dsurqec_mask_eroded10.nii.gz")
	mask = img2.get_fdata()

	img3=nibabel.load(path + "ambmc2dsurqec_mask_eroded6_smoothed.nii.gz")
	mask_smoothed = img3.get_fdata()

	#Replace inner values and run marching cube
	img_data,iso_surface = remove_inner_surface(img_data,mask,mask_smoothed,args.percentile)
	verts, faces, normals, values = measure.marching_cubes_lewiner(img_data,iso_surface)

	write_obj(str.join((path,args.file_prefix,"_1.obj")),verts,faces,normals,values,affine = img.affine,one=True)
	write_obj(str.join((path,"ambmc2dsurqec_15_micron_mesh_0.obj")),verts,faces,normals,values,affine = img.affine,one=False)


main()
