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
filename = "Feb1_2.txt"#str(input("Enter file name : "))
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

#making these arrays into np.arrays is necessary for animating
#x = np.array(x)
#y = np.array(y)

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
    print("We consider only data on the day which the file started logging")
'''
for i in range(0,24):
    for j in range(0,len(timeth[i])):
       if(
'''       
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
    for j in range(0,len(timeth[i])):
        if(click_stateth[i][j] == 1 or click_stateth[i][j] == '0001'):
            click_down_posth[i].append(j)
            t_downth[i].append(j)
        elif(click_stateth[i][j] == 2 or click_stateth[i][j] == '0002'):    
            click_up_posth[i].append(j)
            t_upth[i].append(j)
        elif(click_stateth[i][j] == 4 or click_stateth[i][j] == '0004'):    
            rclick_down_posth[i].append(j)
        elif(click_stateth[i][j] == 8 or click_stateth[i][j] == '0008'):    
            rclick_up_posth[i].append(j)
              
for i in range(0,24):
    if(len(click_up_posth[i]) != len(click_down_posth[i])):
        print("Lengths of click up and click down don't match at ",i)

#------------------------------------------------------------------------------
#Parameter 2 - click coordinates and no.of times clicked

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
#print(distance(x_click_downth[23][10],y_click_downth[23][10],x_click_upth[23][10],y_click_upth[23][10]))                   
#------------------------------------------------------------------------------
#Parameter 3 - length of drag
#take all distances here    

drag_lengthth = [[]*columns for i in range(rows)]

for i in range(0,24):
    for j in range(0,len(click_down_posth[i])):
        drag_lengthth[i].append(distance(x_click_downth[i][j],y_click_downth[i][j],x_click_upth[i][j],y_click_upth[i][j]))
    #print(len(drag_lengthth[i]),len(click_))
        #print(distance(x_click_downth[i][j],y_click_downth[i][j],x_click_upth[i][j],y_click_upth[i][j]))   
#print(drag_lengthth[23][200])
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
            #print("hello")
    #print(len(t_dragth[i]))    
#Decide how to print no.of drag events

for i in range(0,24):
    click_up_posth[i] = list(set(click_up_posth[i])-set(click_up_pos_tbrmvdth[i]))
    click_down_posth[i] = list(set(click_down_posth[i])-set(click_down_pos_tbrmvdth[i]))
    t_upth[i] = list(set(t_upth[i])-set(t_up_tbrmvdth[i]))
    t_downth[i] = list(set(t_downth[i])-set(t_down_tbrmvdth[i]))

#Decide how to print no.of clicks

#------------------------------------------------------------------------------
#Parameter 5 - time betweem clicks

t_btw_clicksth = [[]*columns for i in range(rows)]

for i in range(0,24):
    for j in range(0,len(click_down_posth[i])-1):
        t_btw_clicksth[i].append(abs(t_downth[i][j+1]-t_downth[i][j]))

        
#Decide how to print time between clicks        
        
#------------------------------------------------------------------------------
#Parameter 6 - click duration - defined as time between click up and release

click_durationth = [[]*columns for i in range(rows)]

for i in range(0,24):
    try:
        click_durationth[i] = np.array(t_upth[i])-np.array(t_downth[i])
    except:
        click_durationth[i] = 0
        continue
#------------------------------------------------------------------------------
#Parameter 7 - no.of right clicks

#Decide how to print rclick_up_posth

#------------------------------------------------------------------------------
#Parameter 8 - scroll time/scroll length
#One notch to another is 120
'''
scroll_sum = [[0]*24]
for i in range(0,24):
    for j in range(0,len(scroll_stateth[i])):
        scroll_sum[i] = scroll_sum[i] + int(scroll_stateth[i][j])  
    
    #scroll_sum[i] = (1/120)*scroll_sum[i]
'''
#------------------------------------------------------------------------------
#Displaying data

yc = []
yd = []
x = []
yrc = []

for i in range(0,24):
    yc.append(len(click_up_posth[i]))
    x.append(i)
    yd.append(len(t_dragth[i]))
    yrc.append(len(rclick_up_posth[i]))
plt.scatter(x,yc,c='r',marker='^',s = 70)
plt.plot(x,yc,c='r',label="Left click")
plt.scatter(x,yd,c='g',marker='^',s=70)
plt.plot(x,yd,c='g',label="Drag")
plt.scatter(x,yrc,c='y',marker='^',s=70)
plt.plot(x,yrc,c='y',label="Right click")
#plt.plot([start_time.hour,start_time.hour],[0,max(yc)],'k-')
plt.axvline(x=start_time.hour,color='k',linestyle='-')
plt.xlim(-0.5,24)
plt.xlabel("Time of the day")
plt.ylabel("No.of events")
plt.legend(loc="best")
plt.title("Hourly mouse events")
plt.grid()
plt.show()    

