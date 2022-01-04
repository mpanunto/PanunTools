# Base Data Acquisition Tool
 
I was inspired by [SW - Carl Beyerhelm (GISS)](https://community.esri.com/migrated-users/371529)'s USGS Topo Vector Prep tool, and thought it would be useful to have a tool that could also download a variety of other base data. So, I created what I call the "Base Data Acquisition Tool", which will run in both ArcMap and ArcGIS Pro.

This tool allows users to acquire/process the following datasets for an area of interest (AOI):

1. USGS Topo Vector
2. USGS Topo Raster 24K
3. USGS Historical Topo Raster 100K
4. USGS Historical Topo Raster 250K
5. USFS Topo Vector
6. USFS Topo Raster 24K
7. NAIP Imagery
8. Surface Management Agency (Land Ownership)
9. DEM 10 Meter (1/3rd Arc Second)
10. Hillshade Raster 10 Meter
11. Vector Hillshade 10 Meter
12. DEM 30 Meter (1 Arc Second)
13. Hillshade Raster 30 Meter
14. Vector Hillshade 30 Meter  

I’ve created a [Info Sheet](/docs/BaseDataAcquisition_InfoSheet.pdf?raw=true) that provides more information about each dataset, as well as their spatial coverages. Admittedly, the topo raster products may not be terribly useful considering the availability of vector data, but I figured they would be cool to incorporate anyway. A couple notes about these datasets:

**USGS Topo Raster 24K**: The USGS Topo Raster 24K dataset is processed from the modern series of USGS topo maps, which are currently only available as PDFs. The “PDF to TIFF” tool is used to convert them into a useable format. However, this conversion tool is not yet available in ArcGIS Pro, so users interested in this dataset must run the tool in ArcMap.

**USGS Historical Topo Raster 100K/250K**: I attempted to identify the most recent GeoTIFF for each 100K and 250K quad by referencing the USGS’s master topo spreadsheet (listed in the attached Info Sheet PDF). As a result, each quad can have a vastly different looking topo map. So, these datasets can be a bit of a hodge podge.

**USGS and USFS Topo Raster 24K**: The output symbology for these datasets are based on the image RGB values, but they will be given a random color scheme when first loaded into ArcMap/ArcGIS Pro. Users can either manually apply the RGB value for each class, or they can use the included “Topo Raster 24K Symbology” tool in ArcGIS Pro. If using the tool, users will only have the ability to create .lyrx files since ArcGIS Pro cannot create .lyr files. This symbology tool cannot be used in ArcMap.

**USFS Topo Vector**: Unlike the USGS Topo Vector dataset, the USFS Topo Vector dataset uses annotations
instead of labels. For the annotations to display properly, a series of fonts must be installed
on the user's computer, which can be obtained at:
https://data.fs.usda.gov/geodata/vector/fstopo/FSTopo_Layer_files_and_fonts.zip

**Hillshade and Vector Hillshade**: These datasets require users to acquire a DEM as well. Be sure to specify a ***projected coordinate system*** for the output DEM if wanting these datasets.
 

I hope the tool is fairly straight forward to run. Users will need to:
1. Specify an output directory
2. Specify path to a AOI polygon shapefile
3. Specify a AOI buffer size
4. Specify path to the “BaseDataAcquisitionFiles.zip” file
   - This .zip file comes in the download package, and contains all the layer files and index shapefiles that the tool references. 

Once all the inputs are specified, users simply select the datasets that they want to acquire/process.

![screenshot_BaseDataAcquisition_1.png](/docs/screenshot_BaseDataAcquisition_1.png?raw=true)

Wanna check it out? You can grab it [here](https://github.com/mpanunto/BaseDataAcquisition/archive/refs/heads/master.zip)
 

At this time, the tool does not support processing local data, everything must be downloaded. The output layer files must also be resourced manually. If possible, I would recommend running the tool in ArcGIS Pro (unless you want the USGS Topo Raster 24K dataset), as it is a 64-bit application and can use more memory.

 

Lastly, a big thank you to Carl for sharing his USGS Topo Vector Prep code, and also to Zach Beck (State of Utah AGRC) for providing his Vector Hillshade code.

 

Feel free to contact me (Matt Panunto) at mpanunto@blm.gov with any comments, questions, or error reports.
