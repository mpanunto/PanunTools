# Calculate Containment

Tool that calculates the containment for one or more user specified incidents. This tool also provides users with the ability to inspect their Contained features to ensure that they align with the Wildfire Daily Fire Perimeter.

### How does it work?
\
\
![screenshot_CalculateContainment_1.png](/docs/screenshot_CalculateContainment_1.png?raw=true)
\
If "Inspect Contained Feature Alignment" is selected, the tool will iterate through the provided list of IncidentNames and determine the "Contained" feature alignment for each. **Due to the nature of how this tool was designed, it is highly recommended to always run this inspection prior to calculating containment**. If alignment issues are detected, users can visually inspect the output feature classes to determine where these locations are. Proper Contained feature alignment is crucial for accurate containment calculations when using this tool, and is also necessary for the the [Update Perimeter IR](README_UpdatePerimeterIR.md) tool to function as intended.
\
\
\
\
\
\
![screenshot_CalculateContainment_2.png](/docs/screenshot_CalculateContainment_2.png?raw=true)
\
If "Calculate Containment" is selected, the tool will iterate through the provided list of IncidentNames and calculate containment for each. To do so, it first selects an incident's corresponding "Wildfire Daily Fire Perimeter" and "Contained" features. Next, a Union is performed on the "Wildfire Daily Fire Perimeter" in order to remove any interior gaps. Once gaps are removed, the perimeter is then converted to a line, and dissolved. The "Contained" features are also dissolved. Lastly, the two dissolved features are then projected to the user specified coordinate system prior to calculating geometry and containment percentage. If containment is calculated for more than one incident, a combined total containment will also be calculated across all incidents.

By default, only the "Contained" features that align with the "Wildfire Daily Fire Perimeter" exterior will be included in the containment calculation. However, users have the option to force the inclusion of all "Contained" features in the calculation. This tool doesn't generate any outputs, as the calculations are provided to the user in the Geoprocessing Messages.

### Acknowledgements

Many thanks to [SW - Carl Beyerhelm (GISS)](https://community.esri.com/migrated-users/371529) for developing the original tool.
