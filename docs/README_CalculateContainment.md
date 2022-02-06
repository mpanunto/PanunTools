# Calculate Containment

Tool that calculates the containment for one or more user specified incidents. This tool also provides users with the ability to inspect their Contained features to ensure that they align with the Wildfire Daily Fire Perimeter.

### How does it work?

![screenshot_CalculateContainment_1.png](/docs/screenshot_CalculateContainment_1.png?raw=true)

\
\
\
\
\
\
\
![screenshot_CalculateContainment_2.png](/docs/screenshot_CalculateContainment_2.png?raw=true)
\
The tool will iterate through the provided list of IncidentNames and calculate containment for each. To do so, it first selects an incident's corresponding "Wildfire Daily Fire Perimeter" and "Contained" features from the user specified Event_Polygon and Perimeter_Line feature classes. Next, a Union is performed on the incident's "Wildfire Daily Fire Perimeter" in order to remove any interior gaps. Once gaps are removed, the perimeter is then converted to a line, and dissolved. The incident's "Contained" features are also dissolved. Lastly, the two dissolved features are then projected to the user specified coordinate system prior to calculating geometry, and containment percentage. If containment is calculated for more than one incident, a combined total containment will also be calculated across all incidents.

By default, only the "Contained" features that align with the outer edge of the "Wildfire Daily Fire Perimeter" will be included in the containment calculation. However, users have the option to force the inclusion of all "Contained" features in the calculation. Additionally, users can request a report of the excluded "Contained" features, which will be generated in the geoprocessing messages. Lastly, users may also request an export of the excluded features in order to perform a visual inspection or assist with topology cleanup.

This tool doesn't generate any outputs. The calculations are provided to the user in the Geoprocessing Messages:
\
\
### Acknowledgements

Many thanks to [SW - Carl Beyerhelm (GISS)](https://community.esri.com/migrated-users/371529) for developing the original tool.
