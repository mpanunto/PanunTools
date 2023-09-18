# PDF Multi Export

Like several others have reported, I too have had issues plotting many of my PDFs exported from ArcGIS Pro. Again, like many others, I’ve often had to export two PDFs per map product: one as an *image* for printing purposes, and one as a geospatial PDF dedicated to Avenza use. I became frustrated enough by this cumbersome process that I’ve attempted to automate it to some degree with a script tool.

### How does it work?

If enabled, this tool will harness the Python multiprocessing module to run several instances of Python simultaneously. It is similar to opening numerous ArcGIS Pro project files at once in order to export multiple PDFs at the same time. When running, you will see several command prompt windows appear on your screen. Just leave them be, as they should disappear once ***all*** exports have completed. However, if you run into an error, you may have to terminate ArcGIS Pro in order to manually close them.

The "PDFMultiExport.xlsx" spreadsheet is used to control your export settings for each map product. It may seem a bit daunting, but the export settings only need to be specified one time for each product. After that, users only need to enter their export request, products date, and operational period prior to running the tool. For each map product, a user’s export request can be GEO, IMAGE, GEOIMAGE, GEO AND IMAGE, or GEO AND GEOIMAGE. The script will then use the information entered into the spreadsheet to export the requested PDFs.

Users can either specify the incident's projects directory that contains each of the APRX filenames as listed in the "PDFMultiExport.xlsx" spreadsheet, or they can have the tool reference the APRX_PATH column within the spreadsheet. The option to specify an incident's project directory gives all GISS the ability to reference the same PDFMultiExport.xlsx spreadsheet, assuming all the APRX's are in the specified directory.

Additionally, this tool provides users with the ability to immediately upload the exported PDFs to the NIFC FTP. For the upload to function properly, users must either specify an FTP directory that already exists, or an FTP directory that does not exist but is an immediate subdirectory of one that does. Any immediate subdirectories that do not exist will be created. However, if the parent directory does not already exist, they will not be created. This logic is to prevent users from inadvertently creating lengthly sets of FTP directories.

Here is a sample of what the spreadsheet looks like:

![screenshot_PDFMultiExport_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_PDFMultiExport_1.png)

### To run the tool, users must:
1. Extract PanunTools.tbx, PDFMultiExport.py, and PDFMultiExport.xlsx to the incident's tools folder
2. Ensure that the script path is properly set in the script tool properties
3. Edit the spreadsheet so the information corresponds to the incident
4. Specify tool inputs:
    - Incident Name
    - Incident ID
    - Products directory
    - Path to the PDFMultiExport.xlsx spreadsheet
    - Option for specifying APRX locations
    - Toggle for uploading exports to FTP
    - NIFC FTP Username
    - NIFC FTP Password
    - Toggle for using Multiprocessor
    - Toggle for performing Offline License Check
5. Run tool

![screenshot_PDFMultiExport_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_PDFMultiExport_2.png)
