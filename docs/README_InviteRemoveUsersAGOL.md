# Invite Remove Users AGOL

Tool that automates the Inviting/Removal of ArcGIS Online users across a series of user specified groups.

### How does it work?

Using the 'InviteRemoveUsersAGOL.csv' file, specify a series of ArcGIS Online groups, and usernames that are to be invited or removed. The tool uses this information to automate these tasks via the ArcGIS API for Python.

- The usernames and group names in the default CSV file are simply placeholders, and should be replaced with the actual usernames and group names of interest.
- Do not rename the 'AGOLUsername' CSV field.
- Users running the tool must be the group owners, or group managers in order to have invite or remove capabilities.
- Values of "Invite" and "Remove" must be used to specify whether a user is invited or removed from a group. Any other value (including blanks) will have no effect.
- There is no limit to the number of groups, or users that can be listed in the CSV file.

![screenshot_InviteRemoveUsersAGOL_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_InviteRemoveUsersAGOL_2.png)

### User inputs

1.	Toggle for using ArcGIS Pro’s Active Portal to make org connection
2.	ArcGIS Online Portal URL
3.	ArcGIS Online Username
4.	ArcGIS Online Password
5. Specify path to InviteRemoveUsersAGOL.csv


![screenshot_InviteRemoveUsersAGOL_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_InviteRemoveUsersAGOL_1.png)
