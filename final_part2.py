# -*- coding: utf-8 -*-
"""
Created on Wed May 22 04:52:21 2019

@author: salam
"""
import numpy as np
import matplotlib.pyplot as plt
import xlrd 

n = 81

distancematrix = xlrd.open_workbook("distancematrix.xls")
coordinates = xlrd.open_workbook("Coordinates.xlsx")  

coord_sheet = coordinates.sheet_by_index(0)   
dist_sheet = distancematrix.sheet_by_index(0)

# create distance array=========================================================

distancelist = []
zero_cell = np.arange(0,6561,81)

for row in range (n):
    for col in range (n):
        row_value = dist_sheet.row(row+3) 
        distancelist.append(row_value[col+2].value) 
    distancelist[zero_cell[row] + row] = 0          
                                                    
distance = np.reshape(distancelist,(81,81)) 

##==============================================================================

# create coordinates array======================================================

cities = []
vertical  = []
horizontal  = []
coordinates = np.zeros((n,2)) 

for row in range (n) : 
    get_values = coord_sheet.row(row+1) 
    
    cities.append(get_values[1].value)
    vertical.append(get_values[2].value)
    horizontal.append(get_values[3].value)
    
    coordinates[row,0] = vertical[row]
    coordinates[row,1] = horizontal[row] 
x,y = coordinates[:n,1],coordinates[:n,0]

##==============================================================================

# creat random route from ankara to the other cities and return to ankara ========

def get_route(n):
    
    route = np.arange(n)
    np.random.shuffle(route)
    randroute = np.append(route,route[0])
    
    for i in range (len(randroute)):
        if randroute[0] == 5:
            return randroute
        else:
            if randroute [i] == 5:
                temp = randroute[0]
                randroute[0] = randroute[i]
                randroute[i] = temp
                randroute[81] = randroute[0]                
    return randroute

def get_route_length(route):    
    
    total_length = 0    
    for a,b in zip(route[:-1], route[1:]):
        length = distance[a,b]
        total_length = total_length + length

    return total_length

def draw_route(path):  

    for i,j in zip(path[:-1],path[1:]):
        plt.plot([x[i],x[j]],[y[i],y[j]],'-o')
    plt.show()

randroute = get_route(n)
randroute_length = get_route_length(randroute)
route_line = draw_route(randroute)

##==============================================================================

print(randroute)
print('Length of the random route:',randroute_length)