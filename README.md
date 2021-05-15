## About

Panuntools is a ***very*** cleverly named toolbox created for GISS on wildfire incidents, and currently contains the following tools:

1. [Calculate Ownership](docs/README_CalculateOwnership.md)
2. [Create Fire Progression](docs/README_CreateFireProgression.md)
3. [GISS Workflow Assistant](docs/README_GISSWorkflowAssistant.md)
4. [Multi Export PDF](docs/README_MultiExportPDF.md)
5. [Update Fire Edge](docs/README_UpdateFireEdge.md)

These tools have only been tested for use in ArcGIS Pro 2.7. In the future, some of these tools may be migrated to the [Community GISS Tools](https://github.com/smHooper/giss_community_tools) repository, but for now it was easier to just create my own. I also hope to eventually convert this toolbox of script tools into a Python toolbox in order to tidy up files, enhance collaboration, and improve the visibility of version changes.

## Usage

To use this toolbox:
1. [Download the repository](https://github.com/mpanunto/Panuntools/archive/refs/heads/main.zip)
2. Extract Panuntools.tbx, and the following Python scripts & files to the incident's tools directory:
    - MultiExportPDF.py
    - MultiExportPDF.xlsx
3. Keep Python scripts in the same directory as the extracted toolbox
4. Run tools using ArcGIS Pro

Where possible, I would recommend setting your incident's default input values in the script tool parameters. Doing that will speed up the process of running these tools throughout the duration of the incident.

## Contact
Feel free to contact me at mpanunto@blm.gov with any comments, questions, or error reports.
