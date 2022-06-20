''' 
This program does the following:
1) Load the dataset MCD43A4_006_NDVI: MODIS Combined 16-Day NDVI from EarthEngine Catalog:
   https://developers.google.com/earth-engine/datasets/catalog/MODIS_MCD43A4_006_NDVI?hl=en
2) Get the last available image and print the date
3) Filters for 
   - Region of Interest (roi): Portugal shape file in Earth Engine asset ("users/baldassarre/1_PyroPas/Portugal")
   - The last available date 
   Mosaics over roi
4) Export the derived image in the folder '~/Documents/ISA/LFMC_maps/data'
'''

#############
# Libraries # ------------------------------------
#############

import ee
import os
import geemap

# Initialize the Earth Engine module.
ee.Initialize()


########
# MAIN # ------------------------------------
########

# MODIS NDVI from Earth Engine catalog 
# 16-days T-A: MCD43A4_006_NDVI (https://developers.google.com/earth-engine/datasets/catalog/MODIS_MCD43A4_006_NDVI?hl=en)
# 4-days  T  : MOD09GA_006_NDVI (https://developers.google.com/earth-engine/datasets/catalog/MODIS_MOD09GA_006_NDVI?hl=en)
# 4-days  A  : MYD09GA_006_NDVI (https://developers.google.com/earth-engine/datasets/catalog/MODIS_MYD09GA_006_NDVI?hl=en)

# ------------------------------------
# 1) Select and Load the dataset
ProductName = 'MCD43A4_006_NDVI';  
product = ee.ImageCollection('MODIS/'+ProductName)

# ------------------------------------
# 2) Get the last available image and print the date

# get dataset time range
range = product.reduceColumns(ee.Reducer.minMax(), ["system:time_start"])
# last available image and print the date
day_less = 0
date= ee.Date(range.get('max')).advance(day_less,"day");
today = date.format().getInfo()
today = (today[0:4]+today[5:7]+today[8:10])
print(today)

# ------------------------------------
# 3) Filters for ROI and Last date:

# Country as geometry use Mosaic
roi = ee.FeatureCollection("users/baldassarre/1_PyroPas/Portugal").geometry()
# Filter.date - Filter.bounds - Mosaic
dataset = product.filter(ee.Filter.date(date)).filter(ee.Filter.bounds(roi)).mosaic()

# ------------------------------------
# 4) Export DATASET in the folder '~/Documents/ISA/LFMC/data'
out_dir = os.path.join(os.path.expanduser('~'), 'Documents/ISA/LFMC_maps/data')
filename = os.path.join(out_dir, ProductName+'_'+today+'.tif')
geemap.ee_export_image(dataset, filename=filename, scale=500, region=roi, file_per_band=False)