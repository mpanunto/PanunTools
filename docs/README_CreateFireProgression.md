# Create Fire Progression

I know that several fire progression tools have been created over the years. This is simply one that I wrote a few seasons ago, and am offering it up as an alternative.

### How does it work?

The tool builds a fire progression by iteratively projecting, clipping, erasing, and merging the perimeters inside an incident's Progression GDB. For this tool to work, the fire perimeter feature classes within the incident's Progression GDB must follow a "i_YYYYMMDD_HHMM_IncidentName_AnyOtherInfo" naming convention, as shown in the below screenshot. The tool parses perimeter dates & times from the filenames, and uses this information to create some useful labeling/symbolization fields.


![screenshot_CreateFireProgression_1.png](/docs/screenshot_CreateFireProgression_1.png?raw=true)


### Users have two options:
1. Create a FireProgression feature class by processing all perimeters
2. Create a FireProgression feature class by processing only the latest perimeter
    - Requires a previously generated FireProgression feature class

![screenshot_CreateFireProgression_2.png](/docs/screenshot_CreateFireProgression_2.png?raw=true)


### Output FireProgression Feature Class

The below screenshot shows what the output attribute table looks like. Users can opt to either reference one of the label fields to quickly apply a symbology, or they can create their own symbology field using the parsed datetime information and acreage values.

![screenshot_CreateFireProgression_3.png](/docs/screenshot_CreateFireProgression_3.png?raw=true)

A demonstration of this tool can be viewed [at this link]([https://youtu.be/0jUqQ8PP4Ek?t=282](https://youtu.be/LGal9OCzmcc?t=305)https://youtu.be/LGal9OCzmcc?t=305]).
