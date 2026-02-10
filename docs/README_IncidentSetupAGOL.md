# Incident Setup AGOL

Tool that automates the creation of incident specific groups, services, and web maps.

### How does it work?

The tool uses the ArcGIS API for Python to tap into the NIFC Org, and create/organize the requested items. It is hardcoded to make copies of the official NIFC template services, and template web maps. 
- The requested items will be copied, renamed according to the [GeoOps File Naming Standarda](https://www.nwcg.gov/publications/pms936/file-naming), and moved to a newly created folder for the incident.
- If requested, a new Photo Point service will be created, and will automatically replace the template version within any newly created Operations Edit Maps, Repair Edit Maps, and View Only Maps.
- If the user requests groups to be created along with services and web maps, these items will automatically be shared to the corresponding groups. For example, the Operations Edit Map and Repair Map will automatically be shared with the Mobile Editing group, while the View Only Map will be automatically shared with the Viewer group.

### User inputs
1. Active portal check
2. Specify Incident Name
3. Specify Unique Fire ID
4. Toggles to create incident specific AGOL Groups
5. Toggles to create incident specific Feature Services
6. Toggles to create incident specific Web Maps    


![screenshot_IncidentSetupAGOL_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_IncidentSetupAGOL_1.png)
