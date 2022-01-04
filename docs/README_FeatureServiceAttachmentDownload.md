# Download Feature Layer Attachments
***Latest version is v20210915***

Tool that downloads attachments from feature layers

### How does it work?

The tool uses the ArcGIS API for Python to tap into the ArcGIS Online Organization of interest and download attachments from a user specified feature service. User's must specify the feature service ItemID as input. The tool will then iterate through each feature layer within the service looking for attachments, and will download them if any are found.

### User Inputs:
1.	Toggle for using ArcGIS Pro’s Active Portal to make feature service connections
2.	ArcGIS Online Portal URL
3.	ArcGIS Online Username
4.	ArcGIS Online Password
5.	Feature Service ItemID
6.	Output Directory

![screenshot_DownloadFeatureLayerAttachments_1.png](/docs/screenshot_DownloadFeatureLayerAttachments_1.png?raw=true)




