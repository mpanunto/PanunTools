# Incident Setup ArcGIS Pro

Tool that automates the creation of the Pro Project Template, and Master Projects.

### How does it work?



### User inputs
   


![screenshot_IncidentSetupArcGISPro_1.png](/docs/screenshot_IncidentSetupArcGISPro_1.png?raw=true)

If "Setup Pro Project Template" is selected, the tool will use the user provided input parameters to:
1. Rename the template GDBs to the incident name
2. Rename the project map to the incident name
3. Insert the Credits/Author into the project map's metadata
4. Set the project map's coordinate system
5. Resource the broken DynamicTextUpdate table
6. Insert the IncidentName and UniqueFireID into the DynamicTextUpdate table
7. Resource the broken event layers to the Master Incident GDB (only if the user requested it be created)

![screenshot_IncidentSetupArcGISPro_2.png](/docs/screenshot_IncidentSetupArcGISPro_2.png?raw=true)
