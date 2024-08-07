#Due to printing issues with PDFs exported from ArcGIS Pro, this script was designed with the assumption
#that two separate exports are often needed for each map: one for printing, and one for Avenza use.
#The spreadsheet allows users to customize their export settings for each of these two separate PDFs.
#The spreadsheet also allows users to specify whether one, both, or neither exports are needed for a map.
#Additionally, this script can be used to update the map date, but only if the layout is using dynamictext from
#the summary field of the map's properties

#This script uses the Python multiprocessing module to run several instances of Python simultaneously. It is
#similar to openening numerous .arpx files at once in order to export multiple PDFs are the same time.

#Import libraries
libraries_check = False
libraries_attempt = 1
while(libraries_check == False):
    try:
        print("Importing Libraries")
        print(" ")
        import arcpy, pandas, time, datetime, os, sys, multiprocessing, random, ftplib, glob, shutil
        from urllib.request import urlopen
        from multiprocessing import Pool, freeze_support
        libraries_check = True

    except Exception as e:

        #Need to use print() here, because the arcpy library may not have been imported
        print(e)
        libraries_attempt = libraries_attempt + 1
        if(libraries_attempt < 6):
            print("........LIBRARY IMPORT FAILED, RE-TRYING")
            time.sleep(5)
        if(libraries_attempt >= 6):
            print("........LIBRARY IMPORT FAILED 5 TIMES, QUITTING")
            time.sleep(60)

#There is a reported bug in Python
#Apply the patch in a new class
#Reference: https://stackoverflow.com/questions/33438456/python-ftps-upload-error-425-unable-to-build-data-connection-operation-not-per
class Explicit_FTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session"""
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname=self.host, session=self.sock.session)
        return conn, size

#Define function to export PDFs
def worker_function(in_inputs_list):

    try:

        export_count = len(in_inputs_list)

        if(export_count > 0):
            arcpy.AddMessage("\u200B")
            arcpy.AddMessage("EXPORTING")

        exportrequest_val_list = []
        exportrequest_dupe_val_list = []
        exportrequest_label_val_list = []
        pdf_path_val_list = []
        pdf_prefix_val_list = []
        ftpupload_val_list = []
        ftpuploadrequest_val_list = []
        ftpfilename_val_list = []
        ftp_user_specified_val_list = []
        ftpuploaddir_val_list = []
        for i in range(0, len(in_inputs_list)):

            curr_in_inputs_list = in_inputs_list[i]

            incidentname = curr_in_inputs_list[0]
            unitid = curr_in_inputs_list[1]
            incidentnumber = curr_in_inputs_list[2]
            productdir = curr_in_inputs_list[3]
            projectstoggle = curr_in_inputs_list[4]
            projectsdir = curr_in_inputs_list[5]

            ftpupload_toggle_val = curr_in_inputs_list[6]
            ftp_username_val = curr_in_inputs_list[7]
            ftp_password_val = curr_in_inputs_list[8]
            multiprocess_toggle_val = curr_in_inputs_list[9]
            export = curr_in_inputs_list[10]
            exportrequest = curr_in_inputs_list[11]
            exportrequest_dupe = curr_in_inputs_list[12]
            proddate = curr_in_inputs_list[13]

            exportfilename = curr_in_inputs_list[14]
            export_user_specified = curr_in_inputs_list[15]
            geoops_maptype = curr_in_inputs_list[16]
            geoops_pagesize = curr_in_inputs_list[17]
            geoops_orientation = curr_in_inputs_list[18]
            geoops_period = curr_in_inputs_list[19]
            exportrequest_label = curr_in_inputs_list[20]

            mapseries_pages = curr_in_inputs_list[21]
            mapseries_range = curr_in_inputs_list[22]
            mapseries_files = curr_in_inputs_list[23]

            ftpupload_val = curr_in_inputs_list[24]
            ftpuploadrequest_val = curr_in_inputs_list[25]
            ftpfilename_val = curr_in_inputs_list[26]
            ftp_user_specified_val = curr_in_inputs_list[27]
            ftpuploaddir_val = curr_in_inputs_list[28]

            clipgraphics_val = curr_in_inputs_list[29]
            removelayoutbackground_val = curr_in_inputs_list[30]
            imagecompress_val = curr_in_inputs_list[31]
            imagecompressquality_val = int(curr_in_inputs_list[32])
            compressvectorgraphics_val = curr_in_inputs_list[33]
            vectorresolution_val = int(curr_in_inputs_list[34])
            rasterresample_val = curr_in_inputs_list[35]
            embedfonts_val = curr_in_inputs_list[36]
            convertmarkers_val = curr_in_inputs_list[37]
            layersattributes_val = curr_in_inputs_list[38]
            simulateoverprint_val = curr_in_inputs_list[39]
            embedcolorprofile_val = curr_in_inputs_list[40]
            pdfaccessibility_val = curr_in_inputs_list[41]

            layoutname = curr_in_inputs_list[42]
            aprxfilename = curr_in_inputs_list[43]
            aprxpath = curr_in_inputs_list[44]

            #For some reason, the multiprocessor doesn't like the boolean values read from the spreadsheet, it seems
            #to be reading them in as strings instead of bools. Ensuring the values are bool here.
            if(clipgraphics_val == "True"):
                clipgraphics_val = True
            if(clipgraphics_val == "False"):
                clipgraphics_val = False
            if(compressvectorgraphics_val == "True"):
                compressvectorgraphics_val = True
            if(compressvectorgraphics_val == "False"):
                compressvectorgraphics_val = False
            if(embedfonts_val == "True"):
                embedfonts_val = True
            if(embedfonts_val == "False"):
                embedfonts_val = False

            #If export was requested, proceed
            if export == "YES":

                if(exportrequest in ["GEO AND IMAGE", "GEO AND GEOIMAGE"] and exportrequest_label == "NO" and ftpupload_val == "YES" and ftpuploadrequest_val in ["GEO AND IMAGE", "GEO AND GEOIMAGE"]):
                    exportrequest_label = "YES - PREFIX"

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
                if(len(geoops_str) > 0):
                    if(geoops_str[0] == "_"):
                        geoops_str = geoops_str[1:]

                #Print the current export being processed
                if(exportfilename == "GEO OPS"):
                    arcpy.AddMessage(".." + geoops_str + " (" + str(i+1) + " out of " + str(export_count) + ")")
                if(exportfilename == "USER SPECIFIED"):
                    arcpy.AddMessage(".." + export_user_specified + " (" + str(i+1) + " out of " + str(export_count) + ")")

                #Create aprxpath variable
                #If user selected "Specify Incident 'projects' Directory", need to concatenate the aprxfilename with the
                #user specified projects directory
                if(projectstoggle == "Specify Incident 'projects' Directory"):
                    aprxpath = projectsdir + "/" + aprxfilename
                else:
                    aprxpath = aprxpath


                #First check to make sure the aprx path is good
                aprx_check = arcpy.Exists(aprxpath)

                #If aprx exists, read-in, else throw error
                if(aprx_check == True):
                    aprx = arcpy.mp.ArcGISProject(aprxpath)
                else:
                    arcpy.AddMessage("....APRX NOT FOUND AT USER SPECIFIED PATH:")
                    arcpy.AddMessage(aprxpath)
                    raise arcpy.ExecuteError

                #Now test to see if layout exists, throw error if not
                layoutname_check = (len(aprx.listLayouts(layoutname)) == 1)
                if(layoutname_check == False):
                    arcpy.AddMessage("....LAYOUT NAME NOT FOUND IN APRX, CHECK SPELLING: " + layoutname)
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
                    arcpy.AddMessage("....MAP SERIES LAYOUT")

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
                    arcpy.AddMessage("....FAILED TO CREATE DAILY PRODUCTS FOLDER")

                #Create GEO folder, if it doesn't exist
                if(exportrequest in ["GEO", "GEO AND IMAGE", "GEO AND GEOIMAGE"]):
                    try:
                        if( not os.path.isdir(geo_dir) ):
                            os.mkdir(geo_dir)
                    except:
                        arcpy.AddMessage("....FAILED TO CREATE GEO FOLDER")

                #Create IMAGE folder, if it doesn't exist
                if(exportrequest in ["IMAGE", "GEO AND IMAGE"]):
                    try:
                        if( not os.path.isdir(image_dir) ):
                            os.mkdir(image_dir)
                    except:
                        arcpy.AddMessage("....FAILED TO CREATE IMAGE FOLDER")

                #Create GEOIMAGE folder, if it doesn't exist
                if(exportrequest in ["GEOIMAGE", "GEO AND GEOIMAGE"]):
                    try:
                        if( not os.path.isdir(geoimage_dir) ):
                            os.mkdir(geoimage_dir)
                    except:
                        arcpy.AddMessage("....FAILED TO CREATE GEOIMAGE FOLDER")



                if(exportfilename == "GEO OPS"):
                    if(geoops_period == ""):
                        if(exportrequest_label == "YES - PREFIX"):
                            pdf_geo_outpath = geo_dir + "/GEO_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                            pdf_image_outpath = image_dir + "/IMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                            pdf_geoimage_outpath = geoimage_dir + "/GEOIMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                        if(exportrequest_label == "YES - SUFFIX"):
                            pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_GEO.pdf"
                            pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_IMAGE.pdf"
                            pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_GEOIMAGE.pdf"
                        if(exportrequest_label == "NO"):
                            pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                            pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"
                            pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + ".pdf"

                    if(geoops_period != ""):
                        if(exportrequest_label == "YES - PREFIX"):
                            pdf_geo_outpath = geo_dir + "/GEO_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                            pdf_image_outpath = image_dir + "/IMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                            pdf_geoimage_outpath = geoimage_dir + "/GEOIMAGE_" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                        if(exportrequest_label == "YES - SUFFIX"):
                            pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + "_GEO.pdf"
                            pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + "_IMAGE.pdf"
                            pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + "_GEOIMAGE.pdf"
                        if(exportrequest_label == "NO"):
                            pdf_geo_outpath = geo_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                            pdf_image_outpath = image_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"
                            pdf_geoimage_outpath = geoimage_dir + "/" + geoops_str + "_" + curr_datetime_str + "_" + incidentname + "_" + unitid + incidentnumber + "_" + geoops_period + ".pdf"

                if(exportfilename == "USER SPECIFIED"):
                    if(exportrequest_label == "YES - PREFIX"):
                        pdf_geo_outpath = geo_dir + "/GEO_" + export_user_specified + ".pdf"
                        pdf_image_outpath = image_dir + "/IMAGE_" + export_user_specified + ".pdf"
                        pdf_geoimage_outpath = geoimage_dir + "/GEOIMAGE_" + export_user_specified + ".pdf"
                    if(exportrequest_label == "YES - SUFFIX"):
                        pdf_geo_outpath = geo_dir + "/" + export_user_specified + "_GEO.pdf"
                        pdf_image_outpath = image_dir + "/" + export_user_specified + "_IMAGE.pdf"
                        pdf_geoimage_outpath = geoimage_dir + "/" + export_user_specified + "_GEOIMAGE.pdf"
                    if(exportrequest_label == "NO"):
                        pdf_geo_outpath = geo_dir + "/" + export_user_specified + ".pdf"
                        pdf_image_outpath = image_dir + "/" + export_user_specified + ".pdf"
                        pdf_geoimage_outpath = geoimage_dir + "/" + export_user_specified + ".pdf"



                #If GEO or GEO AND IMAGE was requested, export PDF with georefererence information
                if exportrequest in ["GEO", "GEO AND IMAGE", "GEO AND GEOIMAGE"]:
                    geo_export_complete = False
                    while(geo_export_complete == False):
                        try:

                            #If not a map series, perform a regular export
                            if(mapseries == False):
                                arcpy.AddMessage("....GEO EXPORT")
                                lyt.exportToPDF(pdf_geo_outpath, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                output_as_image=False, georef_info=True)
                                #arcpy.AddMessage("......EXPORT COMPLETE")
                                geo_export_complete = True

                                #Append export paths and ftp parameters to lists
                                exportrequest_val_list.append(exportrequest)
                                exportrequest_dupe_val_list.append(exportrequest_dupe)
                                exportrequest_label_val_list.append(exportrequest_label)
                                pdf_path_val_list.append(pdf_geo_outpath)
                                pdf_prefix_val_list.append("GEO")
                                ftpupload_val_list.append(ftpupload_val)
                                ftpuploadrequest_val_list.append(ftpuploadrequest_val)
                                ftpfilename_val_list.append(ftpfilename_val)
                                ftp_user_specified_val_list.append(ftp_user_specified_val)
                                ftpuploaddir_val_list.append(ftpuploaddir_val)

                            #If a map series, perform a map series export
                            if(mapseries == True):
                                arcpy.AddMessage("......GEO EXPORT")

                                #If ALL was requested, export all pages
                                if(mapseries_pages == "ALL"):
                                    arcpy.AddMessage("........ALL PAGES")
                                    lyt.mapSeries.exportToPDF(pdf_geo_outpath, page_range_type=mapseries_pages, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                    image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                    layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                    pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                    output_as_image=False, georef_info=True)

                                #If RANGE was requested, export range
                                if(mapseries_pages == "RANGE"):
                                    arcpy.AddMessage("........PAGES " + mapseries_range_val)
                                    lyt.mapSeries.exportToPDF(pdf_geo_outpath, page_range_type=mapseries_pages, page_range_string=mapseries_range_val, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                    image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                    layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                    pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                    output_as_image=False, georef_info=True)

                                #arcpy.AddMessage("..........EXPORT COMPLETE")
                                geo_export_complete = True

                                #Get paths to all the map series exports
                                mapseries_dirname = os.path.dirname(pdf_geo_outpath)
                                mapseries_basename = os.path.basename(pdf_geo_outpath)
                                mapseries_basename = mapseries_basename.replace(".pdf", "")
                                mapseries_pattern = "*" + mapseries_basename + "*"
                                mapseries_pdf_path_val_list = glob.glob(mapseries_dirname + "/" + mapseries_pattern)

                                #Create lists of map series ftp parameters
                                mapseries_ftp_user_specified_val_list = []
                                for j in range(0, len(mapseries_pdf_path_val_list)):
                                    curr_mapseries_export_pdf_path = mapseries_pdf_path_val_list[j]
                                    curr_mapseries_dirname = os.path.dirname(curr_mapseries_export_pdf_path)
                                    curr_mapseries_basename = os.path.basename(curr_mapseries_export_pdf_path)
                                    curr_suffix = curr_mapseries_basename.replace(mapseries_basename, "")
                                    curr_ftp_user_specified_val = ftp_user_specified_val + curr_suffix
                                    mapseries_ftp_user_specified_val_list.append(curr_ftp_user_specified_val)
                                mapseries_exportrequest_val_list = [exportrequest] * len(mapseries_pdf_path_val_list)
                                mapseries_exportrequest_dupe_val_list = [exportrequest_dupe] * len(mapseries_pdf_path_val_list)
                                mapseries_exportrequest_label_val_list = [exportrequest_label] * len(mapseries_pdf_path_val_list)
                                mapseries_pdf_prefix_val_list = ["GEO"] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpupload_val_list = [ftpupload_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpuploadrequest_val_list = [ftpuploadrequest_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpfilename_val_list = [ftpfilename_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpuploaddir_val_list = [ftpuploaddir_val] * len(mapseries_pdf_path_val_list)

                                #Append map series export paths and ftp parameters to lists
                                exportrequest_val_list = exportrequest_val_list + mapseries_exportrequest_val_list
                                exportrequest_dupe_val_list = exportrequest_dupe_val_list + mapseries_exportrequest_dupe_val_list
                                exportrequest_label_val_list = exportrequest_label_val_list + mapseries_exportrequest_label_val_list
                                pdf_path_val_list = pdf_path_val_list + mapseries_pdf_path_val_list
                                pdf_prefix_val_list = pdf_prefix_val_list + mapseries_pdf_prefix_val_list
                                ftpupload_val_list = ftpupload_val_list + mapseries_ftpupload_val_list
                                ftpuploadrequest_val_list = ftpuploadrequest_val_list + mapseries_ftpuploadrequest_val_list
                                ftpfilename_val_list = ftpfilename_val_list + mapseries_ftpfilename_val_list
                                ftp_user_specified_val_list = ftp_user_specified_val_list + mapseries_ftp_user_specified_val_list
                                ftpuploaddir_val_list = ftpuploaddir_val_list + mapseries_ftpuploaddir_val_list

                        except Exception as e:
                            arcpy.AddMessage(e)
                            arcpy.AddMessage("......FAILED TO PERFORM GEO EXPORT, SKIPPING")
                            geo_export_complete = True


                #If IMAGE or GEO AND IMAGE was requested, export PDF as an image without georeference information
                if exportrequest in ["IMAGE", "GEO AND IMAGE"]:
                    image_export_complete = False
                    while(image_export_complete == False):
                        try:

                            #If not a map series, perform a regular export
                            if(mapseries == False):
                                arcpy.AddMessage("....IMAGE EXPORT")
                                lyt.exportToPDF(pdf_image_outpath, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                output_as_image=True, georef_info=False)
                                #arcpy.AddMessage("......EXPORT COMPLETE")
                                image_export_complete = True

                                #Append export paths and ftp parameters to lists
                                exportrequest_val_list.append(exportrequest)
                                exportrequest_dupe_val_list.append(exportrequest_dupe)
                                exportrequest_label_val_list.append(exportrequest_label)
                                pdf_path_val_list.append(pdf_image_outpath)
                                pdf_prefix_val_list.append("IMAGE")
                                ftpupload_val_list.append(ftpupload_val)
                                ftpuploadrequest_val_list.append(ftpuploadrequest_val)
                                ftpfilename_val_list.append(ftpfilename_val)
                                ftp_user_specified_val_list.append(ftp_user_specified_val)
                                ftpuploaddir_val_list.append(ftpuploaddir_val)

                            #If a map series, perform a map series export
                            if(mapseries == True):
                                arcpy.AddMessage("......IMAGE EXPORT")

                                #If ALL was requested, export all pages
                                if(mapseries_pages == "ALL"):
                                    arcpy.AddMessage("........ALL PAGES")
                                    lyt.mapSeries.exportToPDF(pdf_image_outpath, page_range_type=mapseries_pages, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                    image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                    layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                    pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                    output_as_image=True, georef_info=False)

                                #If RANGE was requested, export range
                                if(mapseries_pages == "RANGE"):
                                    arcpy.AddMessage("........PAGES " + mapseries_range_val)
                                    lyt.mapSeries.exportToPDF(pdf_image_outpath, page_range_type=mapseries_pages, page_range_string=mapseries_range_val, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                    image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                    layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                    pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                    output_as_image=True, georef_info=False)

                                #arcpy.AddMessage("..........EXPORT COMPLETE")
                                image_export_complete = True

                                #Get paths to all the map series exports
                                mapseries_dirname = os.path.dirname(pdf_image_outpath)
                                mapseries_basename = os.path.basename(pdf_image_outpath)
                                mapseries_basename = mapseries_basename.replace(".pdf", "")
                                mapseries_pattern = "*" + mapseries_basename + "*"
                                mapseries_pdf_path_val_list = glob.glob(mapseries_dirname + "/" + mapseries_pattern)

                                #Create lists of map series ftp parameters
                                mapseries_ftp_user_specified_val_list = []
                                for j in range(0, len(mapseries_pdf_path_val_list)):
                                    curr_mapseries_export_pdf_path = mapseries_pdf_path_val_list[j]
                                    curr_mapseries_dirname = os.path.dirname(curr_mapseries_export_pdf_path)
                                    curr_mapseries_basename = os.path.basename(curr_mapseries_export_pdf_path)
                                    curr_suffix = curr_mapseries_basename.replace(mapseries_basename, "")
                                    curr_ftp_user_specified_val = ftp_user_specified_val + curr_suffix
                                    mapseries_ftp_user_specified_val_list.append(curr_ftp_user_specified_val)
                                mapseries_exportrequest_val_list = [exportrequest] * len(mapseries_pdf_path_val_list)
                                mapseries_exportrequest_dupe_val_list = [exportrequest_dupe] * len(mapseries_pdf_path_val_list)
                                mapseries_exportrequest_label_val_list = [exportrequest_label] * len(mapseries_pdf_path_val_list)
                                mapseries_pdf_prefix_val_list = ["IMAGE"] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpupload_val_list = [ftpupload_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpuploadrequest_val_list = [ftpuploadrequest_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpfilename_val_list = [ftpfilename_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpuploaddir_val_list = [ftpuploaddir_val] * len(mapseries_pdf_path_val_list)

                                #Append map series export paths and ftp parameters to lists
                                exportrequest_val_list = exportrequest_val_list + mapseries_exportrequest_val_list
                                exportrequest_dupe_val_list = exportrequest_dupe_val_list + mapseries_exportrequest_dupe_val_list
                                exportrequest_label_val_list = exportrequest_label_val_list + mapseries_exportrequest_label_val_list
                                pdf_path_val_list = pdf_path_val_list + mapseries_pdf_path_val_list
                                pdf_prefix_val_list = pdf_prefix_val_list + mapseries_pdf_prefix_val_list
                                ftpupload_val_list = ftpupload_val_list + mapseries_ftpupload_val_list
                                ftpuploadrequest_val_list = ftpuploadrequest_val_list + mapseries_ftpuploadrequest_val_list
                                ftpfilename_val_list = ftpfilename_val_list + mapseries_ftpfilename_val_list
                                ftp_user_specified_val_list = ftp_user_specified_val_list + mapseries_ftp_user_specified_val_list
                                ftpuploaddir_val_list = ftpuploaddir_val_list + mapseries_ftpuploaddir_val_list

                        except Exception as e:
                            arcpy.AddMessage(e)
                            arcpy.AddMessage("......FAILED TO PERFORM IMAGE EXPORT, SKIPPING")
                            image_export_complete = True


                #If GEOIMAGE was requested, export PDF as an image and also with georefererence information
                if exportrequest in ["GEOIMAGE", "GEO AND GEOIMAGE"]:
                    geoimage_export_complete = False
                    while(geoimage_export_complete == False):
                        try:

                            #If not a map series, perform a regular export
                            if(mapseries == False):
                                arcpy.AddMessage("....GEOIMAGE EXPORT")
                                lyt.exportToPDF(pdf_geoimage_outpath, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                georef_info=True, output_as_image=True)
                                #arcpy.AddMessage("......EXPORT COMPLETE")
                                geoimage_export_complete = True

                                #Append export paths and ftp parameters to lists
                                exportrequest_val_list.append(exportrequest)
                                exportrequest_dupe_val_list.append(exportrequest_dupe)
                                exportrequest_label_val_list.append(exportrequest_label)
                                pdf_path_val_list.append(pdf_geoimage_outpath)
                                pdf_prefix_val_list.append("GEOIMAGE")
                                ftpupload_val_list.append(ftpupload_val)
                                ftpuploadrequest_val_list.append(ftpuploadrequest_val)
                                ftpfilename_val_list.append(ftpfilename_val)
                                ftp_user_specified_val_list.append(ftp_user_specified_val)
                                ftpuploaddir_val_list.append(ftpuploaddir_val)

                            #If a map series, perform a map series export
                            if(mapseries == True):
                                arcpy.AddMessage("......GEOIMAGE EXPORT")

                                #If ALL was requested, export all pages
                                if(mapseries_pages == "ALL"):
                                    arcpy.AddMessage("........ALL PAGES")
                                    lyt.mapSeries.exportToPDF(pdf_geoimage_outpath, page_range_type=mapseries_pages, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                    image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                    layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                    pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                    georef_info=True, output_as_image=True)

                                #If RANGE was requested, export range
                                if(mapseries_pages == "RANGE"):
                                    arcpy.AddMessage("........PAGES " + mapseries_range_val)
                                    lyt.mapSeries.exportToPDF(pdf_geoimage_outpath, page_range_type=mapseries_pages, page_range_string=mapseries_range_val, multiple_files=multiple_files_val, resolution=vectorresolution_val, image_quality=rasterresample_val, compress_vector_graphics=compressvectorgraphics_val,
                                                    image_compression=imagecompress_val, jpeg_compression_quality=imagecompressquality_val, embed_fonts=embedfonts_val,
                                                    layers_attributes=layersattributes_val, clip_to_elements=clipgraphics_val, embed_color_profile=embedcolorprofile_val,
                                                    pdf_accessibility=pdfaccessibility_val, keep_layout_background=removelayoutbackground_val, convert_markers=convertmarkers_val, simulate_overprint=simulateoverprint_val,
                                                    georef_info=True, output_as_image=True)

                                #arcpy.AddMessage("..........EXPORT COMPLETE")
                                geoimage_export_complete = True

                                #Get paths to all the map series exports
                                mapseries_dirname = os.path.dirname(pdf_geoimage_outpath)
                                mapseries_basename = os.path.basename(pdf_geoimage_outpath)
                                mapseries_basename = mapseries_basename.replace(".pdf", "")
                                mapseries_pattern = "*" + mapseries_basename + "*"
                                mapseries_pdf_path_val_list = glob.glob(mapseries_dirname + "/" + mapseries_pattern)

                                #Create lists of map series ftp parameters
                                mapseries_ftp_user_specified_val_list = []
                                for j in range(0, len(mapseries_pdf_path_val_list)):
                                    curr_mapseries_export_pdf_path = mapseries_pdf_path_val_list[j]
                                    curr_mapseries_dirname = os.path.dirname(curr_mapseries_export_pdf_path)
                                    curr_mapseries_basename = os.path.basename(curr_mapseries_export_pdf_path)
                                    curr_suffix = curr_mapseries_basename.replace(mapseries_basename, "")
                                    curr_ftp_user_specified_val = ftp_user_specified_val + curr_suffix
                                    mapseries_ftp_user_specified_val_list.append(curr_ftp_user_specified_val)
                                mapseries_exportrequest_val_list = [exportrequest] * len(mapseries_pdf_path_val_list)
                                mapseries_exportrequest_dupe_val_list = [exportrequest_dupe] * len(mapseries_pdf_path_val_list)
                                mapseries_exportrequest_label_val_list = [exportrequest_label] * len(mapseries_pdf_path_val_list)
                                mapseries_pdf_prefix_val_list = ["GEOIMAGE"] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpupload_val_list = [ftpupload_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpuploadrequest_val_list = [ftpuploadrequest_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpfilename_val_list = [ftpfilename_val] * len(mapseries_pdf_path_val_list)
                                mapseries_ftpuploaddir_val_list = [ftpuploaddir_val] * len(mapseries_pdf_path_val_list)

                                #Append map series export paths and ftp parameters to lists
                                exportrequest_val_list = exportrequest_val_list + mapseries_exportrequest_val_list
                                exportrequest_dupe_val_list = exportrequest_dupe_val_list + mapseries_exportrequest_dupe_val_list
                                exportrequest_label_val_list = exportrequest_label_val_list + mapseries_exportrequest_label_val_list
                                pdf_path_val_list = pdf_path_val_list + mapseries_pdf_path_val_list
                                pdf_prefix_val_list = pdf_prefix_val_list + mapseries_pdf_prefix_val_list
                                ftpupload_val_list = ftpupload_val_list + mapseries_ftpupload_val_list
                                ftpuploadrequest_val_list = ftpuploadrequest_val_list + mapseries_ftpuploadrequest_val_list
                                ftpfilename_val_list = ftpfilename_val_list + mapseries_ftpfilename_val_list
                                ftp_user_specified_val_list = ftp_user_specified_val_list + mapseries_ftp_user_specified_val_list
                                ftpuploaddir_val_list = ftpuploaddir_val_list + mapseries_ftpuploaddir_val_list

                        except Exception as e:
                            arcpy.AddMessage(e)
                            arcpy.AddMessage("......FAILED TO PERFORM GEOIMAGE EXPORT, SKIPPING")
                            geoimage_export_complete = True

    except Exception as e:
        arcpy.AddMessage(e)
        time.sleep(60)



    #Upload maps to FTP
    if(ftpupload_toggle_val == "Yes" and "YES" in ftpupload_val_list):

        #Loop through each export
        prefix_match_check_list = []
        ftpupload_check_list = []
        for i in range(0, len(ftpupload_val_list)):
            curr_ftpupload_val = ftpupload_val_list[i]
            curr_exportrequest = exportrequest_val_list[i]
            curr_exportrequest_dupe = exportrequest_dupe_val_list[i]
            curr_exportrequest_label = exportrequest_label_val_list[i]
            curr_pdf_path_val = pdf_path_val_list[i]
            curr_pdf_prefix_val = pdf_prefix_val_list[i]
            curr_ftpuploadrequest_val = ftpuploadrequest_val_list[i]
            curr_ftpfilename_val = ftpfilename_val_list[i]
            curr_ftp_user_specified_val = ftp_user_specified_val_list[i]
            curr_ftpuploaddir_val = ftpuploaddir_val_list[i]

            #Check to make sure that EXPORT_REQUEST matches the FTP_UPLOAD_REQUEST, only want to upload if this is true
            prefix_match_check = False
            if(curr_ftpuploadrequest_val == "GEO AND IMAGE" and curr_pdf_prefix_val in ["GEO", "IMAGE"]):
                prefix_match_check = True
            if(curr_ftpuploadrequest_val == "GEO AND GEOIMAGE" and curr_pdf_prefix_val in ["GEO", "GEOIMAGE"]):
                prefix_match_check = True
            if(curr_ftpuploadrequest_val == curr_pdf_prefix_val):
                prefix_match_check = True
            prefix_match_check_list.append(prefix_match_check)

            #Check if an upload should be performed
            if(curr_ftpupload_val == "YES" and prefix_match_check == True):
                ftpupload_check_list.append("YES")
            else:
                ftpupload_check_list.append("NO")


        #If a value of "YES" is found in ftpupload_check_list, proceed with upload(s)
        if("YES" in ftpupload_check_list):

            arcpy.AddMessage("\u200B")
            arcpy.AddMessage("UPLOADING EXPORTS TO FTP")

            #Establish FTP connection
            arcpy.AddMessage("..ESTABLISHING FTP CONNECTION")

            try:
                host = 'ftp.wildfire.gov'
                port = 1021
                session = Explicit_FTP_TLS()
                session.connect(host, port)
                session.auth()
                session.login(ftp_username_val, ftp_password_val)
                session.prot_p()

                #Loop through each ftp upload value
                arcpy.AddMessage("..UPLOADING EXPORTS")
                ftpupload_count = ftpupload_check_list.count("YES")
                curr_iter = 0
                for i in range(0, len(ftpupload_check_list)):
                    curr_ftpupload_val = ftpupload_val_list[i]
                    curr_exportrequest = exportrequest_val_list[i]
                    curr_exportrequest_dupe = exportrequest_dupe_val_list[i]
                    curr_exportrequest_label = exportrequest_label_val_list[i]
                    curr_pdf_path_val = pdf_path_val_list[i]
                    curr_pdf_prefix_val = pdf_prefix_val_list[i]
                    curr_ftpuploadrequest_val = ftpuploadrequest_val_list[i]
                    curr_ftpfilename_val = ftpfilename_val_list[i]
                    curr_ftp_user_specified_val = ftp_user_specified_val_list[i]
                    curr_ftpuploaddir_val = ftpuploaddir_val_list[i]
                    curr_prefix_match_check_val = prefix_match_check_list[i]


                    #If FTP_UPLOAD == "YES" and FTP_UPLOAD_REQUEST value matches the current prefix, proceed with upload
                    if(curr_ftpupload_val == "YES" and curr_prefix_match_check_val == True):

                        curr_iter = curr_iter + 1
                        curr_export_pdf_path_dirname = os.path.dirname(curr_pdf_path_val)
                        curr_export_pdf_path_basename = os.path.basename(curr_pdf_path_val)
                        arcpy.AddMessage("...." + curr_export_pdf_path_basename + " (" + str(curr_iter) + " out of " + str(ftpupload_count) + ")")

                        #Change FTP directory
                        try:
                            session.cwd(curr_ftpuploaddir_val)
                        except:
                            arcpy.AddMessage("......FTP DIRECTORY DOES NOT EXIST, CREATING")
                            try:
                                session.mkd(curr_ftpuploaddir_val)
                                session.cwd(curr_ftpuploaddir_val)
                                arcpy.AddMessage("......SUCCESS, CONTINUING UPLOAD")
                            except:
                                arcpy.AddMessage("......FAILED, SKIPPING UPLOAD. CHECK THAT FTP PARENT DIRECTORY EXISTS")
                                continue


                        #Rename upload
                        rename_check = False
                        if(curr_ftpfilename_val == "SAME AS EXPORT" and curr_exportrequest_label == "NO" and curr_ftpuploadrequest_val in ["GEO AND IMAGE", "GEO AND GEOIMAGE"]):

                            #Force Prefix
                            curr_ftp_rename_val = curr_pdf_prefix_val + "_" + curr_export_pdf_path_basename

                            #Remove duplicate extension if present
                            if(".pdf.pdf" in curr_ftp_rename_val):
                                curr_ftp_rename_val = curr_ftp_rename_val.replace(".pdf.pdf", ".pdf")

                            #Add .pdf extension if it doesn't exist
                            if(curr_ftp_rename_val[-4:] != ".pdf"):
                                curr_ftp_rename_val = curr_ftp_rename_val + ".pdf"

                            rename_check = True

                        if(curr_ftpfilename_val == "USER SPECIFIED"):

                            #Force prefix if necessary
                            if(curr_ftpuploadrequest_val in ["GEO AND IMAGE", "GEO AND GEOIMAGE"]):
                                curr_ftp_rename_val = curr_pdf_prefix_val + "_" + curr_ftp_user_specified_val
                            else:
                                curr_ftp_rename_val = curr_ftp_user_specified_val

                            #Remove duplicate extension if present
                            if(".pdf.pdf" in curr_ftp_rename_val):
                                curr_ftp_rename_val = curr_ftp_rename_val.replace(".pdf.pdf", ".pdf")

                            #Add .pdf extension if it doesn't exist
                            if(curr_ftp_rename_val[-4:] != ".pdf"):
                                curr_ftp_rename_val = curr_ftp_rename_val + ".pdf"

                            rename_check = True


                        #Upload file
                        try:
                            file = open(curr_pdf_path_val,'rb')

                            if(rename_check == True):
                                session.storbinary("STOR " + curr_ftp_rename_val, file)     # send the file
                            else:
                                session.storbinary("STOR " + curr_export_pdf_path_basename, file)     # send the file

                        except:
                            arcpy.AddMessage("......FAILED TO UPLOAD, SKIPPING")
                            continue


            except Exception as e:
                arcpy.AddMessage(e)


    if(multiprocess_toggle_val == "true"):
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("DONE!")






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
    #incident_name = "Deuel Creek"
    incident_name = arcpy.GetParameterAsText(0)

    #incident_id = "UT-NWS-000283"
    incident_id = arcpy.GetParameterAsText(1)

    #Specify the products directory
    #products_dir = r"C:\Workspace\OneDrive - FireNet\2022_DeuelCreek\products"
    products_dir = arcpy.GetParameterAsText(2)

    #Specify the path to the "PDFMultiExport.xlsx" file
    #export_table_xlsx_path = r"C:\Workspace\OneDrive - FireNet\2022_DeuelCreek\tools\PanunTools-main\PDFMultiExport_new.xlsx"
    export_table_xlsx_path = arcpy.GetParameterAsText(3)

    #Toggle to specify projects directory, or use spreadsheet 'APRX_PATH' values
    #projects_toggle = "Specify Incident 'projects' Directory"
    #projects_toggle = "Use spreadsheet 'APRX_PATH' values"
    projects_toggle = arcpy.GetParameterAsText(4)

    #Specify Incident 'projects' Directory
    #projects_dir = r"C:\Workspace\OneDrive - FireNet\2022_DeuelCreek\projects"
    projects_dir = arcpy.GetParameterAsText(5)

    #Toggle for FTP Upload
    #ftpupload_toggle = "No"
    ftpupload_toggle = arcpy.GetParameterAsText(6)

    #ftp_username = "mpanunto"
    ftp_username = arcpy.GetParameterAsText(7)

    #ftp_password = "xxxxxxxxxxx"
    ftp_password = arcpy.GetParameterAsText(8)

    #Toggle for Multiprocessor use
    #multiprocess_toggle = "true"
    multiprocess_toggle = arcpy.GetParameterAsText(9)

    #offline_license_check = "Yes"
    offline_license_check = arcpy.GetParameterAsText(10)



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


    #Test if user's license is offline
    if(multiprocess_toggle == "true" and offline_license_check == "Yes"):
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("PERFORMING OFFLINE LICENSE CHECK")
        try:
            #Create Scratch Directory
            now = datetime.datetime.now()
            computername = os.getenv('COMPUTERNAME')
            scratchdir_datetime_str = now.strftime("%Y%m%d_%H%M")
            scratchdir = products_dir + "/" + scratchdir_datetime_str + "_" + computername + "_licensecheck"
            if(os.path.isdir(scratchdir)):
                shutil.rmtree(scratchdir)
            os.mkdir(scratchdir)

            appdata_path = os.getenv('LOCALAPPDATA')
            license_txt_path = appdata_path + "/ESRI_Licensing/Logs/License.log"
            license_txt_copy_path = scratchdir + "/License.log"
            shutil.copyfile(license_txt_path, license_txt_copy_path)

            offline_true_list = []
            offline_false_list = []
            offline_request_list = []
            line_number = 0
            with open(license_txt_copy_path, 'r') as read_obj:
                for line in read_obj:
                    line_number += 1
                    if "Offline mode = false" in line:
                        offline_false_list.append(line_number)
                    if "Offline mode = true" in line:
                        offline_true_list.append(line_number)
                    if "Application requesting to go in offline mode" in line:
                        offline_request_list.append(line_number)


            #Determine the highest line number (aka the latest occurence) for "Offline mode = false"
            if(len(offline_false_list) > 0):
                offline_false_maxline = max(offline_false_list)
            else:
                offline_false_maxline = 0

            #Determine the highest line number (aka the latest occurence) for "Offline mode = true"
            if(len(offline_true_list) > 0):
                offline_true_maxline = max(offline_true_list)
            else:
                offline_true_maxline = 0

            #Determine the highest line number (aka the latest occurence) for "Application requesting to go in offline mode"
            if(len(offline_request_list) > 0):
                offline_request_maxline = max(offline_request_list)
            else:
                offline_request_maxline = 0

            #Delete Scratch Directory
            if(os.path.isdir(scratchdir)):
                shutil.rmtree(scratchdir)

        except Exception as e:
            arcpy.AddMessage(e)
            arcpy.AddError("UNABLE TO VERIFY IF ARCGIS PRO LICENSE IS ENABLED FOR OFFLINE USE")
            arcpy.AddError("DUE TO RISK OF LICENSE CORRUPTION, IT IS RECOMMENDED TO RETURN AN OFFLINE LICENSE WHEN RUNNING THIS TOOL")
            arcpy.AddError("TO PROCEED WITH AN OFFLINE LICENSE, SET INPUT VALUE 'Perform Offline License Check' TO 'No' AND RE-RUN TOOL")
            #Delete Scratch Directory
            if(os.path.isdir(scratchdir)):
                shutil.rmtree(scratchdir)
            raise arcpy.ExecuteError

        if( (offline_true_maxline > offline_false_maxline) or (offline_request_maxline > offline_false_maxline)):
            #Compare the two highest numbers, whichever is higher is the current license status
            arcpy.AddError("ARCGIS PRO LICENSE IS ENABLED FOR OFFLINE USE")
            arcpy.AddError("DUE TO RISK OF LICENSE CORRUPTION, IT IS RECOMMENDED TO RETURN AN OFFLINE LICENSE WHEN RUNNING THIS TOOL")
            arcpy.AddError("TO PROCEED WITH AN OFFLINE LICENSE, SET INPUT VALUE 'Perform Offline License Check' TO 'No' AND RE-RUN TOOL")
            raise arcpy.ExecuteError


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

    #Check that FTP_UPLOAD_REQUEST values agree with the EXPORT_REQUEST
    ftpuploadrequest_match_check_list = []
    ftpuploadrequest_error_row_list = []
    for i in range(0, len(export_table_df)):
        curr_row = export_table_df.iloc[i]
        curr_row_number = i + 2
        curr_row_export = curr_row["EXPORT"]
        curr_row_exportrequest = curr_row["EXPORT_REQUEST"]
        curr_row_ftpupload = curr_row["FTP_UPLOAD"]
        curr_row_ftpuploadrequest = curr_row["FTP_UPLOAD_REQUEST"]
        if(curr_row_export == "YES" and curr_row_ftpupload == "YES"):
            ftpuploadrequest_match_check = False
            if(curr_row_exportrequest == "GEO AND IMAGE" and curr_row_ftpuploadrequest in ["GEO", "IMAGE"]):
                ftpuploadrequest_match_check = True
            if(curr_row_exportrequest == "GEO AND GEOIMAGE" and curr_row_ftpuploadrequest in ["GEO", "GEOIMAGE"]):
                ftpuploadrequest_match_check = True
            if(curr_row_exportrequest == curr_row_ftpuploadrequest):
                ftpuploadrequest_match_check = True
            ftpuploadrequest_match_check_list.append(ftpuploadrequest_match_check)
            if(ftpuploadrequest_match_check == False):
                ftpuploadrequest_error_row_list.append(curr_row_number)
    if(False in ftpuploadrequest_match_check_list):
        ftpuploadrequest_error_str = [str(element) for element in ftpuploadrequest_error_row_list]
        ftpuploadrequest_error_str = ", ".join(ftpuploadrequest_error_str)
        arcpy.AddError("CHECK ROW(S) " + str(ftpuploadrequest_error_str) + " OF SPREADSHEET")
        arcpy.AddError("FTP_UPLOAD_REQUEST CONTAINS VALUES THAT WERE NOT EXPORTED")
        raise arcpy.ExecuteError


    #Check if any entries have EXPORT == YES and FTP_UPLOAD == "YES", but have a bad FTP_UPLOAD_DIRECTORY value
    ftpuploaddir_issue_list = []
    ftpuploaddir_error_1 = False
    ftpuploaddir_error_1_list = []
    ftpuploaddir_error_2 = False
    ftpuploaddir_error_2_list = []
    for i in range(0, len(export_table_df)):
        curr_row = export_table_df.iloc[i]
        curr_row_number = i + 2
        curr_row_export = curr_row["EXPORT"]
        curr_row_ftpupload = curr_row["FTP_UPLOAD"]
        curr_row_ftpuploaddir = curr_row["FTP_UPLOAD_DIRECTORY"]
        curr_row_layoutname = curr_row["LAYOUT_NAME"]
        if(curr_row_export == "YES" and curr_row_ftpupload == "YES"):
            if(curr_row_ftpuploaddir[0:24] != "/incident_specific_data/"):
                ftpuploaddir_error_1 = True
                ftpuploaddir_error_1_list.append(curr_row_number)
            if(curr_row_ftpuploaddir == "/incident_specific_data/"):
                ftpuploaddir_error_2 = True
                ftpuploaddir_error_2_list.append(curr_row_number)
    if(ftpuploaddir_error_1 == True):
        ftpuploaddir_error_1_str = [str(element) for element in ftpuploaddir_error_1_list]
        ftpuploaddir_error_1_str = ", ".join(ftpuploaddir_error_1_str)
        arcpy.AddError("CHECK ROW(S) " + str(ftpuploaddir_error_1_str) + " OF SPREADSHEET")
        arcpy.AddError("FTP_UPLOAD_DIRECTORY VALUE MUST BEGIN WITH '/incident_specific_data/'")
        raise arcpy.ExecuteError
    if(ftpuploaddir_error_2 == True):
        ftpuploaddir_error_2_str = [str(element) for element in ftpuploaddir_error_2_list]
        ftpuploaddir_error_2_str = ", ".join(ftpuploaddir_error_2_str)
        arcpy.AddError("CHECK ROW(S) " + str(ftpuploaddir_error_2_str) + " OF SPREADSHEET")
        arcpy.AddError("FTP_UPLOAD_DIRECTORY VALUE MUST BE LONGER THAN '/incident_specific_data/'")
        raise arcpy.ExecuteError


    #Check if ftpupload_toggle == YES, and if any entries have EXPORT == YES and EXPORT_REQUEST in ["GEO AND IMAGE", "GEO AND GEOIMAGE"] and EXPORT_REQUEST_LABEL == "NO" and FTP_UPLOAD == "YES"
    #These could cause issues in the FTP upload, as there could be two PDFs uploaded with the same name at the same time
    #If that happens, one will be overwritten. So, if any entries have these values, need to force EXPORT_REQUEST_LABEL to be "YES - PREFIX"
    ftpuploaddir_warning_list = []
    for i in range(0, len(export_table_df)):
        curr_row = export_table_df.iloc[i]
        curr_row_number = i + 2
        curr_row_export = curr_row["EXPORT"]
        curr_row_request = curr_row["EXPORT_REQUEST"]
        curr_row_requestlabel = curr_row["EXPORT_REQUEST_LABEL"]
        curr_row_ftpupload = curr_row["FTP_UPLOAD"]
        curr_row_ftpuploadrequest = curr_row["FTP_UPLOAD_REQUEST"]
        if(ftpupload_toggle == "Yes" and curr_row_export == "YES" and curr_row_ftpupload == "YES" and curr_row_ftpuploadrequest in ["GEO AND IMAGE", "GEO AND GEOIMAGE"] and curr_row_requestlabel == "NO"):
            ftpuploaddir_warning_list.append(curr_row_number)
    ftpuploaddir_warning_str = [str(element) for element in ftpuploaddir_warning_list]
    ftpuploaddir_warning_str = ", ".join(ftpuploaddir_warning_str)

    #Now warn user of entries that had a forced EXPORT_REQUEST_LABEL value
    if(len(ftpuploaddir_warning_list) > 0):
        arcpy.AddMessage("\u200B")
        arcpy.AddWarning("TO AVOID DUPLICATE FTP FILENAMES, ADDING EXPORT REQUEST LABELS TO FTP UPLOADS FOR SPREADSHEET ROW(S) " + ftpuploaddir_warning_str)
        arcpy.AddMessage("\u200B")


    #Create list of EXPORT and REQUEST values from the spreadsheet
    export_col = list(export_table_df["EXPORT"])

    #Get count of how many items need processing, and also determine which items
    processing_needed_list = []
    processing_needed_which_list = []
    for i in range(0, len(export_col)):
        curr_export = export_col[i]
        export_check = (curr_export == "YES")
        if(export_check == True):
            processing_needed_list.append(1)
            processing_needed_which_list.append(i)
        else:
            processing_needed_list.append(0)
    processing_count = len(processing_needed_which_list)

    #Create lists for export request and filename information
    export_list = [list(map(str, export_table_df["EXPORT"]))[i] for i in processing_needed_which_list]
    exportrequest_list = [list(map(str, export_table_df["EXPORT_REQUEST"]))[i] for i in processing_needed_which_list]
    exportrequest_dupe_list = [list(map(str, export_table_df["EXPORT_REQUEST"]))[i] for i in processing_needed_which_list]
    productsdate_list = [list(map(str, export_table_df["PRODUCTS_DATE"]))[i] for i in processing_needed_which_list]

    #Create lists for file naming
    exportfilename_list = [list(map(str, export_table_df["EXPORT_FILENAME"]))[i] for i in processing_needed_which_list]
    export_user_specified_list = [list(map(str, export_table_df["EXPORT_USER_SPECIFIED"]))[i] for i in processing_needed_which_list]
    geoops_maptype_list = [list(map(str, export_table_df["GEOOPS_MAPTYPE"]))[i] for i in processing_needed_which_list]
    geoops_pagesize_list = [list(map(str, export_table_df["GEOOPS_PAGESIZE"]))[i] for i in processing_needed_which_list]
    geoops_orientation_list = [list(map(str, export_table_df["GEOOPS_ORIENTATION"]))[i] for i in processing_needed_which_list]
    geoops_period_list = [list(map(str, export_table_df["GEOOPS_PERIOD"]))[i] for i in processing_needed_which_list]
    exportrequestlabel_list = [list(map(str, export_table_df["EXPORT_REQUEST_LABEL"]))[i] for i in processing_needed_which_list]

    #Create lists for Map Series export settings
    mapseries_pages_list = [list(export_table_df["MAPSERIES_PAGES"])[i] for i in processing_needed_which_list]
    mapseries_range_list = [list(export_table_df["MAPSERIES_RANGE"])[i] for i in processing_needed_which_list]
    mapseries_files_list = [list(export_table_df["MAPSERIES_FILES"])[i] for i in processing_needed_which_list]

    #Create lists of export settings
    clipgraphics_list = [list(export_table_df["CLIP_GRAPHICS_EXTENT"])[i] for i in processing_needed_which_list]
    removelayoutbackground_list = [list(export_table_df["REMOVE_LAYOUT_BACKGROUND"])[i] for i in processing_needed_which_list]
    imagecompress_list = [list(map(str, export_table_df["IMAGE_COMPRESSION"]))[i] for i in processing_needed_which_list]
    imagecompressquality_list = [list(map(int, export_table_df["IMAGE_COMPRESSION_QUALITY"]))[i] for i in processing_needed_which_list]
    compressvectorgraphics_list = [list(export_table_df["COMPRESS_VECTOR_GRAPHICS"])[i] for i in processing_needed_which_list]
    vectorresolution_list = [list(map(int, export_table_df["VECTOR_RESOLUTION"]))[i] for i in processing_needed_which_list]
    rasterresample_list = [list(map(str, export_table_df["RASTER_RESAMPLE"]))[i] for i in processing_needed_which_list]
    embedfonts_list = [list(export_table_df["EMBED_FONTS"])[i] for i in processing_needed_which_list]
    convertmarkers_list = [list(map(str, export_table_df["CONVERT_MARKERS"]))[i] for i in processing_needed_which_list]
    layersattributes_list = [list(map(str, export_table_df["LAYERS_ATTRIBUTES"]))[i] for i in processing_needed_which_list]
    simulateoverprint_list = [list(map(str, export_table_df["SIMULATE_OVERPRINT"]))[i] for i in processing_needed_which_list]
    embedcolorprofile_list = [list(map(str, export_table_df["EMBED_COLOR_PROFILE"]))[i] for i in processing_needed_which_list]
    pdfaccessibility_list = [list(map(str, export_table_df["PDF_ACCESSIBILITY"]))[i] for i in processing_needed_which_list]

    #Create lists of FTP settings
    ftpupload_list = [list(map(str, export_table_df["FTP_UPLOAD"]))[i] for i in processing_needed_which_list]
    ftpuploadrequest_list = [list(map(str, export_table_df["FTP_UPLOAD_REQUEST"]))[i] for i in processing_needed_which_list]
    ftpfilename_list = [list(map(str, export_table_df["FTP_FILENAME"]))[i] for i in processing_needed_which_list]
    ftp_user_specified_list = [list(map(str, export_table_df["FTP_USER_SPECIFIED"]))[i] for i in processing_needed_which_list]
    ftpuploaddir_list = [list(map(str, export_table_df["FTP_UPLOAD_DIRECTORY"]))[i] for i in processing_needed_which_list]

    #Create lists for the Layout name and APRX Path
    layoutname_list = [list(map(str, export_table_df["LAYOUT_NAME"]))[i] for i in processing_needed_which_list]
    aprxfilename_list = [list(map(str, export_table_df["APRX_FILENAME"]))[i] for i in processing_needed_which_list]
    aprxpath_list = [list(map(str, export_table_df["APRX_PATH"]))[i] for i in processing_needed_which_list]

    #Create lists of user specified inputs
    incidentname_list = [incident_name] * processing_count
    unitid_list = [unit_id] * processing_count
    incidentnumber_list = [incident_number] * processing_count
    productsdir_list = [products_dir] * processing_count
    projects_toggle_list = [projects_toggle] * processing_count
    projects_dir_list = [projects_dir] * processing_count
    ftpupload_toggle_list = [ftpupload_toggle] * processing_count
    ftp_username_list = [ftp_username] * processing_count
    ftp_password_list = [ftp_password] * processing_count
    multiprocess_toggle_list = [multiprocess_toggle] * processing_count

    inputs_list = list(map(list, zip(incidentname_list, unitid_list, incidentnumber_list, productsdir_list, projects_toggle_list, projects_dir_list, ftpupload_toggle_list, ftp_username_list, ftp_password_list, multiprocess_toggle_list,
                export_list, exportrequest_list, exportrequest_dupe_list, productsdate_list, exportfilename_list, export_user_specified_list, geoops_maptype_list, geoops_pagesize_list, geoops_orientation_list, geoops_period_list, exportrequestlabel_list,
                mapseries_pages_list, mapseries_range_list, mapseries_files_list,
                ftpupload_list, ftpuploadrequest_list, ftpfilename_list, ftp_user_specified_list, ftpuploaddir_list,
                clipgraphics_list, removelayoutbackground_list, imagecompress_list, imagecompressquality_list, compressvectorgraphics_list, vectorresolution_list, rasterresample_list, embedfonts_list, convertmarkers_list, layersattributes_list, simulateoverprint_list, embedcolorprofile_list, pdfaccessibility_list,
                layoutname_list, aprxfilename_list, aprxpath_list)))


    #Create new inputs_list by finding any export requests that are BOTH
    #Need to split these into separate list elements of AVENZA and IMAGE to speed up multiprocessing
    inputs_list_multiprocess = []
    for i in range(0, len(inputs_list)):

        curr_input_list = list(inputs_list[i])
        curr_input_list_geo = list(inputs_list[i])
        curr_input_list_geo[11] = "GEO"
        curr_input_list_image = list(inputs_list[i])
        curr_input_list_image[11] = "IMAGE"
        curr_input_list_geoimage = list(inputs_list[i])
        curr_input_list_geoimage[11] = "GEOIMAGE"

        curr_exportrequest = curr_input_list[11]

        if(curr_exportrequest == "GEO"):
            inputs_list_multiprocess.append(curr_input_list)

        if(curr_exportrequest == "IMAGE"):
            inputs_list_multiprocess.append(curr_input_list)

        if(curr_exportrequest == "GEOIMAGE"):
            inputs_list_multiprocess.append(curr_input_list)

        if(curr_exportrequest == "GEO AND IMAGE"):
            inputs_list_multiprocess.append(curr_input_list_geo)
            inputs_list_multiprocess.append(curr_input_list_image)

        if(curr_exportrequest == "GEO AND GEOIMAGE"):
            inputs_list_multiprocess.append(curr_input_list_geo)
            inputs_list_multiprocess.append(curr_input_list_geoimage)

    #get CPU count, and range
    cpu_count = multiprocessing.cpu_count()

    #If the number of exports is less than the total number of logical processors available,
    #set CPU count to equal number of exports
    if(cpu_count > len(inputs_list_multiprocess)):
        cpu_count = len(inputs_list_multiprocess)

    #Export maps. Use multiprocessor if user enabled it, else export one map at a time.
    if(multiprocess_toggle == "true"):

        #Shuffle the inputs_list_multiprocess to randomize the processing order
        random.shuffle(inputs_list_multiprocess)
        inputs_list_multiprocess_cpu_split = numpy.array_split(inputs_list_multiprocess, cpu_count)

        #If any of the "inputs_list_multiprocess_cpu_split" elements contain multiple map series, reshuffle
        #Reshuffle up to 1000 times
        reshuffle_check = True
        reshuffle_attempt = 0
        while(reshuffle_check == True and reshuffle_attempt <= 1000):

            #Build list of map series values
            reshuffle_check_list = []
            for i in range(0, len(inputs_list_multiprocess_cpu_split)):
                curr_inputs_list_multiprocess_cpu_split = inputs_list_multiprocess_cpu_split[i]
                mapseries_pages_val_list = []
                for j in range(0, len(curr_inputs_list_multiprocess_cpu_split)):
                    mapseries_pages_val_list.append(curr_inputs_list_multiprocess_cpu_split[j][19])

                #Determine if any elements have 2 or more map series
                mapseries_all_count = mapseries_pages_val_list.count("ALL")
                mapseries_range_count = mapseries_pages_val_list.count("RANGE")
                mapseries_sum_count = sum([mapseries_all_count, mapseries_range_count])
                if(mapseries_sum_count >= 2):
                    reshuffle_check_list.append(True)
                else:
                    reshuffle_check_list.append(False)

            #If any elements have 2 or more map series, reshuffle
            if(True in reshuffle_check_list):
                reshuffle_check = True
                random.shuffle(inputs_list_multiprocess)
                inputs_list_multiprocess_cpu_split = numpy.array_split(inputs_list_multiprocess, cpu_count)
                reshuffle_attempt = reshuffle_attempt + 1
            else:
                reshuffle_check = False
        #arcpy.AddMessage(str(reshuffle_attempt) + " Reshuffle Attempts")


        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("Begin multiprocessing")
        PDFMultiExport.execute(inputs_list_multiprocess_cpu_split)
        arcpy.AddMessage("..Finished multiprocessing")

    else:

        worker_function(inputs_list)


    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("DONE!")
    arcpy.AddMessage("\u200B")

