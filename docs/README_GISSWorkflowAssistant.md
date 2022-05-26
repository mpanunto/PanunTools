# GISS Workflow Assistant

To improve quality of life while performing the GISS Workflow, this tool does the following:
1. Calculates geometry for all Event feature classes (optional, and only if geometries have changed)
2. Inserts missing IrwinIDs and CpxNames, or replaces if incorrect (optional)
3. Extracts elevations from DEMs, and inserts into Event Point ElevationFeet field (optional)
4. Checks for null values in IncidentName field (optional)
5. Checks for case sensitivity issues and hidden spaces in IncidentName fields (optional)
6. Checks for proper attribution so that Wildfire Daily Fire Perimeters are accessible to public (optional)
7. Checks for features with values of DeleteThis = Yes (optional) 
8. Checks for missing Drop Point and Helispot labels (optional)
9. Checks for features with FeatureStatus = Proposed (optional)
10. Checks for features with FeatureStatus = In Review (optional)
11. Checks for features with Duplicate Geometry (optional)
12. Creates a new Master Incident GDB and Backup GDB (optional)
13. Deletes all features in the newly created GDBs that do not match the user specified IncidentName(s) (optional)
  
  
### How does it work?
- Users must specify the IncidentName as input. Edits will only be made to those features whose IncidentName matches the user specified value. As such, the onus is on the user to ensure all their data is properly attributed with the correct IncidentName value.  The tool can check for case sensitivity issues and hidden spaces in IncidentName to aid users in keeping these fields clean. With a clean incident name, the tool is also able to perform a variety of other optional data checks.

- Each feature is tested to determine if the geometry has changed since it was last calculated. If a change is detected, the tool will insert the new geometry value, triggering an edit. No edit will be made if a change is not detected, thus minimizing [conflicts that might arise due to offline edits](https://www.nwcg.gov/publications/pms936-1/edit-incident-data/securing-incident-information#collapseX)

- If the user specifies multiple IncidentNames, the tool will iterate through each incident one at a time, and perform the various geospatial and QA/QC processes for each.

- If requested, the tool will then convert the Mobile GDB to a new Master Incident GDB, and place it in the same directory as the original. It will also place a new Master Incident Backup GDB in the backups folder with an appropriate date/time stamp. If the user specified multiple IncidentNames and IrwinIDs, the data from all incidents will be exported to a single Master Incident GDB.

- Lastly, any features in the new Master Incident GDB and new Backup GDB whose IncidentName does not match any of the user specified values can be deleted. This option provides users a simple way to maintain clean datasets relevant to only their fire(s) of interest.

The main idea behind this tool is that once all manual feature and attribute edits are made, it reduces the GISS workload down to simply ensuring that IncidentName values are clean. The IncidentName field is used because:
- Field users (Collector/Field Maps/Survey123) can enter this information. Sometimes even correctly!
- It would be extremely rare for neighboring incidents to have the same IncidentName
- It's a lot easier for the GISS to visually determine if an IncidentName is incorrect vs an IrwinID

### User inputs
1. Specify Incident Name(s), IrwinID(s), and CpxName(s)
2. Toggle to calculate geometries, and insert missing/bad IrwinIDs and CpxNames
3. Toggle to insert extracted elevations into Event Point ElevationFeet field
4. Path to DEM raster
5. Specify if the DEM's elevation units are in meters or feet
6. Path to Mobile GDB (aka local copy)
7. Specify Coordinate System to use for GISAcres and LengthFeet Calculations
    - Point feature geometries are always calculated in WGS84
8. Specify desired geometry measurement type
9. Toggle to check for IncidentName issues (case sensitivity and hidden spaces)
10. Toggle to check for public access to Wildfire Daily Fire Perimeters
11. Toggle to check for features with values of DeleteThis = Yes
12. Toggle to check for missing Drop Point and Helispot Labels
13. Toggle to check for Proposed features
14. Toggle to check for In Review features
15. Toggle for Duplicate Geometries (Advanced License Only)
16. Toggle for creating new Master Incident and Backup GDBs
17. Path to Master Incident GDB
18. Specify Incident GDB Backup directory
19. Toggle to only keep features with user specified IncidentNames(s)
    - All other features will be deleted from the new Master Incident GDB

![screenshot_GISSWorkflowAssistant_1.png](/docs/screenshot_GISSWorkflowAssistant_1.png?raw=true)
