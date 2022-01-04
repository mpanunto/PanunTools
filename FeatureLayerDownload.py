print("Importing Libraries")
import arcpy, arcgis, pandas, datetime, time, os, sys, multiprocessing, inspect, urllib, zipfile, glob, shutil, warnings, contextlib
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
from arcgis.geometry import filters
from multiprocessing import Pool, freeze_support
warnings.filterwarnings("ignore")
if(sys.version_info[0] == 3):
    import urllib.request
arcpy.env.overwriteOutput = True


#Define worker function that performs data download
def worker_function_services(in_inputs_list):

    try:

        #Use ArcGIS Pro's Active Portal to establish connection to ArcGIS API
        #curr_pro_portal_toggle = inputs_list_primary[65][0]
        #curr_pro_portal_toggle = inputs_list_secondary[1][0]
        curr_pro_portal_toggle = in_inputs_list[0]

        #ArcGIS Online Portal URL
        #curr_portalurl = "https://nifc.maps.arcgis.com"
        #curr_portalurl = inputs_list_primary[65][1]
        #curr_portalurl = inputs_list_secondary[1][1]
        curr_portalurl = in_inputs_list[1]

        #ArcGIS Online Username
        #curr_username = "mpanunto_nifc"
        #curr_username = inputs_list_primary[65][2]
        #curr_username = inputs_list_secondary[1][2]
        curr_username = in_inputs_list[2]

        #ArcGIS Online Password
        #curr_password = "xxxxxx"
        #curr_password = inputs_list_primary[65][3]
        #curr_password = inputs_list_secondary[1][3]
        curr_password = in_inputs_list[3]

        #Path to AOI feature class
        #curr_aoi_fc_path = r"C:\Workspace\development\FeatureLayerDownload\output_gb_test\_scratch\AOI.gdb\AOI_final_OBJID10"
        #curr_aoi_fc_path = inputs_list_primary[65][4]
        #curr_aoi_fc_path = inputs_list_secondary[1][4]
        curr_aoi_fc_path = in_inputs_list[4]

        #User defined output projection
        #curr_output_prj = "PROJCS['NAD_1983_UTM_Zone_12N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-111.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 -9998100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
        #curr_output_prj = inputs_list_primary[65][5]
        #curr_output_prj = inputs_list_secondary[1][5]
        curr_output_prj = in_inputs_list[5]

        #Output Directory
        #curr_outdir = r"C:\Workspace\development\FeatureLayerDownload\output_gb_test"
        #curr_outdir = inputs_list_primary[65][6]
        #curr_outdir = inputs_list_secondary[1][6]
        curr_outdir = in_inputs_list[6]

        #Feature layer urls
        #curr_featurelayer_url = inputs_list_primary[65][7]
        #curr_featurelayer_url = inputs_list_secondary[1][7]
        curr_featurelayer_url = in_inputs_list[7]

        #Features service name
        #curr_featureservice_name = inputs_list_primary[65][8]
        #curr_featureservice_name = inputs_list_secondary[1][8]
        curr_featureservice_name = in_inputs_list[8]

        #curr_multiprocess = inputs_list_primary[65][9]
        #curr_multiprocess = inputs_list_secondary[1][9]
        curr_multiprocess = in_inputs_list[9]

        #Get scratchdir
        curr_scratchdir = curr_outdir + "/_scratch"

        #Get metadatadir
        curr_metadatadir = curr_scratchdir + "/_metadata"

        #Get basename of AOI feature class
        curr_aoi_fc_basename = os.path.basename(curr_aoi_fc_path)

        #Get ObjID string and number
        if(curr_multiprocess == "Secondary"):
            curr_aoi_fc_path_split = curr_aoi_fc_path.split("_")
            curr_objid = curr_aoi_fc_path_split[len(curr_aoi_fc_path_split)-1]
            curr_objid_number = curr_objid.replace("OBJID", "")

        #Establish connection to the ArcGIS Online Org
        print(" " )
        print("REQUESTING API ACCESS TOKEN")
        token_check = False
        while(token_check == False):
            try:
                if(curr_pro_portal_toggle == "Yes"):
                    gis = GIS("pro")
                else:
                    gis = GIS(curr_portalurl, curr_username, curr_password, verify_cert=False)
                token_check = True
            except Exception as e:
                print(e)
                print("..HITTING API ACCESS TOKEN REQUEST LIMIT, BACKING OFF FOR 60s")
                time.sleep(60)


        print("SIGNING INTO PORTAL")
        portal_check = False
        while(portal_check == False):
            try:
                if(curr_pro_portal_toggle == "No"):
                    arcpy_portal = arcpy.SignInToPortal(curr_portalurl, curr_username, curr_password)
                portal_check = True
            except Exception as e:
                print(e)
                print("..FAILED TO SIGN INTO PORTAL, TRYING AGAIN")

        #Get feature layer, and properties
        curr_featurelayer = arcgis.features.FeatureLayer(curr_featurelayer_url)
        curr_featurelayer_name = curr_featurelayer.properties.name
        curr_featurelayer_name_short = curr_featurelayer_name.replace(" ", "")
        curr_featurelayer_name_short = curr_featurelayer_name_short.replace("_", "")
        curr_featurelayer_name_short = curr_featurelayer_name_short.replace("-", "")
        curr_featurelayer_name_short = curr_featurelayer_name_short.replace("&", "")
        curr_featureservice_name_short = curr_featureservice_name.replace(" ", "")
        curr_featureservice_name_short = curr_featureservice_name_short.replace("_", "")
        curr_featureservice_name_short = curr_featureservice_name_short.replace("-", "")
        curr_featureservice_name_short = curr_featureservice_name_short.replace("&", "")
        curr_featurelayer_uniqueidfield = curr_featurelayer.properties.uniqueIdField["name"]
        curr_featurelayer_maxrecordcount = curr_featurelayer.properties.maxRecordCount
        curr_featurelayer_standardmaxrecordcount = curr_featurelayer.properties.standardMaxRecordCount
        curr_featurelayer_tilemaxrecordcount = curr_featurelayer.properties.tileMaxRecordCount
        curr_featurelayer_wkid = curr_featurelayer.properties.extent.spatialReference.wkid
        curr_featurelayer_sr = arcpy.SpatialReference(curr_featurelayer_wkid)

        #Print the name of the current feature layer
        if(curr_multiprocess == "Primary"):
            if("HIFLD" in curr_featureservice_name_short):
                curr_hifld_region = curr_featureservice_name_short[-2:]
                print("PROCESSING FEATURE LAYER: " + "R" + curr_hifld_region + "_" + curr_featurelayer_name)
            else:
                print("PROCESSING FEATURE LAYER: " + curr_featurelayer_name)

        else:
            if("HIFLD" in curr_featureservice_name_short):
                curr_hifld_region = curr_featureservice_name_short[-2:]
                print("PROCESSING FEATURE LAYER: " + "R" + curr_hifld_region + "_" + curr_featurelayer_name + " (ObjID " + str(curr_objid_number) + ")")
            else:
                print("PROCESSING FEATURE LAYER: " + curr_featurelayer_name + " (ObjID " + str(curr_objid_number) + ")")





        ############################################################################
        ## PROJECT AOI
        ############################################################################

        print("..PROJECTING AOI FOR SELECTION")
        project_check = False
        while(project_check == False):
            try:
                #The Transportation HIFLD services all have the same feature layer names, need to parse out the region number from the service name here
                if("HIFLD" in curr_featureservice_name_short):
                    curr_hifld_service_name = "HIFLD" + curr_hifld_region
                    curr_aoi_prj_fc_name = curr_aoi_fc_basename + "_prj_" + str(curr_featurelayer_wkid) + "_" + curr_hifld_service_name + curr_featurelayer_name_short
                else:
                    curr_aoi_prj_fc_name = curr_aoi_fc_basename + "_prj_" + str(curr_featurelayer_wkid) + "_" + curr_featurelayer_name_short

                aoi_proj_gdb_name = curr_aoi_prj_fc_name
                aoi_proj_gdb_path = curr_scratchdir + "/" + aoi_proj_gdb_name + ".gdb"
                arcpy.CreateFileGDB_management(curr_scratchdir, aoi_proj_gdb_name)

                aoi_fc_prj_path = aoi_proj_gdb_path + "/" + curr_aoi_prj_fc_name
                if(not arcpy.Exists(aoi_fc_prj_path)):
                    arcpy.Project_management(curr_aoi_fc_path, aoi_fc_prj_path, out_coor_system=curr_featurelayer_sr)
                    aoi_sdf = arcgis.GeoAccessor.from_featureclass(aoi_fc_prj_path)
                    aoi_geom = aoi_sdf["SHAPE"][0]

                #Test to see if the projected feature class has any features, if not, delete and re-try
                if(int(str(arcpy.GetCount_management(aoi_fc_prj_path))) > 0):
                    project_check = True
                else:
                    print("....PROJECTED OUTPUT HAS NO FEATURES, RE-TRYING")
                    arcpy.Delete_management(aoi_fc_prj_path)
                    time.sleep(5)
            except Exception as e:
                print(e)
                print("....PROJECT FAILED, RE-TRYING")
                project_check = False
                time.sleep(5)


        #Reset environments
        arcpy.ResetEnvironments()

        #Get extent of projected AOI, and set extent environmental variable to that
        print("..SETTING EXTENT FOR SELECTION")
        extent_check = False
        while(extent_check == False):
            try:
                aoi_fc_prj_extent = arcpy.Describe(aoi_fc_prj_path).extent
                curr_extent_xmin = aoi_fc_prj_extent.XMin
                curr_extent_ymin = aoi_fc_prj_extent.YMin
                curr_extent_xmax = aoi_fc_prj_extent.XMax
                curr_extent_ymax = aoi_fc_prj_extent.YMax
                arcpy.env.extent = arcpy.Extent(curr_extent_xmin, curr_extent_ymin, curr_extent_xmax, curr_extent_ymax)
                if(str(arcpy.env.extent.XMin) == "None"):
                    extent_check = False
                    print("....EXTENT FAILED TO SET, RETRYING")
                    time.sleep(5)
                else:
                    extent_check = True
            except Exception as e:
                print(e)
                print("....EXTENT FAILED TO SET, RETRYING")
                time.sleep(5)


        ############################################################################
        ## SELECT FEATURES
        ############################################################################

        print("..SELECTING INTERSECTING FEATURES")
        select_test = False
        features_check = False
        select_attempt = 1
        while(select_test == False):
            try:

                #Perform selection via arcpy
                selection = arcpy.SelectLayerByLocation_management(curr_featurelayer_url, overlap_type="INTERSECT", select_features=aoi_fc_prj_path, selection_type="NEW_SELECTION")
                selection_count = int(arcpy.GetCount_management(selection)[0])

                #Perform selection via arcgis api
                #fl = arcgis.features.FeatureLayer(curr_featurelayer_url)
                #fl_query_objids = fl.query(where="1=1", return_ids_only=True, geometry_filter=filters.intersects(aoi_geom))
                #objectid_fieldname = fl_query_objids["objectIdFieldName"]
                #objectid_values = fl_query_objids["objectIds"]
                #selection_count = len(objectid_values)
                #if(selection_count > 0):
                    #if(selection_count == 1):
                        #wherefield = objectid_fieldname
                        #wherevalues = str(objectid_values[0])
                        #whereClause = '"' + wherefield + '"' + ' = ' + wherevalues
                    #else:
                        #wherefield = objectid_fieldname
                        #wherevalues = str(tuple(objectid_values))
                        #whereClause = '"' + wherefield + '"' + ' IN ' + wherevalues
                    #fl_query = fl.query(where=whereClause)
                    #fl_sdf = fl_query.sdf

                #If the selection returned features, perform query, and set toggle
                if(selection_count > 0):
                    features_check = True

                if(selection_count == 0):
                    print("..NO INTERSECTING FEATURES FOUND, SKIPPING DATASET")

                select_test = True

            except Exception as e:
                print(e)
                select_attempt = select_attempt + 1
                if(select_attempt < 6):
                    print("....SELECTION FAILED, RE-TRYING")
                    select_test = False
                    time.sleep(5)
                if(select_attempt >= 6):
                    print("....SELECTION FAILED 5 TIMES, SKIPPING DATASET")
                    select_test = True

                    #Export CSV file containing information needed to retry query outside of multiprocessor
                    if(curr_multiprocess == "Primary"):
                        csvdata = [{"SHORTNAME":curr_featurelayer_name_short, "URL":curr_featurelayer_url, "AOIFCPATH":curr_aoi_fc_path}]
                        selectfail_df = pandas.DataFrame(csvdata)
                        if("HIFLD" in curr_featureservice_name_short):
                            selectfail_csv_path = curr_outdir + "/selectfail_primary_" + "R" + curr_hifld_region + "_" + curr_featurelayer_name_short + ".csv"
                        else:
                            selectfail_csv_path = curr_outdir + "/selectfail_primary_" + curr_featurelayer_name_short + ".csv"
                        selectfail_df.to_csv(selectfail_csv_path, index=False)
                    if(curr_multiprocess == "Secondary"):
                        csvdata = [{"SHORTNAME":curr_featurelayer_name_short, "URL":curr_featurelayer_url, "AOIFCPATH":curr_aoi_fc_path}]
                        selectfail_df = pandas.DataFrame(csvdata)
                        if("HIFLD" in curr_featureservice_name_short):
                            selectfail_csv_path = curr_outdir + "/selectfail_secondary_" + "R" + curr_hifld_region + "_" + curr_featurelayer_name_short + "_ObjID" + str(curr_objid_number) + ".csv"
                        else:
                            selectfail_csv_path = curr_outdir + "/selectfail_secondary_" + curr_featurelayer_name_short + "_ObjID" + str(curr_objid_number) + ".csv"
                        selectfail_df.to_csv(selectfail_csv_path, index=False)


        ############################################################################
        ## CREATE OUTPUT GDB
        ############################################################################
        create_gdb_check = False
        create_gdb_attempt = 1
        if(features_check == True):

            while(create_gdb_check == False):
                try:
                    #Create output GDB
                    print("..FEATURES SELECTED, CREATING OUTPUT GDB")

                    curr_featurelayer_fc_name = curr_featurelayer_name_short

                    if(curr_multiprocess == "Primary"):
                        curr_gdb_name = curr_featurelayer_name_short + "_1"
                    if(curr_multiprocess == "Secondary"):
                        curr_gdb_name = curr_featurelayer_fc_name + "_OBJID" + str(curr_objid_number) + "_1"

                    curr_gbd_path = curr_outdir + "/" + curr_gdb_name + ".gdb"
                    curr_featurelayer_fc_name = curr_gdb_name

                    #If "_1" already exists, increase it until an unused name is discovered
                    if(os.path.isdir(curr_gbd_path)):
                        gdb_new_check = False
                        last_char = curr_gdb_name[len(curr_gdb_name) - 1]
                        ending_number = 1
                        while(gdb_new_check == False):
                            last_char_new = str(int(last_char) + 1)
                            curr_gdb_name_new = curr_gdb_name[:-1] + str(ending_number + 1)
                            curr_gdb_path_new = curr_outdir + "/" + curr_gdb_name_new + ".gdb"
                            if(not os.path.isdir(curr_gdb_path_new)):
                                curr_gdb_name = curr_gdb_name_new
                                curr_gbd_path = curr_gdb_path_new
                                curr_featurelayer_fc_name = curr_gdb_name_new
                                gdb_new_check = True
                            else:
                                ending_number = ending_number + 1

                    arcpy.CreateFileGDB_management(curr_outdir, curr_gdb_name)
                    create_gdb_check = True

                except Exception as e:
                    print(e)
                    create_gdb_attempt = create_gdb_attempt + 1
                    if(create_gdb_attempt < 6):
                        print("....FAILED TO CREATE OUTPUT GDB, TRYING AGAIN")
                        create_gdb_check = False
                        time.sleep(5)
                    if(create_gdb_attempt >= 6):
                        print("....FAILED TO CREATE OUTPUT GDB 5 TIMES, SKIPPING DATASET")
                        create_gdb_check = True
                        features_check = False


        ############################################################################
        ## EXPORT FEATURES
        ############################################################################

        #If features were selected, export them
        if(features_check == True and create_gdb_check == True):

            #Define output feature class path
            curr_featurelayer_fc_path = curr_gbd_path + "\\" + curr_featurelayer_fc_name

            #Create spatial reference object from user defined output projection
            curr_output_prj_sr = arcpy.SpatialReference(text=curr_output_prj)

            #Define output coordinate system environmental variable
            print("..SETTING OUTPUT COORDINATE SYSTEM")
            outcrs_check = False
            while(outcrs_check == False):
                try:
                    arcpy.env.outputCoordinateSystem = curr_output_prj_sr
                    if(arcpy.env.outputCoordinateSystem.name != curr_output_prj_sr.name):
                        print("....OUTPUT COORDINATE SYSTEM FAILED TO SET, RETRYING")
                        time.sleep(5)
                    else:
                        outcrs_check = True
                except Exception as e:
                    print(e)
                    print("....OUTPUT COORDINATE SYSTEM FAILED TO SET, RETRYING")
                    time.sleep(5)

            #PERFORM EXPORT
            print("..EXPORTING (" + str(selection_count) + " features)")
            export_test = False
            export_attempt = 1
            while(export_test == False):
                try:

                    #Export via arcpy
                    curr_fc_path = curr_gbd_path + "/" + curr_featurelayer_fc_name
                    arcpy.FeatureClassToFeatureClass_conversion(selection, curr_gbd_path, curr_featurelayer_fc_name)

                    #Export via arcgis api
                    #curr_fc_path = curr_gbd_path + "/" + curr_featurelayer_fc_name
                    #fl_sdf.spatial.to_featureclass(curr_fc_path)

                    #Create metadata file
                    curr_fc_metadata_path = curr_metadatadir + "/" + curr_featurelayer_name_short + ".xml"
                    if(not arcpy.Exists(curr_fc_metadata_path)):
                        curr_featurelayer_description = curr_featurelayer.properties.description
                        curr_featurelayer_credits = curr_featurelayer.properties.copyrightText
                        curr_fc_metadata = arcpy.metadata.Metadata(curr_fc_path)
                        curr_fc_metadata.description = curr_featurelayer_description
                        curr_fc_metadata.credits = curr_featurelayer_credits
                        curr_fc_metadata.save()
                        curr_fc_metadata.exportMetadata(curr_fc_metadata_path)

                    export_test = True

                except Exception as e:
                    #print(e)
                    export_attempt = export_attempt + 1
                    if(export_attempt < 6):
                        print("....EXPORT FAILED, RE-TRYING")
                        export_test = False
                    if(export_attempt >= 6):
                        print("....EXPORT FAILED 5 TIMES, SKIPPING DATASET")
                        export_test = True

                        #Export CSV file containing information needed to retry query outside of multiprocessor
                        if(curr_multiprocess == "Primary"):
                            csvdata = [{"SHORTNAME":curr_featurelayer_name_short, "URL":curr_featurelayer_url, "AOIFCPATH":curr_aoi_fc_path}]
                            exportfail_df = pandas.DataFrame(csvdata)
                            if("HIFLD" in curr_featureservice_name_short):
                                exportfail_csv_path = curr_outdir + "/exportfail_primary_" + "R" + curr_hifld_region + "_" + curr_featurelayer_name_short + ".csv"
                            else:
                                exportfail_csv_path = curr_outdir + "/exportfail_primary_" + curr_featurelayer_name_short + ".csv"
                            exportfail_df.to_csv(exportfail_csv_path, index=False)
                        if(curr_multiprocess == "Secondary"):
                            csvdata = [{"SHORTNAME":curr_featurelayer_name_short, "URL":curr_featurelayer_url, "AOIFCPATH":curr_aoi_fc_path}]
                            exportfail_df = pandas.DataFrame(csvdata)
                            if("HIFLD" in curr_featureservice_name_short):
                                exportfail_csv_path = curr_outdir + "/exportfail_secondary_" + "R" + curr_hifld_region + "_" + curr_featurelayer_name_short + "_ObjID" + str(curr_objid_number) + ".csv"
                            else:
                                exportfail_csv_path = curr_outdir + "/exportfail_secondary_" + curr_featurelayer_name_short + "_ObjID" + str(curr_objid_number) + ".csv"
                            exportfail_df.to_csv(exportfail_csv_path, index=False)

            #PROJECT OUTPUT IF THE COORDINATE SYSTEM DOES NOT MATCH THE USER SPECIFIED PROJECTION
            curr_fc_sr = arcpy.Describe(curr_fc_path).spatialReference
            curr_fc_sr_name = curr_fc_sr.name
            if(curr_fc_sr_name != curr_output_prj_sr.name):
                print("..PROJECTING OUTPUT FEATURE CLASS")
                curr_fc_prj_path = curr_gbd_path + "/" + curr_featurelayer_fc_name + "_prj"

                #Project the exported feature class to match the user specified projection
                project_check = False
                while(project_check == False):
                    try:
                        arcpy.Project_management(curr_fc_path, curr_fc_prj_path, curr_output_prj_sr)
                        project_check = True
                    except Exception as e:
                        print(e)
                        print("....PROJECT FAILED, RE-TRYING")
                        if(arcpy.Exists(curr_fc_prj_path)):
                            arcpy.Delete_management(curr_fc_prj_path)
                        time.sleep(5)

                #Delete the original exported output
                delete_check = False
                while(delete_check == False):
                    try:
                        arcpy.Delete_management(curr_fc_path)
                        delete_check = True
                    except Exception as e:
                        print(e)
                        print("....DELETE FEATURE CLASS FAILED, RE-TRYING")
                        time.sleep(5)

                #Rename the projected feature class
                rename_check = False
                while(rename_check == False):
                    try:
                        arcpy.Rename_management(curr_fc_prj_path, curr_fc_path)
                        rename_check = True
                    except Exception as e:
                        print(e)
                        print("....RENAME FEATURE CLASS FAILED, RE-TRYING")
                        time.sleep(5)

                print("..EXPORT COMPLETE")
            else:
                print("..EXPORT COMPLETE")

        print("..DONE!")

    except Exception as e:
        print(e)
        print("TOP LEVEL ERROR")
        time.sleep(60)



def worker_function_elevwetland(in_inputs_list):


    try:
        curr_url_list = list(in_inputs_list[0])
        curr_scratchdir_list = list(in_inputs_list[1])
        curr_outgdb_list = list(in_inputs_list[2])
        curr_cpu_number_list = list(in_inputs_list[3])
        curr_elevcontour_wetland_list = list(in_inputs_list[4])

        curr_scratchdir = curr_scratchdir_list[0]
        curr_outgdb_path = curr_outgdb_list[0]
        curr_cpu_number = curr_cpu_number_list[0]
        curr_elevcontour_wetland = curr_elevcontour_wetland_list[0]

        if(curr_elevcontour_wetland == "ElevContour"):
            elevcontour_wetland_fc_outpath = curr_outgdb_path + "/ElevContour" + "_" + str(curr_cpu_number)
        if(curr_elevcontour_wetland == "Wetlands"):
            elevcontour_wetland_fc_outpath = curr_outgdb_path + "/Wetlands" + "_" + str(curr_cpu_number)


        #Download the GDBs
        print(" ")
        print("DOWNLOADING GDBs")
        curr_url_list_sorted = sorted(curr_url_list)
        download_path_list = []
        for i in range(0, len(curr_url_list)):
            curr_url = curr_url_list[i]
            curr_url_basename = os.path.basename(curr_url)
            curr_download_path = curr_scratchdir + "/" + curr_url_basename

            #Try to download file, will retry if download fails
            print(".." + curr_url_basename + " (" + str(i + 1) + " out of " + str(len(curr_url_list)) + ")")
            download_check = False
            while(download_check == False):
                try:
                    urllib.request.urlretrieve(curr_url, curr_download_path)
                    urllib.request.urlcleanup()  ## Clear the download cache
                    download_check = True
                    download_path_list.append(curr_download_path)
                except:
                    print("....DOWNLOAD FAILED, RE-TRYING")
                    time.sleep(5)

        #Now unzip the downloaded file
        print(" ")
        print("UNZIPPING GDBs")
        download_path_gdbdir_list = []
        for i in range(0, len(download_path_list)):

            # Unzip the ElevContour downloads.
            if(curr_elevcontour_wetland == "ElevContour"):
                curr_download_path = download_path_list[i]
                curr_download_path_basename = os.path.basename(curr_download_path)
                curr_download_path_gdb = curr_download_path.replace(".zip", ".gdb")
                print(".." + curr_download_path_basename + " (" + str(i + 1) + " out of " + str(len(download_path_list)) + ")")
                zip_file = zipfile.ZipFile(curr_download_path)
                zip_file.extractall(curr_scratchdir)
                zip_file.close()
                download_path_gdbdir_list.append(curr_download_path_gdb)

            # Unzip the HUC8 downloads.
            if(curr_elevcontour_wetland == "Wetlands"):
                curr_download_path = download_path_list[i]
                curr_download_path_basename = os.path.basename(curr_download_path)
                curr_download_path_gdb = curr_download_path.replace(".zip", ".gdb")

                print(".." + curr_download_path_basename +  " (" + str(i+1) + " out of " + str(len(download_path_list)) + ")" )
                zip_file = zipfile.ZipFile(curr_download_path)
                zip_file.extractall(curr_scratchdir)
                zip_file.close()
                download_path_gdbdir_list.append(curr_download_path.replace("_watershed.zip", "_Watershed"))


        #Build list of feature class paths that will be merged together
        elevcontour_wetland_fc_path_list = []
        for i in range(0, len(download_path_gdbdir_list)):
            curr_download_path_gdbdir = download_path_gdbdir_list[i]

            if(curr_elevcontour_wetland == "ElevContour"):
                curr_elevcontour_wetland_fcpath = curr_download_path_gdbdir + "/Elev_Contour"
                elevcontour_wetland_fc_path_list.append(curr_elevcontour_wetland_fcpath)

            if(curr_elevcontour_wetland == "Wetlands"):
                curr_huc8_dir_basename = os.path.basename(curr_download_path_gdbdir)
                curr_huc8_number = curr_huc8_dir_basename.replace("_Watershed", "")
                curr_huc8_gdbname = curr_huc8_dir_basename.replace("_Watershed", ".gdb")
                curr_huc8_hucname = curr_huc8_gdbname.replace(".gdb", "")
                curr_huc8_gdbpath = curr_download_path_gdbdir + "/" + curr_huc8_gdbname
                curr_elevcontour_wetland_fcpath = curr_huc8_gdbpath + "/" + curr_huc8_number + "_Wetlands"
                elevcontour_wetland_fc_path_list.append(curr_elevcontour_wetland_fcpath)


        #Merge all features together
        if( len(elevcontour_wetland_fc_path_list) == 1 ):
            print(" ")
            print("COPYING FEATURE CLASS")
            copy_check = False
            while(copy_check == False):
                try:
                    arcpy.Copy_management(curr_elevcontour_wetland_fcpath, elevcontour_wetland_fc_outpath)
                    copy_check = True
                    print("COPY COMPLETE")
                except:
                    print("FAILED TO COPY FEATURE CLASS, RE-TRYING")
                    time.sleep(5)
        else:
            #Else if multiple feature classes, merge all into a single SDF
            print(" ")
            print("MERGING " + str(len(elevcontour_wetland_fc_path_list)) + " FEATURE CLASSES")
            merge_check = False
            while(merge_check == False):
                try:
                    arcpy.Merge_management(elevcontour_wetland_fc_path_list, elevcontour_wetland_fc_outpath)
                    merge_check = True
                    print("MERGE COMPLETE")
                except:
                    print("FAILED TO MERGE FEATURE CLASSES, RE-TRYING")
                    time.sleep(5)

    except Exception as e:
        print(e)
        print("TOP LEVEL ERROR")
        time.sleep(60)




#Reference:
#https://gis.stackexchange.com/questions/140533/can-multiprocessing-with-arcpy-be-run-in-a-script-tool

#Define function that applies multiprocessing to inputs
def execute_services(inputs):

    #Set multiprocessing python exe path
    multiprocessing.set_executable(os.path.join(sys.exec_prefix, 'python.exe'))

    #Get cpu count
    #cpucount = multiprocessing.cpu_count() - 1

    #Create pool of workers
    pool = multiprocessing.Pool()

    #Submit jobs to workers
    for curr_input in inputs:
        pool.imap_unordered(worker_function_services, [curr_input]) # args are passed as a list

    pool.close()
    pool.join()






#Define function that applies multiprocessing to inputs
def execute_elevwetland(inputs):

    #Set multiprocessing python exe path
    multiprocessing.set_executable(os.path.join(sys.exec_prefix, 'python.exe'))

    #Get cpu count
    #cpucount = multiprocessing.cpu_count() - 1

    #Create a pool of workers
    pool = multiprocessing.Pool()

    #Submit jobs to workers
    for curr_input in inputs:
        pool.imap_unordered(worker_function_elevwetland, [curr_input]) # args are passed as a list

    pool.close()
    pool.join()






if __name__=='__main__':

    # import current script to avoid:
    # PicklingError: Can't pickle <type 'function'>: attribute lookup __builtin__.function failed
    import FeatureLayerDownload

    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Feature Layer Download Tool developed by Matt Panunto, DOI-BLM")
    arcpy.AddMessage("Running v20210823")

    #ArcGIS Online Portal URL
    #pro_portal_toggle = "Yes"
    pro_portal_toggle = arcpy.GetParameterAsText(0)

    #ArcGIS Online Portal URL
    #portalurl = "https://www.arcgis.com"
    portalurl = arcpy.GetParameterAsText(1)

    #ArcGIS Online Username
    #username = "mpanunto_nifc"
    username = arcpy.GetParameterAsText(2)

    #ArcGIS Online Password
    #password = "xxxxxx"
    password = arcpy.GetParameterAsText(3)

    #Path to AOI shapefile polygon
    #aoi_shp_path = r"C:\Workspace\development\FeatureLayerDownload\AOI_UT.shp"
    #aoi_shp_path = r"C:\Workspace\development\FeatureLayerDownload\AOI_SLC.shp"
    aoi_shp_path = arcpy.GetParameterAsText(4)

    #AOI Subdivision Area (in square miles)
    #aoi_subdivision_area = "5000"
    aoi_subdivision_area = arcpy.GetParameterAsText(5)

    #User defined output projection
    #output_prj = "PROJCS['NAD_1983_UTM_Zone_12N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-111.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 -9998100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
    output_prj = arcpy.GetParameterAsText(6)

    #Output GDB Directory
    #outdir = r"C:\Workspace\development\FeatureLayerDownload\output_ut"
    #outdir = r"C:\Workspace\development\FeatureLayerDownload\output_slc"
    outdir = arcpy.GetParameterAsText(7)

    #Path to feature service ItemID CSV
    #service_itemid_csv_path = r"C:\Workspace\development\FeatureLayerDownload\FeatureLayerDownload.csv"
    service_itemid_csv_path = arcpy.GetParameterAsText(8)

    #elevcontour_acquire = "Yes"
    elevcontour_acquire = arcpy.GetParameterAsText(9)

    #wetland_acquire = "Yes"
    wetland_acquire = arcpy.GetParameterAsText(10)

    #offline_license_check = "Yes"
    offline_license_check = arcpy.GetParameterAsText(11)



    #Check if active portal includes the text "nifc.maps.arcgis.com", throw error if so
    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("SIGNING INTO PORTAL")
    if(pro_portal_toggle == "Yes"):
        active_portal_url = arcpy.GetActivePortalURL()
        if("nifc.maps.arcgis.com" in active_portal_url):
            arcpy.AddError("USERS ACTIVE PORTAL URL IS https://nifc.maps.arcgis.com. \
            \nTO PROPERLY ESTABLISH NIFC SERVICE CONNECTIONS, THE ACTIVE PORTAL URL MUST BE https://www.arcgis.com")
            raise arcpy.ExecuteError
    else:
        arcpy_portal = arcpy.SignInToPortal(portalurl, username, password)


    #Establish connection to the ArcGIS Online Org
    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("REQUESTING API ACCESS TOKEN")
    if(pro_portal_toggle == "Yes"):
        gis = GIS("pro")
    else:
        gis = GIS(portalurl, username, password, verify_cert=False)


    #Test if output folder is empty, if not, throw error
    if len(os.listdir(outdir)) != 0:
        arcpy.AddError("OUTPUT DIRECTORY IS NOT EMPTY. USER MUST SPECIFY AN EMPTY OUTPUT DIRECTORY.")
        raise arcpy.ExecuteError

    #Create scratch sirectory
    scratchdir = outdir + "/_scratch"
    os.mkdir(scratchdir)

    #Test if user's license is offline
    if(offline_license_check == "Yes"):
        arcpy.AddMessage("PERFORMING OFFLINE LICENSE CHECK")
        try:
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

        except:
            arcpy.AddError("UNABLE TO VERIFY IF ARCGIS PRO LICENSE IS ENABLED FOR OFFLINE USE")
            arcpy.AddError("DUE TO RISK OF LICENSE CORRUPTION, IT IS RECOMMENDED TO RETURN AN OFFLINE LICENSE TEMPORARILY WHILE RUNNING THIS TOOL")
            arcpy.AddError("TO PROCEED WITH AN OFFLINE LICENSE, SET INPUT VALUE 'Perform Offline License Check' TO 'No' AND RE-RUN TOOL")
            raise arcpy.ExecuteError

        if( (offline_true_maxline > offline_false_maxline) or (offline_request_maxline > offline_false_maxline)):
            #Compare the two highest numbers, whichever is higher is the current license status
            arcpy.AddError("ARCGIS PRO LICENSE IS ENABLED FOR OFFLINE USE")
            arcpy.AddError("DUE TO RISK OF LICENSE CORRUPTION, IT IS RECOMMENDED TO RETURN AN OFFLINE LICENSE TEMPORARILY WHILE RUNNING THIS TOOL")
            arcpy.AddError("TO PROCEED WITH AN OFFLINE LICENSE, SET INPUT VALUE 'Bypass Offline License Check' TO 'No' AND RE-RUN TOOL")
            raise arcpy.ExecuteError


    #Create spatial reference object from user defined output projection
    curr_output_prj_sr = arcpy.SpatialReference(text=output_prj)

    #Create AOI GDB
    aoi_gdb_path = scratchdir + "/AOI.gdb"
    arcpy.CreateFileGDB_management(scratchdir, "AOI")

    #DISSOLVE AOI SHAPEFILE IF NECESSARY
    #Get feature count of AOI shapefile, dissolve features if more than 1
    aoi_feature_count = int(str(arcpy.GetCount_management(aoi_shp_path)))
    if(aoi_feature_count > 1):
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("USER SPECIFIED AOI HAS MULTIPLE FEATURES, DISSOLVING")

        #Get AOI shapefile field names
        aoi_shp_field_obj = arcpy.ListFields(aoi_shp_path)
        aoi_shp_field_names = []
        for field in aoi_shp_field_obj:
            aoi_shp_field_names.append(str(field.name))

        #If "AOI_Diss" is not a field in the list, create it
        if("AOI_Diss" not in aoi_shp_field_names):
            arcpy.AddField_management(aoi_shp_path, field_name="AOI_Diss", field_type="SHORT")

        arcpy.CalculateField_management(aoi_shp_path, field="AOI_Diss", expression="1")
        aoi_shp_basename = os.path.basename(aoi_shp_path)
        aoi_dissolve_path = aoi_gdb_path + "/" + aoi_shp_basename.replace(".shp", "_dissolve")
        arcpy.Dissolve_management(aoi_shp_path, aoi_dissolve_path, dissolve_field="AOI_Diss")
    else:
        aoi_shp_basename = os.path.basename(aoi_shp_path)
        aoi_dissolve_name = aoi_shp_basename.replace(".shp", "_dissolve")
        arcpy.FeatureClassToFeatureClass_conversion(aoi_shp_path, aoi_gdb_path, aoi_dissolve_name)
        aoi_dissolve_path = aoi_gdb_path + "/" + aoi_dissolve_name

    #SUBDIVIDE AOI SHAPEFILE/FC IF NECESSARY
    #Calculate total area of AOI feature in square miles. Then compare/divide it with the user specified area value
    arcpy.AddField_management(aoi_dissolve_path, field_name="AOI_Area", field_type="Double")
    arcpy.CalculateField_management(aoi_dissolve_path, "AOI_Area", "!shape.area@SQUAREMILES!", "PYTHON", "")
    aoi_area_calc_df = arcgis.GeoAccessor.from_featureclass(aoi_dissolve_path)
    aoi_area_calc = list(aoi_area_calc_df["AOI_Area"])[0]
    aoi_area_calc_divide = aoi_area_calc / int(aoi_subdivision_area)

    #If AOI area is larger than user specified value, perform subdivide
    if(aoi_area_calc > int(aoi_subdivision_area)):
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("TOTAL AOI AREA GREATER THAN USER SPECIFIED VALUE, SUBDIVIDING")
        aoi_dissolve_basename = os.path.basename(aoi_dissolve_path)
        aoi_dissolve_name = aoi_dissolve_basename.replace(".shp", "")
        aoi_subdivide_path = aoi_gdb_path + "/" + aoi_dissolve_name + "_subdivide"

        #AOI not quite large enough to split into multiple pieces at the user defined size
        #So, need to use the NUMBER_OF_EQUAL_PARTS method instead
        if(aoi_area_calc_divide > 1 and aoi_area_calc_divide < 2):
            arcpy.SubdividePolygon_management(aoi_dissolve_path, aoi_subdivide_path, method="NUMBER_OF_EQUAL_PARTS", num_areas=2, subdivision_type="STACKED_BLOCKS")

        #AOI is large enough to split into multiple pieces at the user defined size
        #So, use the EQUAL_AREAS method
        if(aoi_area_calc_divide > 2):
            target_area_str = aoi_subdivision_area + " SquareMiles"
            arcpy.SubdividePolygon_management(aoi_dissolve_path, aoi_subdivide_path, method="EQUAL_AREAS", target_area=target_area_str, subdivision_type="STACKED_BLOCKS")

        aoi_final_path = aoi_subdivide_path
    else:
        aoi_final_path = aoi_dissolve_path


    #Create AOI final dataframe from shapefile
    aoi_final_df = arcgis.GeoAccessor.from_featureclass(aoi_final_path)

    #Export AOI final df to feature class, and create individual feature classes for each ObjectID
    aoi_final_path = aoi_gdb_path + "/AOI_final"
    aoi_final_df.spatial.to_featureclass(aoi_final_path, sanitize_columns=False)

    #Get ObjectIDs from AOI final feature class
    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("CREATING INDIVIDUAL AOI FEATURE CLASSES")
    objid_list = list(aoi_final_df["OBJECTID"])
    objid_fc_path_list = []
    for i in range(0, len(objid_list)):
        curr_objid = objid_list[i]
        arcpy.AddMessage("..AOI ObjectID " + str(curr_objid) + " out of " + str(max(objid_list)))
        curr_objid_df = aoi_final_df[aoi_final_df["OBJECTID"] == curr_objid]
        curr_objid_fc_path = aoi_final_path + "_OBJID" + str(curr_objid)
        objid_fc_path_list.append(curr_objid_fc_path)
        curr_objid_df.spatial.to_featureclass(curr_objid_fc_path, sanitize_columns=False)

    #Create dataframe of feature service ItemID spreadsheet
    service_itemid_df = pandas.read_csv(service_itemid_csv_path)

    #Create list of feature service ItemIDs
    service_itemid_list = list(service_itemid_df["ItemID"])


    ############################################################################
    ## BEGIN ELEVATION CONTOUR PROCESSING
    ############################################################################
    if(elevcontour_acquire == "Yes"):

        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("ACQUIRING USGS TOPO VECTOR CONTOURS")

        #Get feature layers from the basedata feature service
        basedata_service = curr_service = gis.content.get("6dcb2dab3c314912a45872eabfa467e2")
        basedata_layers = basedata_service.layers

        #Create spatial dataframe from user defined AOI shapefile, and an AOI geometry object
        aoi_sdf = pandas.DataFrame.spatial.from_featureclass(aoi_dissolve_path)
        aoi_geom = aoi_sdf["SHAPE"][0]
        aoi_geom_wkid = aoi_geom.spatialReference["wkid"]

        #Create spatial reference object for user defined output projection
        output_sr = arcpy.SpatialReference()
        output_sr.loadFromString(output_prj)
        output_wkid = output_sr.factoryCode

        #Project AOI geometry object to user defined output projection, just in case the AOI shapefile isn't actually in that projection
        aoi_geom = aoi_geom.project_as(output_wkid)

        #Get feature layers for UGSG_TopoVector index (for contours)
        usgstopovec_featurelayer = basedata_layers[0]
        usgstopovec_url = usgstopovec_featurelayer.url

        #If the user defined projection differs from the USGS_TopoVector layer, reproject to match
        curr_wkid = usgstopovec_featurelayer.properties.extent.spatialReference.wkid
        curr_layer_sr = arcpy.SpatialReference(curr_wkid)
        if(output_wkid != curr_wkid):
            aoi_shp_prj = aoi_gdb_path + "/AOI_final_prj"
            arcpy.Project_management(aoi_dissolve_path, aoi_shp_prj, out_coor_system=curr_wkid)
            aoi_geom_prj = aoi_geom.project_as(curr_wkid)
        else:
            aoi_shp_prj = aoi_dissolve_path
            aoi_geom_prj = aoi_geom


        #Define outpath for the intersection index shapefile
        usgstopovec_index_aoi = scratchdir + "/USGS_TopoVector_Index_AOI.shp"

        #Try querying via ArcGIS API first, if it fails, try again via arcpy
        try:
            arcpy.AddMessage("..QUERYING USGS TOPO VECTOR INDEX VIA ARCGIS API")
            usgstopovec_query = usgstopovec_featurelayer.query(where="1=1", geometry_filter=filters.intersects(aoi_geom_prj), out_sr=output_wkid)
            usgstopovec_count = len(usgstopovec_query)
            if( usgstopovec_count > 0):
                usgstopovec_sdf = usgstopovec_query.sdf
                usgstopovec_url_list = list(usgstopovec_sdf["URL"])
                usgstopovec_sdf.spatial.to_featureclass(usgstopovec_index_aoi)
        except:
            arcpy.AddMessage("..QUERY FAILED, ATTEMPTING QUERY VIA ARCPY" )
            #Reset environment settings
            arcpy.ResetEnvironments()
            #Set overwrite to True
            arcpy.env.overwriteOutput = True
            #Set output coordinate system
            arcpy.env.outputCoordinateSystem = output_sr

            #Project AOI to feature layer's projection
            arcpy.AddMessage("..PROJECTING AOI FOR SELECTION")
            aoi_usgstopovec_prj_path = aoi_gdb_path + "/AOI_usgstopovec_prj"
            arcpy.Project_management(aoi_dissolve_path, aoi_usgstopovec_prj_path, out_coor_system=curr_layer_sr)

            #Perform select by location, try up to 3 times
            arcpy.AddMessage("..SELECTING INTERSECTING FEATURES")
            usgstopovec_selection = arcpy.SelectLayerByLocation_management(usgstopovec_url, overlap_type="INTERSECT", select_features=aoi_usgstopovec_prj_path, selection_type="NEW_SELECTION")
            usgstopovec_count = int(arcpy.GetCount_management(usgstopovec_selection)[0])
            if( usgstopovec_count > 0):
                arcpy.FeatureClassToFeatureClass_conversion(usgstopovec_selection, scratchdir, "USGS_TopoVector_Index_AOI")
                usgstopovec_sdf = arcgis.GeoAccessor.from_featureclass(usgstopovec_index_aoi)
                usgstopovec_url_list = list(usgstopovec_sdf["URL"])


        #Test to see if any quads were intersected, if not, skip to next dataset
        if(usgstopovec_count <= 0):
            arcpy.AddMessage("..NO USGS TOPO VECTOR QUADS FOUND, SKIPPING DATASET")
        else:

            #Create output GDB
            arcpy.AddMessage("..CREATING OUTPUT GDB")
            outGdb = "ElevContour.gdb"
            outGdb_path = outdir + "/" + outGdb
            arcpy.CreateFileGDB_management(outdir, outGdb)
            elevcontour_fc_path = outGdb_path + "/ElevContour"

            #Sort the urlList alphabetically
            urlList_sorted = usgstopovec_url_list
            urlList_sorted.sort()
            url_count = len(urlList_sorted)

            #Create lists for multiprocessor
            scratchdir_list = [scratchdir] * url_count
            outgdb_path_list = [outGdb_path] * url_count
            elevcontour_str_list = ["ElevContour"] * url_count

            #get CPU count, and range
            cpu_count = multiprocessing.cpu_count()
            cpu_range = list(range(1, (cpu_count + 1)))

            #Split lists into equal sizes, based on cpu_count
            url_list_cpu_split = numpy.array_split(urlList_sorted, cpu_count)
            scratchdir_list_cpu_split = numpy.array_split(scratchdir_list, cpu_count)
            outgdb_path_list_cpu_split = numpy.array_split(outgdb_path_list, cpu_count)
            elevcontour_str_list_cpu_split = numpy.array_split(elevcontour_str_list, cpu_count)

            #Create list of CPU numbers for the multiprocessor
            cpu_number_list = []
            for i in range(0, len(url_list_cpu_split)):
                curr_url_list_len = len(url_list_cpu_split[i])
                cpu_number_list = cpu_number_list + ([cpu_range[i]] * curr_url_list_len)

            #Split cpu number list into equal size, based on cpu_count
            cpu_number_list_cpu_split = numpy.array_split(cpu_number_list, cpu_count)

            #Create inputs list for multiprocessor
            inputs_list_elevcontour = list(map(list, zip(url_list_cpu_split, scratchdir_list_cpu_split, outgdb_path_list_cpu_split, cpu_number_list_cpu_split, elevcontour_str_list_cpu_split)))

            arcpy.AddMessage("..BEGINNING MULTIPROCESSOR DOWNLOAD: (" + str(url_count) + " GDBs)")
            FeatureLayerDownload.execute_elevwetland(inputs_list_elevcontour)
            arcpy.AddMessage("..FINISHED MULTIPROCESSING")

            #List multiprocessing output feature classes
            arcpy.env.workspace = outGdb_path
            elevcontour_fc_list = arcpy.ListFeatureClasses()
            elevcontour_fc_path_list = [outGdb_path + "/" + s  for s in elevcontour_fc_list]

            #Merge multiprocessing output feature classes
            arcpy.env.outputCoordinateSystem = curr_output_prj_sr
            arcpy.AddMessage("..PERFORMING FINAL MERGE")
            elevcontour_final_out = outGdb_path + "/ElevContour"
            arcpy.Merge_management(elevcontour_fc_path_list, elevcontour_final_out)
            arcpy.ResetEnvironments()

            #Remove identical features in output feature class
            arcpy.AddMessage("..REMOVING DUPLICATE FEATURES")
            try:
                arcpy.DeleteIdentical_management(elevcontour_final_out, fields=["Shape"])
            except:
                arcpy.AddMessage("....FAILED TO REMOVE DUPLICATE FEATURES, SKIPPING")

            #Delete individual multiprocessor outputs
            arcpy.AddMessage("..DELETING MULTIPROCESSOR OUTPUTS")
            arcpy.Delete_management(elevcontour_fc_path_list)

            #Delete scratch files
            arcpy.AddMessage("..DELETING SCRATCH FILES")
            arcpy.env.workspace = scratchdir

            #Delete all folders (this includes GDBs)
            scratch_folders_list = glob.glob(scratchdir + "/*/")
            for i in range(0, len(scratch_folders_list)):
                curr_folder_del = scratch_folders_list[i]

                #Don't delete the AOI.gdb
                if("AOI.gdb" in curr_folder_del):
                    continue
                try:
                    shutil.rmtree(curr_folder_del)
                except:
                    ""

            #Delete all other files
            scratch_files_list = os.listdir(scratchdir)
            for i in range(0, len(scratch_files_list)):
                curr_file_del = scratch_files_list[i]
                if("aoi_buffer" in curr_file_del):
                    continue
                else:
                    try:
                        os.remove(scratchdir + "/" + curr_file_del)
                    except:
                        ""

    ############################################################################
    ## BEGIN HUC8 WETLAND PROCESSING
    ############################################################################
    if(wetland_acquire == "Yes"):

        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("ACQUIRING WETLAND DATA")

        #Get feature layers from the basedata feature service
        basedata_service = curr_service = gis.content.get("6dcb2dab3c314912a45872eabfa467e2")
        basedata_layers = basedata_service.layers

        #Create spatial dataframe from user defined AOI shapefile, and an AOI geometry object
        aoi_sdf = pandas.DataFrame.spatial.from_featureclass(aoi_dissolve_path)
        aoi_geom = aoi_sdf["SHAPE"][0]
        aoi_geom_wkid = aoi_geom.spatialReference["wkid"]

        #Create spatial reference object for user defined output projection
        output_sr = arcpy.SpatialReference()
        output_sr.loadFromString(output_prj)
        output_wkid = output_sr.factoryCode

        #Project AOI geometry object to user defined output projection, just in case the AOI shapefile isn't actually in that projection
        aoi_geom = aoi_geom.project_as(output_wkid)

        #Get feature layers for HUC8 index (for wetlands)
        huc8_featurelayer = basedata_layers[8]
        huc8_url = huc8_featurelayer.url

        #If the user defined projection is differs from the feature layer, reproject to match
        curr_wkid = huc8_featurelayer.properties.extent.spatialReference.wkid
        curr_layer_sr = arcpy.SpatialReference(curr_wkid)
        if(output_wkid != curr_wkid):
            aoi_shp_prj = aoi_gdb_path + "/AOI_final_prj"
            arcpy.Project_management(aoi_dissolve_path, aoi_shp_prj, out_coor_system=curr_wkid)
            aoi_geom_prj = aoi_geom.project_as(curr_wkid)
        else:
            aoi_shp_prj = aoi_dissolve_path
            aoi_geom_prj = aoi_geom

        #Define outpath for the intersection index shapefile
        huc8_index_path = scratchdir + "/USGS_HUC8_Index_AOI.shp"

        #Try querying via ArcGIS API first, if it fails, try again via arcpy
        try:
            arcpy.AddMessage("..QUERYING HUC8 INDEX VIA ARCGIS API")
            huc8_query = huc8_featurelayer.query(where="1=1", geometry_filter=filters.intersects(aoi_geom_prj), out_sr=output_wkid)
            huc8_count = len(huc8_query)
            if( huc8_count > 0):
                huc8_sdf = huc8_query.sdf
                huc8_url_list = list(huc8_sdf["URL"])
                huc8_sdf.spatial.to_featureclass(huc8_index_path)
        except:
            arcpy.AddMessage("..QUERY FAILED, ATTEMPTING QUERY VIA ARCPY" )
            #Reset environment settings
            arcpy.ResetEnvironments()
            #Set overwrite to True
            arcpy.env.overwriteOutput = True
            #Set output coordinate system
            arcpy.env.outputCoordinateSystem = output_sr

            #Project AOI to feature layer's projection
            arcpy.AddMessage("..PROJECTING AOI FOR SELECTION")
            aoi_huc8_prj_path = aoi_gdb_path + "/AOI_huc8_prj"
            arcpy.Project_management(aoi_dissolve_path, aoi_huc8_prj_path, out_coor_system=curr_layer_sr)

            #Perform select by location, try up to 3 times
            arcpy.AddMessage("..SELECTING INTERSECTING FEATURES")
            huc8_selection = arcpy.SelectLayerByLocation_management(huc8_url, overlap_type="INTERSECT", select_features=aoi_huc8_prj_path, selection_type="NEW_SELECTION")
            huc8_count = int(arcpy.GetCount_management(huc8_selection)[0])
            if( huc8_count > 0):
                arcpy.FeatureClassToFeatureClass_conversion(huc8_selection, scratchdir, "USGS_HUC8_Index_AOI")
                huc8_sdf = arcgis.GeoAccessor.from_featureclass(huc8_index_path)
                huc8_url_list = list(huc8_sdf["URL"])

        #Test to see if any quads were intersected, if not, skip to next dataset
        if(huc8_count <= 0):
            arcpy.AddMessage("..NO HUC8 DATA FOUND, SKIPPING DATASET")
        else:

            #Create the output GDB.
            arcpy.AddMessage("..CREATING OUTPUT GDB")
            outGdb = "Wetlands.gdb"
            outGdb_path = outdir + "/" + outGdb
            arcpy.CreateFileGDB_management(outdir, outGdb)

            #Sort the urlList alphabetically
            urlList_sorted = huc8_url_list
            urlList_sorted.sort()
            url_count = len(urlList_sorted)

            #Create lists for multiprocessor
            scratchdir_list = [scratchdir] * url_count
            outgdb_path_list = [outGdb_path] * url_count
            wetlands_str_list = ["Wetlands"] * url_count

            #get CPU count, and range
            cpu_count = multiprocessing.cpu_count()
            cpu_range = list(range(1, (cpu_count + 1)))

            #Split lists into equal sizes, based on cpu_count
            url_list_cpu_split = numpy.array_split(urlList_sorted, cpu_count)
            scratchdir_list_cpu_split = numpy.array_split(scratchdir_list, cpu_count)
            outgdb_path_list_cpu_split = numpy.array_split(outgdb_path_list, cpu_count)
            wetlands_str_list_cpu_split = numpy.array_split(wetlands_str_list, cpu_count)

            #Create list of CPU numbers for the multiprocessor
            cpu_number_list = []
            for i in range(0, len(url_list_cpu_split)):
                curr_url_list_len = len(url_list_cpu_split[i])
                cpu_number_list = cpu_number_list + ([cpu_range[i]] * curr_url_list_len)

            #Split cpu number list into equal size, based on cpu_count
            cpu_number_list_cpu_split = numpy.array_split(cpu_number_list, cpu_count)

            #Create inputs list for multiprocessor
            inputs_list_wetlands = list(map(list, zip(url_list_cpu_split, scratchdir_list_cpu_split, outgdb_path_list_cpu_split, cpu_number_list_cpu_split, wetlands_str_list_cpu_split)))

            arcpy.AddMessage("..BEGINNING MULTIPROCESSOR DOWNLOAD: (" + str(url_count) + " GDBs)")
            FeatureLayerDownload.execute_elevwetland(inputs_list_wetlands)
            arcpy.AddMessage("..FINISHED MULTIPROCESSING")

            #List multiprocessing output feature classes
            arcpy.env.workspace = outGdb_path
            wetlands_fc_list = arcpy.ListFeatureClasses()
            wetlands_fc_path_list = [outGdb_path + "/" + s  for s in wetlands_fc_list]

            #Merge multiprocessing output feature classes
            arcpy.env.outputCoordinateSystem = curr_output_prj_sr
            arcpy.AddMessage("..PERFORMING FINAL MERGE")
            wetlands_final_out = outGdb_path + "/Wetlands"
            arcpy.Merge_management(wetlands_fc_path_list, wetlands_final_out)
            arcpy.ResetEnvironments()

            #Remove identical features in output feature class
            #arcpy.AddMessage("..REMOVING DUPLICATE FEATURES")
            #try:
                #arcpy.DeleteIdentical_management(wetlands_final_out, fields=["Shape"])
            #except:
                #arcpy.AddMessage("....FAILED TO REMOVE DUPLICATE FEATURES, SKIPPING")

            #Delete individual multiprocessor outputs
            arcpy.AddMessage("..DELETING MULTIPROCESSOR OUTPUTS")
            arcpy.Delete_management(wetlands_fc_path_list)

            #Delete scratch files
            arcpy.AddMessage("..DELETING SCRATCH FILES")
            arcpy.env.workspace = scratchdir

            #Delete all folders (this includes GDBs)
            scratch_folders_list = glob.glob(scratchdir + "/*/")
            for i in range(0, len(scratch_folders_list)):
                curr_folder_del = scratch_folders_list[i]

                #Don't delete the AOI.gdb
                if("AOI.gdb" in curr_folder_del):
                    continue
                try:
                    shutil.rmtree(curr_folder_del)
                except:
                    ""

            #Delete all other files
            scratch_files_list = os.listdir(scratchdir)
            for i in range(0, len(scratch_files_list)):
                curr_file_del = scratch_files_list[i]
                if("aoi_buffer" in curr_file_del):
                    continue
                else:
                    try:
                        os.remove(scratchdir + "/" + curr_file_del)
                    except:
                        ""


    ############################################################################
    ## PREP VARIABLES FOR MULTIPROCESSOR
    ############################################################################


    #Create metadata directory
    metadatadir = scratchdir + "/_metadata"
    os.mkdir(metadatadir)

    #Create service connections, and build a list of feature layers
    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Connecting to feature services")
    featureservice_name_list_primary = []
    featureservice_name_list_secondary = []
    featurelayerurl_list_primary = []
    featurelayerurl_list_secondary = []
    curr_iter = 0
    for i in range(0, len(service_itemid_list)):
        curr_itemid = service_itemid_list[i]
        try:

            #Get service and service name
            try:
                curr_service = gis.content.get(curr_itemid)
            except:
                arcpy.AddMessage("..UNABLE TO CONNECT TO SERVICE, CHECK ACCESS PERMISSIONS (ItemID = " + curr_itemid + ")" )
                continue
            curr_service_name = curr_service.name
            arcpy.AddMessage(".." + curr_service_name)

            #Get a list of layers in the service
            curr_service_layers = curr_service.layers

            #Loop through all the layers
            for j in range(0, len(curr_service_layers)):
                curr_layer = curr_service_layers[j]

                #If current layer is a feature layer, append info to lists
                if(type(curr_layer) == arcgis.features.layer.FeatureLayer):
                    try:

                        curr_featurelayer = curr_layer

                        #Get name
                        curr_featurelayer_name = curr_featurelayer.properties.name
                        curr_featurelayer_name_short = curr_featurelayer_name.replace(" ", "")
                        curr_featurelayer_name_short = curr_featurelayer_name_short.replace("_", "")
                        curr_featurelayer_name_short = curr_featurelayer_name_short.replace("-", "")
                        curr_featurelayer_name_short = curr_featurelayer_name_short.replace("&", "")

                        arcpy.AddMessage("...." + curr_featurelayer_name + " (" + str(curr_iter) + ")")

                        #Get URL
                        curr_featurelayer_url = curr_featurelayer.url

                        #Download feature service metadata xml, then rename it
                        #curr_service_metadata_path = metadatadir + "/metadata.xml"
                        #curr_service_metadata_rename_path = metadatadir + "/" + curr_service_name + "_" + curr_featurelayer_name_short + ".xml"
                        #if(os.path.exists(curr_service_metadata_path)):
                            #os.remove(curr_service_metadata_path)
                        #if(os.path.exists(curr_service_metadata_rename_path)):
                            #os.remove(curr_service_metadata_rename_path)
                        #curr_service.download_metadata(metadatadir)
                        #os.rename(curr_service_metadata_path, curr_service_metadata_rename_path)

                        #Download feature layer metadata xml
                        #curr_featurelayer_metadata_path = metadatadir + "/" + curr_featurelayer_name_short + ".xml"
                        #curr_featurelayer_metadata = arcpy.metadata.Metadata(curr_featurelayer)
                        #curr_featurelayer_metadata.exportMetadata(curr_featurelayer_metadata_path)


                        #Get metadata info from service, and feature layer
                        #curr_service_description = curr_service.description
                        #curr_service_termsofuse = curr_service.licenseInfo
                        #curr_service_tags = curr_service.tags
                        #curr_service_credits = curr_service.accessInformation
                        #curr_service_owner = curr_service.owner
                        #curr_featurelayer_description = curr_featurelayer.properties.description
                        #curr_featurelayer_credits = curr_featurelayer.properties.copyrightText

                        #Append URLs to lists. If they are high-density datasets, send them through the secondary multiprocessor instead
                        if(curr_featurelayer_name in ["Roads", "Forest Service Roads", "NHDFlowline", "NHDWaterbody", "BLM PLSS Sections"]):
                            featurelayerurl_list_secondary.append(curr_featurelayer_url)
                            featureservice_name_list_secondary.append(curr_service_name)
                        else:
                            featurelayerurl_list_primary.append(curr_featurelayer_url)
                            featureservice_name_list_primary.append(curr_service_name)

                        curr_iter = curr_iter + 1


                    except Exception as e:
                        print(e)

        except Exception as e:
            print(e)

    #Create input lists for primary multiprocessing
    featurelayer_count_primary = len(featurelayerurl_list_primary)
    pro_portal_toggle_list_primary = [pro_portal_toggle] * featurelayer_count_primary
    portalurl_list_primary = [portalurl] * featurelayer_count_primary
    username_list_primary = [username] * featurelayer_count_primary
    password_list_primary = [password] * featurelayer_count_primary
    aoi_path_list_primary = [aoi_dissolve_path] * featurelayer_count_primary
    output_prj_list_primary = [output_prj] * featurelayer_count_primary
    gdb_outdir_list_primary = [outdir] * featurelayer_count_primary
    multiprocess_list_primary = ["Primary"] * featurelayer_count_primary
    inputs_list_primary = list(map(list, zip(pro_portal_toggle_list_primary, portalurl_list_primary, username_list_primary, password_list_primary, aoi_path_list_primary, output_prj_list_primary, gdb_outdir_list_primary, featurelayerurl_list_primary, featureservice_name_list_primary, multiprocess_list_primary)))


    ############################################################################
    ## BEGIN MULTIPROCESSOR
    ############################################################################
    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Begin primary multiprocessing")
    FeatureLayerDownload.execute_services(inputs_list_primary)
    arcpy.AddMessage("Finished primary multiprocessing")

    #Now test to see if any queries, selections, or exports failed during the primary multiprocessing
    filelist = os.listdir(outdir)
    queryfailcsv_list = []
    selectfailcsv_list = []
    exportfailcsv_list = []
    failcsv_list = []
    for i in range(0, len(filelist)):
        curr_file = filelist[i]
        if(curr_file[0:17] == "queryfail_primary"):
            queryfailcsv_list.append(curr_file)
        if(curr_file[0:18] == "selectfail_primary"):
            selectfailcsv_list.append(curr_file)
        if(curr_file[0:18] == "exportfail_primary"):
            exportfailcsv_list.append(curr_file)
    failcsv_list = queryfailcsv_list + selectfailcsv_list + exportfailcsv_list

    #If any secondary featurelayerurls, or if any queries, selections, or exports failed, run secondary multiprocessor
    if((len(featurelayerurl_list_secondary) > 0) or (len(failcsv_list) > 0)):

        #Get list of feature layer URLs from failed items
        failcsv_urllist = []
        failcsv_featureservicenamelist = []
        for i in range(0, len(failcsv_list)):
            curr_csv = failcsv_list[i]
            curr_csv_path = outdir + "/" + curr_csv
            curr_df = pandas.read_csv(curr_csv_path)
            curr_featurelayer_url = curr_df["URL"][0]
            curr_featureservice = gis.content.get(curr_featurelayer.properties.serviceItemId)
            curr_featureservice_name = curr_featureservice.name
            failcsv_urllist.append(curr_featurelayer_url)
            failcsv_featureservicenamelist.append(curr_featureservice_name)

        #If any feature layers failed during the primary multiprocessing, append them to the secondary list
        if(len(failcsv_urllist)>0):
            featurelayerurl_list_secondary = featurelayerurl_list_secondary + failcsv_urllist
            featureservice_name_list_secondary = featureservice_name_list_secondary + failcsv_featureservicenamelist

        #Create input lists for secondary multiprocessing
        objid_count = len(objid_list)
        featurelayer_count_secondary = len(featurelayerurl_list_secondary)
        pro_portal_toggle_list_secondary = [pro_portal_toggle] * (objid_count * featurelayer_count_secondary)
        portalurl_list_secondary = [portalurl] * (objid_count * featurelayer_count_secondary)
        username_list_secondary = [username] * (objid_count * featurelayer_count_secondary)
        password_list_secondary = [password] * (objid_count * featurelayer_count_secondary)
        aoi_path_list_secondary = list(numpy.repeat(objid_fc_path_list,featurelayer_count_secondary))
        objid_list_secondary = list(numpy.repeat(objid_list,featurelayer_count_secondary))
        output_prj_list_secondary = [output_prj] * (objid_count * featurelayer_count_secondary)
        gdb_outdir_list_secondary = [outdir] * (objid_count * featurelayer_count_secondary)
        featurelayerurl_list_secondary_all = featurelayerurl_list_secondary * objid_count
        featureservice_name_list_secondary_all = featureservice_name_list_secondary * objid_count
        multiprocess_list_secondary = ["Secondary"] * (objid_count * featurelayer_count_secondary)
        inputs_list_secondary = list(zip(pro_portal_toggle_list_secondary, portalurl_list_secondary, username_list_secondary, password_list_secondary, aoi_path_list_secondary, output_prj_list_secondary, gdb_outdir_list_secondary, featurelayerurl_list_secondary_all, featureservice_name_list_secondary_all, multiprocess_list_secondary))

        #Run secondary multiprocessor
        arcpy.AddMessage("\u200B")
        arcpy.AddMessage("Begin secondary multiprocessing")
        FeatureLayerDownload.execute_services(inputs_list_secondary)
        arcpy.AddMessage("Finished secondary multiprocessing")


    ############################################################################
    ## BEGIN MERGING DATASETS
    ############################################################################

    #Create master output GDB
    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Creating master output GDB")
    master_gdb_outname = "FeatureLayerDownload"
    master_gbd_outpath = outdir + "/" + master_gdb_outname + ".gdb"
    if(not arcpy.Exists(master_gbd_outpath)):
        arcpy.management.CreateFileGDB(outdir, master_gdb_outname)

    #Reset environment settings
    arcpy.ResetEnvironments()
    arcpy.env.overwriteOutput = True

    #Now determine if multiple feature classes exist for any of the datasets. Merge together if so
    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Checking if any output feature classes need merging")

    #First, check if any corrupt GDBs exist, if so, delete them
    corrupgdb_path_list = []
    for file in os.listdir(outdir):
        if file.endswith(".txt"):
            corrupt_txtfile = file
            corrupt_txtfile_splitlist = corrupt_txtfile.split("_")
            txtfile_splitlist_end = txtfile_splitlist[len(txtfile_splitlist) - 1]
            txtfile_splitlist_end_split = txtfile_splitlist_end.split(".txt")
            txtfile_number = txtfile_splitlist_end_split[0]
            corruptgdb_name = txtfile_splitlist[1] + "_" + txtfile_splitlist[2] + "_" + txtfile_number
            corruptgdb_path = outdir + "/" + corruptgdb_name + ".gdb"
            corrupgdb_path_list.append(corruptgdb_path)
    if( len(corrupgdb_path_list) > 0):
        arcpy.Delete_management(corrupgdb_path_list)


    #Get list of GDBs and feature classes
    arcpy.env.workspace = outdir
    output_gdbs = arcpy.ListWorkspaces("*", "FileGDB")
    fc_list = [sub.replace(".gdb", "") for sub in output_gdbs]
    fc_list = [sub.replace((outdir + "\\"), "") for sub in fc_list]
    fcname_list = []
    for i in range(0, len(fc_list)):
        curr_fcname = fc_list[i]
        curr_fcname_split0 = curr_fcname.split("_")[0]
        fcname_list.append(curr_fcname_split0)
    fcname_unique_list = sorted(list(set(fcname_list)), key=str.lower)


    ########################################################################
    ## LOOP THROUGH EACH SERIES OF GDBs, AND PULL DATA TOGETHER
    ########################################################################
    for i in range(0, len(fcname_unique_list)):
        curr_fcname = fcname_unique_list[i]
        target_fc_path = master_gbd_outpath + "/" + curr_fcname
        if(curr_fcname in ["FeatureLayerDownload"]):
            continue

        arcpy.AddMessage("..Processing: " + curr_fcname + " (" + str(i + 1) + " out of " + str(len(fcname_unique_list)) + ")")
        fcname_list_which = []
        for j in range(0, len(fcname_list)):
            if(fcname_list[j] == curr_fcname):
                fcname_list_which.append(j)

        #Build list of corresponding GDB paths
        gdb_path_list = []
        for j in fcname_list_which:
            gdb_path_list.append(output_gdbs[j])

        #Build list of feature class paths that will be merged together
        fc_path_list = []
        for j in range(0, len(gdb_path_list)):
            curr_gdbpath = gdb_path_list[j]
            curr_fcpath = curr_gdbpath + "/" + os.path.basename(curr_gdbpath).replace(".gdb", "")
            fc_path_list.append(curr_fcpath)


        ########################################################################
        ## CREATE OUTPUT FEATURE CLASSES
        ########################################################################
        #I first tried to simply use merge via arcpy to pull all the corresponding feature classes together, but
        #for some reason it wasn't merging all features. There would be holes in the output datasets. So, I came
        #up with a way to do it using Pandas SpatialDataFrames, which is what I'm doing here. I'm concatenating
        #all feature class features into a single dataframe, then exporting as a feature class.

        #If just one GDB/FC simply copy it over
        if( len(fc_path_list) == 1 ):
            arcpy.AddMessage("....Creating output feature class")
            arcpy.Copy_management(curr_fcpath, target_fc_path)

        else:
            #Else if multiple feature classes, concatenate all into a single SDF
            arcpy.AddMessage("....Merging " + str(len(fc_path_list)) + " feature classes")
            sdf_concat_list = []
            for j in range(0, len(fc_path_list)):

                #Create SDF for current iteration
                iter_sdf = arcgis.GeoAccessor.from_featureclass(fc_path_list[j])

                #If it's the first ieration, create the output SDF. Else concatenate to it.
                if(j == 0):
                    output_sdf = iter_sdf
                if(j > 0):
                    sdf_concat_list = [output_sdf, iter_sdf]
                    output_sdf = pandas.concat(sdf_concat_list)

            #Now export concatenated SDF to feature class
            try:
                arcpy.AddMessage("....Creating output feature class")

                #For certain datasets, first drop fields that are known to be cause errors when exporting to feature classes
                if(curr_fcname == "FSOffices"):
                    output_sdf = output_sdf.drop(["LAST_CONDITION_SURVEY", "FACILITY_MASTER_PLAN_DATE", "PRELIM_PROJECT_ANALYSIS_DATE", "REV_DATE"], axis=1)
                if(curr_fcname == "FSNationalRecreationSites"):
                    output_sdf = output_sdf.drop(["CONDITION_SURVEY_DATE"], axis=1)
                if(curr_fcname == "InfrastructureBridgeEDWDeckType"):
                    output_sdf = output_sdf.drop(["INSPECTION_DATE"], axis=1)
                if(curr_fcname == "InfrastructureDamEDW"):
                    output_sdf = output_sdf.drop(["INSPECTION_DATE", "REV_DATE"], axis=1)
                if(curr_fcname == "NPSNationalRecreationSites"):
                    output_sdf = output_sdf.drop(["SOURCEDATE"], axis=1)
                if(curr_fcname == "USFSFirePerimeters"):
                    output_sdf = output_sdf.drop(["DISCOVERYDATETIME", "PERIMETERDATETIME"], axis=1)

                #Export to feature class
                output_sdf.spatial.to_featureclass(target_fc_path, sanitize_columns=False)


            #FSOffices (and possibly others) were giving me problems when exporting to feature class.
            #Looks like its something related to the field data types? Though in my experience, the problematic fields seem to be all date related.
            #See here: https://community.esri.com/t5/arcgis-api-for-python-questions/system-error-when-exporting-spatially-enabled-dataframe-to/td-p/1044880
            #In an attempt to get around this, if the export fails, try to determine if there are any problematic fields. If so, drop them, and try again.
            except:
                arcpy.AddMessage("......Feature class export failed, testing if any problematic fields exist")

                #Create list of column names
                output_sdf_cols = list(output_sdf.columns)

                #Now iterate through columns, and determine if there are any problematic ones
                good_cols = []
                bad_cols = []
                for k in range(0, len(output_sdf_cols)):

                    #Create fresh SDF and column variable
                    output_sdf = pandas.concat(sdf_concat_list)
                    curr_col = output_sdf_cols[k]
                    arcpy.AddMessage("........" + curr_col + " (" + str(k + 1) + " out of " + str(len(output_sdf_cols)) + ")")

                    #Skip if the current column is SHAPE
                    if(curr_col == "SHAPE"):
                        continue

                    #Try isolating current column, and re-exporting. If success, record it in a list. If fail, also record it in a list.
                    try:
                        output_sdf = output_sdf[[curr_col,"SHAPE"]]
                        output_sdf.spatial.to_featureclass(target_fc_path, sanitize_columns=False)
                        good_cols.append(curr_col)
                    except:
                        bad_cols.append(curr_col)
                        arcpy.AddMessage("..........!!!PROBLEMATIC!!!")
                        continue

                #If bad columns were identified, try dropping them and re-export. If none found, or if export fails again after dropping columns, skip dataset
                if(len(bad_cols) > 0):
                    arcpy.AddMessage("......Dropping problematic fields, and re-attempting feature class export")
                    try:
                        output_sdf = pandas.concat(sdf_concat_list)
                        output_sdf = output_sdf.drop(bad_cols, axis=1)
                        output_sdf.spatial.to_featureclass(target_fc_path, sanitize_columns=False)
                        arcpy.AddMessage("......Export success")
                    except:
                        arcpy.AddMessage("......Feature class export still failing, skipping dataset")
                        continue
                else:
                    arcpy.AddMessage("......No problematic fields identified, skipping dataset")
                    continue

            #Remove identical features in output feature class
            arcpy.AddMessage("....Removing duplicate features")
            arcpy.DeleteIdentical_management(target_fc_path, fields=["Shape"])

            #Clear output_sdf from memory
            del output_sdf
            del sdf_concat_list

        #Delete GDBs
        arcpy.AddMessage("....Deleting GDBs")
        arcpy.Delete_management(gdb_path_list)



    ############################################################################
    ## PROCESS HIFLDRoads FEATURE CLASSES
    ############################################################################
    #Now merge PrimaryHighway/SecondaryHighway/Roads feature classes into a single feature class
    primaryhwy_target_fc_path = master_gbd_outpath + "/PrimaryHighway"
    secondaryhwy_target_fc_path = master_gbd_outpath + "/SecondaryHighway"
    roads_target_fc_path = master_gbd_outpath + "/Roads"
    hifldroads_fc_outpath = master_gbd_outpath + "/HIFLDRoads"

    #If any of the PrimaryHighway/SecondaryHighway/Roads feature classes exist, continue
    if(arcpy.Exists(primaryhwy_target_fc_path) or arcpy.Exists(secondaryhwy_target_fc_path) or arcpy.Exists(roads_target_fc_path)):

        arcpy.AddMessage("..Processing: HIFLDRoads")

        #Create PrimaryHighway/SecondaryHighway/Roads SDFs
        sdf_concat_list = []
        if(arcpy.Exists(primaryhwy_target_fc_path)):
            primaryhwy_sdf = arcgis.GeoAccessor.from_featureclass(primaryhwy_target_fc_path)
            sdf_concat_list.append(primaryhwy_sdf)
        if(arcpy.Exists(secondaryhwy_target_fc_path)):
            secondaryhwy_sdf = arcgis.GeoAccessor.from_featureclass(secondaryhwy_target_fc_path)
            sdf_concat_list.append(secondaryhwy_sdf)
        if(arcpy.Exists(roads_target_fc_path)):
            roads_sdf = arcgis.GeoAccessor.from_featureclass(roads_target_fc_path)
            sdf_concat_list.append(roads_sdf)

        #Concatenate PrimaryHighway/SecondaryHighway/Roads SDFs together
        if( len(sdf_concat_list) > 1):
            arcpy.AddMessage("....Merging PrimaryHighway/SecondaryHighway/Roads feature classes")
            output_sdf = pandas.concat(sdf_concat_list)
        else:
            output_sdf = sdf_concat_list[0]

        #Create output feature class
        arcpy.AddMessage("....Creating output feature class")
        output_sdf.spatial.to_featureclass(hifldroads_fc_outpath, sanitize_columns=False)

        #Remove identical features
        arcpy.AddMessage("....Removing duplicate features")
        arcpy.DeleteIdentical_management(hifldroads_fc_outpath, fields=["Shape"])


    ############################################################################
    ## INSERT METADATA INTO OUTPUT FEATURE CLASSES
    ############################################################################

    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Importing Feature Layer metadata to output Feature Classes")

    #Get list of feature classes in master output gdb
    arcpy.env.workspace = master_gbd_outpath
    fc_name_list = arcpy.ListFeatureClasses()

    #Loop through each feature class
    for i in range(0, len(fc_name_list)):
        curr_fc_name = fc_name_list[i]
        curr_fc_path = master_gbd_outpath + "/" + curr_fc_name
        curr_fc_metadata_path = metadatadir + "/" + curr_fc_name + ".xml"

        #If the metadata xml exists for the feature class, proceed
        if(arcpy.Exists(curr_fc_metadata_path)):

            arcpy.AddMessage(".." + curr_fc_name)

            #Create metadata object from feature class
            fc_metadata_obj = arcpy.metadata.Metadata(curr_fc_path)

            #Replace feature class metadata with the feature layer metadata
            fc_metadata_obj.importMetadata(curr_fc_metadata_path)

            #Insert name into feature class metadata
            fc_metadata_obj.title = curr_fc_name

            #Save metadata
            fc_metadata_obj.save()


    arcpy.AddMessage("\u200B")
    arcpy.AddMessage("Done!")


