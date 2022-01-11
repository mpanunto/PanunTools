# Dissolve Explode Perimeter Line

Tool that assists the GISS in tidying up their Perimeter Line features (Contained & Uncontained).

### How does it work?
The tool iterates through the user specified list of IncidentName values, and performs a selection of corresponding Contained and Uncontained features. Once selected, these features are dissolved, and then exploded (Multipart to Singlepart). The original Contained and Uncontained features are then deleted, and replaced with the newly exploded features. The user specified IrwinIDs are inserted into the newly exploded features.

### User Inputs

1. Specify IncidentName and IrwinID
2. Specify Path to PerimeterLine Feature Class
3. Toggle for Dissolving and Exploding Contained Features
4. Toggle for Dissolving and Exploding Uncontained Features
5. Coordinate system to perform acreage calculations
6. Geometry measurement type

![screenshot_DissolveExplodePerimeterLine_1.png](/docs/screenshot_DissolveExplodePerimeterLine_1.png?raw=true)

![screenshot_DissolveExplodePerimeterLine_2.png](/docs/screenshot_DissolveExplodePerimeterLine_2.png?raw=true)
