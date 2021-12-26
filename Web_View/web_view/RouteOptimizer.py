# Library Imports
import numpy as np
import math as m
from random import shuffle
from time import sleep
import sys
import os
import requests
from requests.structures import CaseInsensitiveDict
import openrouteservice as ors
import folium

# Variable Initialization
file_to_charge = {
                  'Delhi' : 'Houses(Delhi).json',
                  'Chennai' : 'Houses(Chennai).json',
                  'Kolkata' : 'Houses(Kolkata).json',
                  'Mumbai' : 'Houses(Mumbai).json',
                  'Dehradun' : 'Houses(Dehradun).json',
                  'Kanpur' : 'Houses(Kanpur).json'
                 }
with open('./storage/Location_For_Show_Map.txt', 'r') as loc:
    locationName = loc.read()
Number_Of_Houses = {
                    'Delhi' : 25,
                    'Chennai' : 25,
                    'Kolkata' : 30,
                    'Mumbai' : 31,
                    'Dehradun' : 31,
                    'Kanpur' : 31
                    }
totalHouses = Number_Of_Houses[locationName]
houses = []
houseRank = {
            1 : [],
            2 : [],
            3 : []
            }
housesDist = dict()
H_Dict = dict()

# GA variables
population, fitness = [],[]
popSize = 500
generationNumber = 0

recordDistance, currentRecord = m.inf,m.inf
bestEver, currentBest = [],[]
mutationRate = 0.01


#Genetic Algorithm
def calculateFitness():
    global houses, popSize, population, recordDistance, bestEver, currentRecord, currentBest, fitness
    
    currentRecord = m.inf
    for i in range(popSize):
        d = calcDistance(population[i])
        if d < recordDistance:
            recordDistance = d
            bestEver = population[i]
        if d < currentRecord:
            currentRecord = d
            currentBest = population[i]
        fitness.append(1 / (m.pow(d, 8) + 1))

def normalizeFitness():
    _sum = sum(fitness)
    for i in range(len(fitness)):
        fitness[i] = fitness[i] / _sum

def nextGeneration():
    global population, mutationRate, generationNumber
    
    newPopulation = []
    orderA, orderB, order = [], [], []
    for i in range(len(population)):
        orderA = pickOne(population , fitness)
        orderB = pickOne(population , fitness)
        order = crossOver(orderA, orderB)
        mutate(order)
        newPopulation.append(order)
    population = list(newPopulation)
    del(newPopulation)
    generationNumber += 1

def pickOne(lst, prob):
    index = 0
    r = np.random.rand(1)[0]
    while r>0:
        r = r - prob[index]
        index += 1
    index -= 1
    return list(lst[index])

def crossOver(orderA, orderB):
    start = np.random.randint(len(orderA)-1)
    end = np.random.randint(start+1, len(orderA))
    neworder = orderA[start:end]
    for i in range(len(orderB)):
        house = orderB[i]
        if house not in neworder:
            neworder.append(house)
    return neworder

def mutate(order):
    global mutationRate
    
    for i in range(totalHouses):
        if (np.random.rand(1)[0]) < mutationRate:
            indexA = np.random.randint(len(order))
            indexB = (indexA + 1) % totalHouses
            swap(order, indexA, indexB)


# Program Data Setup
def setup():
    global totalHouses, houses, housesDist, houseRank, H_Dict, population, popSize, mutationRate
    
    order = []
    
    getHouseFromDataBase()
    
    for i in range(totalHouses):
        houses.append([H_Dict['house'][i]['latitude'], H_Dict['house'][i]['longitude']])
        houses[i].append(i+1)
        order.append(i)

    House_Rank()
    
    for i in range(popSize):
        population.append(list(order))
        shuffle(population[i])
    
    DistanceMatrix()

def draw():
    global generationNumber 
    
    for i in range(popSize):
        genSort_Rank(i)
    
    calculateFitness()
    normalizeFitness()
    nextGeneration()
    
    print(f'Generation: {generationNumber}')

def House_Rank():
    global H_Dict, houseRank

    morning, afternoon, evening = [], [], []
    giventime = ''

    for i in range(totalHouses):
        giventime = H_Dict['house'][i]['time']

        if giventime == "9am to 12noon":
            morning.append(i)
        elif giventime == "12noon to 3pm":
            afternoon.append(i)
        else:
            evening.append(i)
    
    houseRank[1].extend(morning)
    houseRank[2].extend(afternoon)
    houseRank[3].extend(evening)

def swap(a, i ,j):
    a[i], a[j] = a[j], a[i]

def calcDistance(order):
    global housesDist
    
    _sum = 0
    for i in range(len(order)-1):
        houseAindex = order[i]
        houseBindex = order[i+1]
        d = housesDist['sources_to_targets'][houseAindex][houseBindex]['distance']
        _sum += d
    return _sum

def genSort_Rank(orderNumber):
    def getKey(val):
        for key, value in houseRank.items():
            if val in value:
                return int(key)
        return 4
    
    for i in range(1,totalHouses):
        houseNumber,pos = population[orderNumber][i],i
        
        while (pos>0 and getKey(population[orderNumber][pos-1]) > getKey(houseNumber)):
            population[orderNumber][pos] = population[orderNumber][pos-1]
            pos-= 1
        population[orderNumber][pos] = houseNumber

def getHouseFromDataBase():
    global file_to_charge, locationName, H_Dict
    
    url = 'https://raw.githubusercontent.com/AdrijeGuha/Travelling-Salesman-Problem/master/DataSet/'+file_to_charge[locationName]
    
    resp = requests.get(url)
    
    # Error checking and displaying the same
    statusCode = resp.status_code
    codes ={
            204 : 'Error Code 204 - No Content!',
            301 : 'Error Code 301 - Moved Permanently!',
            400 : 'Error Code 400 - Bad Request!',
            401 : 'Error Code 401 - Unauthorized!',
            403 : 'Error Code 403 - Forbidden!',
            404 : 'Error Code 404 - Not Found!',
            500 : 'Error Code 500 - Internal Server Error!'
           }
    if statusCode != 200:
        if statusCode in codes.keys():
             sys.exit(codes[statusCode]+' in getHouseFromDataBase()')
        else:
             sys.exit(f'Error Code {statusCode} in getHouseFromDataBase()')
    
    H_Dict = resp.json()


def DistanceMatrix():
    global totalHouses, houses, housesDist
    
    url = "https://api.geoapify.com/v1/routematrix?apiKey=6c8e353bd11c4807961ed51e8772fb43"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    
    sources, LongLat = '[', ''
    for i in range(totalHouses):
        LongLat='{"location":['+str(houses[i][1])+','+str(houses[i][0])+']}'
        if i < totalHouses-1:
            LongLat +=','
        sources += LongLat
    sources += ']'

    targets = str(sources)
    data = '{"mode":"walk","sources":'+sources+',"targets":'+targets+'}'
    
    resp = requests.post(url, headers=headers, data=data)

    # Error checkinh and displaying the same
    statusCode = resp.status_code
    codes ={
            204 : 'Error Code 204 - No Content!',
            301 : 'Error Code 301 - Moved Permanently!',
            400 : 'Error Code 400 - Bad Request!',
            401 : 'Error Code 401 - Unauthorized!',
            403 : 'Error Code 403 - Forbidden!',
            404 : 'Error Code 404 - Not Found!',
            500 : 'Error Code 500 - Internal Server Error!'
           }
    if statusCode != 200:
        if statusCode in codes.keys():
             sys.exit(codes[statusCode]+' in DistanceMatrix()')
        else:
             sys.exit(f'Error Code {statusCode} in DistanceMatrix()')
    
    housesDist = resp.json()

def mapMaking():
    global houses, bestEver, file_to_charge, locationName, xLim, yLim
    
    map_= folium.Map(location=[houses[bestEver[0]][0],houses[bestEver[0]][1]], zoom_start=18)

    folium.raster_layers.TileLayer('Open Street Map').add_to(map_)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(map_)
    
    client = ors.Client(key='5b3ce3597851110001cf6248056e10b584294591af7668d77907c079')

    for i in range(len(bestEver)-1):
        c = [[houses[bestEver[i]][1],houses[bestEver[i]][0]],[houses[bestEver[i+1]][1],houses[bestEver[i+1]][0]]]
        mapping = client.directions(coordinates=c, profile='driving-car', format='geojson')
        folium.GeoJson(mapping, name=f'House {houses[bestEver[i]][2]}').add_to(map_)
        sleep(2)
    
    for i in range(len(bestEver)):
        folium.Marker([houses[bestEver[i]][0], houses[bestEver[i]][1]], popup=f'House {houses[bestEver[i]][2]}', icon=folium.Icon(color='red'),tooltip='click').add_to(map_)

    folium.LayerControl(position='topright',collapsed=True).add_to(map_)
    
    map_.save('./templates/House_Route_On_Map.html')

def main():
    loopBreaker = 0
    extension = 100
    flg = True
    
    setup()
    
    while flg:
        draw()    
        if generationNumber >= extension:
            if loopBreaker == recordDistance:
                with open('./storage/shortest_path_sequence.txt','w') as file:
                    file.write(f"Shortest visiting sequence of houses is {[i+1 for i in bestEver]}, with total diatnace to cover {recordDistance} units.")

                print(f"Shortest visiting sequence of houses is {[i+1 for i in bestEver]}, with total diatnace to cover {recordDistance} units.")
                flg = False
            else:
                loopBreaker = recordDistance
                extension += 100
        if flg:
            sleep(0.05)
            os.system('cls')
    
    print("\n\aGenerating the map......Please Wait!")
    mapMaking()
    print('\aProgram Completed successfully.')
