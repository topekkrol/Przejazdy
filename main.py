import time

from WyszukiwarkaMakaronowa import wyszukanie
import pandas as pd
pd.options.mode.chained_assignment = None

from Kalkulator_Raben import kalkulator_spedycja
from DoPSGl import PolaczenieBazy
import operator
from flota import Samochod
from datetime import datetime
import csv
from datetime import date,timedelta

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


lacza = PolaczenieBazy() # polaczenie z baza danych faktur
Samochod.odczytaj_z_pliku_wszystkie() # wczytanie danych samochodowych
dane = lacza.get_values(status='planowana')
df = pd.DataFrame(dane, columns=['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana','waga'])
koszty_pokonania_km = 7

if len(df) == 0:
    lacza.generowanie_towaru()
    dane = lacza.get_values()
    df = pd.DataFrame(dane, columns=['nazwa_kontrahenta', 'miejscowosc_dostawy', 'ilosc_dostarczana', 'waga'])
print(df)
koszty = przypisywanie_wartosci_bezposredniego_polaczenia(df)

koszty_dostawy = koszty_odleglosci('Rzeszow',koszty,koszty_pokonania_km) # uzyskanie ceny dostawy przez BOZ

koszty_dostawy = koszty_spedycji(df,koszty_dostawy)
pierwotne_koszty_dostawy = koszty_dostawy

dostawa_boz , dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy,koszty) # uzyskujemy podział na biblioteke i liste zawierajace odpowiednio lista rzeczy do transportu przez boz badz spedycje

spedycja_df =pd.DataFrame(columns=['nazwa_kontrahenta', 'miejscowosc_dostawy', 'ilosc_dostarczana', 'waga'])

i = 0

while len(dostawa_spedycja)>0: # przenoszenie do spedycyjnego df

    i+=1
    for spedycyjne in dostawa_spedycja: # przeniesienie elementów pomiedzy df wysyłanych spedycją
        x =df.where(df['miejscowosc_dostawy'] == spedycyjne).dropna() # wycięcie wiersza do przeniesienia

        # spedycja_df = spedycja_df.append(x) # przeniesienie wiersza do właściwej df
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


for index, row in df.iterrows():

    row['km'] =dostawa_boz[row['miejscowosc_dostawy']][0] # uzyskanie km dla miejscowosci

    row_df = pd.DataFrame([row],columns=transport_df.columns)
    transport_df = pd.concat([transport_df,row_df],ignore_index=True)

transport_df.sort_values(by=['km', 'miejscowosc_dostawy'],ascending=False,inplace=True)
transport_df.reset_index(drop=True, inplace=True)

trasy={}
licznik_tras = 0 # licznik tras

while len(transport_df.where(transport_df['ilosc_dostarczana'] >= Samochod.max_palety(licznik_tras)[1]).dropna()) > 0: # przypisanie tylko dla pełnych samochodów
    y = len(transport_df.where(transport_df['ilosc_dostarczana'] >= Samochod.max_palety(licznik_tras)[1]).dropna())
    df_calosowamochodpwy = transport_df.where(transport_df['ilosc_dostarczana'] >= Samochod.max_palety(licznik_tras)[1]).dropna() # konieczność zresetowania indeksow poniewaz posiadaja wartosci cora df
    df_calosowamochodpwy.reset_index(drop=True, inplace=True)

    for _ in range(y):

        wycienek = df_calosowamochodpwy.loc[_] # linia która jest rozwazana w aspekcie transportowym

        nowa_ilosc = wycienek['ilosc_dostarczana'] - Samochod.max_palety(licznik_tras)[1] #obliczanie nowej ilosci pomniejszonej o w pelni zaladowany samochod

        warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == wycienek['nazwa_kontrahenta']) & \
                            (transport_df['miejscowosc_dostawy'] == wycienek['miejscowosc_dostawy']) # ustalenie warunkow do usuniecia pozycji z df
        transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) # usuniecie pozycji z df
        if nowa_ilosc >0:
            wycienek.update(pd.Series([nowa_ilosc], index=['ilosc_dostarczana'])) # ustawienowej nowej ilosci dostarczanych palet
            # transport_df = transport_df.append(wycienek) # dodanie palet ktore sie nie zmiescily do df
            testing_df_2 = pd.DataFrame([testing], columns=df.columns)
            transport_df = pd.concat([wycienek, testing_df_2], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df
        postoje = {} # format miejsc postojowych
        postoje[wycienek['miejscowosc_dostawy']] = [wycienek['nazwa_kontrahenta']] # dodaniej miejsc postojowych do formatu przechowujacego wskazane dane

        przejazd = {
        'Postoje' : postoje,
        'Palety' : Samochod.max_palety(licznik_tras)[1],
        'Km' : 0,
        'Samochod' : Samochod.max_palety(licznik_tras)[0]
        } # format przejazdu

        trasy[licznik_tras] = przejazd # doddanie przejazdu do wszystkich tras
        licznik_tras+=1 # licznik tras
        transport_df.sort_values(by='km', ascending=False, inplace=True) # posortowanie wartosci  w df
        transport_df.reset_index(drop=True, inplace=True) # zresetowanie indexow w df



for index , row in transport_df.iterrows(): # przypisanie drobnicy do transportów
    postoje = {}
    
    try:
        trasy[0] # warunek wyzwalajcy blad w przypadku kiedy nie ma innych tras
        for przejazdy in trasy:
            warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row[0]) & \
                        (transport_df['miejscowosc_dostawy'] == row[1])  # ustalenie warunkow do usuniecia pozycji z df
            if trasy[przejazdy]['Palety'] == 0.0:
                continue

            procent_obciazenia = (Samochod.max_palety(przejazdy)[1] -trasy[przejazdy]['Palety'])/row[2]

            if procent_obciazenia == 0:
                if len(trasy) ==przejazdy+1:
                    raise Exception
                continue


            if procent_obciazenia > 1 :
                procent_obciazenia = 1.0

            if not (transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row[0]],'miejscowosc_dostawy':[row[1]],'ilosc_dostarczana':[row[2]]}).any().all()): # warunek sprawdzający czy poprzednia pętla nie obsłużyła zapytania
                continue


            if row[1] in trasy[przejazdy]['Postoje'] or licznik_tras >= Samochod.count_objects() and list(trasy).index(przejazdy) >= len(trasy): # pierwszy warunek sprawdza czy wyszukiwana miejscowosc jest w postojach, drugi czy ilość użytych samochodow nie jest rowna max. Trzeci warunek sprawdza czy analizowany przypadek trasy jest ostatnią trasą.

                transport_df = transport_df.drop(transport_df[warunek_usuniecia].index)  # usuniecie z df elementu rozwazanego
                try:
                    postoje = trasy[przejazdy]['Postoje']
                    lista_kontrahentow = postoje[row[1]]
                    lista_kontrahentow.append([row[0]][0])

                    postoje[row[1]] = lista_kontrahentow
                except:
                    postoje[row[1]] = [row[0]]

                palety = trasy[przejazdy]['Palety']

                palety += row[2]*procent_obciazenia
                przejazd = {
                    'Postoje': postoje,
                    'Palety': palety,
                    'Km': 0,
                    'Samochod': Samochod.max_palety(przejazdy)[0]
                }
                trasy[przejazdy] = przejazd

                if procent_obciazenia < 1:

                    row.update(
                        pd.Series([row['ilosc_dostarczana'] - row['ilosc_dostarczana'] * procent_obciazenia],index=['ilosc_dostarczana']))  # ustawienowej nowej ilosci dostarczanych palet
                    new_record = pd.DataFrame([row])

                    if row['km']*koszty_pokonania_km < kalkulator_spedycja(row['km'],row['waga'],row['ilosc_dostarczana'])[0]:
                        postoje ={}
                        raise Exception

                    else:
                        transport_df = pd.concat([new_record, transport_df], ignore_index=True)
                    continue

                else:
                    break
                continue 

            else:
                print(449,trasy[przejazdy]['Postoje'])
                for p in trasy[przejazdy]['Postoje']: # wczytywanie wszyskich miejsc w postojach
                    print(451,p)
                    polaczenia_z_przystankiem = wyszukanie(row[1],p)

                    try:
                        polaczenia_z_przystankiem_km = polaczenia_z_przystankiem[0]['km'] # uzyskanie km, przy braku wyniuku ustalona zostaje nierealna wartosc
                    except:
                        polaczenia_z_przystankiem_km = 999 # nierealna wartosc
                    if wyszukanie(row[1],p)[0]['km'] < row[4]: # sprawdzenie czy km z polaczenia z ktorymz punktow sa mniejsze niz bezposrednie polaczenie z Rzeszowa.
                        transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) # usuniecie z df
                        postoje = trasy[przejazdy]['Postoje']
                        postoje[row[1]] = [row[0]]

                        palety = trasy[przejazdy]['Palety']
                        palety += row[2]*procent_obciazenia
                        przejazd = {
                            'Postoje': postoje,
                            'Palety': palety,
                            'Km': 0,
                            'Samochod': Samochod.max_palety(przejazdy)[0]
                        }
                        trasy[przejazdy] = przejazd
                        if procent_obciazenia < 1:
                            row.update(
                                pd.Series([row['ilosc_dostarczana'] - row['ilosc_dostarczana'] * procent_obciazenia],
                                          index=['ilosc_dostarczana']))  # ustawienowej nowej ilosci dostarczanych palet
                            # transport_df = transport_df.append(row)  # dodanie palet ktore sie nie zmiescily do df

                            row_df = pd.DataFrame([row], columns=transport_df.columns)
                            transport_df = pd.concat([row_df, transport_df], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df

                if len(trasy) ==przejazdy+1:
                    raise Exception

    except RuntimeError as r:
        continue

    except Exception as e:
        if licznik_tras == Samochod.count_objects():
            if (transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row[0]],'miejscowosc_dostawy':[row[1]],'ilosc_dostarczana':[row[2]]}).any().all()) == False: # po odrzuceniu resztki z dolodawanie nie da sie na jej podstawie stworzyc transportu ( maksymalan liczba samochodow ) reszta muszi wrocic do transportu
                row_df = pd.DataFrame([row])
                transport_df = pd.concat([transport_df,row_df], ignore_index=True)
            pass

        else:
            # transport_df = transport_df.drop(transport_df[warunek_usuniecia].index)  # usuniecie z df elementu rozwazanego
            transport_df = transport_df.drop(transport_df.loc[warunek_usuniecia].index) # usuniecie z df elementu rozwazanego
            postoje[row[1]] = [row[0]]  # dodaniej miejsc postojowych do formatu przechowujacego wskazane dane
            cos_klikam = wyszukanie('Rzeszow', row[1])[0]

            try:
                postoje[cos_klikam['Przystanek']] = []

            except:
                postoje=postoje

            try:
                postoje[cos_klikam['Przystanek_1']] = []
                postoje[cos_klikam['Przystanek_2']] = []
                postoje[cos_klikam['Przystanek_3']] = []

            except:
                postoje = postoje

            przejazd = {
                'Postoje': postoje,
                'Palety': row[2],
                'Km': 0,
                'Samochod': Samochod.max_palety(licznik_tras)[0]
                }
            trasy[licznik_tras] = przejazd
            licznik_tras += 1
print(508,transport_df)
print(509,trasy)
if len(transport_df) > 0:
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
    spedycja_df.reset_index(drop=True, inplace=True)
    spedycja_df.sort_values(by='km',ascending=True,inplace=True)
except:
    spedycja_df = spedycja_df


dl_speydcji = len(spedycja_df)

while dl_speydcji > 0: # sprawdzanie czy pozycje z spedycji nie są możliwe do doładowaniaI
    dl_speydcji = len(spedycja_df) # ustalanie długosci, sprawdza czy petla wykonala operacje
    for powrot_z_trasy in trasy: # czytanie tras
        for index, row in spedycja_df.iterrows():
            postoje_lista = list(trasy[powrot_z_trasy]['Postoje']) # zmienienie dict na list do uzytku
            postoje = trasy[powrot_z_trasy]['Postoje'] # wczytanie postoi
            palety_na_powrocie = int(Samochod.dane_auta(trasy[powrot_z_trasy]['Samochod'])) - int(trasy[powrot_z_trasy]['Palety']) # obliczenie palet na powrocie, dla kazdego klient musi zostac obliczona na nowo
            if palety_na_powrocie == 0:
                continue

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

update_nowe_trasy = usun_puste(trasy)
nowe_trasy = remove_duplicates(update_nowe_trasy)


if len(nowe_trasy) > 0:
    for linie in nowe_trasy:
        print(nowe_trasy[linie])
    print("spedycja :",spedycja_df)
    wykorzystanie_danych = input("Na podstawie zaprezentowanych danych transportowych chcesz utworzyć zlecenia transportowe?\n1. Tak\n2. Nie\n Wybor :")
    nr_trasy = lacza.ile_tras()
    lista_transportow=[]
    dt = datetime.now().date()

    if wykorzystanie_danych ==str(1):
        keys = ['nr_trasy','data_dostawy', 'miejsca', 'firmy', 'palety', 'samochod','km']
        grouped_data = []
        jutro = (date.today() + timedelta(days=1))
        for record in nowe_trasy:
            nr_trasy += 1
            postoje = nowe_trasy[record]['Postoje']
            palety = nowe_trasy[record]['Palety']
            samochod = nowe_trasy[record]['Samochod']

            miejsca = ';'.join(postoje.keys())
            firmy = ';'.join([';'.join(v) for v in postoje.values()])

            grouped_data.append(
                {'nr_trasy':nr_trasy,'data_dostawy': jutro, 'miejsca': miejsca, 'firmy': firmy, 'palety': palety, 'samochod': samochod,'km':0})

        # Save the grouped data to CSV
        with open(r'C:\Nowy_folder\output.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writerows(grouped_data)

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
    print(spedycja_df)
    wykorzystanie_danych_spedycja = input("Na podstawie zaprezentowanych danych transportowych chcesz wygenerowac plik csv do spedycji?\n1. Tak\n2. Nie\n Wybor :")
    if wykorzystanie_danych_spedycja == str(1):
        with open('spedycja.csv', 'w', newline='') as file:
            # Use the truncate() method to remove all data from the file
            file.truncate()
        for index, row in spedycja_df.iterrows():
            k = kalkulator_spedycja(km=row['km'], waga=row['waga'], palety=row['ilosc_dostarczana'])
            ilosc_palet = len(k[1])  # konieczność ustalenia ilosc palet w ten sposob poniewaz max waga palety w Raben to 1200 kg, w transporcie wlasnym nie ma takich ogranicznen.
            opis = ["302_G_3,", "302_G_3,", row['nazwa_kontrahenta'], '_', row['miejscowosc_dostawy'], ',',
                    datetime.now().date().strftime("%Y-%d-%m"), ',plytki,ep,', ilosc_palet, ',120,80,150,',
                    row['waga'], ',fb+t,', 'plytki,,,,,1,,,,,,,,,,,,,,,,,,,,Premium,']
            opis_2 = "".join(map(str, opis))
            with open('spedycja.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(opis_2.split(','))
        print("Dane zapisane w pliku spedycja.csv")
else: # ustawienia odpowiedzi aby w nastepnych liniach program sie nie wysypal
    wykorzystanie_danych_spedycja = 0

if wykorzystanie_danych == str(1) and wykorzystanie_danych_spedycja ==  str(1):
    lacza.przesylka(r'C:\Nowy_folder\output.csv')
    for index, rows in spedycja_df.iterrows():
        zmiana_statusu_warunek = f"miejscowosc_dostawy = '{rows['miejscowosc_dostawy']}' AND nazwa_kontrahenta = '{rows['nazwa_kontrahenta']}' AND status = 'przetwarzanie_danych' AND (SELECT SUM(ilosc_dostarczana) FROM dokumenty WHERE miejscowosc_dostawy = '{rows['miejscowosc_dostawy']}' AND nazwa_kontrahenta = '{rows['nazwa_kontrahenta']}' AND status = 'przetwarzanie_danych') = {rows['ilosc_dostarczana']};"

        if PolaczenieBazy().zmiana_statusu(status="spedycja", warunek_dniowy=zmiana_statusu_warunek) == 0:
            zmiana_statusu_warunek = f"miejscowosc_dostawy = '{rows['miejscowosc_dostawy']}' AND nazwa_kontrahenta = '{rows['nazwa_kontrahenta']}' AND status = 'przetwarzanie_danych' ;"
            PolaczenieBazy().zmiana_statusu(status="dostawa_mieszana", warunek_dniowy=zmiana_statusu_warunek)

    PolaczenieBazy().zmiana_statusu(warunek_dniowy="status = 'przetwarzanie_danych'", status="transport_wlasny")

if len(spedycja_df) == 0 and wykorzystanie_danych == str(1): # ustawienie status w sytuacji kiedy nie ma żadnych spedycji
    PolaczenieBazy().zmiana_statusu(warunek_dniowy="status = 'przetwarzanie_danych'", status="transport_wlasny")
    # zmiana wszystkich statusów planowanych na transport wlasny
elif len(trasy) == 0 and wykorzystanie_danych_spedycja == str(1): # ustawienie statusu w sytuacji kiedy nie ma żadnych transportow
    PolaczenieBazy().zmiana_statusu(warunek_dniowy="status = 'przetwarzanie_danych'", status="spedycja")
    print("Obsługa status jest możliwa tylko przy obsłudze wszystkich dokumentów do rozważenia.")

PolaczenieBazy().zmiana_statusu(warunek_dniowy="status = 'przetwarzanie_danych'", status="planowana")



### czesci z nowy_mail:
if wykorzystanie_danych == str(1) and wykorzystanie_danych_spedycja ==  str(1): # dwa razy tak
    for ride in trasy:
        print(trasy[ride])
        for index,row in trasy[ride].iterrows():
            print(790,row)
            if row['nazwa_kontrahenta'] in spedycja_df.values : #sprawdzenie miejscowosci
                pozycja_przejazdu = (spedycja_df[spedycja_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']].index)[0] #wybranie wiersza w którym nastapila zgodnosc
                if spedycja_df.loc[pozycja_przejazdu]['miejscowosc_dostawy'] == row['miejscowosc_dostawy'] : #sprawdzenie czy miejscowosc dostawy sie zgadza
                    status = "mieszany"
                else:
                    status = "transport_wlasny"
            else :
                status = "transport_wlasny"
            print(status)
    #tutaj trzeba dopisac cos niecos o spedycja.df

elif wykorzystanie_danych == str(1) and wykorzystanie_danych_spedycja !=  str(1): # transport wlasny tak, spedycja nie
    for ride in trasy:
        for index,row in trasy[ride].iterrows():
            print(790,row)
            status = "transport_wlasny"
            print(status)

elif wykorzystanie_danych != str(1) and wykorzystanie_danych_spedycja ==  str(1): # transport wlasny nie, spedycja tak
    #tutaj trzeba dopisac o sprawdzeniu czy warunek juz nie zostal obsluzony
    for index,row in spedycja_df.iterrows():
        print(row)
        status ="spedycja"