# Create Fire Perimeter Export

Simple tool that exports fire perimeters to a new GDB feature class, Shapefile, or KMZ. 

### How does it work?

First, a selection of 'Wildfire Daily Fire Perimeter' features is performed using the user specified IncidentNames of interest. Once selected, these features are then exported to the user specified output directories, and are given proper file naming conventions.

### User Inputs

1. List of Incident Names
2. Path to Event_Polygon feature class
3. Specify IncidentName to use in output file name
4. Specify Incident ID to use in output file name
5. Specify DateTime to use in output filename
6. Toggle to export GDB feature class
7. Specify GDB to store export feature class
8. Toggle to export Shapefile
9. Specify Shapefile export directory
10. Toggle to export KMZ
11. Specify KMZ export directory


![screenshot_CreateFirePerimeterExport_1.png](/docs/screenshot_CreateFirePerimeterExport_1.png?raw=true)

![screenshot_CreateFirePerimeterExport_2.png](/docs/screenshot_CreateFirePerimeterExport_2.png?raw=true)
