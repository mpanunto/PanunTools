# GISS Workflow Assistant

To improve quality of life when performing the GISS Workflow, this tool does the following:
- Calculates geometry for all 8 Event feature classes (only if the geometry has changed)
- Inserts missing IrwinIDs
- Creates a new Master Incident GDB
- Creates a new Master Incident Backup GDB
- Deletes all features from the newly created GDBs that do not match the user specified IncidentName(s)
- Checks for case sensitivity issues and hidden spaces in IncidentName fields
- Checks for missing Drop Point and Helispot labels
  
  
  
### How does it work?
Users must specify the IncidentName as input. Edits will only be made to those features whose IncidentName matches the user specified value. As such, the onus is on the user to ensure all their data is properly attributed with the correct IncidentName value.  The checks for case sensitivity issues and hidden spaces in IncidenName try to assist the user in keeping these fields clean.

The tool will first copy each Event feature class from the Mobile GDB (aka local copy) to a Scratch GDB. Geometries will then be calculated for all features in this Scratch GDB, and will be compared to the actual values in the Mobile GDB. Each feature is tested to determine if the geometry has changed. If a change is detected, the tool will insert the value from the Scratch GDB into the Mobile GDB, triggering an edit. No edit will be made if a change is not detected, thus minimizing [conflicts that might arise due to offline edits](https://www.nwcg.gov/publications/pms936-1/edit-incident-data/securing-incident-information#collapseX)

After geometries have been calculated, the tool will copy the Mobile GDB to a new Master Incident GDB, and place it into the same directory as original. It will also place a new Backup GDB in the backups folder with an appropriate date/time stamp. 

Lastly, any features in the new Master Incident GDB and new Master Incident Backup GDB whose IncidentName does not match the user specified value will be deleted. However, users may specify additional incident names that they want to keep in these new GDBs. This is simply to maintain clean datasets that are relevant to only the fire(s) of interest.

The general idea behind this tool is that it reduces the GISS workload down to simply ensuring that IncidentName values are clean.

### If using this tool, the general workflow is:
1) Download Map (aka Create Local Copy) or Sync
2) Perform all feature and attribute edits
    - The tool will calculate geometries for you
    - The tool will insert IrwinIDs for you
3) Save Edits
4) Run this tool
5) Sync
6) Swap out Master Incident GDB
&nbsp;&nbsp;&nbsp;
To speed things up, I would recommend setting your incident's default input values in the script tool parameters, that way you can just open the tool and run.
