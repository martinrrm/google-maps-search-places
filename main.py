''' 
    El objetivo de este script es encontrar todos los oxxos en las diferentes ubicaciones 
    El primer aproach fue reutilizar un codigo de yelp, pero las llamadas regresaban pocas 
    ubicaciones y se descarto esta posibilidad.
'''

import pandas as pd
from googleplaces import GooglePlaces, types, lang
from decimal import *
import requests
import json
import pprint
from geopy.distance import geodesic
# https://pypi.org/project/geopy/
import time

APIKEY = 'AIzaSyAF8DUYCN0jZbdhWHdax0J82K42UleiSx0'
i = 0
s = pd.DataFrame()

'''
    Codigo para hacer una busqueda de manera mas facil, se esta usando la libreria de googleplaces
    https://github.com/slimkrazy/python-google-places#installation
'''
# google_places = GooglePlaces(YOUR_API_KEY)
# query_result = google_places.nearby_search(
#         keyword='Crematorio',
#         radius=8000, lat_lng={'lat': Decimal('19.655726'), 'lng': Decimal('-99.208605')})

# print(query_result)


'''
    Aun no esta automatizado del todo, hay variables que se tienen que cambiar manualmente:
    Main:
        getPoints(), introducir las coordenadas del punto central de la ubicacion
        findPlaces(), cambiar el nombre del file al que se va a guardar y si es necesario cambiar el radio.
    
    getPoints():
        Cambiar la division de 'divisions' para que concuerde, se introduce el radio de la division, preferentemente has ceil
        manualmente y si la ubicacion es muy grande cambia el divisor y las coords variation
'''

cities = {
    'Jalpan de Serra': {
        'location': (21.219232, -99.474387),
        'radius': 2000
    },
    'Landa de Matamoros': {
        'location': (21.183289, -99.319800),
        'radius': 1300
    },
    'San Juan del Rio': {
        'location': (20.396467, -99.983945),
        'radius': 6300
    },
    'Huimilpan': {
        'location': (20.374581, -100.276412),
        'radius': 1100
    },
    'Corregidora': {
        'location': (20.533836, -100.446358),
        'radius': 3000
    },
    'El Marques': {
        'location': (20.738440, -100.268843),
        'radius': 27000
    },
    'Queretaro': {
        'location': (20.609082, -100.414159),
        'radius': 9000
    }
}

def getPoints(coords=(20.609082, -100.414159), radius=9000):
    ''' Aprox 00.009032 es 1km 1.0000214983816433 '''
    ''' Aprox 0.009642 es 1km 1.0000771022236825 '''
    lat_variation = 0.009032
    lng_variation = 0.009642
    ''' La cantidad de divisiones son los metros de las variaciones 1km = 1000 divisiones '''
    divisions = radius/1000
    coordinates = []
    coords = (coords[0] + lat_variation*int(divisions), coords[1]-lng_variation*int(divisions))
    #coordinates.append(coords)
    for i in range(0,int(divisions*2)):
        for j in range(0,int(divisions*2)):
            aux = (coords[0]-(lat_variation*i), coords[1]+(lng_variation*j))
            coordinates.append(aux)
            #print(len(coordinates))

    return coordinates

def findPlaces(loc=("19.480757", "-99.050909"), radius=1100, pagetoken = None, file="data"):
    global i
    global s

    lat, lng = loc
    name = "Oxxo"
    keyword = "Oxxo"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&keyword={keyword}&key={APIKEY}{pagetoken}".format(lat = lat, lng = lng, radius = radius, type = type, keyword = keyword,APIKEY = APIKEY, pagetoken = "&pagetoken=" + pagetoken if pagetoken else "")
    response = requests.get(url)
    res = json.loads(response.text)
    print(res)
    print("here results ---->>> ", len(res["results"]))

    for result in res["results"]:
        info = "    ".join(map(str,[result["name"],result["vicinity"],result["geometry"]["location"]["lat"],result["geometry"]["location"]["lng"],result.get("rating",0)]))
        titles = ["Nombre","Direccion","Latitud","Longitud","Rating"]
        data = info.split("    ")
        zipObj = zip(titles, data)
        data = dict(zipObj)
        if(i == 0):
            s = pd.DataFrame(data=data, index=[0])
            i = 1
        else:
            s = s.append(data, ignore_index=[True])

        s.to_csv(file+".csv")
        print(len(s))

    pagetoken = res.get("next_page_token",None)

    print("here -->> ", pagetoken)
    print("\n")

    return pagetoken

pagetoken = None
if __name__ == "__main__":
    print("--- SI EL RADIO A EXPLORAR ES MAYOR A 9000M ES RECOMENDABLE CAMBIAR 'divisions', la variacion de lat y lng y radio de findPlaces ---")
    for c in cities:
        print(c)
        print(cities[c]['location'])
        data = getPoints(cities[c]['location'], radius=cities[c]['radius'])
        ############################################
        if(cities[c]['radius'] > 9000):
            print("--- SI EL RADIO A EXPLORAR ES MAYOR A 9000M ES RECOMENDABLE CAMBIAR 'divisions', la variacion de lat y lng y radio de findPlaces ---")
            break
        ############################################
        counter = 0
        for i in data:
            '''cities['Queretaro']['radius']'''
            print(i)
            print(counter)
            counter = counter + 1
            pagetoken = findPlaces(loc=i, radius=1100, pagetoken=pagetoken, file=c)
            time.sleep(1)

            if not pagetoken:
                pass
