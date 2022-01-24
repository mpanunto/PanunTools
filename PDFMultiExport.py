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
print(" ")
import arcpy, pandas, time, datetime, os, sys, multiprocessing
from urllib.request import urlopen
from multiprocessing import Pool, freeze_support


#Define function to export PDFs
def worker_function(in_inputs_list):

    incidentname = in_inputs_list[0]
    unitid = in_inputs_list[1]
    incidentnumber = in_inputs_list[2]
    productdir = in_inputs_list[3]
    export = in_inputs_list[4]
    proddate = in_inputs_list[5]

    filename = in_inputs_list[6]
    user_specified = in_inputs_list[7]
    geoops_maptype = in_inputs_list[8]
    geoops_pagesize = in_inputs_list[9]
    geoops_orientation = in_inputs_list[10]
    geoops_period = in_inputs_list[11]
    export_label = in_inputs_list[12]


    mapseries_pages = in_inputs_list[13]
    mapseries_range = in_inputs_list[14]
    mapseries_files = in_inputs_list[15]

    clipgraphics_val = in_inputs_list[16]
    imagecompress_val = in_inputs_list[17]
    imagecompressquality_val = in_inputs_list[18]
    compressvectorgraphics_val = in_inputs_list[19]
    vectorresolution_val = in_inputs_list[20]
    rasterresample_val = in_inputs_list[21]
    embedfonts_val = in_inputs_list[22]
    layersattributes_val = in_inputs_list[23]

    layoutname = in_inputs_list[24]
    aprxpath = in_inputs_list[25]

    #Cleanup filename variables if they are blank
    if(geoops_maptype == "nan"):
        geoops_maptype = ""
    if(geoops_pagesize == "nan"):
        geoops_pagesize = ""
    if(geoops_orientation == "nan"):
        geoops_orientation = ""
    if(geoops_period == "nan"):
        geoops_period = ""

    #Build GeoOps filenaming string
    geoops_list = [geoops_maptype, geoops_pagesize, geoops_orientation]
    geoops_str = ""
    if(geoops_list[0] != ""):
        geoops_str = geoops_list[0]
    if(geoops_list[1] != ""):
        geoops_str = geoops_str + "_" + geoops_list[1]
    if(geoops_list[2] != ""):
        geoops_str = geoops_str + "_" + geoops_list[2]
    if(geoops_str[0] == "_"):
        geoops_str = geoops_str[1:]

    #Print the current export being processed
    if(filename == "GEO OPS"):
        arcpy.AddMessage("PROCESSING: " + geoops_str)
    if(filename == "USER SPECIFIED"):
        arcpy.AddMessage("PROCESSING: " + user_specified)

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

    #Create layout object
    lyt = aprx.listLayouts(layoutname)[0]

    #Determine if layout is a map series
    if(lyt.mapSeries == None):
        mapseries = False
    else:
        mapseries = lyt.mapSeries.enabled

    #Print message informing user it is a map series
    if(mapseries == True):
        arcpy.AddMessage("..MAP SERIES LAYOUT")

    #If Map Series, get the proper parameter value for "multiple_files" paramter
    if(mapseries == True):
        if(mapseries_files == "SINGLE PDF FILE"):
            multiple_files_val = "PDF_SINGLE_FILE"
        if(mapseries_files == "MULTIPLE PDF FILES (PAGE NAME AS SUFFIX)"):
            multiple_files_val = "PDF_MULTIPLE_FILES_PAGE_NAME"
        if(mapseries_files == "MULTIPLE PDF FILES (PAGE NUMBER AS SUFFIX)"):
            multiple_files_val = "PDF_MULTIPLE_FILES_PAGE_NUMBER"

    #If Map Series, and RANGE is specified, remove the spaces from the user specified range
    if(mapseries == True and mapseries_pages == "RANGE"):
        mapseries_range_val = mapseries_range.replace(" ", "")

    #Create datetime stamp for current time
    now = datetime.datetime.now()
    curr_datetime_str = now.strftime("%Y%m%d_%H%M")

    #If export was requested, proceed
    if export in ["IMAGE", "GEO", "GEOIMAGE", "GEO AND IMAGE"]:

        #Create variables for output directory paths
        product_date_dir = productdir + "/" + proddate
        image_dir = product_date_dir + "/IMAGE"
        geo_dir = product_date_dir + "/GEO"
        geoimage_dir = product_date_dir + "/GEOIMAGE"

        #Create daily product folder, if it doesn't exist
        try:
            if( not os.path.isdir(product_date_dir) ):
                os.mkdir(product_date_dir)
        except:
            arcpy.AddMessage("..FAILED TO CREATE DAILY PRODUCTS FOLDER")

        #Create GEO folder, if it doesn't exist
        if(export == "GEO"):
            try:
                if( not os.path.isdir(geo_dir) ):
                    os.mkdir(geo_dir)
            except:
                arcpy.AddMessage("..FAILED TO CREATE GEO FOLDER")

        #Create IMAGE folder, if it doesn't exist
        if(export == "IMAGE"):
            try:
                if( not os.path.isdir(image_dir) ):
                    os.mkdir(image_dir)
            except:
                arcpy.AddMessage("..FAILED TO CREATE IMAGE FOLDER")

        #Create GEOIMAGE folder, if it doesn't exist
        if(export == "GEOIMAGE"):
            try:
                if( not os.path.isdir(geoimage_dir) ):
                    os.mkdir(geoimage_dir)
            except:
                arcpy.AddMessage("..FAILED TO CREATE GEOIMAGE FOLDER")



        if(filename == "GEO OPS"):
            if(geoops_period == ""):
                if(export_label == "YES - PREFIX"):
                    pdf_geo_outpath = geo_dir + "/GEO_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                    pdf_image_outpath = image_dir + "/IMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                    pdf_geoimage_outpath = geoimage_dir + "/GEOIMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                if(export_label == "YES - SUFFIX"):
                    pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_GEO.pdf"
                    pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_IMAGE.pdf"
                    pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_GEOIMAGE.pdf"
                if(export_label == "NO"):
                    pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                    pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                    pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"

            if(geoops_period != ""):
                if(export_label == "YES - PREFIX"):
                    pdf_geo_outpath = geo_dir + "/GEO_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                    pdf_image_outpath = image_dir + "/IMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                    pdf_geoimage_outpath = geoimage_dir + "/GEOIMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                if(export_label == "YES - SUFFIX"):
                    pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + "_GEO.pdf"
                    pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + "_IMAGE.pdf"
                    pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + "_GEOIMAGE.pdf"
                if(export_label == "NO"):
                    pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                    pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                    pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
        if(filename == "USER SPECIFIED"):
            if(export_label == "YES - PREFIX"):
                pdf_geo_outpath = geo_dir + "/GEO_" + user_specified + ".pdf"
                pdf_image_outpath = image_dir + "/IMAGE_" + user_specified + ".pdf"
                pdf_geoimage_outpath = geoimage_dir + "/GEOIMAGE_" + user_specified + ".pdf"
            if(export_label == "YES - SUFFIX"):
                pdf_geo_outpath = geo_dir + "/" + user_specified + "_GEO.pdf"
                pdf_image_outpath = image_dir + "/" + user_specified + "_IMAGE.pdf"
                pdf_geoimage_outpath = geoimage_dir + "/" + user_specified + "_GEOIMAGE.pdf"
            if(export_label == "NO"):
                pdf_geo_outpath = geo_dir + "/" + user_specified + ".pdf"
                pdf_image_outpath = image_dir + "/" + user_specified + ".pdf"
                pdf_geoimage_outpath = geoimage_dir + "/" + user_specified + ".pdf"



        if(mapseries == False):
            arcpy.AddMessage("..EXPORTING")
        else:
            arcpy.AddMessage("....EXPORTING")


        #If GEO or GEO AND IMAGE was requested, export PDF with georefererence information
        if export in ["GEO", "GEO AND IMAGE"]:
            geo_export_complete = False
            while(geo_export_complete == False):
                try:

                    #If not a map series, perform a regular export
                    if(mapseries == False):
                        arcpy.AddMessage("....GEO EXPORT")
                        lyt.exportToPDF(pdf_geo_outpath, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                        image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                        output_as_image=False, georef_info=True)
                        arcpy.AddMessage("......EXPORT COMPLETE")
                        geo_export_complete = True

                    #If a map series, perform a map series export
                    if(mapseries == True):
                        arcpy.AddMessage("......GEO EXPORT")

                        #If ALL was requested, export all pages
                        if(mapseries_pages == "ALL"):
                            arcpy.AddMessage("........ALL PAGES")
                            lyt.mapSeries.exportToPDF(pdf_geo_outpath, page_range_type=mapseries_pages, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                            image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                            output_as_image=False, georef_info=True)

                        #If RANGE was requested, export range
                        if(mapseries_pages == "RANGE"):
                            arcpy.AddMessage("........PAGES " + mapseries_range_val)
                            lyt.mapSeries.exportToPDF(pdf_geo_outpath, page_range_type=mapseries_pages, page_range_string=mapseries_range_val, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                            image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                            output_as_image=False, georef_info=True)

                        arcpy.AddMessage("..........EXPORT COMPLETE")
                        geo_export_complete = True

                except Exception as e:
                    arcpy.AddMessage(e)
                    arcpy.AddMessage("....FAILED TO PERFORM GEO EXPORT, SKIPPING")
                    geo_export_complete = True


        #If IMAGE or GEO AND IMAGE was requested, export PDF as an image without georeference information
        if export in ["IMAGE", "GEO AND IMAGE"]:
            image_export_complete = False
            while(image_export_complete == False):
                try:

                    #If not a map series, perform a regular export
                    if(mapseries == False):
                        arcpy.AddMessage("....IMAGE EXPORT")
                        lyt.exportToPDF(pdf_image_outpath, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                        image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                        output_as_image=True, georef_info=False)
                        arcpy.AddMessage("......EXPORT COMPLETE")
                        image_export_complete = True

                    #If a map series, perform a map series export
                    if(mapseries == True):
                        arcpy.AddMessage("......IMAGE EXPORT")

                        #If ALL was requested, export all pages
                        if(mapseries_pages == "ALL"):
                            arcpy.AddMessage("........ALL PAGES")
                            lyt.mapSeries.exportToPDF(pdf_image_outpath, page_range_type=mapseries_pages, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                            image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                            output_as_image=True, georef_info=False)

                        #If RANGE was requested, export range
                        if(mapseries_pages == "RANGE"):
                            arcpy.AddMessage("........PAGES " + mapseries_range_val)
                            lyt.mapSeries.exportToPDF(pdf_image_outpath, page_range_type=mapseries_pages, page_range_string=mapseries_range_val, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                            image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                            output_as_image=True, georef_info=False)

                        arcpy.AddMessage("..........EXPORT COMPLETE")
                        image_export_complete = True

                except Exception as e:
                    arcpy.AddMessage(e)
                    arcpy.AddMessage("....FAILED TO PERFORM IMAGE EXPORT, SKIPPING")
                    image_export_complete = True





        #If GEOIMAGE was requested, export PDF as an image and also with georefererence information
        if export == "GEOIMAGE":
            geoimage_export_complete = False
            while(geoimage_export_complete == False):
                try:

                    #If not a map series, perform a regular export
                    if(mapseries == False):
                        arcpy.AddMessage("....GEOIMAGE EXPORT")
                        lyt.exportToPDF(pdf_geoimage_outpath, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                        image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                        georef_info=True, output_as_image=True)
                        arcpy.AddMessage("......EXPORT COMPLETE")
                        geoimage_export_complete = True

                    #If a map series, perform a map series export
                    if(mapseries == True):
                        arcpy.AddMessage("......GEOIMAGE EXPORT")

                        #If ALL was requested, export all pages
                        if(mapseries_pages == "ALL"):
                            arcpy.AddMessage("........ALL PAGES")
                            lyt.mapSeries.exportToPDF(pdf_geoimage_outpath, page_range_type=mapseries_pages, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                            image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                            georef_info=True, output_as_image=True)

                        #If RANGE was requested, export range
                        if(mapseries_pages == "RANGE"):
                            arcpy.AddMessage("........PAGES " + mapseries_range_val)
                            lyt.mapSeries.exportToPDF(pdf_geoimage_outpath, page_range_type=mapseries_pages, page_range_string=mapseries_range_val, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                            image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val, layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val,
                                            georef_info=True, output_as_image=True)

                        arcpy.AddMessage("..........EXPORT COMPLETE")
                        geoimage_export_complete = True

                except Exception as e:
                    arcpy.AddMessage(e)
                    arcpy.AddMessage("....FAILED TO PERFORM GEOIMAGE EXPORT, SKIPPING")
                    geoimage_export_complete = True



        #Add space to separate print text from next export
        arcpy.AddMessage(" ")



#Define function to create pool of processes
def execute(inputs):

    #Set multiprocessing python exe path
    multiprocessing.set_executable(os.path.join(sys.exec_prefix, 'python.exe'))

    #Get cpu count
    #cpucount = multiprocessing.cpu_count() - 1

    #Create pool of workers
    pool = multiprocessing.Pool()

    #Submit jobs to workers
    for curr_input in inputs:
        pool.imap_unordered(worker_function, [curr_input]) # args are passed as a list

    pool.close()
    pool.join()





if __name__=="__main__":

    #Specify incident name, unit id, and incident number
    #incident_name = "Windy"
    incident_name = arcpy.GetParameterAsText(0)

    #incident_id = "CA-TIA-003058"
    incident_id = arcpy.GetParameterAsText(1)

    #Specify the products directory
    #products_dir = r"C:\Workspace\FireNet\2021_CATIA_Windy - GIS Data\2021_Windy\products"
    products_dir = arcpy.GetParameterAsText(2)

    #Specify the path to the "ExportPDFtable.xlsx" file
    #export_table_xlsx_path = r"C:\Workspace\development\PanunTools_All\PDFMultiExport.xlsx"
    #export_table_xlsx_path = r"C:\Workspace\FireNet\2021_CATIA_Windy - GIS Data\2021_Windy\tools\PanunTools-main\MultiExportPDF_MP.xlsx"
    export_table_xlsx_path = arcpy.GetParameterAsText(3)

    #Toggle for Multiprocessor use
    #multiprocess_toggle = "false"
    multiprocess_toggle = arcpy.GetParameterAsText(4)


    import PDFMultiExport

    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("PDF Multi Export tool developed by Matt Panunto, DOI-BLM")

    #Get toolbox version
    scriptpath = sys.argv[0]
    scriptdirpath = os.path.dirname(scriptpath)
    tbxpath = scriptdirpath + "/PanunTools.tbx"
    tbximport = arcpy.ImportToolbox(tbxpath)
    tbxversion = arcpy.Usage(tbximport)

    #Test if current PanunTools version is up to date
    githuburl = "https://github.com/mpanunto/PanunTools"
    try:
        github_page = urlopen(githuburl)
        github_html_bytes = github_page.read()
        github_html = github_html_bytes.decode("utf-8")
        github_html_split = github_html.split("Latest version is ")
        github_version = github_html_split[1][:9]
        if(int(github_version[1:]) > int(tbxversion[1:])):
            arcpy.AddWarning("New version of PanunTools available (" + github_version + ") at https://github.com/mpanunto/PanunTools")
    except:
        "skip"


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
        export_table_df = pandas.read_excel(export_table_xlsx_path, sheet_name="ExportTable")
    except:
        arcpy.AddError("UNABLE TO READ PDF MULTI EXPORT SPREADSHEET, CHECK TO MAKE SURE IT ISN'T CURRENTLY OPEN")
        raise arcpy.ExecuteError


    #Create list of EXPORT values from the spreadsheet
    export_col = list(export_table_df["EXPORT"])

    #Get count of how many items need processing, and also determine which items
    processing_needed_list = []
    processing_needed_which_list = []
    for i in range(0, len(export_col)):
        curr_str = export_col[i]
        export_check = any(x in curr_str for x in ["IMAGE", "GEO", "GEOIMAGE", "GEO AND IMAGE"])
        if(export_check == True):
            processing_needed_list.append(1)
            processing_needed_which_list.append(i)
        else:
            processing_needed_list.append(0)
    processing_count = len(processing_needed_which_list)

    #Create lists for export request and filename information
    export_list = [list(map(str, export_table_df["EXPORT"]))[i] for i in processing_needed_which_list]
    productsdate_list = [list(map(str, export_table_df["PRODUCTS_DATE"]))[i] for i in processing_needed_which_list]

    #Create lists for file naming
    filename_list = [list(map(str, export_table_df["FILENAME"]))[i] for i in processing_needed_which_list]
    user_specified_list = [list(map(str, export_table_df["USER_SPECIFIED"]))[i] for i in processing_needed_which_list]
    geoops_maptype_list = [list(map(str, export_table_df["GEOOPS_MAPTYPE"]))[i] for i in processing_needed_which_list]
    geoops_pagesize_list = [list(map(str, export_table_df["GEOOPS_PAGESIZE"]))[i] for i in processing_needed_which_list]
    geoops_orientation_list = [list(map(str, export_table_df["GEOOPS_ORIENTATION"]))[i] for i in processing_needed_which_list]
    geoops_period_list = [list(map(str, export_table_df["GEOOPS_PERIOD"]))[i] for i in processing_needed_which_list]
    exportlabel_list = [list(map(str, export_table_df["EXPORT_LABEL"]))[i] for i in processing_needed_which_list]

    #Create lists for Map Series export settings
    mapseries_pages_list = [list(export_table_df["MAPSERIES_PAGES"])[i] for i in processing_needed_which_list]
    mapseries_range_list = [list(export_table_df["MAPSERIES_RANGE"])[i] for i in processing_needed_which_list]
    mapseries_files_list = [list(export_table_df["MAPSERIES_FILES"])[i] for i in processing_needed_which_list]

    #Create lists of export settings
    clipgraphics_list = [list(export_table_df["CLIP_GRAPHICS_EXTENT"])[i] for i in processing_needed_which_list]
    imagecompress_list = [list(map(str, export_table_df["IMAGE_COMPRESSION"]))[i] for i in processing_needed_which_list]
    imagecompressquality_list = [list(map(int, export_table_df["IMAGE_COMPRESSION_QUALITY"]))[i] for i in processing_needed_which_list]
    compressvectorgraphics_list = [list(export_table_df["COMPRESS_VECTOR_GRAPHICS"])[i] for i in processing_needed_which_list]
    vectorresolution_list = [list(map(int, export_table_df["VECTOR_RESOLUTION"]))[i] for i in processing_needed_which_list]
    rasterresample_list = [list(map(str, export_table_df["RASTER_RESAMPLE"]))[i] for i in processing_needed_which_list]
    embedfonts_list = [list(export_table_df["EMBED_FONTS"])[i] for i in processing_needed_which_list]
    layersattributes_list = [list(map(str, export_table_df["LAYERS_ATTRIBUTES"]))[i] for i in processing_needed_which_list]

    #Create lists for the Layout name and APRX Path
    layoutname_list = [list(map(str, export_table_df["LAYOUT_NAME"]))[i] for i in processing_needed_which_list]
    aprxpath_list = [list(map(str, export_table_df["APRX_PATH"]))[i] for i in processing_needed_which_list]

    #Create lists of user specified inputs
    incidentname_list = [incident_name] * processing_count
    unitid_list = [unit_id] * processing_count
    incidentnumber_list = [incident_number] * processing_count
    productsdir_list = [products_dir] * processing_count

    inputs_list = list(map(list, zip(incidentname_list, unitid_list, incidentnumber_list, productsdir_list,
                export_list, productsdate_list, filename_list, user_specified_list, geoops_maptype_list, geoops_pagesize_list, geoops_orientation_list, geoops_period_list, exportlabel_list,
                mapseries_pages_list, mapseries_range_list, mapseries_files_list,
                clipgraphics_list, imagecompress_list, imagecompressquality_list, compressvectorgraphics_list, vectorresolution_list, rasterresample_list, embedfonts_list, layersattributes_list,
                layoutname_list, aprxpath_list)))

    #Create new inputs_list by finding any export requests that are BOTH
    #Need to split these into separate list elements of AVENZA and IMAGE to speed up multiprocessing
    inputs_list_multiprocess = []
    for i in range(0, len(inputs_list)):

        curr_input_list = list(inputs_list[i])
        curr_input_list_geo = list(inputs_list[i])
        curr_input_list_geo[4] = "GEO"
        curr_input_list_image = list(inputs_list[i])
        curr_input_list_image[4] = "IMAGE"

        curr_export = curr_input_list[4]

        if(curr_export == "GEO"):
            inputs_list_multiprocess.append(curr_input_list)

        if(curr_export == "IMAGE"):
            inputs_list_multiprocess.append(curr_input_list)

        if(curr_export == "GEOIMAGE"):
            inputs_list_multiprocess.append(curr_input_list)

        if(curr_export == "GEO AND IMAGE"):
            inputs_list_multiprocess.append(curr_input_list_geo)
            inputs_list_multiprocess.append(curr_input_list_image)




    #Export maps. Use multiprocessor if user enabled it, else export one map at a time.
    if(multiprocess_toggle == "true"):
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("Begin multiprocessing")
        PDFMultiExport.execute(inputs_list_multiprocess)
        arcpy.AddMessage("..Finished multiprocessing")

    else:
        for i in range(0, len(inputs_list)):
            arcpy.AddMessage("\u200B")
            arcpy.AddMessage("EXPORT REQUEST " + str(i+1) + " OUT OF " + str(len(inputs_list)))
            curr_inputs_list = inputs_list[i]
            worker_function(curr_inputs_list)

    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Done!")

