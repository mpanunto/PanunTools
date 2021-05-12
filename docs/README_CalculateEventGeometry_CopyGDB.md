# Calculate Event Geometry & Copy GDB

To improve GISS quality of life during the edit process, this tool does the following:
- Calculates geometry for all 8 Event feature classes
- Inserts IrwinIDs for features missing this information
- Creates a new Master Incident GDB
- Creates a new Backup GDB
- Checks for case sensitivity issues and hidden spaces in IncidentName fields
- Checks for missing Drop Point and Helispot labels

The tool will first copy each Event feature class from the Mobile GDB (aka local copy) to a Scratch GDB. Geometries will then be calculated for all features in this Scratch GDB, and will be compared to the actual values in the Mobile GDB. Each feature is tested to determine if the geometry has changed. If a change is detected, the tool will insert the value from the Scratch GDB into the Mobile GDB, triggering an edit. No edit will be made if a change is not detected, thus minimizing [conflicts that might arise due to offline edits](https://www.nwcg.gov/publications/pms936-1/edit-incident-data/securing-incident-information#collapseX)

Users must specify the IncidentName as input. Edits will only be made to those features whose IncidentName matches the user specified value. As such, the onus is on the user to ensure all their data is properly attributed with the correct IncidentName value.  The checks for case sensitivity issues and hidden spaces in IncidenName try to assist the user in keeping these fields clean.

After geometries have been calculated, the tool will copy the Mobile GDB to a new Master Incident GDB, and place it into the same directory as original. It will also place a new Backup GDB in the backups folder with an appropriate date/time stamp. 

Lastly, any features in the new Master Incident GDB and new Backup GDB whose IncidentName does not match the user specified value will be deleted. However, users may specify additional incident names that they want to keep in these new GDBs. This is simply to maintain clean datasets that are relevant to only the fire(s) of interest.

If using this script, the general workflow is that you first perform all your feature and attribute edits, save/stop editing, then you run this script to:

Calculate geometry
Create a new master incident fGDB
Create a new backup fGDB
Rename feature classes for the master incident fGDB and backup fGDB
 

After the script has ran, you then manually sync your edits to the server. Interested in trying it out? You can download the script here:

https://drive.google.com/file/d/114VISXtzo_aTUOJPg2XywnUJiq6QAcGv/view?usp=sharing 

Also, just for reference, below is a summary of some of the major differences between ArcGIS Pro and ArcMap that I’ve encountered which can make this edit process a bit cumbersome, warranting a scripted solution.

 

ArGIS Pro:

- “Download Map” results in a local mobile/runtime geodatabase file (.geodatabase)
- When selecting Download Map, ArcGIS Pro projects all the feature classes to the Map Frame’s coordinate system when creating the local .geodatabase file. So, you need to make sure you set your Map Frame’s projection before clicking Download Map. Otherwise, there will only be geographic/geodesic options when calculating geometry due to the NIFS’s coordinate system being WGS84.
- The Calculate Geometry tool allows you to specify a different coordinate system when calculating geometry. However, this tool seems to have poor performance when calculating geometry for the feature classes within the mobile/runtime .geodatabase file when there are many features present. Additionally, it yields lots of decimals when calculating Lat/Long coordinates, which is not a big deal, just kind of annoying.
- An additional step must be taken in order to convert the mobile/runtime .geodatabase file to a fGDB, by running the “Mobile Geodatabase to File Geodatabase” tool.
- The feature class names in the mobile/runtime .geodatabase differ compared to those in an ArcMap local copy fGDB. Not a big deal as long as everyone is using the same software, just kind of annoying.
