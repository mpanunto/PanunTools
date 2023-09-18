# Create Group Member List AGOL

Tool that pulls together AGOL group member information and exports to a CSV

### How does it work?

Using the ArcGIS API for Python, the tool will attempt to connect to the user specified ArcGIS Online group. If found, it will generate a list of group members, then iterate through each one and grab the following information:

- Username
- Full Name
- First Name
- Last Name
- Group Role
- Org Role
- Last Login
- Email

This information is then compiled into a dataframe and exported to a CSV file.

![screenshot_CreateGroupMemberListAGOL_2.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateGroupMemberListAGOL_2.png)

### User inputs

1.	Toggle for using ArcGIS Pro’s Active Portal to make org connection
2.	ArcGIS Online Portal URL
3.	ArcGIS Online Username
4.	ArcGIS Online Password
5.	Group Name
6.	Output Directory

![screenshot_CreateGroupMemberListAGOL_1.png](https://raw.githubusercontent.com/mpanunto/PanunTools/main/docs/screenshot_CreateGroupMemberListAGOL_1.png)
