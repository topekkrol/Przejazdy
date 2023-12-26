import time
import random
from WyszukiwarkaMakaronowa import wyszukanie
import pandas as pd

from Kalkulator_Raben import kalkulator_spedycja
from DoPSGl import PolaczenieBazy
import operator
from flota import Samochod
from datetime import datetime
import csv
from datetime import date,timedelta
import matplotlib.pyplot as plt

def rozwiazywania_rownania_a(b,plik):
    # przypisywanie wartosci do list. Podczas wyliczania odleglosci istnieje zmienna ktora moze być określona dopiero pod koniec ostatniej pętli.
    # Funckja rozwiazuje problem przypisujac konkretna wartość i usuwając element z list
    a =max(b)
    for m in plik:
        x = 0 # testowo
        plyk = plik[m]
        for elementy in plik[m]:
            try:
                wartosc = elementy[0] + a
                plyk.insert(1,wartosc) # dodawanie wartosci na drugim miejscu listy, nie mozemy dodac na 0 poniewaz przechowywana tam jest wartosc bezposredniego polaczenie, dodawnie na koncu zakloca logike rozwiazywania nastepnych list.
                plyk.remove(elementy) # usuwanie z listy
                koszty[m] = plyk
            except:
                x +=1
                continue

    return []

def sprawdzanie_czy_z_tylu_sie_wszystko_zgadza(polaczenie,miejscowosc,koszty_wewnetrzne):
    # start : Przypisywanie poprzednim miejscowosciom literki zmiennej, jeżeli warunek wczesniej trafił do 'else' i wykonal operacje zamiany list na dane
    if [polaczenie[0]['km'], 'a'] not in koszty[miejscowosc]:
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
                                    a = rozwiazywania_rownania_a(a,koszty)


                                else:
                                    a.append(koszty[miejscowosci1][0]/2)
                                    a = rozwiazywania_rownania_a(a,koszty)


                    else:
                        a.append(koszty[miejscowosci][0])
                        a = rozwiazywania_rownania_a(a,koszty)


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
                    a = rozwiazywania_rownania_a(a,koszty)

                else:
                    a.append(koszty[miejscowosci][0])
                    a = rozwiazywania_rownania_a(a,koszty)

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
            a =rozwiazywania_rownania_a(a,koszty)

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

    for _ in (koszty_dostawy):

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

lacza = PolaczenieBazy() # polaczenie z baza danych faktur
Samochod.odczytaj_z_pliku_wszystkie() # wczytanie danych samochodowych
dane = lacza.get_values(status='planowana')
df = pd.DataFrame(dane, columns=['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana','waga'])
koszty_pokonania_km = 7
print(df)
koszty = przypisywanie_wartosci_bezposredniego_polaczenia(df)

koszty_dostawy = koszty_odleglosci('Rzeszow',koszty,koszty_pokonania_km) # uzyskanie ceny dostawy przez BOZ

koszty_dostawy = koszty_spedycji(df,koszty_dostawy)
pierwotne_koszty_dostawy = koszty_dostawy

dostawa_boz , dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy,koszty) # uzyskujemy podział na biblioteke i liste zawierajace odpowiednio lista rzeczy do transportu przez boz badz spedycje

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

#while len(transport_df.where(transport_df['ilosc_dostarczana'] >= Samochod.max_palety(len(trasy))[1]).dropna()) > 0: # przypisanie tylko dla pełnych samochodów
#    
#    y = len(transport_df.where(transport_df['ilosc_dostarczana'] >= Samochod.max_palety(len(trasy))[1]).dropna())
#    df_calosowamochodpwy = transport_df.where(transport_df['ilosc_dostarczana'] >= Samochod.max_palety(len(trasy
#    ))[1]).dropna() # konieczność zresetowania indeksow poniewaz posiadaja wartosci cora df
#    df_calosowamochodpwy.reset_index(drop=True, inplace=True)
#
#    for index,row in df_calosowamochodpwy.iterrows():
#
#        nowa_ilosc = row['ilosc_dostarczana'] - Samochod.max_palety(len(trasy))[1] #obliczanie nowej ilosci pomniejszonej o w pelni zaladowany samochod
#
#        warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
#                            (transport_df['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) # ustalenie warunkow do usuniecia pozycji z df
#
#        transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) # usuniecie pozycji z df
#
#        if nowa_ilosc >0:
#            row.update(pd.Series([nowa_ilosc], index=['ilosc_dostarczana'])) # ustawienowej nowej ilosci dostarczanych palet
#            testing_df_2 = pd.DataFrame([testing], columns=df.columns)
#            transport_df = pd.concat([row, testing_df_2], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df
#
#        dodanie = pd.DataFrame([row],columns=transport_df.columns)
#
#        trasy[len(trasy)] = dodanie # doddanie przejazdu do wszystkich tras
#        transport_df.sort_values(by='km', ascending=False, inplace=True) # posortowanie wartosci  w df
#        transport_df.reset_index(drop=True, inplace=True) # zresetowanie indexow w df

print(368,transport_df,spedycja_df,sep='\n')
print(369,trasy,'\n')

for index , row in transport_df.iterrows(): # przypisanie drobnicy do transportów
    
    print('\n',row,len(trasy))
    try:
        for przejazdy in trasy:
            postoje = []
            warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1]) 
            print(383,warunek_usuniecia)
            ilosc_palet_na_zleceniu = int(trasy[przejazdy]['ilosc_dostarczana'].sum())
            print(384,ilosc_palet_na_zleceniu)
            #print(385,ilosc_palet_na_zleceniu)
            #print(386,list(trasy).index(przejazdy),len(trasy))

            if ilosc_palet_na_zleceniu == 0: #  warunek sprawdz ile jest palet do transportu
                continue

            #print(389,Samochod.max_palety(przejazdy)[1],ilosc_palet_na_zleceniu)
            ciezarowka = Samochod.max_palety(len(trasy))
            print(393,ciezarowka)
            procent_obciazenia = (ciezarowka[1] - ilosc_palet_na_zleceniu)/row.iloc[2]
            print(392,procent_obciazenia)
            #print(389.1,transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all()) # warunek sprawdzający czy poprzednia pętla nie obsłużyła zapytania
            
            #pierwszy warunek sprawdza czy procent obciążenia nie jest równy 0, drugi czy towar nie został wcześniej dodany do innego zlecenia
            if procent_obciazenia == 0\
                and \
                    transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all():
                if len(trasy) ==przejazdy+1:
                    print(385.1)
                    raise Exception

            else: # tutaj wpadaja wszystkie przypadki mające coś do zawiezienia
                if procent_obciazenia > 1 :
                    procent_obciazenia = 1.0
                
                print(ilosc_palet_na_zleceniu)
                print("procent obciazenia",procent_obciazenia)
                lista_postoi = trasy[przejazdy]['miejscowosc_dostawy'].tolist()
                lista_postoi = list(dict.fromkeys(lista_postoi)) # usuniecie duplikatów z listy postoi
                print(408.1,lista_postoi,row.iloc[1])
                if trasy[przejazdy]['miejscowosc_dostawy'].isin([row.iloc[1]])[0].any() or len(trasy) >= Samochod.count_objects(): # pierwszy warunek sprawdza czy wyszukiwana miejscowosc jest w postojach, drugi czy ilość użytych samochodow nie jest rowna max. Trzeci warunek sprawdza czy analizowany przypadek trasy jest ostatnią trasą.

                    print(412.1,transport_df,warunek_usuniecia)
                    transport_df = transport_df.drop(transport_df[warunek_usuniecia].index)
                    print(403,trasy[przejazdy])
                    print(404,trasy)
                    row.update(pd.Series([row['ilosc_dostarczana']*procent_obciazenia],index=['ilosc_dostarczana']))
                    print(405,trasy)
                    dodanie = pd.DataFrame([row])
                    print(406.1,dodanie)
                    przejazd_0 = pd.concat([dodanie, trasy[przejazdy]], ignore_index=True)
                    print(407,przejazd_0)
                    trasy[przejazdy] = przejazd_0  # doddanie przejazdu do wszystkich tras
                    print(409,trasy)

                    if procent_obciazenia < 1:
                        print(431,(row['ilosc_dostarczana'] / procent_obciazenia) - row['ilosc_dostarczana'],procent_obciazenia,sep='\n')
                        row.update(
                            pd.Series([(row['ilosc_dostarczana'] / procent_obciazenia) - row['ilosc_dostarczana']],index=['ilosc_dostarczana']))  # ustawienowej nowej ilosci dostarczanych palet
                        row.update(
                           pd.Series([int((1 - procent_obciazenia) * row['waga'])],index=['waga']))  # obliczanie nowej wagi, bardzo teoretyczna operacja, teoretycznie do wyjebania
                        new_record = pd.DataFrame([row])
                        print(441,new_record)
                        print(442,procent_obciazenia)
                        print(443,row)
                        print(443.1,row['km']*koszty_pokonania_km ,kalkulator_spedycja(row['km'],row['waga'],row['ilosc_dostarczana'])[0])
                        transport_df = pd.concat([new_record, transport_df], ignore_index=True)
                        if row['km']*koszty_pokonania_km < kalkulator_spedycja(row['km'],row['waga'],row['ilosc_dostarczana'])[0]:
                            warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1]) 
                            postoje ={}
                            raise Exception

                        continue

                    else:
                        break

                else:
                    print(455,lista_postoi)
                    for p in lista_postoi: # wczytywanie wszyskich miejsc w postojach, poprzednia wersja trasy[przejazdy]['Postoje']

                        polaczenia_z_przystankiem =  wyszukanie(row.iloc[1],p)
                        print(456,polaczenia_z_przystankiem[0])
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

                            dodanie_drobnicy = pd.DataFrame([row],columns=transport_df.columns)
                            
                            if len(postoje)>0: # dodanie przystankow do dataframu aby przy analizowaniu nastepnych przypadkow dostawy byly pelne informacje
                                for miasta_przystankowe in postoje:
                                    print(538,len(miasta_przystankowe))
                                    if len(miasta_przystankowe) > 0:
                                        data = {'nazwa_kontrahenta': 'Postoj','miejscowosc_dostawy': miasta_przystankowe,'ilosc_dostarczana': 0,'waga': 0,'km': 0}
                                        series = pd.Series(data)
                                        przystanek_df = pd.DataFrame([series])
                                        dodanie = pd.concat([dodanie,przystanek_df])


                            print(458,dodanie_drobnicy,sep='\n')
                            przejazd = pd.concat([dodanie_drobnicy, trasy[przejazdy]], ignore_index=True)
                            print(460,przejazd,trasy,sep='\n')
                            trasy[przejazdy] = przejazd
                            print(462,trasy)
                            print(467,"tutaj powinien byc koniec")

                            if procent_obciazenia < 1:
                                print(468,"ciekawe")
                                row.update(
                                    pd.Series([row['ilosc_dostarczana'] - row['ilosc_dostarczana'] * procent_obciazenia],
                                            index=['ilosc_dostarczana']))  # ustawienowej nowej ilosci dostarczanych palet

                                row_df = pd.DataFrame([row], columns=transport_df.columns)
                                transport_df = pd.concat([row_df, transport_df], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df
                            print(478)
                            break 
                    
                    print(389.1,transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all()) # warunek sprawdzający czy poprzednia pętla nie obsłużyła zapytania
                    print(512,list(trasy).index(przejazdy))
                    #pierwszy warunek sprawdza czy nie jest to ostatnia możliwa do stworzenia trasa, a inne nie warunki nie stwarzaja mozliwosc utworzenia trasy. Drugi warunek sprawdza czy towar nie zostal juz dodany do innego zlecenia.
                    if len(trasy) == list(trasy).index(przejazdy)+1\
                        and \
                            transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all():
                        print(480,len(trasy),przejazdy+1)
                        raise Exception
        
        if len(trasy) ==0: # dla pierwszego dostarczanego towaru
            warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1])  # warunek usunieci musi tez byc utworzony w tym miejscu w przypadku pierwszej trasy
            postoje = [] # to samo z postojami, czysty wymóg pierwszej trasy
            raise Exception
    
    except RuntimeError as r:
        print(483)
        continue

    except Exception as e:
        print(e)
        if len(trasy) == Samochod.count_objects():
            if (transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row.iloc[2]]}).any().all()) == False: # po odrzuceniu resztki z dolodawanie nie da sie na jej podstawie stworzyc transportu ( maksymalan liczba samochodow ) reszta muszi wrocic do transportu
                row_df = pd.DataFrame([row])
                transport_df = pd.concat([transport_df,row_df], ignore_index=True)
            pass

        else:

            transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) # usuniecie z df elementu rozwazanego
            cos_klikam = wyszukanie('Rzeszow', row.iloc[1])[0]
            print(488,cos_klikam)
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
                    print(538,len(miasta_przystankowe))
                    if len(miasta_przystankowe) > 0:
                        data = {'nazwa_kontrahenta': 'Postoj','miejscowosc_dostawy': miasta_przystankowe,'ilosc_dostarczana': 0,'waga': 0,'km': 0}
                        series = pd.Series(data)
                        przystanek_df = pd.DataFrame([series])
                        dodanie = pd.concat([dodanie,przystanek_df])
                        print(540,dodanie)
            
            print(563,len(trasy))
            samochod = Samochod.max_palety(len(trasy))
            trasy[samochod[0]] = dodanie  # doddanie przejazdu do wszystkich tras
            print(511,trasy)


print(508,transport_df)
print(509)
print(trasy)
for ttt in trasy:
    print('\n',trasy[ttt])


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

print(559,transport_df,spedycja_df,sep="\n")

try:
    spedycja_df.dropna(inplace=True)
    spedycja_df.sort_values(by='km',ascending=True,inplace=True)
    spedycja_df.reset_index(drop=True, inplace=True)
except:
    spedycja_df = spedycja_df

print(568,transport_df,spedycja_df,sep="\n")

dl_speydcji = len(spedycja_df)
## trzeba sprawdzic na innym przykladzie, dla pierwszego zre jak pies koperek

while dl_speydcji > 0: # sprawdzanie czy pozycje z spedycji nie są możliwe do doładowaniaI
    dl_speydcji = len(spedycja_df) # ustalanie długosci, sprawdza czy petla wykonala operacje
    for powrot_z_trasy in trasy: # czytanie tras
        print(609,trasy[powrot_z_trasy],powrot_z_trasy)
        for index, row in spedycja_df.iterrows():
            print(611,row,index)
            
            lista_postoi = trasy[przejazdy]['miejscowosc_dostawy'].tolist()
            postoje_lista = list(dict.fromkeys(lista_postoi))
            
            palety_na_powrocie = int(Samochod.dane_auta(powrot_z_trasy)) - int(trasy[powrot_z_trasy]['ilosc_dostarczana'].sum()) # obliczenie palet na powrocie, dla kazdego klient musi zostac obliczona na nowo
            print(622,palety_na_powrocie,postoje_lista)
            if palety_na_powrocie == 0:
                continue

            print(626)    
            try:
                if palety_na_powrocie / row['ilosc_dostarczana'] > 1.0 : # obliczenie ilości do doładowania
                    procent_wypelnienia_auta =1
                else:
                    procent_wypelnienia_auta = palety_na_powrocie / row['ilosc_dostarczana']

                warunek_usuniecia = (spedycja_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
                                    (spedycja_df['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
                                    (spedycja_df['ilosc_dostarczana'] == row['ilosc_dostarczana']) & \
                                    (spedycja_df['waga'] == row['waga'])

                if row['miejscowosc_dostawy'] in postoje_lista: # sprawdzenie czy miejscowosc nie wystepuje w postojach
                    spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index) # usuniecie z df
                    klienci = postoje[row['miejscowosc_dostawy']] # wczytanie klientow z miejscoowsci
                    klienci.append(row['nazwa_kontrahenta']) # dodanie nowego klienta do miejscowisc
                    postoje[row['miejscowosc_dostawy']] = klienci # zaktualizowanie klientow w miejscoowsci
                    przejazd = {
                        'Postoje': postoje,
                        'Palety': trasy[powrot_z_trasy]['Palety']+(row['ilosc_dostarczana']*procent_wypelnienia_auta),
                        'Km': 0,
                        'Samochod': trasy[powrot_z_trasy]['Samochod']
                    }

                    trasy[powrot_z_trasy] = przejazd

                    if procent_wypelnienia_auta < 1:
                        row.update(pd.Series([row['ilosc_dostarczana'] - row['ilosc_dostarczana']*procent_wypelnienia_auta], index=['ilosc_dostarczana']))  # ustawienowej nowej ilosci dostarczanych palet
                        # spedycja_df = spedycja_df.append(row)  # dodanie palet ktore sie nie zmiescily do df
                        spedycja_df = pd.concat([row, spedycja_df], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df
                    continue
                    # dodanie

                try: # sprawdzenie czy dołożenie miejsca dostawy nie jest tańsze niż wysyłka spedycja
                    dodatkowe_km_dla_punktu = wyszukanie(zaczynamy=postoje_lista[0], konczymy='Rzeszow',obowiazkowy_przystanek=row['miejscowosc_dostawy'])[0]['km'] - \
                                                  wyszukanie(zaczynamy=postoje_lista[0], konczymy='Rzeszow')[0]['km'] # wyzwalacz bledu, jezeli nie trasy to zwraca blad

                    if dodatkowe_km_dla_punktu * koszty_pokonania_km < row['koszt_spedycji']*procent_wypelnienia_auta: # sprawdzenie czy tańsze jest połączenie z którymś z punktow czy bezpośrednio z Rzeszowa

                        spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index)  # usuniecie z df spedycyjnego
                        up_postoje = {row['miejscowosc_dostawy']: [row['nazwa_kontrahenta']]}
                        up_postoje.update(postoje)
                        przejazd = {
                            'Postoje': up_postoje,
                            'Palety': trasy[powrot_z_trasy]['Palety'] + (row['ilosc_dostarczana']*procent_wypelnienia_auta),
                            'Km': 0,
                            'Samochod': trasy[powrot_z_trasy]['Samochod']
                        }

                        trasy[powrot_z_trasy] = przejazd
                        if procent_wypelnienia_auta < 1:
                            row_w_if = row
                            new_pallet = row['ilosc_dostarczana'] - (row['ilosc_dostarczana'] * procent_wypelnienia_auta)
                            new_value = row['koszt_spedycji'] - (row['koszt_spedycji'] * procent_wypelnienia_auta)
                            row_w_if.update(pd.Series([new_pallet], index=['ilosc_dostarczana'])) # ustawienowej nowej ilosci dostarczanych palet
                            spedycja_df = spedycja_df.append(row_w_if)  # dodanie palet ktore sie nie zmiescily do df


                except Exception as e:
                    continue


            except ZeroDivisionError as e:
                continue

            except Exception as e:
                continue

    dl_speydcji -= len(spedycja_df)
#resetowanie i usuwanie postoi indexów w trasach
for przejazd in trasy:
    trasy[przejazd] = trasy[przejazd][trasy[przejazd]['nazwa_kontrahenta'] != 'Postoj']
    trasy[przejazd].reset_index(drop=True, inplace=True)

keys = ['nr_trasy','data_dostawy', 'miejsca', 'firmy', 'palety', 'samochod','km','koszt','status']
grouped_data = []
os_x = []
os_y =[]

print(708)
if len(trasy) > 0:
    print("no to rura")
    
    #pokazanie na grafie realizowanych tras
    #for linie in trasy:
        #print(trasy[linie])
        #for index, rowll in trasy[linie].iterrows():
            #csv_file = csv.reader(open('Trasy-zmiana_przypisywania_do_coru\latilon.csv', "r"), delimiter=",")
            #print(rowll)
            #for rowl in csv_file:
                #if rowl[0] == rowll['miejscowosc_dostawy']:
                   #os_x.append(rowl[1])
                   #os_y.append(rowl[2])

            #print(722,os_x,os_y)
            #plt.plot(os_x, os_y, label='Linia 1', color='blue', linestyle='-')
            #plt.show()

    print("spedycja :",spedycja_df,sep="\n")

    wykorzystanie_danych = input("Na podstawie zaprezentowanych danych transportowych chcesz utworzyć zlecenia transportowe?\n1. Tak\n2. Nie\n Wybor :")
    #wykorzystanie_danych = "1"
    
    #dzialanie dla pierwszego uruchomienia 
    try:
        nr_trasy = lacza.ile_tras_nowe_trasy()
    except:
        nr_trasy = 0 
    lista_transportow=[]
    dt = datetime.now().date()

    if wykorzystanie_danych ==str(1):
        jutro = (date.today() + timedelta(days=1))
        for record in trasy:
            nr_trasy += 1
            
            for index,row in trasy[record].iterrows():
                if row['nazwa_kontrahenta'] in spedycja_df.values : #sprawdzenie miejscowosci
                    pozycja_przejazdu = (spedycja_df[spedycja_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']].index)[0] #wybranie wiersza w którym nastapila zgodnosc
                    if spedycja_df.loc[pozycja_przejazdu]['miejscowosc_dostawy'] == row['miejscowosc_dostawy'] : #sprawdzenie czy miejscowosc dostawy sie zgadza
                        status = "mieszany"
                    else:
                        status = "transport_wlasny"
                else :
                    status = "transport_wlasny"
                grouped_data.append(
            {'nr_trasy':nr_trasy,'data_dostawy': jutro, 'miejsce': row['miejscowosc_dostawy'], 'firma': row['nazwa_kontrahenta'], 'palety': row['ilosc_dostarczana'], 'samochod': record, 'koszt':0, 'km':row['km'], 'status':status})

        # Save the grouped data to CSV
        #with open(r'C:\Nowy_folder\output.csv', 'w', newline='') as file:
        #    writer = csv.DictWriter(file, fieldnames=keys)
        #    writer.writerows(grouped_data)

        # lacza.przesylka(r'C:\Nowy_folder\output.csv')
        #  MECHAINZM PRZYPISYWANIA PALET DO KLIENTOW ( DO POPRWAY JEZELI MIALBY DZIALAC ) START
        # for d1 in trasy:
        #     nr_trasy += 1
        #     samochod = (trasy[d1]['Samochod'])
        #     palety_samochod = (trasy[d1]['Palety'])
        #
        #     if len(trasy[d1]['Postoje']) == 1 and len(list(trasy[d1]['Postoje'].values())[0]) == 1: # jezeli jedzie do jednej miejscowosci do jednego punktu
        #
        #         miejscowosc = list(trasy[d1]['Postoje'].keys())[0]
        #         kontrahent = list(trasy[d1]['Postoje'].values())[0][0]
        #         palety_na_kursie = trasy[d1]['Palety']
        #         transport = [nr_trasy, miejscowosc, kontrahent, palety_na_kursie, samochod, dt, 0]
        #         lista_transportow.append(transport)
        #
        #     else:
        #         for d2 in (trasy[d1]['Postoje']): # przypisywanie do drobnicy
        #             postoje_df = transport_df2.where(transport_df2['miejscowosc_dostawy']==d2).dropna()
        #             kontrahent = (postoje_df['nazwa_kontrahenta'].max()) # uzyskania nazwy kontraheta
        #
        #             for d3 in trasy[d1]['Postoje'][d2]:
        #                 palety = postoje_df['ilosc_dostarczana'].where(postoje_df['nazwa_kontrahenta']==d3).dropna()
        #                 x = float(palety.max()) # uzyskanie wartosci palet, metoda max jest przypadkowa rownie dobrze moze byc min
        #
        #                 transport= [nr_trasy, d2, d3, x, samochod, dt,0]
        #
        #                 lista_transportow.append(transport)
    #  MECHAINZM PRZYPISYWANIA PALET DO KLIENTOW ( DO POPRWAY JEZELI MIALBY DZIALAC ) STOP

else:
    wykorzystanie_danych = 0


if len(spedycja_df) > 0:
    grouped_data2=[]
    print(spedycja_df)
    #wykorzystanie_danych_spedycja = "1"
    wykorzystanie_danych_spedycja = input("Na podstawie zaprezentowanych danych transportowych chcesz wygenerowac plik csv do spedycji?\n1. Tak\n2. Nie\n Wybor :")
    if wykorzystanie_danych_spedycja == str(1):
        # with open('spedycja.csv', 'w', newline='') as file:
        #     # Use the truncate() method to remove all data from the file
        #     file.truncate()
        for index, row in spedycja_df.iterrows():
            k = kalkulator_spedycja(km=row['km'], waga=row['waga'], palety=row['ilosc_dostarczana'])
            ilosc_palet = len(k[1])  # konieczność ustalenia ilosc palet w ten sposob poniewaz max waga palety w Raben to 1200 kg, w transporcie wlasnym nie ma takich ogranicznen.
            opis = ["302_G_3,", "302_G_3,", row['nazwa_kontrahenta'], '_', row['miejscowosc_dostawy'], ',',
                    datetime.now().date().strftime("%Y-%d-%m"), ',towar,ep,', ilosc_palet, ',120,80,150,',
                    row['waga'], ',fb+t,', 'nazwa_towaru,,,,,1,,,,,,,,,,,,,,,,,,,,Premium,']
            opis_2 = "".join(map(str, opis))
            print(opis_2)
            nr_trasy = "SPE_"+str(random.randint(1000000, 90000000))
            
            for ddd in grouped_data:
                print(791,ddd['miejsce'],len(ddd['miejsce']),row['miejscowosc_dostawy'],len(row['miejscowosc_dostawy']),ddd['firma'],len(ddd['firma']),row['nazwa_kontrahenta'],len(row['nazwa_kontrahenta']))
                print(792,ddd['miejsce'] == row['miejscowosc_dostawy'], ddd['firma'] == row['nazwa_kontrahenta'])
                if ddd['miejsce'] == row['miejscowosc_dostawy'] and ddd['firma'] == row['nazwa_kontrahenta']:
                    status = "mieszany"
                    break
                
                else:
                    status = "spedycja"

            grouped_data.append(
                    {'nr_trasy':nr_trasy,'data_dostawy': jutro, 'miejsce': row['miejscowosc_dostawy'], 'firma': row['nazwa_kontrahenta'], 'palety': row['ilosc_dostarczana'], 'samochod': 'Raben' , 'koszt':row['koszt_spedycji'], 'km':row['km'], 'status':status})
                
            #with open('spedycja.csv', mode='a', newline='') as file:
            #    writer = csv.writer(file)
            #    writer.writerow(opis_2.split(','))

else: # ustawienia odpowiedzi aby w naqstepnych liniach program sie nie wysypal
    wykorzystanie_danych_spedycja = 0

csv_file = 'your_data.csv'

# Open the CSV file in write mode and write the data
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f,delimiter=',', fieldnames=['nr_trasy','data_dostawy', 'miejsce', 'firma', 'palety', 'samochod' , 'koszt','km', 'status'])
    writer.writerows(grouped_data)

lacza.przesylka_nowe_trasy(csv_file)




##dodac mapke jak wyglada podzial tras + spedycji