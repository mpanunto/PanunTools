#Due to printing issues with PDFs exported from ArcGIS Pro, this script was designed with the assumption
#that two separate exports are often needed for each map: one for printing, and one for Avenza use.
#The spreadsheet allows users to customize their export settings for each of these two separate PDFs.
#The spreadsheet also allows users to specify whether one, both, or neither exports are needed for a map.
#Additionally, this script can be used to update the map date, but only if the layout is using dynamictext from
#the summary field of the map's properties

#This script uses the Python multiprocessing module to run several instances of Python simultaneously. It is
#similar to openening numerous .arpx files at once in order to export multiple PDFs are the same time.

#Import libraries
print("Importing Libraries")
import arcpy, pandas, time, datetime, os, sys, multiprocessing
from multiprocessing import Pool, freeze_support


#Define function to export PDFs
def worker_function(incidentname, unitid, incidentnumber, productdir,
                exportrequest, update_mapdate, mapdate, proddate, shift, maptype, pagesize, orientation,
                image_clipgraphics, image_compress, image_compressquality, image_compressvecgraphics, image_vectorresolution, image_rasterresample,
                avenza_clipgraphics, avenza_compress, avenza_compressquality, avenza_compressvecgraphics, avenza_vectorresolution, avenza_rasterresample, avenza_embedfonts, avenza_georefinfo, avenza_layersattributes,
                layoutname, mapname, aprxpath):


    arcpy.AddMessage(" ")
    arcpy.AddMessage("PROCESSING: " + maptype + " " + pagesize + " " + orientation)

    #Create datetime stamp for current time
    now = datetime.datetime.now()
    curr_datetime_str = now.strftime("%Y%m%d_%H%M")

    #First check to make sure the aprx path is good
    aprx_check = arcpy.Exists(aprxpath)

    #If aprx exists, read-in, else throw error
    if(aprx_check == True):
        aprx = arcpy.mp.ArcGISProject(aprxpath)
    else:
        arcpy.AddMessage("APRX NOT FOUND AT USER SPECIFIED PATH:")
        arcpy.AddMessage(aprxpath)
        raise arcpy.ExecuteError

    #Now test to see if layout exists, throw error if not
    layoutname_check = (len(aprx.listLayouts(layoutname)) == 1)
    if(layoutname_check == False):
        arcpy.AddMessage("LAYOUT NAME NOT FOUND IN APRX, CHECK SPELLING: " + layoutname)
        raise arcpy.ExecuteError

    #Now test to see if map exists, throw error if not
    mapname_check = (len(aprx.listMaps(mapname)) == 1)
    if(mapname_check == False):
        arcpy.AddMessage("MAP NAME NOT FOUND IN APRX, CHECK SPELLING: " + mapname)
        raise arcpy.ExecuteError

    #If UPDATE_MAP_DATE == Yes, first update the map date before any exporting
    if update_mapdate == "Yes":
        update_map_complete = False
        while(update_map_complete == False):
            try:
                arcpy.AddMessage("..UPDATING MAP DATE")
                curr_map = aprx.listMaps(mapname)[0]
                curr_map_metadata = curr_map.metadata
                curr_map_metadata.summary = mapdate
                curr_map_metadata.save()
                aprx.save()

                #Have to reload the project again, because it was exporting with blank titles and dates
                del aprx
                aprx = arcpy.mp.ArcGISProject(aprxpath)
                update_map_complete = True
            except:
                arcpy.AddMessage("....PROJECT MAY BE IN USE, WAITING 60s THEN TRYING AGAIN")
                time.sleep(60)

    #If export was requested, proceed
    if exportrequest in ["IMAGE", "AVENZA", "BOTH"]:

        #Create variables for output directory paths
        product_date_dir = productdir + "/" + proddate
        image_dir = product_date_dir + "/image"
        avenza_dir = product_date_dir + "/avenza"

        #Create daily product folder, if it doesn't exist
        if( not os.path.isdir(product_date_dir) ):
            os.mkdir(product_date_dir)

        #Create image folder, if it doesn't exist
        if( not os.path.isdir(image_dir) ):
            os.mkdir(image_dir)

        #Create avenza folder, if it doesn't exist
        if( not os.path.isdir(avenza_dir) ):
            os.mkdir(avenza_dir)

        lyt = aprx.listLayouts(layoutname)[0]
        pdf_image_outpath = image_dir + "/IMAGE_" + maptype + "_" + pagesize + "_" + orientation + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + shift + ".pdf"
        pdf_avenza_outpath = avenza_dir + "/AVENZA_" + maptype + "_" + pagesize + "_" + orientation + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + shift + ".pdf"

        if exportrequest in ["IMAGE", "AVENZA", "BOTH"]:
            arcpy.AddMessage("..EXPORTING")

        #If IMAGE or BOTH was requested, export PDF for printing (export as image)
        if exportrequest in ["IMAGE", "BOTH"]:
            image_export_complete = False
            while(image_export_complete == False):
                try:
                    arcpy.AddMessage("....IMAGE EXPORT")
                    lyt.exportToPDF(pdf_image_outpath, resolution=image_vectorresolution, image_quality=image_rasterresample, compress_vector_graphics=image_compressvecgraphics,
                                    image_compression=image_compress, jpeg_compression_quality=image_compressquality, clip_to_elements=image_clipgraphics, output_as_image=True)
                    arcpy.AddMessage("......EXPORT COMPLETE")
                    image_export_complete = True
                except:
                    arcpy.AddMessage("......PROJECT IN USE, WAITING 60s THEN TRYING AGAIN")
                    time.sleep(60)

        #If AVENZA or BOTH was requested, export PDF for Avenza use
        if exportrequest in ["AVENZA", "BOTH"]:
            avenza_export_complete = False
            while(avenza_export_complete == False):
                try:
                    arcpy.AddMessage("....AVENZA EXPORT")
                    lyt.exportToPDF(pdf_avenza_outpath, resolution=avenza_vectorresolution, image_quality=avenza_rasterresample, compress_vector_graphics=avenza_compressvecgraphics,
                                    image_compression=avenza_compress, jpeg_compression_quality=avenza_compressquality, embed_fonts=avenza_embedfonts, layers_attributes=avenza_layersattributes,
                                    georef_info=avenza_georefinfo, clip_to_elements=avenza_clipgraphics, output_as_image=False)
                    arcpy.AddMessage("......EXPORT COMPLETE")
                    avenza_export_complete = True
                except:
                    arcpy.AddMessage("......PROJECT IN USE, WAITING 60s THEN TRYING AGAIN")
                    time.sleep(60)


#Define function to create pool of processes
def execute(inputs):

    #Set multiprocessing python exe path
    multiprocessing.set_executable(os.path.join(sys.exec_prefix, 'python.exe'))

    #Create a pool of workers
    pool = multiprocessing.Pool()

    #Apply "worker_function" to the list of inputs
    pool.starmap(worker_function, inputs)

    pool.close()
    pool.join()





if __name__=="__main__":

    import MultiExportPDF

    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Multi Export PDF tool developed by Matt Panunto, DOI-BLM")

    #Specify incident name, unit id, and incident number
    #incident_name = "Vinegar"
    incident_name = arcpy.GetParameterAsText(0)

    #incident_id = "ID-PAF-000433"
    incident_id = arcpy.GetParameterAsText(1)

    #Specify the products directory
    #products_dir = r"C:\Workspace\OneDrive - FireNet\2021_Vinegar\products"
    products_dir = arcpy.GetParameterAsText(2)

    #Specify the path to the "ExportPDFtable.xlsx" file
    #export_table_xlsx_path = r"C:\Workspace\OneDrive - FireNet\2021_Vinegar\tools\MultiExportPDF_Vinegar.xlsx"
    export_table_xlsx_path = arcpy.GetParameterAsText(3)

    #Convert Incident Name to CamelCase
    if(" " in incident_name):
        incident_name = incident_name.replace(" ", "")
    if("." in incident_name):
        incident_name = incident_name.replace(".", "")
    if("-" in incident_name):
        incident_name = incident_name.replace("-", "")
    if("'" in incident_name):
        incident_name = incident_name.replace("'", "")

    #Split the IncidentID into the UnitID and IncidentNumber
    incident_id_split = incident_id.split("-")
    unit_id = incident_id_split[0] + incident_id_split[1]
    incident_number = incident_id_split[2]

    #Create dataframe from spreadsheet
    try:
        export_table_df = pandas.read_excel(export_table_xlsx_path)
    except:
        arcpy.AddError("UNABLE TO READ MULTI EXPORT PDF SPREADSHEET, CHECK TO MAKE SURE IT ISN'T CURRENTLY OPEN")
        raise arcpy.ExecuteError


    #Create lists of EXPORT_REQUEST and UPDATE_MAP_DATE values from the spreadsheet
    exportrequest_col = list(export_table_df["EXPORT_REQUEST"])
    updatemapdate_col = list(export_table_df["UPDATE_MAP_DATE"])

    #Get count of how many items need processing, and also determine which items
    exportrequest_updatemapdate_list = [m+str(n) for m,n in zip(exportrequest_col, updatemapdate_col)]
    processing_needed_list = []
    processing_needed_which_list = []
    for i in range(0, len(exportrequest_updatemapdate_list)):
        curr_str = exportrequest_updatemapdate_list[i]
        exportrequest_check = any(x in curr_str for x in ["IMAGE", "AVENZA", "BOTH"])
        updatemapdate_check = ("Yes" in curr_str)
        if(exportrequest_check == True or updatemapdate_check == True):
            processing_needed_list.append(1)
            processing_needed_which_list.append(i)
        else:
            processing_needed_list.append(0)
    processing_count = len(processing_needed_which_list)


    #Create variables from spreadsheets when there is only 1 item in the sheet
    if(processing_count == 1):

        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("Single project export requested")
        arcpy.AddMessage("\u200B")

        process_which = processing_needed_list.index(1)



        #Create lists for export request and filename information
        exportrequest_list = str(export_table_df["EXPORT_REQUEST"][process_which])
        update_mapdate_list = str(export_table_df["UPDATE_MAP_DATE"][process_which])
        mapdate_list = str(export_table_df["MAP_DATE"][process_which])
        proddate_list = str(export_table_df["PRODUCTS_DATE"][process_which])
        shift_list = str(export_table_df["SHIFT"][process_which])
        maptype_list = str(export_table_df["MAP_TYPE"][process_which])
        pagesize_list = str(export_table_df["PAGE_SIZE"][process_which])
        orientation_list = str(export_table_df["ORIENTATION"][process_which])

        #Create lists for the IMAGE export settings
        image_clipgraphics_list = export_table_df["IMAGE_CLIP_GRAPHICS"][process_which]
        image_compress_list = str(export_table_df["IMAGE_COMPRESSION"][process_which])
        image_compressquality_list = int(export_table_df["IMAGE_COMPRESSION_QUALITY"][process_which])
        image_compressvecgraphics_list = export_table_df["IMAGE_COMPRESS_VECTOR_GRAPHICS"][process_which]
        image_vectorresolution_list = int(export_table_df["IMAGE_VECTOR_RESOLUTION"][process_which])
        image_rasterresample_list = str(export_table_df["IMAGE_RASTER_RESAMPLE"][process_which])

        #Create lists for the AVENZA export settings
        avenza_clipgraphics_list = export_table_df["AVENZA_CLIP_GRAPHICS"][process_which]
        avenza_compress_list = str(export_table_df["AVENZA_COMPRESSION"][process_which])
        avenza_compressquality_list = int(export_table_df["AVENZA_COMPRESSION_QUALITY"][process_which])
        avenza_compressvecgraphics_list = export_table_df["AVENZA_COMPRESS_VECTOR_GRAPHICS"][process_which]
        avenza_vectorresolution_list = int(export_table_df["AVENZA_VECTOR_RESOLUTION"][process_which])
        avenza_rasterresample_list = str(export_table_df["AVENZA_RASTER_RESAMPLE"][process_which])
        avenza_embedfonts_list = export_table_df["AVENZA_EMBED_FONTS"][process_which]
        avenza_georefinfo_list = export_table_df["AVENZA_GEOREF_INFO"][process_which]
        avenza_layersattributes_list = str(export_table_df["AVENZA_LAYERS_ATTRIBUTES"][process_which])

        #Create lists for the Layout name and APRX Path
        layoutname_list = str(export_table_df["LAYOUT_NAME"][process_which])
        mapname_list = str(export_table_df["MAP_NAME"][process_which])
        aprxpath_list = str(export_table_df["APRX_PATH"][process_which])

        #Create lists of user specified inputs
        incidentname_list = incident_name
        unitid_list = unit_id
        incidentnumber_list = incident_number
        productdir_list = products_dir

        #If only 1 row in xlsx, run worker_function() function
        worker_function(incidentname_list, unitid_list, incidentnumber_list, productdir_list,
                    exportrequest_list, update_mapdate_list, mapdate_list, proddate_list, shift_list, maptype_list, pagesize_list, orientation_list,
                    image_clipgraphics_list, image_compress_list, image_compressquality_list, image_compressvecgraphics_list, image_vectorresolution_list, image_rasterresample_list,
                    avenza_clipgraphics_list, avenza_compress_list, avenza_compressquality_list, avenza_compressvecgraphics_list, avenza_vectorresolution_list, avenza_rasterresample_list, avenza_embedfonts_list, avenza_georefinfo_list, avenza_layersattributes_list,
                    layoutname_list, mapname_list, aprxpath_list)


    #Create variables from spreadsheets when there are multiple items in the sheet
    if(processing_count > 1):

        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("Mulitple project exports requested")

        #Create lists for export request and filename information
        exportrequest_list = [list(map(str, export_table_df["EXPORT_REQUEST"]))[i] for i in processing_needed_which_list]
        update_mapdate_list = [list(map(str, export_table_df["UPDATE_MAP_DATE"]))[i] for i in processing_needed_which_list]
        mapdate_list = [list(map(str, export_table_df["MAP_DATE"]))[i] for i in processing_needed_which_list]
        proddate_list = [list(map(str, export_table_df["PRODUCTS_DATE"]))[i] for i in processing_needed_which_list]
        shift_list = [list(map(str, export_table_df["SHIFT"]))[i] for i in processing_needed_which_list]
        maptype_list = [list(map(str, export_table_df["MAP_TYPE"]))[i] for i in processing_needed_which_list]
        pagesize_list = [list(map(str, export_table_df["PAGE_SIZE"]))[i] for i in processing_needed_which_list]
        orientation_list = [list(map(str, export_table_df["ORIENTATION"]))[i] for i in processing_needed_which_list]

        #Create lists for the IMAGE export settings
        image_clipgraphics_list = [list(export_table_df["IMAGE_CLIP_GRAPHICS"])[i] for i in processing_needed_which_list]
        image_compress_list = [list(map(str, export_table_df["IMAGE_COMPRESSION"]))[i] for i in processing_needed_which_list]
        image_compressquality_list = [list(map(int, export_table_df["IMAGE_COMPRESSION_QUALITY"]))[i] for i in processing_needed_which_list]
        image_compressvecgraphics_list = [list(export_table_df["IMAGE_COMPRESS_VECTOR_GRAPHICS"])[i] for i in processing_needed_which_list]
        image_vectorresolution_list = [list(map(int, export_table_df["IMAGE_VECTOR_RESOLUTION"]))[i] for i in processing_needed_which_list]
        image_rasterresample_list = [list(map(str, export_table_df["IMAGE_RASTER_RESAMPLE"]))[i] for i in processing_needed_which_list]

        #Create lists for the AVENZA export settings
        avenza_clipgraphics_list = [list(export_table_df["AVENZA_CLIP_GRAPHICS"])[i] for i in processing_needed_which_list]
        avenza_compress_list = [list(map(str, export_table_df["AVENZA_COMPRESSION"]))[i] for i in processing_needed_which_list]
        avenza_compressquality_list = [list(map(int, export_table_df["AVENZA_COMPRESSION_QUALITY"]))[i] for i in processing_needed_which_list]
        avenza_compressvecgraphics_list = [list(export_table_df["AVENZA_COMPRESS_VECTOR_GRAPHICS"])[i] for i in processing_needed_which_list]
        avenza_vectorresolution_list = [list(map(int, export_table_df["AVENZA_VECTOR_RESOLUTION"]))[i] for i in processing_needed_which_list]
        avenza_rasterresample_list = [list(map(str, export_table_df["AVENZA_RASTER_RESAMPLE"]))[i] for i in processing_needed_which_list]
        avenza_embedfonts_list = [list(export_table_df["AVENZA_EMBED_FONTS"])[i] for i in processing_needed_which_list]
        avenza_georefinfo_list = [list(export_table_df["AVENZA_GEOREF_INFO"])[i] for i in processing_needed_which_list]
        avenza_layersattributes_list = [list(map(str, export_table_df["AVENZA_LAYERS_ATTRIBUTES"]))[i] for i in processing_needed_which_list]

        #Create lists for the Layout name and APRX Path
        layoutname_list = [list(map(str, export_table_df["LAYOUT_NAME"]))[i] for i in processing_needed_which_list]
        mapname_list = [list(map(str, export_table_df["MAP_NAME"]))[i] for i in processing_needed_which_list]
        aprxpath_list = [list(map(str, export_table_df["APRX_PATH"]))[i] for i in processing_needed_which_list]

        #Create lists of user specified inputs
        incidentname_list = [incident_name] * processing_count
        unitid_list = [unit_id] * processing_count
        incidentnumber_list = [incident_number] * processing_count
        productdir_list = [products_dir] * processing_count

        inputs_list = list(zip(incidentname_list, unitid_list, incidentnumber_list, productdir_list,
                    exportrequest_list, update_mapdate_list, mapdate_list, proddate_list, shift_list, maptype_list, pagesize_list, orientation_list,
                    image_clipgraphics_list, image_compress_list, image_compressquality_list, image_compressvecgraphics_list, image_vectorresolution_list, image_rasterresample_list,
                    avenza_clipgraphics_list, avenza_compress_list, avenza_compressquality_list, avenza_compressvecgraphics_list, avenza_vectorresolution_list, avenza_rasterresample_list, avenza_embedfonts_list, avenza_georefinfo_list, avenza_layersattributes_list,
                    layoutname_list, mapname_list, aprxpath_list))

        ############################################################################
        ## BEGIN MULTIPROCESSOR
        ############################################################################
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("Begin multiprocessing")
        MultiExportPDF.execute(inputs_list)
        arcpy.AddMessage("..Finished multiprocessing")
        ############################################################################
        ## END MULTIPROCESSOR
        ############################################################################
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("Done!")

