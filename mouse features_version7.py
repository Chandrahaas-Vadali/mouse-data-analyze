# modules
#------------------------------------------------------------------------------
import xlrd
from math import log,exp
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib import animation
import pandas as pd
import os
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import sys

plt.close('all') # close all previous plots


#Partitioning into hours
#------------------------------------------------------------------------------

#Input file name
filename = "Apr 14_2.log"#str(input("Enter file name : "))
#The time stamp of when it was last modified
lastmod = datetime.fromtimestamp(os.stat(filename).st_mtime)
print("The file ",filename,"  was last edited at : ",lastmod)

#Collect all the mouse data
x = [] #x-coordinate
y = [] #y-coordinate
click_state = [] #left click down = 1 #left click up = 2 #right click up = 8
#right click down = 4
scroll_state = []

#Read as CSV
book = pd.read_csv(filename,header=None) 
time_stamp = 0.001*book[0].to_numpy()
x = book[5].to_numpy()
y = -book[6].to_numpy()
click_state = book[1].to_numpy()
scroll_state = book[2].to_numpy()
totaltime = int(max(time_stamp) - min(time_stamp))
print("Total time : ", totaltime/3600, "hours")
start_time = lastmod + timedelta(seconds=-totaltime)
print("The file started logging at : ", str(start_time))

#Labeling with "th" to indicate hourly paritions
columns = 1
rows = 24 #hours
timeth = [[]*columns for i in range(rows)]
xth = [[]*columns for i in range(rows)]
yth = [[]*columns for i in range(rows)]
click_stateth = [[]*columns for i in range(rows)]
scroll_stateth = [[]*columns for i in range(rows)]

#Initialize arrays for stroing the x after hourly partioning
for i in range(0,len(time_stamp)):
    t = int(datetime.fromtimestamp(time_stamp[i]).hour) #temporary variable to store the hour
    timeth[t].append(time_stamp[i])
    xth[t].append(x[i])
    yth[t].append(y[i])
    click_stateth[t].append(click_state[i])
    scroll_stateth[t].append(scroll_state[i])
  
if(str(date.fromtimestamp(min(time_stamp))) != str(date.fromtimestamp(max(time_stamp)))):
    print("There are different dates here ranging from = ", str(date.fromtimestamp(min(time_stamp))), " to ",str(date.fromtimestamp(max(time_stamp))))
       
#------------------------------------------------------------------------------
#Start analyzing
#define distance function
def distance(x1,y1,x2,y2):
    dist = np.sqrt((x2-x1)**2+(y2-y1)**2)
    return dist;

#Mouse parameters
#------------------------------------------------------------------------------
#Parameter 1 - time between clicks - defined as time between clicks is defined as the time elapsed between two instances of mouse release

#Labeling with "th" to indicate hourly paritions
t_downth = [[]*columns for i in range(rows)] #stores the time stamp when the mouse is clicked down
t_upth = [[]*columns for i in range(rows)] #stores the time stamp when the mouse is released
click_down_posth = [[]*columns for i in range(rows)] #stores the position in the array when the mouse is clicked down
click_up_posth = [[]*columns for i in range(rows)] #stores the position in the array when the mouse is released
rclick_down_posth = [[]*columns for i in range(rows)] #stores the position in the array when the right button is clicked down
rclick_up_posth = [[]*columns for i in range(rows)] #stores the position in the array when the right button mouse is released

for i in range(0,24):
    flag = 0 #variable to check if 1 follows 2 in click states
    for j in range(0,len(timeth[i])):
        if(click_stateth[i][j] == 1 or click_stateth[i][j] == '0001'):
            click_down_posth[i].append(j)
            t_downth[i].append(timeth[i][j])
            flag = 1
        elif((click_stateth[i][j] == 2 or click_stateth[i][j] == '0002') and flag==1):    
            click_up_posth[i].append(j)
            t_upth[i].append(timeth[i][j])
            flag = 0
        elif(click_stateth[i][j] == 4 or click_stateth[i][j] == '0004'):    
            rclick_down_posth[i].append(j)
        elif(click_stateth[i][j] == 8 or click_stateth[i][j] == '0008'):    
            rclick_up_posth[i].append(j)
              
for i in range(0,24):
    if(len(click_up_posth[i]) != len(click_down_posth[i])):
        print("Lengths of click up and click down don't match at ",i)
    if(len(click_up_posth[i]) < len(click_down_posth[i]) and i != 15): # this means it's most likely at the hour change
        click_up_posth[i].append(click_up_posth[i+1][0])
        t_upth[i].append(t_upth[i+1][0])
        print("Lengths now match at ",i)
        

#Using map() and lambda 
def listOfTuples(l1, l2): 
	return list(map(lambda x, y:(x,y), l1, l2)) 



#------------------------------------------------------------------------------
#Parameter 2 - click coordinates 

x_click_downth = [[]*columns for i in range(rows)]
y_click_downth = [[]*columns for i in range(rows)]
x_click_upth = [[]*columns for i in range(rows)]
y_click_upth = [[]*columns for i in range(rows)]
x_rclick_downth = [[]*columns for i in range(rows)]
y_rclick_downth = [[]*columns for i in range(rows)]
x_rclick_upth = [[]*columns for i in range(rows)]
y_rclick_upth = [[]*columns for i in range(rows)]
        
for i in range(0,24):
    for j in click_down_posth[i]:
        x_click_downth[i].append(float(xth[i][j]))
        y_click_downth[i].append(float(yth[i][j]))
    for j in click_up_posth[i]:
        x_click_upth[i].append(float(xth[i][j]))
        y_click_upth[i].append(float(yth[i][j]))           
    for j in rclick_down_posth[i]:
        x_rclick_downth[i].append(float(xth[i][j]))
        y_rclick_downth[i].append(float(yth[i][j]))
    for j in rclick_up_posth[i]:
        x_click_upth[i].append(float(xth[i][j]))
        y_click_upth[i].append(float(yth[i][j]))
                   
#------------------------------------------------------------------------------
#Parameter 3 - length of drag
#take all distances here    

drag_lengthth = [[]*columns for i in range(rows)]

for i in range(0,24):
    for j in range(0,len(click_down_posth[i])):
        drag_lengthth[i].append(distance(x_click_downth[i][j],y_click_downth[i][j],x_click_upth[i][j],y_click_upth[i][j]))
        
#------------------------------------------------------------------------------
#Parameter 4 - identifying drag and no.of clicks

t_dragth = [[]*columns for i in range(rows)]

click_down_pos_tbrmvdth = [[]*columns for i in range(rows)]
click_up_pos_tbrmvdth = [[]*columns for i in range(rows)]
t_up_tbrmvdth = [[]*columns for i in range(rows)]
t_down_tbrmvdth = [[]*columns for i in range(rows)]        

for i in range(0,24):
    for j in range(0,len(click_down_posth[i])):
        if(drag_lengthth[i][j]>100): #can adjust drag threshold here
            click_up_pos_tbrmvdth[i].append(click_up_posth[i][j])
            click_down_pos_tbrmvdth[i].append(click_down_posth[i][j])
            t_dragth[i].append(float(t_upth[i][j]-t_downth[i][j]))
            t_up_tbrmvdth[i].append(t_upth[i][j])
            t_down_tbrmvdth[i].append(t_downth[i][j])
            

for i in range(0,24):
    click_up_posth[i] = [ j for j in click_up_posth[i] if j not in click_up_pos_tbrmvdth[i]]
    click_down_posth[i] = [ j for j in click_down_posth[i] if j not in click_down_pos_tbrmvdth[i]]
    t_upth[i] = [j for j in t_upth[i] if j not in t_up_tbrmvdth[i]]
    t_downth[i] = [j for j in t_downth[i] if j not in t_down_tbrmvdth[i]]

#------------------------------------------------------------------------------
#Parameter 5 - time betweem clicks, number of double clicks, and time between double clicks

t_btw_clicksth = [[]*columns for i in range(rows)]
double_clicks = [[]*columns for i in range(rows)] #counts no.of double clicks in each hour
t_btw_clicks_tbrmd = [[]*columns for i in range(rows)] #remove double clicks
for i in range(0,24):
    for j in range(0,len(click_down_posth[i])-1):
        t_btw_clicksth[i].append(abs(t_downth[i][j+1]-t_downth[i][j]))
            
for i in range(0,24):
    for j in range(0,len(click_down_posth[i])-1,2):
        if(abs(t_downth[i][j+1]-t_downth[i][j])<0.65 or abs(t_downth[i][j+1]-t_downth[i][j])==0.65 ): #if the time between clicks is less than 0.65 second count as a double click
            double_clicks[i].append(t_downth[i][j])
            t_btw_clicks_tbrmd[i].append(abs(t_downth[i][j+1]-t_downth[i][j]))
        
for i in range(24):
    t_btw_clicksth[i] = [j for j in t_btw_clicksth[i] if j not in t_btw_clicks_tbrmd[i]]


#------------------------------------------------------------------------------
#Parameter 6 - click duration - defined as time between click up and release

click_durationth = []

for i in range(0,24):
    try:
        click_durationth.append(np.array(t_upth[i])-np.array(t_downth[i]))
    except:
        click_durationth.append([0]*columns)
        continue

#------------------------------------------------------------------------------
#Parameter 7 - no.of right clicks

#Check section on displaying data

#------------------------------------------------------------------------------
#Parameter 8 - scroll time/scroll length
#One notch to another is 120

scroll_sum = [[]*columns for i in range(rows)]
for i in range(24):
    for j in range(0,len(scroll_stateth[i])):
        scroll_sum[i].append(scroll_stateth[i][j])
    
    scroll_sum[i] = (1/120)*scroll_sum[i]


#------------------------------------------------------------------------------
#Parameter 9 - statistics for drag time

avg_t_dragth = []
std_t_dragth = []
avg_t_btw_clicksth = []
std_t_btw_clicksth = []
avg_click_durationth = []
std_click_durationth = []
for i in range(0,24):
    if(len(t_dragth[i]) == 0):
        avg_t_dragth.append(0)
        std_t_dragth.append(0)
    else:
        avg_t_dragth.append(np.mean(t_dragth[i]))
        std_t_dragth.append(np.std(t_dragth[i]))
    if(len(t_btw_clicksth[i]) ==0):
        avg_t_btw_clicksth.append(0)
        std_t_btw_clicksth.append(0)
    else:
        avg_t_btw_clicksth.append(np.mean(t_btw_clicksth[i]))
        std_t_btw_clicksth.append(np.std(t_btw_clicksth[i]))
    if(len(click_durationth[i]) == 0):
        avg_click_durationth.append(0)
        std_click_durationth.append(0)
    else:
        avg_click_durationth.append(np.mean(click_durationth[i]))
        std_click_durationth.append(np.std(click_durationth[i]))
        
x = range(0,24)

#------------------------------------------------------------------------------
#Displaying data

yc = []
yd = []
x = []
yrc = []
ydc = [] #double clicks
for i in range(0,24):
    yc.append(len(click_up_posth[i]))
    x.append(i)
    yd.append(len(t_dragth[i]))
    yrc.append(len(rclick_up_posth[i]))
    ydc.append(len(double_clicks[i]))

plt.scatter(x,yc)
plt.plot(x,yc)
plt.xlabel("Time of the day")
plt.ylabel("Average value in seconds")
plt.grid()
plt.xlim(-0.5,24)
plt.legend()
plt.show()

#------------------------------------------------------------------------------
#Writing data into a file

mouse_events_file = "Mouse events.txt"
tdrag_file = "Drag time.txt"
t_btw_clicks_file = "Time btw clicks.txt"
click_dur_file = "Click duration.txt"


# The 'a' flag tells Python to keep the file contents
# and append (add line) at the end of the file.
myfile1 = open(mouse_events_file, 'a')
# Add the line
myfile1.write('Left clicks. The file started logging at: '+ str(start_time)+'\n')
myfile1.write(str(x)+'\n')
myfile1.write(str(yc)+'\n')
myfile1.write(str(yd)+'\n')
myfile1.write(str(yrc)+'\n')
myfile1.write(str(ydc)+'\n')
# Close the file
myfile1.close()


myfile2 = open(tdrag_file, 'a')
# Add the line
myfile2.write('Drag times. The file started logging at: '+ str(start_time)+'\n')
myfile2.write(str(x)+'\n')
myfile2.write(str(t_dragth)+'\n')
# Close the file
myfile2.close()

myfile3 = open(t_btw_clicks_file, 'a')
# Add the line
myfile3.write('Time between clicks. The file started logging at: '+ str(start_time)+'\n')
myfile3.write(str(x)+'\n')
myfile3.write(str(t_btw_clicksth)+'\n')
# Close the file
myfile3.close()

myfile4 = open(click_dur_file, 'a')
# Add the line
myfile4.write('Click duration. The file started logging at: '+ str(start_time)+'\n')
myfile4.write(str(x)+'\n')
myfile4.write(str(click_durationth)+'\n')
# Close the file
myfile4.close()

