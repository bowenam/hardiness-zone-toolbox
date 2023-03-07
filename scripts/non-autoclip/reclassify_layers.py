import arcpy
from arcpy.sa import *
from arcpy.management import *

aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.activeMap
arcpy.env.overwriteOutput = True

def reclass(param, out, clr):
    arcpy.AddMessage('Beginning reclassification of minimum temperatures to plant hardiness zones.')
    arcpy.AddMessage('NOTE: For bioclimatic variables, bio_6 MUST be used for the intended purpose of this tool.')
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
        
        lyr_path = out+rf'\{lyr}_reclass.tif'
        
        arcpy.AddMessage('Reclassifying data.')
        new_reclass = Reclassify(lyr, 'Value', remap, '#')    
        arcpy.AddMessage('Reclass complete.')
        
        CopyRaster(new_reclass, lyr_path, pixel_type='16_BIT_UNSIGNED')
        try:
            arcpy.management.AddColormap(lyr_path, '#', clr)
        except:
            pass
        aprxMap.addDataFromPath(lyr_path)
        
        arcpy.AddMessage('-'*60)
        

if __name__ == '__main__':
    
    param = arcpy.GetParameter(0)
    out = arcpy.GetParameterAsText(1)
    clr = arcpy.GetParameterAsText(2)
    
    reclass(param, out, clr)