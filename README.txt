This readme describes the software routines for LFMC map over Portugal.

This system has been tested, ported, and run successfully on macOS Catalina version 10.15.7 OS

################################
##### Install Instructions #####
################################ 

1) Start with a fresh install miniconda3

2) create new environment and install the following library:
conda install -c conda-forge mamba
mamba install -c conda-forge gdal
mamba install -c conda-forge fiona shapely rasterio pyproj pandas jupyterlab
mamba install -c conda-forge rioxarray
mamba install -c conda-forge leafmap xarray netcdf4 localtileserver
Update the library if nevessary

3) If there are no error messages, the software libraries and dependencies are correctly configured.

4) The crontab commands in the crontab.txt file list the scripts and the schedule when 
they are automatically running according conrab sintax in the vi editor.

##############################
##### Usage Instructions #####
##############################

**************************************
******** Folder : NRT_Flood **********
**************************************

Description: This set of programs downloads, processes, and applies classification algorithm 
to MODIS and ERA5 data to determine LFMC maps over scrublands and woodlands of Portugal.

Programs in this module and descriptions:
1) a1_e_swvl.py - determines the day of the year and fetches the respective ERA5 Evaporation and 
Soil Moisture hourly products and calculate the daily average.
2) a1_ndvi.py - fetches the latest MODIS Combined 16-Day NDVI from EarthEngine Catalog: MCD43A4_006_NDVI
3) a2_1_upsampling.py - Upsample the ERA5 Evaporation and Soil Moisture according to MCD43A4_006_NDVI resolution (500m) 
4) a2_2_coreg.py - Does the Co-Registration and Clipping Upsampled ERA5 Evaporation and Soil Moisture map according to MCD43A4_006_NDVI map.

The programs should be run in numerical order: 

(1) --> (2) --> (3) --> (4)

Each program contains a more detailed description within the docstring of the .py file as well as in-line comments for code clarity