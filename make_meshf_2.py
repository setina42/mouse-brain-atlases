import sys
from glob import glob
import skimage
from skimage import measure
import nibabel
import numpy
import os
from math import floor
from skimage.exposure import rescale_intensity
import matplotlib.pyplot as plt


path = os.path.abspath('.')
#file = path + '/ambmc2dsurqec_15micron_masked.nii.gz'
file = path + '/ambmc2dsurqec_15micron_masked.nii.gz'


#Load nifti
img= nibabel.load(file)
img_data = img.get_fdata()
origin = numpy.copy(img_data)
new_header=img.header.copy()
new_header=img.header.copy()
new_header=img.header.copy()

print("main file loaded")
img2=nibabel.load("eroded_python_10iteration.nii.gz")
mask = img2.get_fdata()
print("mask loaded")
img3=nibabel.load("eroded_python_6iteration_smooth10.nii.gz")
mask_smoothed = img3.get_fdata()

print("smoothed mask loaded")
#In order to not distort size, take only smoothed values that lie wihtin the boundary of the bigger mask. Leave that step out maybe as well and also consider mask made with FSL
mask[numpy.nonzero(mask)] = mask_smoothed[numpy.nonzero(mask)]

#print(numpy.mean(mask[numpy.nonzero(mask)]))

x1,y1,z1 = numpy.shape(img_data)
x = floor(x1*0.5)
y=floor(y1*0.5)
z=floor(z1*0.5)

print("the unchanged data matrix is")

print(img_data[:,y,z])

x_axis = numpy.arange(x1)

iso = 0.5 * (numpy.max(img_data) + numpy.min(img_data))


plt.plot(x_axis, img_data[:,y,z])
fig = plt.gcf()
fig.savefig("plot_f_1")



#fig = plt.gcf()
#fig.savefig("plot_239_mask_smoothed_3")

print("mask smoothed printed")


#i
#
#
#mask=numpy.multiply(img_data2,2674614)
#print(mask.shape)

mean_value= numpy.mean(img_data[numpy.nonzero(img_data)])
mean_value=floor(mean_value) 


print("mean value calculated")

#Fill in the holes within the nboundary of the eroded mask
img_data[(img_data > 0) & (mask == 1)] = mean_value

#Extract an overall surface value
surface_mean_value = numpy.mean(img_data[(img_data !=0) & (img_data != mean_value)])

print(surface_mean_value)      
print("mean value applied")

#img_data[(img_data > 0) & (mask ==1)] = numpy.multiply(surface_mean_value,numpy.random.uniform(low=0.8,high=1.2,size=numpy.shape(img_data[(img_data > 0) & (mask ==1)])))
#Now take the smoothed mask and multiply the values:
#print("randomized internal")
#print(img_data[(img_data > 0) & (mask ==1)])
##Bring smoothed mask to useful values betweeen 0.8 and 1.2

#determine range and stepsize for mapping values 

#it_tresh = 30

#mi = numpy.min(mask[(mask != 0) & (mask < 1)])
#ma = numpy.max(mask[(mask != 0) & (mask < 1)])

#range = float(ma) / float(mi)

#bound = 1.2 -0.8

#stepsize_tresh = float(bound) / float(it_tresh)
#stepsize_min = float(range) / float(it_tresh)





#min = numpy.min(mask[numpy.nonzero(mask)])
#tresh = 0.9     
#while (min < 0.9):
#   mask[(mask < (min*1.2)) & (mask != 0)] = tresh
#   print("tresh = ")
#   print(tresh)
#   print("min=")
#   print(min)
#   tresh = tresh + stepsize_tresh
#   min = numpy.min(mask[numpy.nonzero(mask)])

#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.000000000000001)] = 0.8
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.0000000000001)] = 0.82
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.00000000001)] = 0.84
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.000000001)] = 0.86
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.0000001)] = 0.88
#print("mask is a third way treshholded")
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.00001)] = 0.9
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.001)] = 0.92
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.01)] = 0.94
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.1)] = 0.96
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.25)] = 0.97
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.35)] = 0.98
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.45)] = 0.985
#print("mask is amost finished treshholded")
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.55)] = 0.99
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.65)] = 0.995
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.75)] = 0.999
#mask_smoothed[(mask_smoothed > 0) & (mask_smoothed < 0.8)] = 1



##Scale mask as to have smooth treshhold on both sides.

mask_min = numpy.min(mask[numpy.nonzero(mask)])

#Extract min from all values
mask[numpy.nonzero(mask)] = numpy.subtract(mask[numpy.nonzero(mask)],mask_min)

mask_min = numpy.min(mask[numpy.nonzero(mask)])

#Extract min from all values
mask[numpy.nonzero(mask)] = numpy.subtract(mask[numpy.nonzero(mask)],mask_min)


#value to be applied 

#take the max outer value
maxx = numpy.max(img_data[(mask == 0)])

substitute_value = float(mean_value) / float(numpy.max(mask))


print("mean value and substitte value")
print(mask[:,y,z])


#mask_nifti=nibabel.Nifti1Image(mask_smoothed,None,header=new_header)
#mask_nifti=nibabel.Nifit1Image(mask_eroded, img.affine)
#nibabel.save(mask_nifti,"wökli.nii.gz")

print("File saved")
#print("the smoothed mask is now:")
#print(mask_smoothed[:,y,z])

#print("randomize internal values")
#mask_smoothed[(mask_smoothed ==1)] = numpy.multiply(mask_smoothed[(mask_smoothed ==1)],numpy.random.uniform(low=0.8,high=1.2,size=numpy.shape(mask_smoothed[(mask_smoothed ==1)])))
#print(mask_smoothed[:,y,z])


a = numpy.multiply(mask,substitute_value)

plt.plot(x_axis, a[:,y,z])
fig.savefig("plot_f_2")







img_data[numpy.nonzero(mask)]=numpy.multiply(mask[numpy.nonzero(mask)],substitute_value)

print("the data matrix now")

#This is a safety step. Ideally, the mask should be chosen so that this issue diappears, but due to the stoachstic nature of the registration (and eroding???) This might be problematic as to having some high valus between the internal smooht mask and the surface values. Thos lead to an artiafact of a second, internal mehs
#img_data[(img_data > surface_mean_value)] = numpy.multiply(img_data[(img_data > surface_mean_value)],0.6)

#img_data[(mask == 0) & (img_data > 0)] =  rescale_intensity(img_data[(mask == 0) & (img_data > 0)] , in_range=(212406,maxx))
print("after scale intensity")

#rint(img_data[:,y,z])

#plt.legend(['unchanged data matrix', 'scaled mask', 'changed data matrix'], loc='upper left')



fin = numpy.fmax(img_data,origin)

print("origin")
print(origin[:,y,z])

print("img_data")
print(img_data[:,y,z])


print("fin")
print(fin[:,y,z])



plt.clf()


plt.plot(x_axis,origin[:,y,z])
plt.plot(x_axis,img_data[:,y,z])
plt.plot(x_axis,fin[:,y,z])



#plt.legend(['unchanged data matrix', 'scaled mask', 'changed data matrix'], loc='upper left')
fig = plt.gcf()
fig.savefig("plot_checkfmax_new")


print("masking done")
#it = numpy.nditer(mask,flags=['multi_index'])
#while not it.finished:
#   if it[0] != 0:
#      img_data[it.multi_index]=0
#   it.iternext()

#new=numpy.add(img_data,mask)
#nibabel.save(new,"new.nii.gz")
#Extract affine transformation to use on vertices
affine = img.affine
M = affine[:3, :3]
abc = affine[:3, 3]

def f(i, j, k):
   """ Return X, Y, Z coordinates for i, j, k """
   return M.dot([i, j, k]) + abc

#Create Mesh
##Figure out automatic treshhold or parameterize
verts, faces, normals, values = measure.marching_cubes_lewiner(fin)
print("Marching Cube done")
#This seems only necessary for SurfIce/Blender, but does not work with for example mayavi
faces=faces +1


thefile = open(path + '/ambmc2dsurqec_f_2_godplease.obj','w')
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

