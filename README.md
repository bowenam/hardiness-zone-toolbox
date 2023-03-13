# hardiness-zone-toolbox
This toolbox was created by Andrew Bowen (bowenam@etsu.edu) at East Tennessee State University as part of a Master's thesis project. The toolboxes contain arcpy scripts that convert raster datasets containing annual average minimum temperatures (BIO 6) to a Plant Hardiness Zone Map. 

## Reclassify (Layers)
Reclassifies raster layer in current map. Also takes filepath raster input. 
#### Input Parameters
* Raster to Reclassify - Single-band raster that contains average annual minimum temperatures.
* Output Directory - Directory to save output raster file to.
* Colormap - Color coding to use with the output zones. See (bathymetric.clr link). 

## Reclassify (WorldClim)
This script tool targets WorldClim data; reclassifies raster files that contain multiple raster bands, each (band) corresponding to a bioclimatic variable. This tool seeks out the BIO_6 band, which corresponds to extreme minimum temperature.
#### Input Parameters
* Directory - The directory containing the multi-band TIF files. Each TIF file should contain the BIO_6 band for the tool to work. 
* Colormap - Color coding to use with the output zones. See (bathymetric.clr link). 

## Reclassify (PaleoClim)
This script tool targets PaleoClim data; reclassifies raster files that represnet bioclimatic variables. This tool seeks out folders containing bio_6 GeoTIFF files to reclassify.
#### Input Parameters
* Directory - The superdirectory containing the subdirectories, each corresponding to a time frame and itself containing a TIF file. This tool searches for the TIF file entitled "bio_6.tif". 
* Colormap - Color coding to use with the output zones. See (bathymetric.clr link). 

## A note about the two toolboxes:
There are two similar toolboxes included: autoclip and non-autoclip. The differences are noted below. 
#### Non-Autoclip Scripts
These scripts will produce Plant Hardiness Zone Maps (PHZMs) of the same coverage of the original input raster file. 
#### Autoclip Scripts
These scripts take an additional input parameter: a shapefile layer to clip the output data. Otherwise are the same as the Non-Autoclip Scripts.
