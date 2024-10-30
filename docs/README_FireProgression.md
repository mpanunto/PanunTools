# Burn Period

Tool that calculates a 6-Day burn period forecast for each RAWS station within ONCC and OSCC.

### How does it work?
</br>

The tool attempts to  [Southwest U.S. Burn Period Tracker](https://cales.arizona.edu/climate/SWBurnPeriod/) first determines the proximity of ONCC and OSCC fires (in miles) to each of the Timberland Owners as provided in the [Forest Inventory Owner Feature Service](https://nifc.maps.arcgis.com/home/item.html?id=8d60bf094c8b4dfd912f505193df4091). It uses the following fire point and fire perimeter datasets for these calculations. If an incident has both a fire point and fire perimeter, the vertex that is closest to the Timberland Owner will be used as the proximity distance.

1. [WFIGS Current Points Boundaries](https://nifc.maps.arcgis.com/home/item.html?id=4181a117dc9e43db8598533e29972015)
2. [WFIGS Current Perimeters](https://nifc.maps.arcgis.com/home/item.html?id=d1c32af3212341869b3c810f1a215824)
3. [FIRIS Points and Perimeters](https://nifc.maps.arcgis.com/home/item.html?id=c7f3bc42548f486890eeda8f8deac8c7)
4. [Bode Points and Perimeters](https://nifc.maps.arcgis.com/home/item.html?id=049253ae18b04416b8eb9b5ab6890c9d)

</br>


After intersecting the fire perimeters with these administrative boundary datasets, the output is dissolved, and ***acreage is calculated in WGS84 Geodesic***. Percentages of burned acreage by ownership are also calculated relative to the entire GACC, and also to the individual incidents. The calculations are then pushed to the [CA Perimeter Acreage Summary Feature Service](https://nifc.maps.arcgis.com/home/item.html?id=61aa3bf5286d47d8a69c11643991ef0f), which is used to drive the [CA Perimeter Acreage Summary Dashboard](https://nifc.maps.arcgis.com/home/item.html?id=02f16a3166e94ef09ad3f292a7c06f1b).



Within the dashboard, the list of incidents will be filtered to the selected GACC. Additionally, upon selection of a GACC, the "GACC Summary" tab will have its percentages correctly sum together. The percentages will not sum properly until a GACC selection is made. Furthermore, upon selection of a incident, the "Incident Summary" tab will have its percentages correctly sum together as well. There will also be several information fields displayed for the selected incident, which are pulled from IRWIN.

![screenshot_PerimeterAcreageSummary_1.png](/docs/screenshot_PerimeterAcreageSummary_1.png?raw=true)


Running the tool to update the feature service is very simple, and does not require any input parameters other than specifying the ArcGIS Online login method.

![screenshot_PerimeterAcreageSummary_2.png](/docs/screenshot_PerimeterAcreageSummary_2.png?raw=true)


</br>
</br>

### Full Automation


This script tool has also been restructured for full automation via Windows Task Scheduler on a dedicated machine. It is currently set to run hourly.
  - Log File: https://1drv.ms/x/s!AgiBqEhgaH85y4FPmkyC3M3uGcos1g?e=xbU00t
    
</br>
</br>
