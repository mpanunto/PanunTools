# Update Perimeter IR

This tool automates the Perimeter/IR update process. It allows users to quickly import new perimeters and IR data into their Mobile GDB, calculate geometry, and properly attribute their data. It also has several toggles that provide additional functionality, including the ability to delete old features in the Mobile GDB, and create an updated 'Uncontained' feature, which will conform to the new perimeter and existing 'Contained' features. Additionally, this tool can be used to inspect the new IR Heat Perimeter.



### How does it work?

![screenshot_UpdatePerimeterIR_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_UpdatePerimeterIR_1.png)

If users select the "Inspect IR Heat Perimeter" option, the outputs generated by the tool will provide information about how the new IR Heat Perimeter differs from the Wildfire Daily Fire Perimeter currently in the Mobile GDB. Locations of perimeter growth and reduction will be identified, and the alignment of the two perimeter edges will be determined. Lastly, the alignment of Contained features will also be determined relative to the new IR Heat Perimeter. These outputs may be useful in identifying the presence of an accidental geometry shift in the IR data, or the need to make minor edits to the IR Heat Perimeter prior to running the "Update IR Data" option. The incident's Contained features should always align with the new IR Heat Perimeter, unless Ops has confirmed that the fire has actually burned across. **Due to the nature of how this tool was designed, it is highly recommended to always perform this inspection prior to running "Update IR Data"**.



![screenshot_UpdatePerimeterIR_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_UpdatePerimeterIR_2.png)


If users select the "Update IR Data" option, the tool will perform a series of feature appends to the user's Mobile GDB from the specified IR feature classes. Any new data appended to the Mobile GDB will have attributes automatically filled with the user specified input values. 

Deletion of old features, and the creation of updated 'Uncontained' features is made possible by a series of selections that query the IRWINID and FeatureCategory fields. As such, users ***MUST*** properly attribute their data with the correct IRWINID and FeatureCategory. All features of the following FeatureCategory types must have correct IRWINIDs.

- Wildfire Daily Fire Perimeter
- Contained
- Uncontained
- IR Isolated Heat Source
- Possible IR Heat Source
- IR Intense Heat
- IR Scattered Heat


Additionally, for the updated 'Uncontained' features to be correct, the incident's 'Contained' features ***MUST*** match the fire perimeter's edge. If the newly generated 'Uncontained' features appear to be overlapping any 'Contained' features, this is a good indication that the incident's 'Contained' features do not match the fire perimeter's edge at these locations, and need to be cleaned up.
