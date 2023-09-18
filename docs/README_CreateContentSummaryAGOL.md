# Create Content Summary AGOL

Tool that generates a CSV summary of a user's ArcGIS Online content.

### How does it work?

Using the ArcGIS API for Python, the tool will first connect to the user's specified ArcGIS Online Portal. It will then cycle through each content item that the user owns, and will pull together a variety of descriptive information. This information is then compiled into a dataframe and exported to a CSV file.

![screenshot_CreateContentSummaryAGOL_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateContentSummaryAGOL_1.png)

### User inputs

1.	Toggle for using ArcGIS Pro’s Active Portal to make org connection
2.	ArcGIS Online Portal URL
3.	ArcGIS Online Username
4.	ArcGIS Online Password
5. Specify output directory


![screenshot_CreateContentSummaryAGOL_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateContentSummaryAGOL_2.png)
