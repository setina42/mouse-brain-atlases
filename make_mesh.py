import sys
from glob import glob
import skimage
from skimage import measure
import nibabel
import numpy
import os
from math import floor
import scipy
import argparse
#
def remove_inner_surface(img_data,mask,treshhold=0):
	"""
	Function to replace inner data of the given volume with a smoothed, uniform masking to avoid generation of inner surface structures and staircase artifacts when using marching cube algorithm
	
	Input:
	img_data :input volume data to extract mesh from, numpy-array
	mask : smoothed internal mask, numpy-array
	treshhold : determines isosurface and values for the inner mask
	
	Returns:
	fin : manipulated data matrix to be used for marching cube
	iso_surface : corresponding iso surface value to use for marching cube
	"""
	x,y,z = numpy.shape(img_data)
	x = floor(0.5* x)
	y = floor(0.5*y)
	z = floor(0.5*z)

	#Keep original array
	origin = numpy.copy(img_data)

	
	#Fill in the holes within the boundary of the eroded mask
	img_data[(img_data > 0) & (mask == 1)] = treshhold
	
	#To create a smooth inner data matrix that has the overall mean value as max value, calculate value needed to multiply with mask
	substitute_value = float(treshhold) / float(numpy.max(mask))

	#Replace all inner values of the original data matrix with the smoothed mask multiplied by substitute
	img_data[numpy.nonzero(mask)]=numpy.multiply(mask[numpy.nonzero(mask)],substitute_value)

	#Choose the isosurface value slightly below the substitute value. This will ensure a singular mesh and a smooth surface in case mask is visible.
	iso_surface = float(treshhold) / float(1.05)
	
	#The final data matrix consists of the maximum values in either the smoothed mask or the original. This ensures that either the original data will be taken or, in case
	#where the original data matrix will have too low intensities for marching cube to detect (i.e creating wholes in the mesh), the smoothed mask will be taken,resulting in smooth surface
	
	fin = numpy.copy(img_data)
	fin[numpy.nonzero(img_data)] = numpy.fmax(img_data[numpy.nonzero(img_data)],origin[numpy.nonzero(img_data)])
	print(img_data[:,y,z])
	return(fin,iso_surface);

#Either take boundary from supplied mask or if not specified, from image directly
def cut_img_mas(file_input,file_output,size,axis,direction,mask = None):
	"""
	Function to trim data matrix before mesh creation. Reads in nifti file and saves the trimmed image as nifti file.

	Input:
	file_input:file name of image to be loaded and cut (nifti format)
	file_output: output file name
	size : number of voxels to trim
	axis : axis along which to trim (0,1,2)
	direction : either trim form beginning af axis inwards or from end of axis inwards
	mask : optional. If given, boundary of image will be determined from the mask. Needed if image has boundary with non-zero entries
	"""

	path = os.path.abspath('.')
	path = path + '/'
	img= nibabel.load(path+file_input)
	img_data = img.get_fdata()
	header=img.header.copy()
	if (mask != None):
		mask= nibabel.load(mask)
		mask_data = mask.get_fdata()
		box = get_bounding_slices(mask_data)
	else:
		box = get_bounding_slices(img_data)
	img_data = cut_img(img_data,box,size,axis,direction)
	img_nifti=nibabel.Nifti1Image(img_data,None,header=header)
	nibabel.save(img_nifti,file_output)
	return

#Define the boundin:g box of the data matrix. 
def get_bounding_slices(img):
	"""
	Function to determine the boundaries of the given image. Returns range of indices through the matrix that contain non-zero entries alon each axis
	"""

	dims = numpy.shape(img)
	mask = img == 0
	bbox = []
	all_axis = numpy.arange(img.ndim)
	for kdim in all_axis:
		nk_dim = numpy.delete(all_axis, kdim)
		mask_i = mask.all(axis=tuple(nk_dim))
		dmask_i = numpy.diff(mask_i)
		idx_i = numpy.nonzero(dmask_i)[0]
		if len(idx_i) != 2:
			#TODO: see if one boundary has been found, and check that)
			print("No clear boundary found (no zero entries?) in dimension" + kdim)
			print("Boundary of data matrix is returned instead")
			idx_i = [0, dims[kdim]-2]
		bbox.append([idx_i[0]+1, idx_i[1]+1])
	return bbox

# Trim image along specified axis, size input = voxel
def cut_img(img,bbox,size,axis,direction):
	"""
	Function to trim an image data matrix.

	Input:
	img: Image,numpy array
	bbox: Integer values for each axis that specify bounding box of image
	size: number of voxels to trim
	axis: axis along which to trim (0,1,2)
	direction: either trim form beginning af axis inwards or from end of axis inwards

	returns:
	img trimmed data matrix 
	"""

	dims = numpy.shape(img)
	ind = bbox[axis-1]
	if (direction == 0):
		new_ind = ind[0] + size
		slc = [slice(None)] * len(img.shape)
		slc[axis] = slice(0,new_ind)
	elif (direction == 1):
		new_ind = ind[1] - size
		slc = [slice(None)] * len(img.shape)
		slc[axis] = slice(new_ind,dims[axis])
	img[tuple(slc)] = 0
	return img

def f(i, j, k, affine):
	"""
	Returns affine transformed coordinates (i,j,k) -> (x,y,z) Use to set correct coordinates and size for the mesh
	
	"""

	M = affine[:3, :3]
	abc = affine[:3, 3]
	return M.dot([i, j, k]) + abc

#Writes an .obj file for the output of marching cube algorithm. Specify affine if needed in mesh. One = True for faces indexing starting at 1 as opposed to 0. Necessary for Blender/SurfIce
def write_obj(name,verts,faces,normals,values,affine=None,one=False):
	"""
	Write a .obj file for the output of marching cube algorithm

	input:
	name,verts,faces,normals: output of marching cube algoritgm
	affine: optional, if specified, vertices coordinates are affine transformed to create mesh with correct origin and size
	one : Specify if faces values should start at 1 or at 0. Different programs use different conventions.
	"""
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
	parser.add_argument('--treshhold','-t',default=0,type=float)
	parser.add_argument('--image_name','-i',type=str)
	parser.add_argument('--mask_name','-m',type=str)
	parser.add_argument('--cut', '-c',type=int,nargs = '*')
	args = parser.parse_args()

	path = os.path.abspath('.')
	path = path + '/'
	
	#Load necessary niftifiles: data volume, internal mask, intenal smoothed mask
	img= nibabel.load(path + args.image_name)
	img_data = img.get_fdata()

	img2=nibabel.load(path + args.mask_name)
	mask = img2.get_fdata()

	#Replace inner values and run marching cube
	img_data,iso_surface = remove_inner_surface(img_data,mask,args.treshhold)
	verts, faces, normals, values = measure.marching_cubes_lewiner(img_data,iso_surface)

	#save mesh as .obj
	write_obj((path + (args.image_name).split(".")[0] + "_mesh_1.obj"),verts,faces,normals,values,affine = img.affine,one=True)
	write_obj((path + (args.image_name).split(".")[0] + "_mesh_0.obj"),verts,faces,normals,values,affine = img.affine,one=False)

if __name__ == '__main__': main()
