# Create Fire Progression

I know that several fire progression tools have been created over the years. This is simply one that I wrote a few seasons ago, and am offering it up as an alternative. Not very fancy, but works (as far as I know!).


For this tool to work, the fire perimeter feature classes within the incident's Progression GDB must follow a "IncidentName_YYYYMMDD_HHMM" naming convention. For example: "EastFork_20200907_0203". The tool parses perimeter dates & times from the filenames, and uses this information to create some useful labeling/symbolization fields. It is hardcoded to assume that the datetimes are the last 13 characters of the filenames.


![screenshot_CreateFireProgression_1.png](/docs/screenshot_CreateFireProgression_1.png?raw=true)


### Users have two options:
1. Create a new FireProgression feature class from scratch
2. Update an already existing FireProgression feature class

![screenshot_CreateFireProgression_2.png](/docs/screenshot_CreateFireProgression_2.png?raw=true)
