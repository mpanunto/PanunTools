# PDF Georeference Check

Tool that searches for PDF files, and checks if they are georeferenced.

### How does it work?

The tool iterates through the user specified list of IncidentName values, and performs a selection of corresponding Contained Line and Fire Edge features. Once selected, these features are dissolved, and then exploded (Multipart to Singlepart). The original Contained Line and Fire Edge features are then deleted, and replaced with the newly exploded features. The user specified IrwinIDs are inserted into the newly exploded features.

### User Inputs
1. Toggle to check for Georeferenced PDFs
2. Toggle to check for Non-Georeferenced PDFs
3. Specify PDF search directory
4. Toggle for perform a PDF search recursively

![screenshot_PDFGeoreferenceCheck_1.png](/docs/screenshot_PDFGeoreferenceCheck_1.png?raw=true)

![screenshot_PDFGeoreferenceCheck_2.png](/docs/screenshot_PDFGeoreferenceCheck_2.png?raw=true)
