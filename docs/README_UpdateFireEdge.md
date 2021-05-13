# Update Fire Edge

Don't you hate having to meticulously split, delete, and swap the feature categories of Contained Line and Fire Edge during the early morning perimeter update? Well with the Update Fire Edge tool, you can simply dump all the old Fire Edge features, and quickly paste in an updated Fire Edge feature that conforms to the new fire perimeter and existing Contained Line.



### The general workflow is:
1. Download Map (aka create local copy) or Sync
2. Perform edits to the Wildfire Daily Fire Perimeter
3. Save edits
4. Run this tool to generate the new Fire Edge features
6. Delete the old Fire Edge feature(s) from the EventLine feature class
7. Paste in the new Fire Edge feature(s) to the EventLine feature class
8. Save edits

At this point the incident's "Fire Edge" is now up to date. If all edits are complete, I would recommend users proceed by running the [GISS Workflow Assistant tool](/docs/README_GISSWorkflowAssistant.md) prior to syncing.

### Bonus Feature
Due to the nature of how this tool works, it can also be used to identify segments of Contained Line that do not match the fire perimeter. If there are segments of Contained Line that appear to be overlapping the new Fire Edge features that were pasted in, chances are these segments of Contained Line need to be cleaned up to match the fire perimeter.
