# Multi Export PDF

Like several others have reported, I too have had issues plotting many of my PDFs exported from ArcGIS Pro. Again, like many others, I’ve often had to export two PDFs per map product: one as an image for printing purposes, and one dedicated to Avenza use. I became frustrated enough by this cumbersome process that I’ve attempted to automate it to some degree with a script tool.
\
\
This tool harnesses the Python multiprocessing module to run several instances of Python simultaneously. It is similar to opening numerous ArcGIS Pro project files at once in order to export multiple PDFs at the same time. When running, you will see several command prompt windows appear on your screen (it’s not a virus, I promise :winking_face:). Just leave them be, as they should disappear once all exports have completed. However, if you run into an error, you may have to terminate ArcGIS Pro in order to manually close them.
\
\
The accompanying spreadsheet is used to control your export settings for each map product. It may seem a bit daunting, but the export settings only need to be specified one time for each product. After that, users only need to enter their export request, map dates, product dates, and day/shift values prior to running the tool. For each map product, a user’s export request can be IMAGE, AVENZA, BOTH, or NONE. The script will then use the information entered into the spreadsheet to export the requested PDFs.
\
\
In addition to automating the export process, this tool can also be used to quickly update all the incident map dates. It will update the map’s “Summary” metadata field with the user defined spreadsheet value. So for this value to actually be visible on your map, the layout must be using dynamic text that references the Summary metadata field (like the default GeoOps layouts do).
\
\
Here is a sample of what the spreadsheet looks like:

![screenshot_MultiExportPDF_1.png](/docs/screenshot_MultiExportPDF_1.png?raw=true)
\
\
To run the tool itself, users must:
1) Extract the toolbox, script, and spreadsheet
2) Keep the script in the same directory as the toolbox
3) Set the path to the script in the script tool properties
4) Specify Incident Name, Incident ID, Products directory, and the path to the MultiExportPDF.xlsx spreadsheet.
5) Run

![screenshot_MultiExportPDF_2.png](/docs/screenshot_MultiExportPDF_2.png?raw=true)
\
\
To speed things up, I would recommend setting your incident's default input values in the script tool parameters, that way you can just open the tool and run. I have found this tool to be particularly useful when fresh exports are needed and the map extents have not changed. Or if I simply want to quickly update all the map dates. It has saved me a lot of time not having to open several projects, or fiddle around with different export settings.
