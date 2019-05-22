# -*- coding: utf-8 -*-
"""
Created on Wed May 22 04:43:21 2019

@author: salam
"""

import numpy as np
import xlrd

n = 81
distancematrix = xlrd.open_workbook("distancematrix.xls")
coordinates = xlrd.open_workbook("Coordinates.xlsx")  

coord_sheet = coordinates.sheet_by_index(0)   
dist_sheet = distancematrix.sheet_by_index(0)

# create the distance array  ===================================================

distancelist = []
zero_cell = np.arange(0,6561,81)  

for row in range (n):
    for col in range (n):
        row_value = dist_sheet.row(row+3) 
        distancelist.append(row_value[col+2].value)
    distancelist[zero_cell[row] + row] = 0         
                                                    
distance = np.reshape(distancelist,(81,81)) 

##==============================================================================

# create coordinates array  ====================================================

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

print(distance)
print(coordinates)