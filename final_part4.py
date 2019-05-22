# -*- coding: utf-8 -*-
"""
Created on Wed May 22 05:13:50 2019

@author: salam
"""
import numpy as np
import xlrd
import matplotlib.pyplot as plt

n = 81

distancematrix = xlrd.open_workbook("distancematrix.xls")
coordinates = xlrd.open_workbook("Coordinates.xlsx")  

coord_sheet = coordinates.sheet_by_index(0)   
dist_sheet = distancematrix.sheet_by_index(0)

# create the distance array====================================================

distancelist = []
zero_cell = np.arange(0,6561,81)  

for row in range (n):
    for col in range (n):
        row_value = dist_sheet.row(row+3) 
        distancelist.append(row_value[col+2].value) 
    distancelist[zero_cell[row] + row] = 0         
                                                    
distance = np.reshape(distancelist,(81,81)) 

##==============================================================================

# create coordinates array =====================================================

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

# Calculating the shortest route based on genetic algorithm ====================

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
    
def create_population(n): # create and sort population
    
    population = []
    for i in range(n):
        pops = get_route(n)

        population.append(pops)
    population = np.array(population)
    sorted_population = sort_population(population)

    return sorted_population

def sort_population(population): # sort according to performance (fitness)

    performance = get_fitness(population)
    sort = np.argsort(performance)

    return population[sort]

def get_fitness(population):  # get the performance of each elements in population

    fitness = []
    for route in population:
        fitness.append(get_route_length(route))

    return fitness

def draw_route(path):  

    for i,j in zip(path[:-1],path[1:]):
        plt.plot([x[i],x[j]],[y[i],y[j]],'-o')
    plt.show()
        
def crossover(route1,route2):

    route1 = route1[:-1]
    route2 = route2[:-1] 
    subs_num = []
    
    rand_int = np.random.randint(0,n)
    newroute = np.hstack((route1[:rand_int], route2[rand_int:])) 
    unique, counts = np.unique(newroute, return_counts=True)
    zip_ = zip(unique,counts)
    dictionary = dict(zip_)
    
    for i in dictionary:    
        
        if dictionary[i] == 2:
            subs_num.append(i) 

    missing = (set(route1)-set(newroute))
    missing = list(missing)

    for i,j in zip(subs_num,missing):  
        if np.random.rand() > 0.5:
            index = np.where(newroute == i)[0][0] 
        else:
            index = np.where(newroute == i)[0][1]            
        newroute[index] = j 
        
    if np.random.rand() > 0.1:
        m,l = np.random.randint(0,n,2)
        newroute[m], newroute[l] = newroute[l], newroute[m]
        
    newroute = np.append(newroute, newroute[0]) 
    
    for i in range (len(newroute)):
        
        if newroute[0] == 5:
            return newroute
        else:
            if newroute[i] == 5:
                temp = newroute[0]
                newroute[0] = newroute[i]
                newroute[i] = temp
                newroute[81] = newroute[0]  
                
    return newroute


def new_gen(population, m): # create new generation from the crossover
    
    population = population[:m]
    newpopulation = []
    for i in population:
        for j in population:
            newpopulation.append(crossover(i, j))
    newpopulation = np.array(newpopulation)
    newpopulation = sort_population(newpopulation)

    return newpopulation

##==============================================================================

population = create_population(81)     
performance1 = []

for i in range(450):
    
    draw_route(population[0])
    best_route = get_route_length(population[0])
    performance1.append(best_route)  
    plt.plot(performance1,'.-')
    plt.show() 
    population = new_gen(population,15) 
    
    print('Iteration:',i)
    print('Calculated total distance:',get_route_length(population[0]))
    
print('The shortest distance consists of following routes:')
print(population[0])