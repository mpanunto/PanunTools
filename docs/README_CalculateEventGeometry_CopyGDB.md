# Calculate Event Geometry & Copy GDB

To improve GISS quality of life during the edit process, this tool does the following:
- Calculates geometry for all 8 Event feature classes
- Creates a new Master Incident GDB
- Creates a new Backup GDB
- Checks for case sensitivity issues and hidden spaces in IncidentName fields
- Checks for missing Drop Point and Helispot labels

*Update 07/11/20*: I modified the script a bit to minimize conflicts that might arise due to offline edits. Thanks to SW - Carl Beyerhelm (GISS) for pointing these concerns out. Now, for both ArcGIS Pro and ArcMap users, the script will first copy each NIFS feature class to a scratch GDB. Geometry will be calculated for all features in this scratch GDB, and will then be compared with the actual values in the local copy. It will test each feature to determine if the geometry has changed. If it has, it will insert the value from the scratch GDB. If it hasn't, no edit will be made.

      Additionally, users must specify the IncidentName as input. Edits will only be made to those features whose IncidentName matches the user specified value. The onus in on the user to ensure all their data is properly attributed. This is a better safeguard than having to remember to remove features from neighboring fires each edit cycle.

 

Additionally, the script will copy the local copy fGDB or mobile/runtime .geodatabase to a new master incident fGDB, and place it into the same directory as the old master incident fGDB. It will also place an additional copy into the backups folder with an appropriate date/time stamp. Lastly, it will rename the feature classes inside of these fGDBs to a series of user specified values in order to maintain adherence to the incident’s feature class naming standard (whatever the incident GISS decide they should be).

 

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
