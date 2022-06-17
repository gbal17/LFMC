''' 
This program does the following:
1) determines the day of the year
2) open reference MODIS file in '~/Documents/ISA/LFMC/data': MCD43A4_006_NDVI_20220525.tif
   and get resolution
3) Upsample according to reference file the following files in '~/Documents/ISA/LFMC/data/YYYY/mm': 
   3.1) 'e'    Evaporation:    ECMWF_e_yyyymmdd_mean     to became ---> ECMWF_e_yyyymmdd_mean_wrap
   3.2) 'swvl' Soil Moisture:  ECMWF_swvl_yyyymmdd_mean  to became ---> ECMWF_swvl_yyyymmdd_mean_wrap
and save temporarily in the directory '~/Documents/ISA/LFMC/data'
'''

#############
# Libraries # ------------------------------------
#############

from osgeo import gdal
import os

########
# MAIN # ------------------------------------
########

main_folder='/Users/gb/Documents/ISA/LFMC/';
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
referenceFile = os.path.join(main_folder+'data/', 'MCD43A4_006_NDVI_20220525.tif')
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
inputFile = os.path.join(main_folder+'data/'+year+'/'+month, file_name)
outputFile = os.path.join(main_folder+'data/', file_name1)
# call gdal Warp
kwargs = {"format": "GTiff", "xRes": x_res, "yRes": y_res}
ds = gdal.Warp(outputFile, inputFile, **kwargs)

# 3.2) Soil Moisture (SWVL)
variable = 'swvl'
file_name = dataset+'_'+variable+'_'+today+'_mean.tif'
file_name1 = dataset+'_'+variable+'_'+today+'_mean_wrap.tif'
inputFile = os.path.join(main_folder+'data/'+year+'/'+month, file_name)
outputFile = os.path.join(main_folder+'data/', file_name1)
# call gdal Warp
kwargs = {"format": "GTiff", "xRes": x_res, "yRes": y_res}
ds = gdal.Warp(outputFile, inputFile, **kwargs)