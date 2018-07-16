This file details the calibration of the new RTD probes with 6 RTDS in each probe.
Each probe is labeled with an indicator("A" , "B" , or "C")
There are 2 groups of 9 wires each on each probe labeled "1" and "2"
Of these 9 wires the grouping of wires go as follow
1st Red/Black
2nd Orange/Blue
3rd White/Green

With the extra wire for each group having a stripe on it

The 6 RTDS were taken to be in this order based on this

RTD 1 | Group 1 |  Red/Black 
RTD 2 | Group 1 |  Orange/Blue
RTD 3 | Group 1 |  White/Green
RTD 4 | Group 2 |  Red/Black 
RTD 5 | Group 2 |  Orange/Blue
RTD 6 | Group 2 |  White/Green


There are up to 14 AIN channels read from each Labjack at a time
The Old probe RTDs used for comparison will be marked OG while the Wisconsin probe RTDs are marked WI


LabJack SIN 139

AIN 0  | B1 | OG
AIN 1  | B2 | OG
AIN 2  | B3 | OG
AIN 3  | B4 | OG
AIN 4  | B5 | OG
AIN 5  | B6 | OG
AIN 6  |-------
AIN 7  |-------
AIN 8  | B1 | WI
AIN 9  | B2 | WI
AIN 10 | B3 | WI
AIN 11 | B4 | WI
AIN 12 | B5 | WI
AIN 13 | B6 | WI

_______________________________________

LabJack SIN 166

AIN 0  | A1 | WI
AIN 1  | A2 | WI
AIN 2  | A3 | WI
AIN 3  | A4 | WI
AIN 4  | A5 | WI
AIN 5  | A6 | WI
AIN 6  | C1 | WI
AIN 7  | C2 | WI
AIN 8  | C3 | WI
AIN 9  | C4 | WI
AIN 10 | C5 | WI
AIN 11 | C6 | WI
AIN 12 | B7 | OG
AIN 13 | B8 | OG