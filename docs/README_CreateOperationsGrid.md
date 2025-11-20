# Create Operations Grid

Tool that creates a reference grid for operational use.

### How does it work?

The user must provide a point feature class containing a single feature that serves as the grid’s reference point. This point can represent either the grid’s center or its origin (bottom-left corner). 

Users must also define the grid’s width and height (in miles), along with the grid cell size (in miles). Specific letters can be excluded from grid labeling to prevent communication conflicts (for example: **D** for Drop Points, **H** for Helispots, **S** for Sling Sites, or Division labels, etc).

Lastly, specify a Sub-Grid Factor to control the level of detail in the sub-grid — this determines how many rows and columns are created inside each grid cell.

### User Inputs

1. Specify Path to Grid Reference Point Feature Class
2. Specify Reference Point Type
3. Specify Specify Grid Width/Height (in miles)
4. Specify Grid Cell Size (in miles)
5. Specify Grid Label Starting Number
6. Specify Letters to Exclude from Grid Labeling
7. Specify Sub-Grid Factor (number of rows & columns for each grid cell)
8. Specify Output Directory

![screenshot_CreateOperationsGuide_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateOperationsGrid_1.png)


An output GDB with three feature classes will then be created based on the user's inputs:
- Grid
- SubGrid
- Header

![screenshot_CreateOperationsGuide_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateOperationsGrid_2.png)
