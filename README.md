# mouse-data-analyze
Takes the data from mouselogger V2 and extracts different features such as 
1. Number of left/right clicks
2. Number of drag events
3. Time between two clicks
4. Average click duration 
5. Average drag duration
6. Scroll length/time

Here is how the code works -

1. Check when the logger file was last edited.
2. Check how long the logger was logging the data in this file.
3. Create multiple multidimensional [24xn] arrays to store different features for each hour.
4. Distance function is defined to calculate the distance between two clicks.
5. Identify clicks - 0x01 for left button down, 0x02 for left button up, 0x04 for right button down, and 0x08 for right button up
6. Check if the size of arrays for click up and click down match - notify otherwise.
7. Store click co-ordinates.
8. Check drag length between every two clicks using distance function. If distance > (threshold value), classify those clicks as drag and remove these from the click list. The threshold value is set to 100 for now.
9. Number of clicks = Total number of clicks initially identified - Number of drags
10. Calcualte time between clicks for all those arrays where the size of arrays of click up and click down match.
11. Scroll length - add up all the scroll data stored and divide by 120 (distance between one notch to another is 120).
12. Display all the data.
