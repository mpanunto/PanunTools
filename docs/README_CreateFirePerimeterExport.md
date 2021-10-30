# Create Fire Perimeter Export

Tool that exports fire perimeters of interest to a new GDB feature class, shapefile or KMZ.

### How does it work?

The tool will iterate through the user specified list of IncidentName values and calculate containment for each. To do so, it first selects an incident's corresponding features of "Wildfire Daily Fire Perimeter" and "Contained Line" from the user specified Event_Polygon and Event_Line feature classes. Next, a Union is performed on the incident's "Wildfire Daily Fire Perimeter" in order to remove any interior gaps. Once gaps are removed, the perimeter is then converted to a line, and dissolved. The incident's "Contained Line" is also dissolved. Lastly, features are then projected to the user specified coordinate system prior to calculating geometry, and containment percentage. If containment is calculated for more than one incident, a combined total containment will also be calculated across all incidents.

By default, only the "Contained Line" features that align with the outer edge of the "Wildfire Daily Fire Perimeter" will be included in the containment calculation. However, users have the option to force the inclusion of all "Contained Line" features in the calculation. Additionally, users can request a report of the excluded "Contained Line" features, which will be generated in the geoprocessing messages. Lastly, users may also request an export of the excluded features in order to perform a visual inspection or assist with topology cleanup.


### User Inputs

1. List of Incident Names
2. Path to Event_Polygon feature class
3. Toggle to export GDB feature class
4. Specify GDB to store exported feature class
5. Toggle to export Shapefile
6. Specify Shapefile export directory
7. Toggle to export KMZ
8. Specify KMZ export directory


![screenshot_CreateFirePerimeterExport_1.png](/docs/screenshot_CreateFirePerimeterExport_1.png?raw=true)

![screenshot_CreateFirePerimeterExport_2.png](/docs/screenshot_CreateFirePerimeterExport_2.png?raw=true)
