''' 
This program does the following:
1) determines the day of the year
2) Does the Co-Registration according to reference MODIS file in '~/Documents/ISA/LFMC_maps/data': MCD43A4_006_NDVI_20220525.tif
   for the following files generated in the previous script in '~/Documents/ISA/LFMC_maps/data':
   2.1) 'e'    Evaporation:    ECMWF_e_yyyymmdd_mean_wrap       to became ---> ECMWF_e_yyyymmdd_mean_coreg
   2.2) 'swvl' Soil Moisture:  ECMWF_swvl_yyyymmdd_mean_wrap    to became ---> ECMWF_swvl_yyyymmdd_mean_coreg
   and save temporarily in the same directory.
3) Remove the intermediate files (_wrap) from the directory
'''

#############
# Libraries # ------------------------------------
#############

import os
from rasterio.warp import reproject, Resampling, calculate_default_transform
import rasterio
import glob

#############
# Functions # ------------------------------------
#############
def reproj_match(infile, match, outfile):
    """Reproject a file to match the shape and projection of existing raster. 
    
    Parameters
    ----------
    infile : (string) path to input file to reproject
    match : (string) path to raster with desired shape and projection 
    outfile : (string) path to output file tif
    """
    # open input
    with rasterio.open(infile) as src:
        src_transform = src.transform
        
        # open input to match
        with rasterio.open(match) as match:
            dst_crs = match.crs
            
            # calculate the output transform matrix
            dst_transform, dst_width, dst_height = calculate_default_transform(
                src.crs,     # input CRS
                dst_crs,     # output CRS
                match.width,   # input width
                match.height,  # input height 
                *match.bounds,  # unpacks input outer boundaries (left, bottom, right, top)
            )

        # set properties for output
        dst_kwargs = src.meta.copy()
        dst_kwargs.update({"crs": dst_crs,
                           "transform": dst_transform,
                           "width": dst_width,
                           "height": dst_height,
                           "nodata": -32767})
        print("Coregistered to shape:", dst_height,dst_width,'\n Affine',dst_transform)
        # open output
        with rasterio.open(outfile, "w", **dst_kwargs) as dst:
            # iterate through bands and write using reproject function
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)

########
# MAIN # ------------------------------------
########

main_folder='/Users/gb/Documents/ISA/LFMC_maps/';
dataset = 'ECMWF'
# REFERENCE FILE
referenceFile = os.path.join(main_folder+'data/',\
                'MCD43A4_006_NDVI_20220525.tif')

# ------------------------------------
# 1) determines the day of the year 

from datetime import datetime
now = datetime.now() # current date and time
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
# day = str(int(now.strftime("%d"))-1) 
today = year+month+day

# ------------------------------------
# 2) Co-Register according to a reference file: MCD43A4_006_NDVI_20220525.tif

# 2.1) EVAPORATION
variable = 'e'
file_name = dataset+'_'+variable+'_'+today+'_mean_wrap.tif'
file_name1 = dataset+'_'+variable+'_'+today+'_mean_coreg.tif'
inputFile = os.path.join(main_folder+'data/', file_name)
outputFile = os.path.join(main_folder+'data/', file_name1)
# co-register LS to match precip raster
reproj_match(infile = inputFile, 
             match= referenceFile,
             outfile = outputFile)

# 2.2) Soil Moisture (SWVL)
variable = 'swvl'
file_name = dataset+'_'+variable+'_'+today+'_mean_wrap.tif'
file_name1 = dataset+'_'+variable+'_'+today+'_mean_coreg.tif'
inputFile = os.path.join(main_folder+'data/', file_name)
outputFile = os.path.join(main_folder+'data/', file_name1)
# co-register LS to match precip raster
reproj_match(infile = inputFile, 
             match= referenceFile,
             outfile = outputFile)

# ------------------------------------
# 3) Remove the files upsampled (wrap) from previous process (upsampling)
# get a recursive list of nc files
fileList = glob.glob(os.path.join(main_folder+'data/', '*_wrap.tif'), recursive=True) 

# iterate over the list of filepaths & remove each file. 
for filePath in fileList:
    try:
        os.remove(filePath)
    except OSError:
        print("Error while deleting file")