# interpolate_coordinates

Expects a CSV file with 5 columns
0. Lat
1. Lon
2. Date
3. Time
4. Dist

If order of columns varies you can specify order using flags in command line.
Data has to be formated mm/dd/yyyy
Time has to be formated HH:MM:SS (24 hours)

Will output new file FILENAME_new.csv

```
Interpolate_Coorditates.py
```

call with options
```
-f PATH to CSV file
-d index of date column 
-t index of time column
-x index of lon column
-y index of lat column
-z index of distance column
-m interpolation method (dist or time)
```
