# Update Fire Edge

Don't you hate having to meticulously split, and delete Fire Edge features during the early morning perimeter update? Well with this tool, you can simply dump all the old Fire Edge features, and quickly paste in an updated Fire Edge that conforms to the new fire perimeter and existing Contained Line. The GISS should be the only position on the incident editing the Fire Edge/Contained Line features, so there are minimal concerns with "Last in Wins" issues.

### How does it work?

Users must specify the following inputs to the tool:
1. Incident Name
2. Path to the Mobile GDB (aka local copy)
3. Output Directory

![screenshot_UpdateFireEdge_1.png](/docs/screenshot_UpdateFireEdge_1.png?raw=true)


The tool selects 'Wildfire Daily Fire Perimeter', and 'Contained Line' features that match the user specified incident name, and copies them to an output GDB. Once copied over, the fire perimeter is converted to a polyline. Then, the copied 'Contained Line' features are erased from the fire perimeter polyline. The result of this erase provides updated Fire Edge features that conform to the new fire perimeter, and existing Contained Line. This tool generates two output feature classes:

- "UpdateFireEdge_dissolve"
    - Has a single dissolved feature of all updated Fire Edge
- "UpdateFireEdge_explode"
    - Explodes the dissolved Fire Edge, in case users need singlepart features

### The general workflow is:
1. Download Map (aka create local copy) or Sync
2. Perform edits to the Wildfire Daily Fire Perimeter
3. Save edits
4. Run this tool to generate the new Fire Edge features
6. Delete the old Fire Edge feature(s) from the Event_Line feature class
7. Paste in the new Fire Edge feature(s) to the Event_Line feature class
8. Save edits

At this point the incident's "Fire Edge" is now up to date. If all edits are complete, I would recommend users proceed by running the [GISS Workflow Assistant tool](/docs/README_GISSWorkflowAssistant.md) prior to syncing. To speed things up, I would also recommend setting your incident's default input values in the script tool parameters, that way you can just open the tool and run.

### Bonus Use
Due to the nature of how this tool works, it can also be used to identify segments of Contained Line that do not match the fire perimeter. If there are segments of Contained Line that appear to be overlapping with updated Fire Edge features pasted in, chances are these segments of Contained Line need to be cleaned up to match the fire perimeter.
