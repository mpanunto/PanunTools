# Create Event Point Numbering Guide

Tool that creates a radial numbering guide to assist with numbering various Event Points (Drop Points, Helispots, Sling Sites, etc).

### How does it work?
The tool iterates through the user specified list of IncidentName values, and performs a selection of corresponding Contained and Uncontained features. Once selected, these features are dissolved, and then exploded (Multipart to Singlepart). The original Contained and Uncontained features are then deleted, and replaced with the newly exploded features. The user specified IrwinIDs are inserted into the newly exploded features.

### User Inputs

1. Specify IncidentName and IrwinID
2. Specify Path to PerimeterLine Feature Class
3. Toggle for Dissolving and Exploding Contained Features
4. Toggle for Dissolving and Exploding Uncontained Features
5. Coordinate system to perform acreage calculations
6. Geometry measurement type

![screenshot_CreateEventPointNumberingGuide_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateEventPointNumberingGuide_1.png)

![screenshot_CreateEventPointNumberingGuide_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateEventPointNumberingGuide_2.png)
