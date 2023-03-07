import arcpy
from arcpy.sa import *
from arcpy.management import *
import numpy as np

aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.activeMap
arcpy.env.overwriteOutput = True

def reclass(param, clip_layer, out_directory, clr):   
    arcpy.AddMessage('Beginning reclassification of minimum temperatures to plant hardiness zones.')
    arcpy.AddMessage('NOTE: For bioclimatic variables, bio_6 MUST be used or results have little meaning.')
    arcpy.AddMessage('-'*60)

    for lyr in param:
        arcpy.AddMessage(str(lyr))
        # Checking for temperature in degrees C or degrees C * 10
        
        # Create a range of temperatures to remap existing temperatures
        # on the selected extreme min. temperature raster file. 
        # NOTE: The beginning and end of the included list are extremes,
        # outside the current plant hardiness zone. 
        desc = arcpy.Describe(lyr)
        if desc.isInteger == False:
            remap = RemapRange([[-51.1, -45.6, 1], [-45.6, -40.0, 2],
                                [-40.0, -34.4, 3], [-34.4, -28.9, 4], [-28.9, -23.3, 5],
                                [-23.3, -17.8, 6], [-17.8, -12.2, 7], [-12.2, -6.7, 8],
                                [-6.7, -1.1, 9], [-1.1, 4.4, 10], [4.4, 10, 11],
                                [10, 15.6, 12], [15.6, 21.1, 13]])
        else:
            remap = RemapRange([[-511, -456, 1], [-456, -400, 2],
                                [-400, -344, 3], [-344, -289, 4], [-289, -233, 5],
                                [-233, -178, 6], [-178, -122, 7], [-122, -67, 8],
                                [-67, -11, 9], [-11, 44, 10], [44, 100, 11],
                                [100, 156, 12], [156, 211, 13]])
        
        #clip_raster = out_directory+'\\'+f'{str(lyr)}_c.tif'
        rstr_path = out_directory+'\\'+f'{lyr}_clipped.tif'

        arcpy.AddMessage(f'Clipping to {str(clip_layer)}.')
        Clip(lyr, clip_layer, rstr_path, clip_layer, '#', 'ClippingGeometry')
        arcpy.AddMessage('Clip complete.')

        arcpy.AddMessage('Reclassifying data.')
        new_reclass = Reclassify(rstr_path, 'Value', remap, '#')
        arcpy.AddMessage('Reclass complete.')
        
        CopyRaster(new_reclass, rstr_path, pixel_type='16_BIT_UNSIGNED')
        AddColormap(rstr_path, '#', clr)
        aprxMap.addDataFromPath(rstr_path)
        
        arcpy.AddMessage('-'*60)

    arcpy.AddMessage(f'Reclassification complete, please check {out_directory} for output rasters.')

if __name__ == '__main__':
    
    param = arcpy.GetParameter(0)
    clip_layer = arcpy.GetParameter(1)
    out_directory = arcpy.GetParameterAsText(2)
    clr = arcpy.GetParameterAsText(3)
    
    reclass(param, clip_layer, out_directory, clr)