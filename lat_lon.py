import pandas as pd
import csv
import requests
import unicodedata
from hasla import api_key_openweather

from odleglosci_api import get_distance
def znalezenie_lokalizacji(miasto):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={miasto}&limit={api_key_openweather}'

    ddane = requests.get(url)

    dane = ddane.json()
    try:
        if dane[0]['country'] == 'PL':
          lat = (dane[0]['lat'])
          lon = (dane[0]['lon'])
          return lat,lon
    except:
        return dane

def dodanie_miejscowosci(miejscowosc):
    filename = 'latilon.csv'

    ddane = pd.read_csv(filename)

    dane = pd.DataFrame(ddane)


    if not miejscowosc in dane.values:
        miejscowosc_zapytanie = znalezenie_lokalizacji(miejscowosc)

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([miejscowosc,miejscowosc_zapytanie[0],miejscowosc_zapytanie[1]])

            lista_przejazdow = []
            for index, row in dane.iterrows():
                polaczenie = (row['miasto'],miejscowosc,int(get_distance(row['lat'],row['lon'],miejscowosc_zapytanie[0],miejscowosc_zapytanie[1])))
                lista_przejazdow.append(polaczenie)

            sorted_records = sorted(lista_przejazdow, key=lambda x: x[-1])

            posortowane = sorted_records[0:3]

            new_list = []

            for record in posortowane: # usuwanie polskich znakow
                new_record = tuple(unicodedata.normalize('NFKD', str(element)).encode('ASCII', 'ignore').decode('utf-8') if isinstance(element, str) else element for element in record)
                new_list.append(new_record)


            with open('Zeszyt1.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                if csvfile.tell() == 0:  # Check if the file is empty
                    writer.writerow(['Rozpoczecie', 'Zakonczenie', 'km'])  # Write headers
                for record in new_list:
                    writer.writerow(record)
