import os
import arcpy
from arcpy.sa import *
from arcpy.management import *  

aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.activeMap
arcpy.env.overwriteOutput = True

def reclass(my_dir, clip_layer, clr):
    arcpy.env.workspace = my_dir
    
    # Creates an 'output' directory in the selected directory. 
    arcpy.CreateFolder_management(my_dir, 'output')

    # Finds the files in the directory given in the first parameter.
    file_iter = []
    for item in os.listdir(my_dir):
        if os.path.isfile(os.path.join(my_dir, item)):
            try:
                desc = arcpy.Describe(item)
                for child in desc.children:
                    if '_6' in child.name:
                        band_name = child.name
                        file_iter.append(os.path.join(item, band_name))
            except:
                arcpy.AddMessage(f'{item} may not contain bio_6 or may not be of an applicable file type.')

    for rstr in file_iter:
        arcpy.AddMessage(rstr)
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
        
        clip_raster = my_dir+'\\output\\'+str(rstr).replace('\\', '_')+'_c.tif'
        rstr_path = my_dir+'\\output\\'+str(rstr).replace('\\', '_')+'.tif'

        arcpy.AddMessage(f'Clipping to {clip_layer}.')
        # Clipping the raw data layer to the given clip layer. 
        arcpy.management.Clip(in_raster=rstr, 
                              rectangle=clip_layer, 
                              out_raster=clip_raster, 
                              in_template_dataset=clip_layer, 
                              nodata_value='#', 
                              clipping_geometry='ClippingGeometry')
        arcpy.AddMessage('Clip complete.')
        
        arcpy.AddMessage('Reclassifying data.')
        # Reclassifying the clipped raw data into plant hardiness zones. 
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