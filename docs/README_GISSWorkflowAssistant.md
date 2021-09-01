# GISS Workflow Assistant

To improve quality of life while performing the GISS Workflow, this tool does the following:
1. Calculates geometry for all Event feature classes (only if geometries have changed)
2. Inserts missing IrwinIDs, or replaces if incorrect
3. Checks for case sensitivity issues and hidden spaces in IncidentName fields
4. Checks for missing Drop Point and Helispot labels
5. Creates a new Master Incident GDB
6. Creates a new Master Incident Backup GDB
7. Deletes all features in the newly created GDBs that do not match the user specified IncidentName(s)  
  
  
### How does it work?
- Users must specify the IncidentName as input. Edits will only be made to those features whose IncidentName matches the user specified value. As such, the onus is on the user to ensure all their data is properly attributed with the correct IncidentName value.  The tool checks for case sensitivity issues and hidden spaces in IncidentName to aid users in keeping these fields clean.

- Each feature is tested to determine if the geometry has changed since it was last calculated. If a change is detected, the tool will insert the new geometry value, triggering an edit. No edit will be made if a change is not detected, thus minimizing [conflicts that might arise due to offline edits](https://www.nwcg.gov/publications/pms936-1/edit-incident-data/securing-incident-information#collapseX)

- If the user specifies multiple IncidentNames and IrwinIDs, the tool will iterate through each incident one at a time, and perform the various geospatial and QA/QC processes for each.

- If requested, the tool will then convert the Mobile GDB to a new Master Incident GDB, and place it in the same directory as the original. It will also place a new Master Incident Backup GDB in the backups folder with an appropriate date/time stamp. If the user specified multiple IncidentNames and IrwinIDs, the data from all incidents will be exported to a single Master Incident GDB.

- Lastly, any features in the new Master Incident GDB and new Backup GDB whose IncidentName does not match any of the user specified values will be deleted. This is simply to maintain clean datasets that are relevant to only the fire(s) of interest.

The main idea behind this tool is that once all manual feature and attribute edits are made, it reduces the GISS workload down to simply ensuring that IncidentName values are clean. The IncidentName field is used because:
- Field users (Collector/Field Maps/Survey123) can enter this information. Sometimes correctly!
- It would be extremely rare for neighboring incidents to have the same IncidentName
- It's a lot easier for the GISS to visually determine if an IncidentName is incorrect vs an IrwinID

### User inputs
1. Specify Incident Name(s) and IrwinID(s)
2. Path to Mobile GDB (aka local copy)
3. Specify Coordinate System to use for GISAcres and LengthFeet Calculations
    - Point feature geometries are always calculated in WGS84
4. Specify desired geometry measurement type
5. Toggle for creating new Master Incident and Backup GDBs
6. Path to Master Incident GDB
7. Specify Incident GDB Backup directory

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
