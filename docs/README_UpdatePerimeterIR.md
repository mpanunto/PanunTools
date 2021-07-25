# Update Perimeter IR

This tool automates the Perimeter/IR update process. It allows users to quickly import new perimeters and IR data into their Mobile GDB. It also has several toggles that provide additional functionality, including the ability to delete old features in the Mobile GDB, and also create an updated 'Fire Edge' feature, which will conform to the new perimeter and existing 'Contained Line' (just like the [Update Fire Edge](docs/README_UpdateFireEdge.md) tool).

### How does it work?

To complete these processes, the tool performs a series of feature appends to the user's Mobile GDB from the specified Perimeter/IR feature classes. Once new data is appended to the Mobile GDB, attributes for these new features are filled with the user specified input values. Deletion of old features, and the creation of an updated Fire Edge is made possible by a series of feature selections using the IRWIN ID and FeatureCategory fields. Therefore, for things to work correctly, users ***MUST*** properly attribute their data with the correct IRWIN ID and FeatureCategory. All features of the following FeatureCategory type must have IRWIN IDs.

- Wildfire Daily Fire Perimeter
- Fire Edge
- Contained Line
- IR Isolated Heat Source
- IR Intense Heat
- IR Scattered Heat

#If these features are not properly attributed with IRWIN ID, the code will not
#be able perform proper selections of the data already in the geodatabase,
#which is necessary in order to delete old features, and create an updated
#Fire Edge feature.

Additionally, for the updated Fire Edge feature to be correct, the 'Contained Line' ***MUST*** match the fire perimeter's edge. If the newly generated 'Fire Edge' feature is overlapping any 'Contained Line', this is a good indication that the 'Contained Line' does not match the fire perimeter's edge at these locations, and needs to be cleaned up.



### User Inputs

1. Path to Mobile GDB
2. Incident Name
3. Incident IRWIN ID
4. Map Method
5. IR Flight Time (UTC)
6. IRIN Contact Name
7. IRIN Contact Email
8. IRIN Contact Phone
9. Path to Heat Perimter feature class
10. Toggle to delete old Wildfire Daily Fire Perimeter features
11. Toggle to delete old Fire Edge features
12. Toggle to create updated Fire Edge with new perimeter
13. Path to IR Isolated Heat feature class
14. Toggle to delete old IR Isolated Heat features
15. Path to IR Intense Heat feature class
16. Toggle to delete old IR Intense Heat features
17. Path to Scattered Heat feature class
18. Toggle to delete old IR Scattered Heat features

![screenshot_UpdatePerimeterIR_1.png](/docs/screenshot_UpdatePerimeterIR_1.png?raw=true)


If all edits are complete after running this tool, I would recommend users proceed by running the [GISS Workflow Assistant tool](/docs/README_GISSWorkflowAssistant.md) prior to syncing, which will calculate all Point/Line/Polygon geometry for you. Otherwise, the features will need to be calculated manually before syncing.
