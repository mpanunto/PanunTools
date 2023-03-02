# Feature Service Backup

Tool that downloads feature service data by exporting feature layers to GDB feature classes.

### How does it work?

The tool's primary purpose is to simplify the cumbersome "Export Data" process within the ArcGIS Online browser interface. Normally, for a user to be able to export an entire feature service to a GDB, they must either be owner of the service, or the owner must have "Export Data" enabled for the service. This tool however allows users to download entire features services with only read access to the services.

The tool uses the ArcGIS API for Python to tap into the ArcGIS Online Organization of interest and backup/download data from user specified feature services. The tool will iterate through all feature layers within a service, and attempts to download each in entirety. Though similar to the [Feature Layer Download](README_FeatureLayerDownload.md) tool in the fact that it downloads data from feature services, this tool was designed to be a more simplistic and lightweight option when users only need to backup a handful of services. It requires no accompanying files, no AOI specification, and does not use the Python Multiprocessing library. Unlike the Feature Layer Download tool, it also provides a toggle for including attachments, and the option to apply GeoOps file naming standards to the outputs.

### User Inputs:
1.	Toggle for using ArcGIS Pro’s Active Portal to make feature service connections
2.	ArcGIS Online Portal URL
3.	ArcGIS Online Username
4.	ArcGIS Online Password
5.	Specify feature service ItemIDs
6.	Toggle for including attachments
7.	Specify output directory
8.	Toggle for applying GeoOps file naming standards
9.	Specify Incident Name
10.	Specify Incident ID
11.	Specify ArcGIS Pro version

![screenshot_FeatureServiceBackup_1.png](/docs/screenshot_FeatureServiceBackup_1.png?raw=true)

![screenshot_FeatureServiceBackup_2.png](/docs/screenshot_FeatureServiceBackup_2.png?raw=true)




