# Set up environment

1) Start with a fresh install miniconda3

2) in Terminal create a new environment and install the following library:
```
conda env create -f path-to-ee-shared-env.yml
```
alternatively:
```
conda create --name lfmcmaps
conda activate lfmcmaps
conda install --yes --file requirements.txt
```

3) If there are no error messages, the software libraries and dependencies are correctly configured.

4) The crontab commands in the crontab.txt file list the scripts and the schedule when 
they are automatically running according to conrab syntax in the vi editor.

# Make LFMC maps

1. **Export input feature maps.** This step downloads input ERA5 maps from ftpserver.meteo.pt and  MODIS Combined 16-Day NDVI maps from gee. 

Programs in this module and descriptions:
1) `a1_e_swvl.py` - determines the day of the year and fetches the respective ERA5 Evaporation and 
Soil Moisture hourly products and calculate the daily average.
2) `a1_ndvi.py` - fetches the latest MODIS Combined 16-Day NDVI from EarthEngine Catalog: MCD43A4_006_NDVI
3) `a2_1_upsampling.py` - Upsample the ERA5 Evaporation and Soil Moisture according to MCD43A4_006_NDVI resolution (500m) 
4) `a2_2_coreg.py` - Does the Co-Registration and Clipping Upsampled ERA5 Evaporation and Soil Moisture map according to MCD43A4_006_NDVI map.

The programs should be run in numerical order: 

(1) --> (2) --> (3) --> (4)

the script `az_main.py` runs all the scripts together at once in the correct order.
Each program contains a more detailed description within the docstring of the .py file as well as in-line comments for code clarity


2. **Download input feature maps** 

3. **Predict LFMC maps.** 
	

# Upload LFMC maps
