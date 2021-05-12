# Create Fire Progression

I know that several fire progression tools have been created over the years. This is simply one that I wrote a few seasons ago, and am offering it up as an alternative.


For this tool to work, the fire perimeter feature classes within the incident's Progression GDB must follow a "IncidentName_YYYYMMDD_HHMM" naming convention, as shown in the below screenshot. The tool parses perimeter dates & times from the filenames, and uses this information to create some useful labeling/symbolization fields. It is hardcoded to assume that the datetimes are the last 13 characters of the filenames.


![screenshot_CreateFireProgression_1.png](/docs/screenshot_CreateFireProgression_1.png?raw=true)


### Users have two options:
1. Create a FireProgression feature class by processing all perimeters
2. Create a FireProgression feature class by processing only the latest perimeter
    - Requires a previously generated FireProgression feature class

![screenshot_CreateFireProgression_2.png](/docs/screenshot_CreateFireProgression_2.png?raw=true)


### Output FireProgression Feature Class

The below screenshot shows what the output attribute table looks like. Users can opt to either reference one of the label fields to quickly apply a symbology, or they can create their own symbology field using the parsed datetime information and acreage values.

![screenshot_CreateFireProgression_3.png](/docs/screenshot_CreateFireProgression_3.png?raw=true)
