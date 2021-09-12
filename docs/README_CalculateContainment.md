# Calculate Containment

Tool that calculates the containment for one or more user specified incidents

### How does it work?

The tool will iterate through the user specified list of IncidentName values, and will select corresponding features of "Wildfire Daily Fire Perimeter" and "Contained Line" from the user specified Event_Polygon and Event_Line feature classes. It uses these features to calculate containment.

A Union is first performed on the incident's "Wildfire Daily Fire Perimeter" in order to remove any interior gaps. It is then converted to a line, and dissolved. The "Contained Line" is also dissolved. Lastly, features are then projected to the user specified coordinate system prior to calculating geometry, and containment.



### User Inputs

1. List of Incident Names
2. Path to Event_Polygon feature class
3. Path to Event_Line feature class
4. Coordinate system to perform acreage calculations
5. Geometry measurement type

![screenshot_CalculateContainment_1.png](/docs/screenshot_CalculateContainment_1.png?raw=true)
\
\
\
This tool doesn't generate any outputs. The calculations are provided to the user in the Geoprocessing Messages:
\
\
![screenshot_CalculateContainment_2.png](/docs/screenshot_CalculateContainment_2.png?raw=true)
