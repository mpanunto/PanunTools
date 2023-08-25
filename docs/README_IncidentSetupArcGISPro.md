# Incident Setup ArcGIS Pro

Tool that automates much of the process to setup the Pro Project Template, create Master Projects, and create an Edit Project.

### How does it work?
</br>
</br>

![screenshot_IncidentSetupArcGISPro_1.png](/docs/screenshot_IncidentSetupArcGISPro_1.png?raw=true)

If "Setup Pro Project Template" is selected, the tool will use the user provided input parameters to:
1. Rename the template GDBs to the incident name
2. Rename the project map to the incident name
3. Insert the Credits/Author into the project map's metadata
4. Set the project map's coordinate system
5. Resource the broken DynamicTextUpdate table
6. Insert the IncidentName and UniqueFireID into the DynamicTextUpdate table
7. Resource the broken event layers to the Master Incident GDB (only if the user requested it be created)
  
Once the tool has finished, users will still need to:
    -Open the Pro Project Template and manually remove the broken incident GDBs from the project
    -Add the correct named incident GDBs to the project
    -Rename the project's home folder to the incident name
</br>
</br>
</br>
</br>

![screenshot_IncidentSetupArcGISPro_2.png](/docs/screenshot_IncidentSetupArcGISPro_2.png?raw=true)

If "Create Master Projects" is selected, the tool will use the user provided input parameters to:
1. Create copies of the Pro Project Template for each requested Master Project, and rename them accordingly
2. Rename the project map type
3. Insert the Title into the project map's metadata
4. If the requested Master Project contains the text "Brief" or "brief":
    - The "Event Group BAM Large Symbols" group layer will be added to the project map
5. If the requested Master Project contains the text "Repair" or "repair":
    - The "Event Group Repair Status" group layer will be added to the project map
6. If requested, apply definition queries to the Event layers
7. If requested, create an Edit project for the user
    - The GISS Edit Service will be added to the project map using the provided NIFC AGOL credentials
    - A broken Event Group Layer will be added to the project map for quick resourcing to Mobile GDB
