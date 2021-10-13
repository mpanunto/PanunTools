# Dissolve Explode Perimeter Edge

Basic tool that assists the GISS in tidying up their perimeter edge (Contained Line & Fire Edge).

### How does it work?

The tool iterates through the user specified list of IncidentName values, and performs a selection of corresponding Contained Line and Fire Edge features. Once selected, these features are dissolved, and then exploded (Multipart to Singlepart). The original Contained Line and Fire Edge features are then deleted, and replaced with the newly exploded features. The user specified IrwinIDs are inserted into the newly exploded features.

### User Inputs
1. Specify IncidentName and IrwinID
2. Specify Path to EventLine Feature Class
3. Toggle for Dissolving and Exploding Contained Line Features
4. Toggle for Dissolving and Exploding Fire Edge Features

![screenshot_DissolveExplodePerimeterEdge_1.png](/docs/screenshot_DissolveExplodePerimeterEdge_1.png?raw=true)

![screenshot_DissolveExplodePerimeterEdge_2.png](/docs/screenshot_DissolveExplodePerimeterEdge_2.png?raw=true)
