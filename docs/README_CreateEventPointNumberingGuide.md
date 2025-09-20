# Create Event Point Numbering Guide

Tool that creates a radial numbering guide to assist with numbering various Event Points (Drop Points, Helispots, Sling Sites, etc).

![screenshot_CreateEventPointNumberingGuide_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateEventPointNumberingGuide_1.png)

### How does it work?

The user must provide the tool with a point feature class containing a single feature that represents the "center point" of the incident. This point will be used as the center point for the radial numbering guide and will be buffered by the user provided distance (in miles). This buffer will then be sliced into a number of equal sized features based on the user specified start/end range. 

### User Inputs

1. Specify Path to Incident Center Point Feature Class
2. Specify Event Point Numbering Range - Start
3. Specify Event Point Numbering Range - End
4. Specify Radius of Guide (miles)
5. Specify Output Directory

![screenshot_CreateEventPointNumberingGuide_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateEventPointNumberingGuide_2.png)
