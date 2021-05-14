# Calculate Ownership

Pretty basic tool that automates the Intersect & Dissolve process to obtain acres burned by ownership. To run, users must provide the following inputs to the tool:
1. Path to ownership feature class
2. Field that defines ownership
3. Path to fire perimeter feature class
4. Coordinate system to perform acreage calculations
5. Scratch directory







![screenshot_CalculateOwnership_1.png](/docs/screenshot_CalculateOwnership_1.png?raw=true)







This tool doesn't generate any outputs. The calculations are provided to the user in the Geoprocessing Messages:  
![screenshot_CalculateOwnership_2.png](/docs/screenshot_CalculateOwnership_2.png?raw=true)

To speed things up, I would recommend setting your incident's default input values in the script tool parameters, that way you can just open the tool and run.
