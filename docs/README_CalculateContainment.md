# Calculate Containment

Tool that calculates the containment of one or more user specified incidents

### How does it work?

The tool will iterate through the user specified list of IncidentNames value, querying the user defined Event_Polygon and Event_Line feature classes for features of "Wildfire Daily Fire Perimeter" and "Contained Line". 

A Union is first performed on the incident's "Wildfire Daily Fire Perimeter" in order to remove any interior gaps. It is then converted to a line, and dissolved prior to calculating it's length. The "Contained Line" is also dissolved prior to calculating it's length



### User Inputs

1. Path to ownership feature class
2. Field that defines ownership
3. Path to fire perimeter feature class
4. Coordinate system to perform acreage calculations
5. Geometry measurement type
6. Scratch directory

![screenshot_CalculateContainment_1.png](/docs/screenshot_CalculateContainment_1.png?raw=true)
\
\
\
This tool doesn't generate any outputs. The calculations are provided to the user in the Geoprocessing Messages:
\
\
![screenshot_CalculateContainment_2.png](/docs/screenshot_CalculateContainment_2.png?raw=true)
