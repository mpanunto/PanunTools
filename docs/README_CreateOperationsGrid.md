# Create Operations Grid

Tool that creates a reference grid for operational use.

### How does it work?

The user must provide a point feature class containing a single feature, which is the reference point to create the grid. The point can represent the grid's CENTER or ORIGIN (bottom-left corner). 

Users must also specify the grid's width & height (in miles), and the grid cell size (in miles). Specific letters can also be excluded from the grid labeling to avoid communication conflicts (D for Drop Points, H for Helispots, S for Sling Sites, Division Labels, etc)

Lastly, a Sub-Grid Factor must be specified that provides the desired resolution of the sub-grid (number of rows & columns per grid cell)

### User Inputs

1. Specify Path to Grid Reference Point Feature Class
2. Specify Reference Point Type
3. Specify Specify Grid Width/Height (in miles)
4. Specify Grid Cell Size (in miles)
5. Specify Grid Label Starting Number
6. Specify Letters to Exclude from Grid Labeling
7. Specify Sub-Grid Factor (number of rows & columns for each grid cell)
8. Specify Output Directory

![screenshot_CreateOperationsGuide_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateOperationsGuide_1.png)


An output GDB with three feature classes will then be created based on the user's inputs:
- Grid
- SubGrid
- Header

![screenshot_CreateOperationsGuide_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateOperationsGuide_2.png)
