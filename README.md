***Latest version is v20220113***

## About

PanunTools is a ***very*** cleverly named toolbox created for GISS on wildfire incidents, and currently contains the following toolsets and tools:

#### Daily Workflow Toolset
1. [Calculate Containment](docs/README_CalculateContainment.md)
2. [Calculate Ownership](docs/README_CalculateOwnership.md)
3. [Create Fire Perimeter Export](docs/README_CreateFirePerimeterExport.md)
4. [Create Fire Progression](docs/README_CreateFireProgression.md)
5. [Dissolve Explode Perimeter Line](docs/README_DissolveExplodePerimeterLine.md)
6. [GISS Workflow Assistant](docs/README_GISSWorkflowAssistant.md)
7. [PDF Georeference Check](docs/README_PDFGeoreferenceCheck.md)
8. [PDF Multi Export](docs/README_PDFMultiExport.md)
9. [Update Perimeter IR](docs/README_UpdatePerimeterIR.md)

#### Data Download Toolset
1. [Base Data Acquisition](docs/README_BaseDataAcquisition.md)
2. [Feature Layer Download](docs/README_FeatureLayerDownload.md)
3. [Feature Service Attachment Download](docs/README_FeatureServiceAttachmentDownload.md)

#### Incident Setup Toolset
1. [Incident Setup AGOL](docs/README_IncidentSetupAGOL.md)
2. [Invite Remove Users AGOL](docs/README_InviteRemoveUsersAGOL.md)

The script tool code and properties are password protected, but can be accessed by entering "password" in the Enter Password box.

These tools have only been tested for use in ArcGIS Pro 2.7. In the future, some of these tools may be migrated to the [Community GISS Tools](https://github.com/smHooper/giss_community_tools) repository, but for now it is easier for me to maintain them as my own toolbox. I also hope to eventually convert this toolbox of script tools into a Python toolbox in order to tidy up files, enhance collaboration, and improve the visibility of version changes.

## Usage

To use this toolbox:
1. [Download the repository](https://github.com/mpanunto/PanunTools/archive/refs/heads/main.zip)
2. Extract PanunTools.tbx, and all accompanying files to the incident's tools directory
3. Keep extracted Python scripts in the same directory as the PanunTools toolbox
4. Run tools using ArcGIS Pro

Where possible, I would recommend setting your incident's default input values in the script tool parameters. Doing so will speed up the process of running these tools throughout the duration of the incident.

## Contact
Feel free to contact me (Matt Panunto) at mpanunto@blm.gov with any comments, questions, or error reports.
