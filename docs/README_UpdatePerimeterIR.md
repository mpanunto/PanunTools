# Update Perimeter IR

This tool is used to automate the Perimeter/IR update process. It allows users to quickly import new perimeters and IR data into their Mobile GDB. This tool also has several toggles that provide additional functionality, including the ability to delete old features in the Mobile GDB, and also the ability to automate the creation of an updated Fire Edge feature, which will conform to the new perimeter and existing Contained Line.

### How does it work?



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
