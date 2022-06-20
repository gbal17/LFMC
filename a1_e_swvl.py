''' 
This program does the following:
1) determines the day of the year
2) enter the server "ftpserver.meteo.pt" in the folder "/Modelos/ECMWFfepc/"
3) Fetch the most recent (AFTER 9:30 A.M.) 
   - 'e'    Evaporation:    ECMWF_e_yyyymmdd00_0hh          e.g. ECMWF_e_2022060700_0012.nc         (https://apps.ecmwf.int/codes/grib/param-db?id=182)
   - 'swvl' Soil Moisture:  ECMWF_swvl[1,4]_yyyymmdd00_0hh  e.g. ECMWF_swvl[1,4]_2022060700_0012.nc (https://apps.ecmwf.int/codes/grib/param-db?id=39)
Dowloads the NetCDF files from 00:00 to 24:00 and close the ftp
4) Concatenates them, 
   average over time (for swvl calculate the spatial weigthed average)
   write the daily mean as NetCDF 
   convert this to TIFF
5) Remove the NetCDF files
6) Move the TIFF files from 
   '~/Documents/ISA/LFMC_maps' to 
   '~/Documents/ISA/LFMC_maps/data' in the correct Year(e.g: 2022) and Month(e.g: 06) folder.
'''

#############
# Libraries # ------------------------------------
#############
import ftplib 
import sys     
import os
import xarray as xr   # to load and open the NetCDF file to convert:
import rioxarray as rio 
import netCDF4 as nc
import leafmap
import glob
import shutil

from dirs import dir_data, dir_codes
#############
# Functions # ------------------------------------
#############

# Write a function that initiates a FTP session
def open_ftp_session(ftp_server, my_userid, my_passwd): 
    """
       Open a ftp session given the server ftp address,the user's ID and the user's password.
       @param ftp_server: name of the ftp server (string)
       @param my_userid:  user ID on the ftp server (string)
       @param my_passwd:  user password on the ftp server (string)
    """
    ftp_session = ftplib.FTP(ftp_server)
    ftp_session.login(my_userid, my_passwd)
    return ftp_session

# Download a File
def ftp_get_file(ftp_session, file_name):
    """
         Get a file from a ftp server
         @param ftp_session: ftp session object
         @param file_name: name of the file you want to download  
    """
    try:
        ftp_session.retrbinary("RETR " + file_name ,open(file_name, 'wb').write)
    except:
        print("Error - Cannot obtain file: "+ file_name)

########
# MAIN # ------------------------------------
########

# ------------------------------------
# 1) determines the day of the year 

from datetime import datetime
now = datetime.now() # current date and time
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
# day = str(int(now.strftime("%d"))-1) 
today = year+month+day

# 1.1) Create the directory "year" inside "data"
# Check whether the specified path exists or not
path = dir_data+year
isExist = os.path.exists(path)
if not isExist:
# Create a new directory because it does not exist 
  os.makedirs(path)

# 1.2) Create the directory "month" inside the directory "year"
# Check whether the specified path exists or not
path = dir_data+year+'/'+month
isExist = os.path.exists(path)
if not isExist:
# Create a new directory because it does not exist 
  os.makedirs(path)

# ------------------------------------
# 2) enter the server "ftpserver.meteo.pt" in the folder "/Modelos/ECMWFfepc/" 

# Insert userid and a password
ftp_server = "ftpserver.meteo.pt"
my_userid  = "fogos01"
my_passwd  = "fo20sog"
# Directory and Files to download
dir_name  = '/Modelos/ECMWFfepc/'

# ------------------------------------
# 3) Fetch the most recent (AFTER 9:30 A.M.) 
#    - Evaporation: ECMWF_e_yyyymmdd00_0hh e.g. ECMWF_e_2022060700_0012.nc (https://apps.ecmwf.int/codes/grib/param-db?id=182)
#    - Soil Moisture: 
#    and Dowloads the NetCDF files from 00:00 to 24:00

dataset = 'ECMWF'
variable = 'e'

# Open ftp session:
ftp_session = open_ftp_session(ftp_server, my_userid, my_passwd)

# go to the directory where to find the files to download
ftp_session.cwd(dir_name)  

# Download the files: range (1, 25) [to try (11, 13)]
for hour in range(1, 25):
 if hour < 10:
  variable = 'e'  
  file_name = dataset+'_'+variable+'_'+today+'00_00'+str(hour)+'.nc'
  variable = 'swvl1'  
  ftp_get_file(ftp_session, file_name)
  file_name = dataset+'_'+variable+'_'+today+'00_00'+str(hour)+'.nc'
  variable = 'swvl2'  
  ftp_get_file(ftp_session, file_name)
  file_name = dataset+'_'+variable+'_'+today+'00_00'+str(hour)+'.nc'
  variable = 'swvl3'  
  ftp_get_file(ftp_session, file_name)
  file_name = dataset+'_'+variable+'_'+today+'00_00'+str(hour)+'.nc'
  variable = 'swvl4'  
  ftp_get_file(ftp_session, file_name)
  file_name = dataset+'_'+variable+'_'+today+'00_00'+str(hour)+'.nc'
  ftp_get_file(ftp_session, file_name)
 else:
  variable = 'e'
  file_name = dataset+'_'+variable+'_'+today+'00_0'+str(hour)+'.nc'
  ftp_get_file(ftp_session, file_name)
  variable = 'swvl1'
  file_name = dataset+'_'+variable+'_'+today+'00_0'+str(hour)+'.nc'
  ftp_get_file(ftp_session, file_name)
  variable = 'swvl2'
  file_name = dataset+'_'+variable+'_'+today+'00_0'+str(hour)+'.nc'
  ftp_get_file(ftp_session, file_name)
  variable = 'swvl3'
  file_name = dataset+'_'+variable+'_'+today+'00_0'+str(hour)+'.nc'
  ftp_get_file(ftp_session, file_name)
  variable = 'swvl4'
  file_name = dataset+'_'+variable+'_'+today+'00_0'+str(hour)+'.nc'
  ftp_get_file(ftp_session, file_name)
# Quit ftp session:
ftp_session.quit()

# ------------------------------------
# 4) Concatenates them and average over time

# concatenate the 24 values for EVAPORATION SWVL...
# Calculate the daily mean (average over time)
# write the mean in NCDF

# 4.1) EVAPORATION
variable = 'e'
ds = xr.open_mfdataset(dir_codes+dataset+'_'+variable+'*.nc')
ds_mean = ds.mean(dim = "time")
file_name = dataset+'_'+variable+'_'+today+'_mean.nc'
ds_mean.to_netcdf(file_name)

# convert EVAPORATION mean to raster (TIF)
data = leafmap.read_netcdf(file_name)
band = data['e'] 
band = band.rio.set_spatial_dims(x_dim='longitude', y_dim='latitude')
band.rio.write_crs("epsg:4326", inplace=True)
band.rio.crs
file_name = dataset+'_'+variable+'_'+today+'_mean.tif'
band.rio.to_raster(file_name)

# 4.2) Soil Moisture (SWVL)
variable = 'swvl1'
ds1 = xr.open_mfdataset(dir_codes+dataset+'_'+variable+'*.nc')
variable = 'swvl2'
ds2 = xr.open_mfdataset(dir_codes+dataset+'_'+variable+'*.nc')
variable = 'swvl3'
ds3 = xr.open_mfdataset(dir_codes+dataset+'_'+variable+'*.nc')
variable = 'swvl4'
ds4 = xr.open_mfdataset(dir_codes+dataset+'_'+variable+'*.nc')

variable = 'swvl'
ds_mean = ((ds1['swvl1'].mean('time')*7) + (ds2['swvl2'].mean('time')*21) + \
           (ds3['swvl3'].mean('time')*72)+ (ds4['swvl4'].mean('time')*189))/ 289
# rename the Band (Data variables) from "__xarray_dataarray_variable__" to "swvl"
ds_mean = ds_mean.rename("swvl")
file_name = dataset+'_'+variable+'_'+today+'_mean.nc'
swvl = ds_mean.to_netcdf(file_name)

# convert SWVL mean to raster (TIF) 
data = leafmap.read_netcdf(file_name)
band = data['swvl'] 
band = band.rio.set_spatial_dims(x_dim='longitude', y_dim='latitude')
band.rio.write_crs("epsg:4326", inplace=True)
band.rio.crs
file_name = dataset+'_'+variable+'_'+today+'_mean.tif'
band.rio.to_raster(file_name)

# ------------------------------------
# 5) Remove the NetCDF files
# get a recursive list of nc files
fileList = glob.glob('*.nc', recursive=True)    
# iterate over the list of filepaths & remove each file. 

for filePath in fileList:
    try:
        os.remove(filePath)
    except OSError:
        print("Error while deleting file")

# ------------------------------------
# 6) Move the TIFF files from Main Folder to DATA folder
src_folder = dir_codes
dst_folder = dir_data+year+'/'+month+'/'

# Search files with tiff extension in source directory
pattern = "/*.tif"
files = glob.glob(src_folder + pattern)
# print(files)

# move the files with tiff extension
for file in files:
    # extract file name form file path
    file_name = os.path.basename(file)
    shutil.move(file, dst_folder + file_name)
    print('Moved:', file)