# Feature Layer Download

This tool can be used to download a series of vector datasets published to ArcGIS Online as feature layers. It was created to simplify the data download process for the [USFS National Basemap](https://community.esri.com/t5/wildfire-response-gis-questions/national-base-map-for-fire/m-p/727457), but can be used to download data from any accessible feature layer. 

**The PanunTools download package also includes the fonts, and layer files needed to generate the USFS National Basemap, and can be found in the BaseDataDownload folder.**

## How does it work?

For a user-specified list of feature services, the tool downloads vector datasets published as feature layers, and stores them as a series of feature classes in an output file geodatabase. This tool consists of 2 components:

-	**Python Script** (FeatureLayerDownload.py)
    -	The script that the script tool must reference. Place this in the same directory as the PanunTools toolbox, and ensure that the script path is properly set in the script tool properties
-	**CSV File** (FeatureLayerDownload.csv)
    -	Contains a list of feature services and corresponding Item IDs. The tool iterates through these services looking for feature layers. If found, feature layers will be downloaded for the user specified AOI.
    -   By default, this CSV file consists of all services needed to produce the USFS National Basemap. However, it can be modified to download feature layers from any published feature service.
    -   This can be found in the BaseDataDownload folder.

If enabled, this tool will harness the Python multiprocessing module to run several instances of Python simultaneously. When running, several command prompt windows will appear on your screen. Just leave them be, as they should disappear once all datasets have been downloaded. However, if you run into an error, you may have to terminate ArcGIS Pro in order to manually close them.

A demonstration of this tool can be viewed [at this link](https://youtu.be/ReyW6eprs18).

## User Inputs:
1.	Toggle for using ArcGIS Pro’s Active Portal to make feature service connections
2.	ArcGIS Online Portal URL
3.	ArcGIS Online Username
4.	ArcGIS Online Password
5.	Path to AOI Polygon Shapefile (must be a Shapefile)
6.	AOI Subdivision Size (in Sq. Miles)
7.	Output Coordinate System
8.	Output Directory
9.	Path to FeatureLayerDownload.csv
10.	Toggle for downloading Elevation Contour data from the USGS
11.	Toggle for downloading Wetlands data from the USFWS
12.	Toggle for using multiprocessor
13.	Toggle for performing Offline License Check

![screenshot_FeatureLayerDownload_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_FeatureLayerDownload_1.png)

![screenshot_FeatureLayerDownload_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_FeatureLayerDownload_2.png)
