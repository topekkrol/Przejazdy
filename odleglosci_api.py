import requests
import time
from hasla import api_key_graphhopper, api_key_openweather
def get_distance(lat1,lon1,lat2='50.040150',lon2='21.979790'):
  time.sleep(5) # ustawione dla umożliwienia wykonania sprawdzenia API, darmowa wersja ma ograniczenia.
  url = "https://graphhopper.com/api/1/route"

  query = {
    "key": api_key_graphhopper
  }

  payload = {
    "points": [
      [
        lon1,
        lat1
      ],
      [
        lon2,
        lat2
      ]
    ],
    "point_hints": [
      "Lindenschmitstraße",
      "Thalkirchener Str."
    ],
    "snap_preventions": [
      "motorway",
      "ferry",
      "tunnel"
    ],
    "details": [
      "road_class",
      "surface"
    ],
    "vehicle": "car",
    "locale": "pl",
    "instructions": True,
    "calc_points": True,
    "points_encoded": False
  }

  headers = {"Content-Type": "application/json"}

  response = requests.post(url, json=payload, headers=headers, params=query)

  data = response.json()
  try:
    return (data['paths'][0]['distance']/1000)
  except:
    return 999 # jezeli nie ma odleglosci zwraca abstrakcyjne 999 jako maksymalan odleglosc

def get_location(miasto):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={miasto}&limit=5&appid={api_key_openweather}'

    ddane = requests.get(url)

    dane = ddane.json()
    if dane[0]['country'] == 'PL':
      lat = (dane[0]['lat'])
      lon = (dane[0]['lon'])
      dystans = get_distance(lat,lon)
      return dystans
    
