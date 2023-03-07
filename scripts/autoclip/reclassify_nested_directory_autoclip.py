import os
import arcpy
from arcpy.sa import *
from arcpy.management import *

aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.activeMap
arcpy.env.overwriteOutput = True

def reclass(my_dir, clip_layer, clr):
    # Creates an 'output' directory in the selected directory to remap. 
    arcpy.CreateFolder_management(my_dir, 'output')

    # Finds the subdirectories in the directory given in the first parameter.
    for root, dirs, files in os.walk(my_dir):
        if len(dirs) > 1:
            data_dirs = dirs
            data_dirs.remove('output')
    
    for rstr in data_dirs:
        arcpy.AddMessage(rstr)
        raster = os.path.join(my_dir, rstr, 'BIO_6.tif')
        # Checking for temperature in degrees C or degrees C * 10
        desc = arcpy.Describe(raster)
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
        
        clip_raster = my_dir+'\\output\\'+str(rstr).replace('\\', '_')+'_c.tif'
        rstr_path = my_dir+'\\output\\'+rstr+'_bio_6_reclass.tif'

        arcpy.AddMessage(f'Clipping to {clip_layer}')
        Clip(in_raster=raster, 
             rectangle=clip_layer, 
             out_raster=clip_raster, 
             in_template_dataset=clip_layer, 
             nodata_value='#', 
             clipping_geometry='ClippingGeometry')
        arcpy.AddMessage('Clip complete.')
        
        arcpy.AddMessage(f'Reclassifying data.')
        new_reclass = Reclassify(in_raster=clip_raster, 
                                 reclass_field='Value', 
                                 remap=remap, 
                                 missing_values='#')
        arcpy.AddMessage('Reclass complete.')
        CopyRaster(new_reclass, rstr_path, pixel_type='16_BIT_UNSIGNED')
        AddColormap(rstr_path, '#', clr)
        aprxMap.addDataFromPath(rstr_path)
                
        arcpy.AddMessage('-'*60)
    
    arcpy.AddMessage(f'Reclassification complete, please check '+my_dir+'\\output for output rasters.')

if __name__ == '__main__':
    
    my_dir = arcpy.GetParameterAsText(0)
    clip_layer = arcpy.GetParameterAsText(1)
    clr = arcpy.GetParameterAsText(2)
    
    reclass(my_dir, clip_layer, clr)
    
