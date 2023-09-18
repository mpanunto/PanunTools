# Incident Setup AGOL

Tool that automates the creation of incident specific groups, services, and web maps.

### How does it work?

The tool uses the ArcGIS API for Python to tap into the NIFC Org, and create/organize the requested items. It is hardcoded to make copies of the official NIFC template services, and template web maps. 
- The requested items will be copied, renamed to the [GeoOps standard](https://www.nwcg.gov/publications/pms936/file-naming#:~:text=Web%20maps%2C%20mobile%20maps%2C%20and%20data%20services), and moved to a newly created folder for the incident.
- If requested, a new Photo Point service will be created, and will automatically replace the template version within any newly created Incident Web Maps, View Only Incident Web Maps, and Suppression Repair Web Maps.
- If the user requests groups to be created along with services and web maps, these items will automatically be shared to the corresponding groups. For example, the Incident Web Map and Suppression Repair Web Map will automatically be shared with the Mobile Editing group, while the View Only Incident Web Map will be automatically shared with the Viewer group.
- Lastly, checks are performed on the layers of the two Mobile Editing web maps (Incident and Suppression Repair) to ensure they are Sync enabled.

### User inputs
1. Specify NIFC ArcGIS Online Username
2. Specify NIFC ArcGIS Online Password
3. Specify Incident Name
4. Specify Unique Fire ID
5. Toggles to create incident specific AGOL Groups
6. Toggles to create incident specific Feature Services
7. Toggles to create incident specific Web Maps    


![screenshot_IncidentSetupAGOL_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_IncidentSetupAGOL_1.png)
