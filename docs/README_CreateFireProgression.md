# Create Fire Progression

I know that several fire progression tools have been created over the years. This is simply one that I wrote a few seasons ago, and offer it up as an alternative. Not very fancy, but works (as far as I know!).


This script requires users to already have a GDB containing all daily wildfire perimeters sorted by date.
The perimeters in this GDB can use any naming convention, but it must be consistent across all feature classes.

For this tool to work, the fire perimeter feature classes within the incident's Progression GDB must follow a "IncidentName_YYYYMMDD_HHMM" naming convention. Example: "EastFork_20200907_0203". The tool parses perimeter date & time from the filenames, and uses this information to create some useful labeling/symbolization fields. It is hardcoded to assume that the date/times are the last 13 characters of the filenames.





![screenshot_CreateFireProgression_1.png](/docs/screenshot_CreateFireProgression_1.png?raw=true)

![screenshot_CreateFireProgression_2.png](/docs/screenshot_CreateFireProgression_2.png?raw=true)
