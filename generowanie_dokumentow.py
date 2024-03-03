from datetime import datetime
import random 
import string
import pandas as pd

def miejscowosc_dla_dnia():

    tydzien = {
        1: ['Jaroslaw', 'Przeworsk', 'Lubaczow', 'Tomaszow', 'Sanok', 'Brzozow','Stalowa Wola','Nisko','Rudnik nad Sanem'], # gotowa baza testowa
        2: ['Lezajsk', 'Bilgoraj', 'Janow Lubelski', 'Strzyzow', 'Jaslo', 'Stalowa Wola', 'Kolbuszowa', 'Mielec',
            'Debica', 'Tarnobrzeg'],  # gotowa baza testowa
        3: ['Bilgoraj', 'Zamosc', 'Stalowa Wola', 'Tarnobrzeg','Janow Lubelski'], # gotowa baza testowa
        4: ["Staszow","Debica","Gorlice","Jaslo","Krosno","Strzyzow"], # gotowa baza testowa
        5: ['Bilgoraj', 'Zamosc', 'Stalowa Wola', 'Mielec', 'Lezajsk'],
        }  

    date_ob= datetime.now().date()

    day_num = date_ob.weekday()
    if day_num > 5 :
        day_num = 1

    return tydzien[day_num]

def generowanie_wz(miejscowosc=miejscowosc_dla_dnia()):

    wuzety = []
    for nowy_dokument in range(random.randint(5,10)):
        nazwa_kontrahenta = random.choice(string.ascii_letters).upper()
        miejscowosc_dostawy = random.choice(miejscowosc)
        ilosc_dostarczana = random.randint(1,10)
        waga_dostarczana = random.randint(400,1200)*ilosc_dostarczana
        wuzety.append([nazwa_kontrahenta,miejscowosc_dostawy,ilosc_dostarczana,waga_dostarczana])
    
    df_z_danymi = pd.DataFrame(wuzety,columns=['nazwa_kontrahenta','miejscowosc_dostawy',  'ilosc_dostarczana',    'waga'])

    return df_z_danymi
