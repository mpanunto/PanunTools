# Create Event Point Numbering Guide

Tool that creates a radial numbering guide to assist with numbering various Event Points (Drop Points, Helispots, Sling Sites, etc).

![screenshot_CreateEventPointNumberingGuide_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateEventPointNumberingGuide_1.png)

### How does it work?

The user must provide a point feature class containing a single feature representing the incident's center point. This point serves as the origin for the radial numbering guide and will be buffered by a user-defined distance (in miles). The resulting buffer will then be divided into a specified number of equal segments based on the user-defined start and end range. 

### User Inputs

1. Specify Path to Incident Center Point Feature Class
2. Specify Event Point Numbering Range - Start
3. Specify Event Point Numbering Range - End
4. Specify Radius of Guide (miles)
5. Specify Output Directory

![screenshot_CreateEventPointNumberingGuide_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateEventPointNumberingGuide_2.png)
