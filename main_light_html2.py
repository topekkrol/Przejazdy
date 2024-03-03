import time
import random
import pandas as pd
from datetime import datetime, date,timedelta
#import matplotlib.pyplot as plt
import csv
import os
#from __main__ import app
from Kalkulator_Raben import kalkulator_spedycja
from DoPSGl import PolaczenieBazy
import operator
from flota import Samochod
from WyszukiwarkaMakaronowa import wyszukanie
from flask import render_template, request
import traceback
from bla2 import sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym, compare_dictionaries


def rozwiazywania_rownania_a(b,plik):
    # przypisywanie wartosci do list. Podczas wyliczania odleglosci istnieje zmienna ktora moze być określona dopiero pod koniec ostatniej pętli.
    # Funckja rozwiazuje problem przypisujac konkretna wartość i usuwając element z list
    a =max(b)
    for m in plik:
        for elementy in plik[m]:
            try:
                wartosc = elementy[0] + a
                plik[m].insert(1,wartosc) # dodawanie wartosci na drugim miejscu listy, nie mozemy dodac na 0 poniewaz przechowywana tam jest wartosc bezposredniego polaczenie, dodawnie na koncu zakloca logike rozwiazywania nastepnych list.
                plik[m].remove(elementy) # usuwanie z listy

            except:
                continue
    return [], plik

def sprawdzanie_czy_z_tylu_sie_wszystko_zgadza(polaczenie,miejscowosc,koszty_wewnetrzne):
    # start : Przypisywanie poprzednim miejscowosciom literki zmiennej, jeżeli warunek wczesniej trafił do 'else' i wykonal operacje zamiany list na dane
    if [polaczenie[0]['km'], 'a'] not in koszty_wewnetrzne[miejscowosc]:
        wejsciowe = koszty_wewnetrzne[miejscowosc]
        wejsciowe.append([polaczenie[0]['km'], 'a'])
        koszty_wewnetrzne[miejscowosc] = wejsciowe
    return koszty_wewnetrzne

def koszty_odleglosci(start, koszty,koszt_km):
    a = []
    for miejscowosci in koszty:
        poleczenie1 = (wyszukanie(start,miejscowosci,glebokosc=1))
        if len(poleczenie1) >= 1:
            wejsciowe = koszty[miejscowosci]
            wejsciowe.append([poleczenie1[0]['km'] ,'a'])
            koszty[miejscowosci] = wejsciowe

            for miejscowosci1 in koszty:

                if miejscowosci == miejscowosci1:
                    continue
                else:
                    poleczenie2 = wyszukanie(miejscowosci,miejscowosci1,glebokosc=1)
                    if len(poleczenie2) >= 1:
                        try:
                            wejsciowe = koszty[miejscowosci1]
                            wejsciowe.append([poleczenie2[0]['km'],'a'])
                        except:
                            wejsciowe = [[poleczenie2[0]['km'],'a']]

                        koszty[miejscowosci1] = wejsciowe

                        for miejscowosci2 in koszty:
                            if miejscowosci1 == miejscowosci2 or miejscowosci2 == miejscowosci:
                                continue
                            else:
                                poleczenie3 = wyszukanie(miejscowosci1,miejscowosci2,glebokosc=1)
                                if len(poleczenie3) >= 1:
                                    try:
                                        wejsciowe = koszty[miejscowosci2]
                                        wejsciowe.append([poleczenie3[0]['km'],'a'])
                                    except:
                                        wejsciowe = [[poleczenie3[0]['km'],'a']]

                                    koszty[miejscowosci2] = wejsciowe
                                    koszty = sprawdzanie_czy_z_tylu_sie_wszystko_zgadza(poleczenie2,miejscowosci1,koszty)
                                    koszty = sprawdzanie_czy_z_tylu_sie_wszystko_zgadza(poleczenie1,miejscowosci,koszty)
                                    a.append(koszty[miejscowosci2][0]/3)
                                    a, koszty = rozwiazywania_rownania_a(a,koszty)

                                else:
                                    a.append(koszty[miejscowosci1][0]/2)
                                    a, koszty  = rozwiazywania_rownania_a(a,koszty)

                    else:
                        a.append(koszty[miejscowosci][0])
                        a, koszty  = rozwiazywania_rownania_a(a,koszty)


    # koniec etapu szukania połaczeń pierwszego stopnia ( Rzeszow - Lezajsk - Bilgoraj - Zamosc ) i poczatek szukania etapu drugiego stopnia ( Bilgoraj - Zamosc )

        poleczenie4 = wyszukanie(start,miejscowosci,glebokosc=2)
        if len(poleczenie4) >= 1:
            try:
                wejsciowe = koszty[miejscowosci]
                wejsciowe.append([poleczenie4[0]['km'],'a'])
            except:
                wejsciowe = [[poleczenie4[0]['km'],'a']]

            koszty[miejscowosci] = wejsciowe

            for miejscowosci3 in koszty:
                if miejscowosci3 == miejscowosci:
                    continue

                poleczenie5 = wyszukanie(miejscowosci,miejscowosci3,glebokosc=1)
                if len(poleczenie5) >= 1:
                    try:
                        wejsciowe = koszty[miejscowosci3]
                        wejsciowe.append([poleczenie5[0]['km'],'b'])
                    except:
                        wejsciowe = [[poleczenie5[0]['km'],'b']]

                    koszty[miejscowosci3] = wejsciowe

                    a.append(koszty[miejscowosci3][0]/2)
                    a, koszty = rozwiazywania_rownania_a(a,koszty)

                else:
                    a.append(koszty[miejscowosci][0])
                    a, koszty = rozwiazywania_rownania_a(a,koszty)

        # koniec etapu szukania połaczeń drugiego stopnia ( Rzeszow - Bilgoraj - Zamosc ) i poczatek szukania etapu trzeciego stopnia ( Rzeszow - Zamosc )
        poleczenie6 = wyszukanie(start,miejscowosci,glebokosc=3)
        if len(poleczenie6) >= 1:
            try:
                wejsciowe = koszty[miejscowosci]
                wejsciowe.append([poleczenie6[0]['km'],'a'])

            except:
                wejsciowe = [poleczenie6[0]['km'],'a']
            koszty[miejscowosci] = wejsciowe
            a.append(koszty[miejscowosci][0])
            a, koszty  =rozwiazywania_rownania_a(a,koszty)

    koszty_dostawy={}
    for odleglosci in koszty:
        koszty_dostawy[odleglosci] = {"koszt_BOZ" : min(koszty[odleglosci])*koszt_km,  "km" : koszty[odleglosci][0],"spedycja":0} # nie bierzemy pierwszej wartości ponieważ to odległość bezpośredniego połączenia punktu z Rzeszowem, ten warunek odzwierciedla sie w min(koszty[odleglosci][1:])*koszt_km, nastapila zmiana.

    return koszty_dostawy
    # koniec obliczania kosztow dostawy step1

def koszty_spedycji(data_frame,wewnetrzne_koszty_dostawy):
    for s in range (len(data_frame)): # s jako zmienna bo x jest zbyt powszechne
        miejsce = (data_frame.loc[s]['miejscowosc_dostawy'])
        waga = int(data_frame.loc[s]['waga'])
        palety = int(data_frame.loc[s]['ilosc_dostarczana'])
        km = wewnetrzne_koszty_dostawy[miejsce]['km']
        try:
            spedycja = wewnetrzne_koszty_dostawy[miejsce]['spedycja']
            spedycja += kalkulator_spedycja(km,waga,palety)[0]
            wewnetrzne_koszty_dostawy[miejsce]['spedycja'] = spedycja
        except:

            wewnetrzne_koszty_dostawy[miejsce]['spedycja'] = kalkulator_spedycja(km,waga,palety)[0]

    return wewnetrzne_koszty_dostawy

def wlasny_transport_vs_spedycja(wewnetrzne_dostawy_koszty,wewnetrzne_koszty):

    w_dostawa_boz = {}  # musimy stworzyć dict ponieważ dane wchodzące do koszty_odleglosci są w takim formacie
    w_dostawa_spedycja = []  # dodajemy do listy ponieważ oprócz informacji o miejscowsci nie przechowujemy innych informacji
    
    for _ in wewnetrzne_dostawy_koszty:
        if wewnetrzne_dostawy_koszty[_]['spedycja'] > wewnetrzne_dostawy_koszty[_]['koszt_BOZ']:
            w_dostawa_boz[_] = [wewnetrzne_koszty[_][0]]
        else:
            w_dostawa_spedycja.append(_)

    return w_dostawa_boz, w_dostawa_spedycja

def przypisywanie_wartosci_bezposredniego_polaczenia(df):
    koszty = {}
    wewnetrzne_pogrupowane = (df.groupby(['miejscowosc_dostawy'], as_index=False).sum(numeric_only=True))  ## as_index ustawiamy ponieważ bez tego brało kolumne miejsce_dostawy jako kolumne index
    wewnetrzne_pogrupowane = list(wewnetrzne_pogrupowane.iloc[:, 0])
    # ustalenie ilości kilometrów jakie będą obciążeniem dla firmy aby dojechać do danego miejsca
    for miejscowosci in wewnetrzne_pogrupowane:
        # pierwsza wartosci w liscie koszty odpowiada polaczeniu bezpośredniemu
        polaczenie0 = wyszukanie('Rzeszow', miejscowosci)

        koszty[miejscowosci] = [polaczenie0[0]['km']]
        # trzeba to zrobić w osobnej pętli ponieważ wartości powrotne będą dzielone i dodawane to wartości kilometrów przy połączeniach łączonych

    return koszty

def usun_puste(d):
    for k, v in list(d.items()):
        for sub_k, sub_v in list(v.items()):
            if isinstance(sub_v, dict):
                for subsub_k, subsub_v in list(sub_v.items()):
                    if not subsub_v:
                        del d[k][sub_k][subsub_k]
            elif not sub_v:
                del d[k][sub_k]

    return d

def remove_duplicates(data):
    for key, value in data.items():
        if isinstance(value, dict):
            remove_duplicates(value)
        elif isinstance(value, list):
            data[key] = list(set(value))
    return data

def generowanie_tras():
    trasa_df = pd.DataFrame(columns=['nazwa_kontrahenta', 'miejscowosc_dostawy', 'ilosc_dostarczana', 'waga','km'])
    return trasa_df

def przygotwanie_przesylki_do_bazy_danych(dict_tabor, df_spedycja, decyzja):    
    grouped_data = []
    #dzialanie dla pierwszego uruchomienia 
    try:
        nr_trasy = lacza.ile_tras_nowe_trasy()
    except:
        nr_trasy = 0 

    lista_transportow=[]
    dt = datetime.now().date()
    jutro = (date.today() + timedelta(days=1))

    if decyzja =="2" or decyzja =="0":

        #for record in trasy:
        for record in dict_tabor:
            nr_trasy += 1

            for index,row in dict_tabor[record].iterrows():
                if row['nazwa_kontrahenta'] in df_spedycja.values : #sprawdzenie miejscowosci
                    pozycja_przejazdu = (df_spedycja[df_spedycja['nazwa_kontrahenta'] == row['nazwa_kontrahenta']].index)[0] #wybranie wiersza w którym nastapila zgodnosc

                    if df_spedycja.loc[pozycja_przejazdu]['miejscowosc_dostawy'] == row['miejscowosc_dostawy'] : #sprawdzenie czy miejscowosc dostawy sie zgadza
                        status = "mieszany"

                    else:
                        status = "transport_wlasny"
                else :
                    status = "transport_wlasny"
                
                grouped_data.append({'nr_trasy':nr_trasy,'data_dostawy': jutro, 'miejsce': row['miejscowosc_dostawy'], 'firma': row['nazwa_kontrahenta'], 'palety': row['ilosc_dostarczana'], 'samochod': record, 'koszt':0, 'km':row['km'], 'status':status})

    if decyzja =="1" or decyzja =="0":

        for index, row in df_spedycja.iterrows():
            k = kalkulator_spedycja(km=row['km'], waga=row['waga'], palety=row['ilosc_dostarczana'])
            ilosc_palet = len(k[1])  # konieczność ustalenia ilosc palet w ten sposob poniewaz max waga palety w Raben to 1200 kg, w transporcie wlasnym nie ma takich ogranicznen.
            opis = ["302_G_3,", "302_G_3,", row['nazwa_kontrahenta'], '_', row['miejscowosc_dostawy'], ',',
                    datetime.now().date().strftime("%Y-%d-%m"), ',towar,ep,', ilosc_palet, ',120,80,150,',
                    row['waga'], ',fb+t,', 'nazwa_towaru,,,,,1,,,,,,,,,,,,,,,,,,,,Premium,']
            opis_2 = "".join(map(str, opis))
            nr_trasy = "SPE_"+str(random.randint(1000000, 90000000))
            
            status = "" #konieczne ustawienie dla późniejszego działania programu

            for framy in dict_tabor:
                
                for index, row_1 in dict_tabor[framy].iterrows():

                    if status == "mieszany":
                        break
                    
                    elif row_1['miejscowosc_dostawy'] == row['miejscowosc_dostawy'] and row_1['nazwa_kontrahenta'] == row['nazwa_kontrahenta']:
                        status = "mieszany"

                    else:
                        status = "spedycja"

            grouped_data.append({'nr_trasy':nr_trasy,'data_dostawy': jutro, 'miejsce': row['miejscowosc_dostawy'], 'firma': row['nazwa_kontrahenta'], 'palety': row['ilosc_dostarczana'], 'samochod': 'Raben' , 'koszt':row['koszt_spedycji'], 'km':row['km'], 'status':status})
                
            with open('nowy_2spedycja.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(opis_2.split(','))
                opis = ''
                opis_2 = ''

    csv_file = 'your_data2.csv'

    # Open the CSV file in write mode and write the data
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f,delimiter=',', fieldnames=['nr_trasy','data_dostawy', 'miejsce', 'firma', 'palety', 'samochod' , 'koszt','km', 'status'])
        writer.writerows(grouped_data)

    #lacza.przesylka_nowe_trasy(csv_file)

    with open(csv_file, 'r') as plik:
        czytnik_csv = csv.reader(plik)
        for poszukiwany in czytnik_csv:
            if poszukiwany[-1] == "mieszany":
                if decyzja == 2: # wysylam transport, spedycje nie
            #spedycja musi wrócić do dokumentów
                    wynik = spedycja_df[(spedycja_df['nazwa_kontrahenta'] == poszukiwany[3]) & (spedycja_df['miejscowosc_dostawy'] == poszukiwany[2])]

                elif decyzja == 1:#wysylamy spedycje, transport nie
            #transport musi wrócic do dokumentow
                    for dejty in dict_tabor:
                        wynik = dict_tabor[dejty][(dict_tabor[dejty]['nazwa_kontrahenta'] == poszukiwany[3]) & (trasy[dejty]['miejscowosc_dostawy'] == poszukiwany[2])]
                        if len(wynik) > 0:
                            break
            try:
                print("Wynik który wróci do bazy danych",wynik)
            except:
                print("Nie ma nic zwrotnego")
                #PolaczenieBazy().dodanie_faktury(wynik['nazwa_kontrahenta'][0],'DZL',dt, dt, wynik['ilosc_dostarczana'][0],wynik['waga'][0],999,wynik['miejscowosc_dostawy'][0])

#funkcja sprawdzajaca czy logika nie trafila na szczegolny przypadek
def model_deflacyjny_dla_stworzonych_tras(nosnik_informacji_transportowych,koszt_km_w_funkcji,nosnik_informacji_spedycyjnej):
    #odczytywanie przejazdow z calosci wszystkich tras
    for przewiezienia in nosnik_informacji_transportowych:
        
        #odczytywanie miejscowosc dostawy
        for index, miejsce_docelowe in nosnik_informacji_transportowych[przewiezienia].iterrows():
            #uzyskiwanie listy miejscowosci posrednich wraz z usunieciem miejscowosci dla ktorej bedziemy sprawdzali oplacalnosc
            lista_miejsc_dostarczania = list(nosnik_informacji_transportowych[przewiezienia]['miejscowosc_dostawy'])
            #usuwanie duplikatow z listy
            lista_miejsc_dostarczania = list(set(lista_miejsc_dostarczania))
            lista_miejsc_dostarczania.remove(miejsce_docelowe['miejscowosc_dostawy'])
            
            if len(lista_miejsc_dostarczania) > 0:
                km_z_miastem_glownym = wyszukanie(zaczynamy='Rzeszow',konczymy=miejsce_docelowe["miejscowosc_dostawy"])[0]['km']
                koszt_spedycji_z_miasta_glownego = kalkulator_spedycja(km=km_z_miastem_glownym,waga=miejsce_docelowe['waga'],palety=miejsce_docelowe['ilosc_dostarczana'])
                
                for inne_miejscowosci in lista_miejsc_dostarczania:
                    punkty_przeniesienia = 0
                    km_pomiedzy_punktami = wyszukanie(zaczynamy=inne_miejscowosci,konczymy=miejsce_docelowe['miejscowosc_dostawy'])[0]['km']
                    km_pomiedzy_punktami += km_z_miastem_glownym
                    km_dla_polaczenia_bezposredniego = wyszukanie(zaczynamy='Rzeszow',konczymy=inne_miejscowosci)[0]['km']
                    km_pomiedzy_punktami = km_pomiedzy_punktami - km_dla_polaczenia_bezposredniego

                    if km_pomiedzy_punktami*koszt_km_w_funkcji > koszt_spedycji_z_miasta_glownego[0]:
                        punkty_przeniesienia += 1
                
                #warunek przeniesienia
                if punkty_przeniesienia > 0:
                    warunek_usuniecia = (nosnik_informacji_transportowych[przewiezienia]['nazwa_kontrahenta'] == miejsce_docelowe['nazwa_kontrahenta']) & \
                                    (nosnik_informacji_transportowych[przewiezienia]['miejscowosc_dostawy'] == miejsce_docelowe['miejscowosc_dostawy']) & \
                                    (nosnik_informacji_transportowych[przewiezienia]['ilosc_dostarczana'] == miejsce_docelowe['ilosc_dostarczana']) & \
                                    (nosnik_informacji_transportowych[przewiezienia]['waga'] == miejsce_docelowe['waga'])
                    #print(350,warunek_usuniecia)
                    nosnik_informacji_transportowych[przewiezienia] = nosnik_informacji_transportowych[przewiezienia].drop(nosnik_informacji_transportowych[przewiezienia][warunek_usuniecia].index) # usunięcie wiersza
                    #print(351,nosnik_informacji_transportowych[przewiezienia])
                    #print(352,miejsce_docelowe)
                    testing_df = pd.DataFrame([miejsce_docelowe], columns=nosnik_informacji_spedycyjnej.columns)
                    testing_df.loc[0, 'koszt_spedycji'] = koszt_spedycji_z_miasta_glownego[0]
                    #print(354,testing_df,nosnik_informacji_spedycyjnej)
                    nosnik_informacji_spedycyjnej = pd.concat([testing_df, nosnik_informacji_spedycyjnej], ignore_index=True) # wysylka do spedycji
                    #print(356,nosnik_informacji_spedycyjnej,nosnik_informacji_transportowych)                    
            
    return nosnik_informacji_spedycyjnej,nosnik_informacji_transportowych

try:
    os.remove('nowy_2spedycja.csv')
except:
    pass

lacza = PolaczenieBazy() # polaczenie z baza danych faktur
Samochod.odczytaj_z_pliku_wszystkie() # wczytanie danych samochodowych
#lacza.generowanie_towaru_custome()
dane = lacza.get_values_custome(status='testowania')
df = pd.DataFrame(dane, columns=['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana','waga'])
print(df)
df_do_wyswietlenia = df.copy()
koszty_pokonania_km = 7

koszty = przypisywanie_wartosci_bezposredniego_polaczenia(df)

koszty_dostawy = koszty_odleglosci('Rzeszow',koszty,koszty_pokonania_km) # uzyskanie ceny dostawy przez BOZ

koszty_dostawy = koszty_spedycji(df,koszty_dostawy)
pierwotne_koszty_dostawy = koszty_dostawy

dostawa_boz , dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy,koszty) # uzyskujemy podział na biblioteke i liste zawierajace odpowiednio lista rzeczy do transportu przez boz badz spedycje
print(382,dostawa_boz , dostawa_spedycja)
breakpoint()
spedycja_df =pd.DataFrame(columns=['nazwa_kontrahenta', 'miejscowosc_dostawy', 'ilosc_dostarczana', 'waga'])

pierwszy_rekord_do_uruchamienia_tworzenia_df = 0

while len(dostawa_spedycja)>0: # przenoszenie do spedycyjnego df

    for spedycyjne in dostawa_spedycja: # przeniesienie elementów pomiedzy df wysyłanych spedycją
        pierwszy_rekord_do_uruchamienia_tworzenia_df+= 1
        x =df.where(df['miejscowosc_dostawy'] == spedycyjne).dropna() # wycięcie wiersza do przeniesienia
        if pierwszy_rekord_do_uruchamienia_tworzenia_df == 1 :
            spedycja_df =pd.DataFrame(x)
        else:
            spedycja_df = pd.concat([x, spedycja_df], ignore_index=True) # przeniesienie wiersza do właściwej df
        df.drop(df[df['miejscowosc_dostawy'] == spedycyjne].index, inplace=True) # usunięcie wiersza z tramsportowej df
        df.reset_index(drop=True, inplace=True) # usunięcie powstałej luki po usunięciu z df miejscowości wysłanych spedycją
        spedycja_df.reset_index(drop=True, inplace=True)

    koszty_dostawy = koszty_odleglosci('Rzeszow',dostawa_boz,koszty_pokonania_km)
    koszty_dostawy = koszty_spedycji(df,koszty_dostawy)
    dostawa_boz, dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy, koszty)


while int(df['ilosc_dostarczana'].sum()) > Samochod.wyswietl_wage_i_palety()[1]: # sprawdzenie czy potrzeby transportowe nie są większe niż możliwości

    miejsce = (max(dostawa_boz.items(), key=operator.itemgetter(1))[0])
    x = df.where(df['miejscowosc_dostawy'] == miejsce).dropna() # wyszukanie miejscowości najdalej położonej od punktu startowego w df transportowej
    dostawa_boz.pop(miejsce) # usuniecie z dict miejscowości transportowej
    # spedycja_df = spedycja_df.append(x) # przeniesienie miejscowosći to df spedycyjnej

    spedycja_df = pd.concat([spedycja_df,x], ignore_index=True)
    (df.drop(df[df['miejscowosc_dostawy'] == miejsce].index, inplace=True)) # usniecie z df transportowej pozycji które zostały przeniesione do df spedycyjnej
    df.reset_index(drop=True, inplace=True)
    spedycja_df.reset_index(drop=True, inplace=True)


    if int(df['ilosc_dostarczana'].sum()) <= Samochod.wyswietl_wage_i_palety()[1]: # sprawdzenie czy po usunięciu ostatniej miejscowości nie zostało za dużo miejsca na aucie, jeżeli cos zostało sprawdza z ostaniej miejscowości możliwości doładunkowe i przenoisi wiersze pomiędzy df
        for y in range (len(x.sort_values(by=['ilosc_dostarczana'],ascending=False))): # wystwietlenie danych z ostatniej miejscowosci w pojedynczych 'wierszach'

            testing = (x.iloc[y]) # wewnetrzna zmienna, przechowujaca dane o wskazanym wierszu, stworzone dla wygody.
            ilosc_na_series = (x.iloc[y, :]['ilosc_dostarczana'])
            ilosc_do_doladowania = (Samochod.wyswietl_wage_i_palety()[1] - df['ilosc_dostarczana'].sum())

            if ilosc_do_doladowania > 0: # sprawdzenie czy poprzedni rekord w funkcji for nie spełnił warunki, po próbie zmiany warunki if na while generowało zle wyniki
                warunek_usuniecia = (spedycja_df['nazwa_kontrahenta'] == testing['nazwa_kontrahenta']) & \
                                    (spedycja_df['miejscowosc_dostawy'] == testing['miejscowosc_dostawy']) & \
                                    (spedycja_df['ilosc_dostarczana'] == testing['ilosc_dostarczana']) & \
                                    (spedycja_df['waga'] == testing['waga'])  # potwierdzenie wszystkich zmiennych aby mieć pewność że usuwamy napewno właściwy wiersz


                if ilosc_na_series > ilosc_do_doladowania: # w przypadku kiedy do jednego klienta jest wiecej towaru niż miejsca na samochodzie, dzieli towar na max wypelnienie samochodu a reszta do wysylki spedycha

                    doladowanie = ilosc_na_series - ilosc_do_doladowania  # ustalenie ilości przelowowej pomiędzy df

                    # dodanie przeliczaniwa wag
                    spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index) # usunięcie wiersza

                    testing.update(pd.Series([doladowanie], index=['ilosc_dostarczana'])) # ustalenia nowej wartości dla wracjacych danych do spedycji, wprowadziłem zmiane pod importem pandas
                    # spedycja_df = spedycja_df.append(testing) # wysylka do spedycji
                    testing_df = pd.DataFrame([testing], columns=spedycja_df.columns)
                    spedycja_df = pd.concat([testing_df, spedycja_df], ignore_index=True) # wysylka do spedycji
                    testing.update(pd.Series([ilosc_do_doladowania], index=['ilosc_dostarczana'])) # ustalenie wartosci dla df transportowego


                elif ilosc_na_series <= df['ilosc_dostarczana'].sum(): # w przypadku kiedy do jednego klienta nie jest wiecej towaru niz wolnego miejsca na samochodzie

                    spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index) # usunięcie wiersza
                    testing.update(pd.Series([ilosc_na_series], index=['ilosc_dostarczana'])) # ustalenie wartosci dla df transportowego

                # df = df.append(testing) # wysylka do transportu
                testing_df = pd.DataFrame([testing], columns=df.columns)
                df = pd.concat([df, testing_df], ignore_index=True)

                df.reset_index(drop=True, inplace=True)  # reset indexow
                spedycja_df.reset_index(drop=True, inplace=True)  # reset indexow


            #po przypisaniu palet do pełnego auta  sprawdzenie czy napewno wszystkiego rekordy są opłacalne
        koszty = przypisywanie_wartosci_bezposredniego_polaczenia(df)
        koszty_dostawy = koszty_odleglosci('Rzeszow',koszty,koszty_pokonania_km)  # uzyskanie ceny dostawy przez BOZ

        koszty_dostawy = koszty_spedycji(df, koszty_dostawy)
        dostawa_boz, dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy,
                                                                     koszty)  # uzyskujemy podział na biblioteke i liste zawierajace odpowiednio
        # jeżeli koszty spedycji są niższe niż koszty dostawy nowej ilości zwracamy miejscowość do spedycji
        if (len(dostawa_spedycja)) > 0: #testowo ustawiamy ==, normalnie ma byc >

            x = df.where(df['miejscowosc_dostawy'] == testing['miejscowosc_dostawy']).dropna()  # wycięcie wiersza do przeniesienia
            # spedycja_df = spedycja_df.append(x)  # przeniesienie wiersza do właściwej df
            x_df = pd.DataFrame([x], columns=spedycja_df.columns)
            spedycja_df = pd.concat([x_df, spedycja_df], ignore_index=True) # przeniesienie wiersza do właściwej df
            (df.drop(df[df['miejscowosc_dostawy'] == testing['miejscowosc_dostawy']].index,
                     inplace=True))  # usunięcie wiersza z tramsportowej df
            df.reset_index(drop=True, inplace=True)
            spedycja_df.reset_index(drop=True, inplace=True)



transport_df = pd.DataFrame(columns=['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana','waga','km'])

pierwszy_rekord_do_uruchamienia_tworzenia_df = 0

for index, row in df.iterrows():
    pierwszy_rekord_do_uruchamienia_tworzenia_df += 1
    row['km'] =dostawa_boz[row['miejscowosc_dostawy']][0] # uzyskanie km dla miejscowosci

    row_df = pd.DataFrame([row],columns=transport_df.columns)
    if pierwszy_rekord_do_uruchamienia_tworzenia_df == 1 :
            transport_df =pd.DataFrame(row_df)
    else:
        transport_df = pd.concat([transport_df,row_df],ignore_index=True)

transport_df.sort_values(by=['km', 'miejscowosc_dostawy'],ascending=False,inplace=True)
transport_df.reset_index(drop=True, inplace=True)
trasy={}
print(569,trasy)
for index , row in transport_df.iterrows(): # przypisanie drobnicy do transportów
    transport_df.reset_index(drop=True, inplace=True)
    print(572,row)
    try:
        for przejazdy in trasy:
            print(575,przejazdy,trasy)
            postoje = []
            warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1]) 
            ilosc_palet_na_zleceniu = int(trasy[przejazdy]['ilosc_dostarczana'].sum())
             
            if ilosc_palet_na_zleceniu == 0: #  warunek sprawdz ile jest palet do transportu
                continue

            ciezarowka = Samochod.dane_auta(nr_rej=przejazdy)
            print(584,ciezarowka)
            procent_obciazenia = (ciezarowka - ilosc_palet_na_zleceniu)/row.iloc[2]
            print(586,procent_obciazenia)
            #pierwszy warunek sprawdza czy procent obciążenia nie jest równy 0, drugi czy towar nie został wcześniej dodany do innego zlecenia
            if procent_obciazenia == 0\
                and \
                    transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all():
                
                #to ma sprawdzac czy wszystkie z utworzonych tras juz mialy szanse przyjac towar 
                if len(trasy) == list(trasy).index(przejazdy)+1:
                    raise Exception

            else: # tutaj wpadaja wszystkie przypadki mające coś do zawiezienia
                if procent_obciazenia > 1 :
                    procent_obciazenia = 1.0

                lista_postoi = trasy[przejazdy]['miejscowosc_dostawy'].tolist()
                lista_postoi = list(dict.fromkeys(lista_postoi)) # usuniecie duplikatów z listy postoi
                if trasy[przejazdy]['miejscowosc_dostawy'].isin([row.iloc[1]])[0].any() or len(trasy) >= Samochod.count_objects(): # pierwszy warunek sprawdza czy wyszukiwana miejscowosc jest w postojach, drugi czy ilość użytych samochodow nie jest rowna max. Trzeci warunek sprawdza czy analizowany przypadek trasy jest ostatnią trasą.

                    transport_df = transport_df.drop(transport_df[warunek_usuniecia].index)
                    row.update(pd.Series([row['ilosc_dostarczana']*procent_obciazenia],index=['ilosc_dostarczana']))
                    row.update(pd.Series([row['waga']*procent_obciazenia],index=['waga']))
                    dodanie = pd.DataFrame([row])
                    przejazd_0 = pd.concat([dodanie, trasy[przejazdy]], ignore_index=True)
                    trasy[przejazdy] = przejazd_0  # doddanie przejazdu do wszystkich tras

                    if procent_obciazenia < 1:
                        row.update(
pd.Series([(row['ilosc_dostarczana'] / procent_obciazenia) - row['ilosc_dostarczana']],index=['ilosc_dostarczana']))  # ustawienowej nowej ilosci dostarczanych palet
                        row.update(
                           pd.Series([(row['waga'] / procent_obciazenia) - row['waga']],index=['waga']))  # obliczanie nowej wagi, bardzo teoretyczna operacja, teoretycznie do wyjebania
                        new_record = pd.DataFrame([row])
                        transport_df = pd.concat([new_record, transport_df], ignore_index=True)
                        if row['km']*koszty_pokonania_km < kalkulator_spedycja(row['km'],row['waga'],row['ilosc_dostarczana'])[0]:
                            warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1]) 
                            postoje ={}
                            raise Exception

                        continue

                    else:
                        break

                else:
                    for p in lista_postoi: # wczytywanie wszyskich miejsc w postojach, poprzednia wersja trasy[przejazdy]['Postoje']

                        polaczenia_z_przystankiem =  wyszukanie(row.iloc[1],p)
                        try:
                            polaczenia_z_przystankiem_km = polaczenia_z_przystankiem[0]['km'] # uzyskanie km, przy braku wyniuku ustalona zostaje nierealna wartosc
                        except:
                            polaczenia_z_przystankiem_km = 999 # nierealna wartosc
                        
                        if wyszukanie(row.iloc[1],p)[0]['km'] < row.iloc[4]: # sprawdzenie czy km z polaczenia z ktorymz punktow sa mniejsze niz bezposrednie polaczenie z Rzeszowa.
                            
                            transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) # usuniecie z df
                            try:
                                postoje.append(cos_klikam['Przystanek'])

                            except:
                                postoje=postoje

                            try:
                                postoje.append(cos_klikam['Przystanek_1'])
                                postoje.append(cos_klikam['Przystanek_2'])
                                postoje.append(cos_klikam['Przystanek_3'])

                            except: 
                                postoje = postoje

                            row.update(pd.Series([row['ilosc_dostarczana']*procent_obciazenia],index=['ilosc_dostarczana']))
                            row.update(pd.Series([row['waga']*procent_obciazenia],index=['waga']))
                            dodanie_drobnicy = pd.DataFrame([row],columns=transport_df.columns)
                            
                            if len(postoje)>0: # dodanie przystankow do dataframu aby przy analizowaniu nastepnych przypadkow dostawy byly pelne informacje
                                for miasta_przystankowe in postoje:
                                    if len(miasta_przystankowe) > 0:
                                        data = {'nazwa_kontrahenta': 'Postoj','miejscowosc_dostawy': miasta_przystankowe,'ilosc_dostarczana': 0,'waga': 0,'km': 0}
                                        series = pd.Series(data)
                                        przystanek_df = pd.DataFrame([series])
                                        dodanie = pd.concat([dodanie,przystanek_df])

                            przejazd = pd.concat([dodanie_drobnicy, trasy[przejazdy]], ignore_index=True)
                            trasy[przejazdy] = przejazd

                            if procent_obciazenia < 1:
                                nowa_wartosc = (row['ilosc_dostarczana'] / procent_obciazenia) - row['ilosc_dostarczana']
                                nowa_waga = (row['waga'] / procent_obciazenia) - row['waga'] #waga narazie jest zle ustawiana ale to kwestia tego ze trzeba poprawic wage dodwana
                                row.update(pd.Series(nowa_wartosc ,index=['ilosc_dostarczana']))  # ustawienowej nowej ilosci dostarczanych palet
                                row.update(pd.Series(nowa_waga ,index=['waga']))  # ustawienowej nowej ilosci dostarczanych palet
                                
                                row_df = pd.DataFrame([row], columns=transport_df.columns)
                                transport_df = pd.concat([row_df, transport_df], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df
                            break 
                    
                    #pierwszy warunek sprawdza czy nie jest to ostatnia możliwa do stworzenia trasa, a inne nie warunki nie stwarzaja mozliwosc utworzenia trasy. Drugi warunek sprawdza czy towar nie zostal juz dodany do innego zlecenia.
                    if len(trasy) == list(trasy).index(przejazdy)+1\
                        and \
                            transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all():
                        raise Exception
        
        if len(trasy) ==0: # dla pierwszego dostarczanego towaru
            warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1])  # warunek usunieci musi tez byc utworzony w tym miejscu w przypadku pierwszej trasy
            postoje = [] # to samo z postojami, czysty wymóg pierwszej trasy
            raise Exception
    
    except RuntimeError as r:
        continue

    except Exception as e:
        print(688,e.args,e,row)
        traceback.print_exc()
        if len(trasy) == Samochod.count_objects():
            if (transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all()) == False: # po odrzuceniu resztki z dolodawanie nie da sie na jej podstawie stworzyc transportu ( maksymalan liczba samochodow ) reszta muszi wrocic do transportu
                row_df = pd.DataFrame([row])
                transport_df = pd.concat([transport_df,row_df], ignore_index=True)
            pass

        else:

            transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) # usuniecie z df elementu rozwazanego
            cos_klikam = wyszukanie('Rzeszow', row.iloc[1])[0]
            postoje = []
            try:
                postoje.append(cos_klikam['Przystanek'])

            except:
                postoje=postoje

            try:
                postoje.append(cos_klikam['Przystanek_1'])
                postoje.append(cos_klikam['Przystanek_2'])
                postoje.append(cos_klikam['Przystanek_3'])

            except:
                postoje = postoje
    
            dodanie = pd.DataFrame([row], columns=transport_df.columns) # stworzenie df z odczytywanego wiersza

            if len(postoje)>0: # dodanie przystankow do dataframu aby przy analizowaniu nastepnych przypadkow dostawy byly pelne informacje
                for miasta_przystankowe in postoje:
                    if len(miasta_przystankowe) > 0:
                        data = {'nazwa_kontrahenta': 'Postoj','miejscowosc_dostawy': miasta_przystankowe,'ilosc_dostarczana': 0,'waga': 0,'km': 0}
                        series = pd.Series(data)
                        przystanek_df = pd.DataFrame([series])
                        dodanie = pd.concat([dodanie,przystanek_df])
            
            samochod = Samochod.max_palety(len(trasy))
            trasy[samochod[0]] = dodanie  # doddanie przejazdu do wszystkich tras

for przejazd in trasy: #resetowanie indeksu w trasie
    trasy[przejazd].reset_index(drop=True, inplace=True)


if len(transport_df) > 0: #przenoszenie pozostałych towarow z przeznaczonych do transportu, do wysyłką spedycja.
    spedycja_df = pd.concat([transport_df,spedycja_df])

for index, row in spedycja_df.iterrows():  # przypisywanie kosztow dostawy spedycja
    try:
        if str(row['km']) == "nan":
            raise Exception
        else:
            km = row['km']
    except:
        km = (pierwotne_koszty_dostawy[row['miejscowosc_dostawy']]['km'])


    palety = (row['ilosc_dostarczana'])
    waga = (row['waga'])
    row['koszt_spedycji'] = kalkulator_spedycja(km=km, waga=waga, palety=palety)[0]
    row['km'] = km
    row_df = pd.DataFrame([row])
    spedycja_df = pd.concat([row_df, spedycja_df], ignore_index=True)

try:
    spedycja_df.dropna(inplace=True)
    spedycja_df.sort_values(by='km',ascending=True,inplace=True)
    spedycja_df.reset_index(drop=True, inplace=True)
except:
    spedycja_df = spedycja_df

#x , y = sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy,spedycja_df,koszty_pokonania_km)
#print(693,x,y)

# ostatnie wirowanie
while True:
    #sprawdzenie aby pętla while nie leciała w nieskończoność 
    bezpiecznik = 0
    trasy0 = trasy.copy()
    spedycja0 = spedycja_df.copy()
    trasy, spedycja_df = sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy_do_przyjcia = trasy, spedycje_do_sprawdzenia = spedycja_df, ile_kosztuje_km = koszty_pokonania_km)
    trast, spedycja_df = sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy_do_przyjcia = trasy, spedycje_do_sprawdzenia = spedycja_df, ile_kosztuje_km = koszty_pokonania_km)

    if compare_dictionaries(trasy0,trasy) and spedycja0.equals(spedycja_df):
        print("koniec")
        break
    elif bezpiecznik > 30:
        break
    else:
        print("nie koniec")

    bezpiecznik += 1
print(trast, spedycja_df)

test_trasy, test_spedycja = sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy_do_przyjcia = trasy, spedycje_do_sprawdzenia = spedycja_df, ile_kosztuje_km = koszty_pokonania_km)
print(698,test_trasy, test_spedycja)
#while dl_speydcji > 0: # sprawdzanie czy pozycje z spedycji nie są możliwe do doładowaniaI
#    
#    dl_speydcji = len(spedycja_df) # ustalanie długosci, sprawdza czy petla wykonala operacje
#    
#    for powrot_z_trasy in trasy: # czytanie tras
#
#        for index, row in spedycja_df.iterrows():           
#            lista_postoi = trasy[powrot_z_trasy]['miejscowosc_dostawy'].tolist() #uzyskanie listy miejscowosci ktore odwiedza auto
#            postoje_lista = list(dict.fromkeys(lista_postoi)) #usuniecie duplikatow
#            palety_na_powrocie = int(Samochod.dane_auta(powrot_z_trasy)) - int(trasy[powrot_z_trasy]['ilosc_dostarczana'].sum()) # obliczenie palet na powrocie, dla kazdego klient musi zostac obliczona na nowo
#            
#            if palety_na_powrocie == 0:
#                continue
#
#            try:
#                if  row['ilosc_dostarczana'] <= palety_na_powrocie : # obliczenie ilości do doładowania
#                    procent_wypelnienia_auta =1 #procent wyplnienia auta w rozumieniu procent w jakim towar w zamowieniu jest w stanie zmiesci sie na aucie
#                else:
#                    procent_wypelnienia_auta =  palety_na_powrocie / row['ilosc_dostarczana'] 
#
#                warunek_usuniecia = (spedycja_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
#                                    (spedycja_df['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
#                                    (spedycja_df['ilosc_dostarczana'] == row['ilosc_dostarczana']) & \
#                                    (spedycja_df['waga'] == row['waga'])
#
#                if row['miejscowosc_dostawy'] in postoje_lista: # sprawdzenie czy miejscowosc nie wystepuje w postojach
#                    spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index)  # usuniecie z df spedycyjnego  
#                    row.update(pd.Series([row['ilosc_dostarczana']*procent_wypelnienia_auta],index=['ilosc_dostarczana']))
#                    row.update(pd.Series([row['waga']*procent_wypelnienia_auta],index=['waga']))
#                    dodanie_drobnicy = pd.DataFrame([row],columns=transport_df.columns)
#                    przejazd = pd.concat([dodanie_drobnicy, trasy[powrot_z_trasy]], ignore_index=True)
#                    trasy[powrot_z_trasy] = przejazd
#
#                    if procent_wypelnienia_auta < 1:
#                        row['ilosc_dostarczana'] = row['ilosc_dostarczana'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['ilosc_dostarczana'] / procent_wypelnienia_auta))  # ustawienowej nowej ilosci dostarczanych palet
#                        row['waga'] = row['waga'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['waga'] / procent_wypelnienia_auta))  # analogiczne ustawienie wagi
#                        dodanie_spadkow = pd.DataFrame([row],columns=spedycja_df.columns)
#                        spedycja_df = pd.concat([dodanie_spadkow, spedycja_df], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df
#                    continue
#                    # dodanie
#
#                try: # sprawdzenie czy dołożenie miejsca dostawy nie jest tańsze niż wysyłka spedycja
#                    dodatkowe_km_dla_punktu = wyszukanie(zaczynamy=postoje_lista[0], konczymy='Rzeszow',obowiazkowy_przystanek=row['miejscowosc_dostawy'])[0]['km'] - \
#                                                  wyszukanie(zaczynamy=postoje_lista[0], konczymy='Rzeszow')[0]['km'] # wyzwalacz bledu, jezeli nie trasy to zwraca blad
#
#                    
#                    if dodatkowe_km_dla_punktu * koszty_pokonania_km < row['koszt_spedycji']*procent_wypelnienia_auta: # sprawdzenie czy tańsze jest połączenie z którymś z punktow czy bezpośrednio z Rzeszowa
#                        spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index)  # usuniecie z df spedycyjnego  
#                        row.update(pd.Series([row['ilosc_dostarczana']*procent_wypelnienia_auta],index=['ilosc_dostarczana']))
#                        row.update(pd.Series([row['waga']*procent_wypelnienia_auta],index=['waga']))
#                        dodanie_drobnicy = pd.DataFrame([row],columns=transport_df.columns)
#                        przejazd = pd.concat([dodanie_drobnicy, trasy[powrot_z_trasy]], ignore_index=True)
#                        trasy[powrot_z_trasy] = przejazd
#
#                        if procent_wypelnienia_auta < 1:
#                            row['ilosc_dostarczana'] = row['ilosc_dostarczana'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['ilosc_dostarczana'] / procent_wypelnienia_auta))  # ustawienowej nowej ilosci dostarczanych palet
#                            row['waga'] = row['waga'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['waga'] / procent_wypelnienia_auta))  # analogiczne ustawienie wagi
#                            dodanie_spadkow = pd.DataFrame([row],columns=spedycja_df.columns)
#                            spedycja_df = pd.concat([dodanie_spadkow, spedycja_df], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df
#
#                except Exception as e:
#                    continue
#
#
#            except ZeroDivisionError as e:
#                continue
#
#            except Exception as e:
#                continue
#
#    dl_speydcji -= len(spedycja_df)
#resetowanie i usuwanie postoi indexów w trasach

print(766,spedycja_df,trasy)
for przejazd in trasy:
    trasy[przejazd] = trasy[przejazd][trasy[przejazd]['nazwa_kontrahenta'] != 'Postoj']
    trasy[przejazd].reset_index(drop=True, inplace=True)

keys = ['nr_trasy','data_dostawy', 'miejsca', 'firmy', 'palety', 'samochod','km','koszt','status']
grouped_data = []
os_x = []
os_y =[]
print(781,spedycja_df)
spedycja_df,trasy = model_deflacyjny_dla_stworzonych_tras(trasy,koszty_pokonania_km,spedycja_df)
print(783,spedycja_df,trasy)

test_trasy1, test_spedycja1 = sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy_do_przyjcia = trasy, spedycje_do_sprawdzenia = spedycja_df, ile_kosztuje_km = koszty_pokonania_km)

print(782,test_trasy1,test_spedycja1)