''' 
This program does the following:
1) determines the day of the year
2) open the 1st available MODIS NDVI in "dir_data" to use as a reference
   and get resolution
3) Upsample according to reference file the following files in "dir_data"+'/YYYY/mm': 
   3.1) 'e'    Evaporation:    ECMWF_e_yyyymmdd_mean     to became ---> ECMWF_e_yyyymmdd_mean_wrap
   3.2) 'swvl' Soil Moisture:  ECMWF_swvl_yyyymmdd_mean  to became ---> ECMWF_swvl_yyyymmdd_mean_wrap
and save temporarily in the directory "dir_data"
'''

#############
# Libraries # ------------------------------------
#############

from osgeo import gdal
import os
import glob

from dirs import dir_data

########
# MAIN # ------------------------------------
########

dataset = 'ECMWF'

# ------------------------------------
# 1) determines the day of the year 

from datetime import datetime
now = datetime.now() # current date and time
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
# day = str(int(now.strftime("%d"))-1) 
today = year+month+day

# 2) open reference file and get resolution
# get the first MODIS NDVI in the data folder as reference
fileNDVI = glob.glob(os.path.join(dir_data,'*NDVI*'))
referenceFile = fileNDVI[0];
reference = gdal.Open(referenceFile, 0)  # this opens the file in only reading mode
referenceTrans = reference.GetGeoTransform()
print(referenceTrans)
x_res = referenceTrans[1]
y_res = -referenceTrans[5]  # make sure this value is positive
print(x_res)
print(referenceTrans[5])

# 3) Upsample according to reference file
# specify input and output filenames

# 3.1) EVAPORATION
variable = 'e'
file_name = dataset+'_'+variable+'_'+today+'_mean.tif'
file_name1 = dataset+'_'+variable+'_'+today+'_mean_wrap.tif'
inputFile = os.path.join(dir_data+year+'/'+month, file_name)
outputFile = os.path.join(dir_data, file_name1)
# call gdal Warp
kwargs = {"format": "GTiff", "xRes": x_res, "yRes": y_res}
ds = gdal.Warp(outputFile, inputFile, **kwargs)

# 3.2) Soil Moisture (SWVL)
variable = 'swvl'
file_name = dataset+'_'+variable+'_'+today+'_mean.tif'
file_name1 = dataset+'_'+variable+'_'+today+'_mean_wrap.tif'
inputFile = os.path.join(dir_data+year+'/'+month, file_name)
outputFile = os.path.join(dir_data, file_name1)
# call gdal Warp
kwargs = {"format": "GTiff", "xRes": x_res, "yRes": y_res}
ds = gdal.Warp(outputFile, inputFile, **kwargs)