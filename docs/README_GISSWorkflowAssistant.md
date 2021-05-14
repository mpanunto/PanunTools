# GISS Workflow Assistant

To improve quality of life while performing the GISS Workflow, this tool does the following:
1. Calculates geometry for all Event feature classes (only if geometries have changed)
2. Inserts missing IrwinIDs, or replaces if incorrect
3. Creates a new Master Incident GDB
4. Creates a new Master Incident Backup GDB
5. Deletes all features in the newly created GDBs that do not match the user specified IncidentName(s)
6. Checks for case sensitivity issues and hidden spaces in IncidentName fields
7. Checks for missing Drop Point and Helispot labels
  
  
  
### How does it work?
- Users must specify the IncidentName as input. Edits will only be made to those features whose IncidentName matches the user specified value. As such, the onus is on the user to ensure all their data is properly attributed with the correct IncidentName value.  The tool checks for case sensitivity issues and hidden spaces in IncidenName to aid users in keeping these fields clean.

- The tool will first copy each Event feature class from the Mobile GDB (aka local copy) to a Scratch GDB. Geometries will then be calculated for all features in this Scratch GDB, and will be compared to the values in the Mobile GDB. Each feature is tested to determine if the geometry has changed. If a change is detected, the tool will insert the value from the Scratch GDB into the Mobile GDB, triggering an edit. No edit will be made if a change is not detected, thus minimizing [conflicts that might arise due to offline edits](https://www.nwcg.gov/publications/pms936-1/edit-incident-data/securing-incident-information#collapseX)

- After geometries have been calculated, the tool will convert the Mobile GDB to a new Master Incident GDB, and place it in the same directory as the original. It will also place a new Master Incident Backup GDB in the backups folder with an appropriate date/time stamp. 

- Lastly, any features in the new Master Incident GDB and new Master Incident Backup GDB whose IncidentName does not match the user specified value will be deleted. However, users may specify additional incident names that they want to keep in these new GDBs. This is simply to maintain clean datasets that are relevant to only the fire(s) of interest.

The main idea behind this tool is that once all feature and attribute edits are made, it reduces the GISS workload down to simply ensuring that IncidentName values are clean. It's a lot easier to focus on one thing, rather than having to manually navigate through several processes.

### User inputs
1. Specify Incident Name
2. Specify Incident IrwinID
3. Path to Mobile GDB (aka local copy)
4. Path to Master Incident GDB
5. Specify Incident GDB Backup directory
6. Specify Coordinate System to use for GISAcres and LengthFeet Calculations
    - Point feature geometries are always calculated in WGS84
7. Specify Scratch Directory
8. Specify Other IncidentNames to keep in the newly created Master Incident GDB and Backup GDB

![screenshot_GISSWorkflowAssistant_1.png](/docs/screenshot_GISSWorkflowAssistant_1.png?raw=true)

### When using this tool, the general workflow is:
1. Download Map (aka Create Local Copy) or Sync
2. Perform all feature and attribute edits
    - The tool will calculate geometries for you
    - The tool will insert IrwinIDs for you
3. Save Edits
4. Run this tool
5. Sync
6. Swap out Master Incident GDB

To speed things up, I would recommend setting your incident's default input values in the script tool parameters, that way you can just open the tool and run.
