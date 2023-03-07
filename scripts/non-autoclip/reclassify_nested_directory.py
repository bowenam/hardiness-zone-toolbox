import os
import arcpy
from arcpy.sa import *
from arcpy.management import *

aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.activeMap
arcpy.env.overwriteOutput = True

def reclass(my_dir, clr):    
    # Create an 'output' directory in the selected directory to remap. 
    arcpy.CreateFolder_management(my_dir, 'output')

    # Find the subdirectories in the directory.
    data_dirs = []
    for item in os.listdir(my_dir):
        if os.path.isdir(os.path.join(my_dir, item)) and 'bio_6.tif' in os.listdir(os.path.join(my_dir, item)):
            data_dirs.append(item)
        else:
            arcpy.AddMessage(f'{item} may not contain bio_6.')
    
    arcpy.AddMessage('-'*60)
    for rstr_dir in data_dirs:
        rstr = os.path.join(my_dir, rstr_dir, 'BIO_6.tif')
        arcpy.AddMessage(rstr_dir)
        # Checking for temperature in degrees C or degrees C * 10
        desc = arcpy.Describe(rstr)
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
        
        rstr_path = my_dir+'\\output\\'+rstr_dir+'_bio_6_reclass.tif'
        
        # Perform the reclassification.
        arcpy.AddMessage('Reclassifying data.')
        new_reclass = Reclassify(rstr, 'Value', remap, '#')
        arcpy.AddMessage('Reclass complete.')
        
        CopyRaster(new_reclass, rstr_path, pixel_type='16_BIT_UNSIGNED')
        try:
            arcpy.management.AddColormap(rstr_path, '#', clr)
        except:
            pass
        aprxMap.addDataFromPath(rstr_path)
        
        arcpy.AddMessage('-'*60)
    
    arcpy.AddMessage(f'Reclassification complete, please check '+my_dir+'\\output for output rasters.')

if __name__ == '__main__':
    
    my_dir = arcpy.GetParameterAsText(0)
    clr = arcpy.GetParameterAsText(1)
    reclass(my_dir, clr)