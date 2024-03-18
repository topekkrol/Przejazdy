
import pandas as pd
import os
import operator

from datetime import datetime, date,timedelta
from Kalkulator_Raben import kalkulator_spedycja
from DoPSGl import PolaczenieBazy
from flota import Samochod
from WyszukiwarkaMakaronowa import wyszukanie
from flask import render_template, request
from trzeci_etap import sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym, compare_dictionaries, round_column_values_in_dict,filtr_najwiekszych_miejscowosci, usuwanie_podkreslenia
from __main__ import app

def rozwiazywania_rownania_a(b,plik):
    # przypisywanie wartosci do list. Podczas wyliczania odleglosci istnieje zmienna ktora moze być określona dopiero pod koniec ostatniej pętli.
    # Funckja rozwiazuje problem przypisujac konkretna wartość i usuwając element z list
    for m in plik:
        for elementy in plik[m]:
            try:
                wartosc = elementy[0] + max(b)
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
                                    a, koszty = rozwiazywania_rownania_a(a,koszty)


                    else:
                        a.append(koszty[miejscowosci][0])
                        a, koszty = rozwiazywania_rownania_a(a,koszty)


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
            a, koszty =rozwiazywania_rownania_a(a,koszty)

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

#funkcja sprawdzajaca czy logika nie trafila na szczegolny przypadek
def model_deflacyjny_dla_stworzonych_tras(nosnik_informacji_transportowych,koszt_km_w_funkcji,nosnik_informacji_spedycyjnej):
    #odczytywanie przejazdow z calosci wszystkich tras
    for przewiezienia in nosnik_informacji_transportowych:
        #odczytywanie miejscowosc dostawy
        for index, miejsce_docelowe in nosnik_informacji_transportowych[przewiezienia].iterrows():
            # warunek sprawdza czy to nie jest postoj
            if miejsce_docelowe['nazwa_kontrahenta']=='Postoj':
                continue

            #uzyskiwanie listy miejscowosci posrednich wraz z usunieciem miejscowosci dla ktorej bedziemy sprawdzali oplacalnosc
            lista_miejsc_dostarczania = list(nosnik_informacji_transportowych[przewiezienia]['miejscowosc_dostawy'])
            #warunek sprawdza czy miasto nie zostalo juz przeniesione
            if not miejsce_docelowe['miejscowosc_dostawy'] in lista_miejsc_dostarczania:
                continue
            
            #usuwanie duplikatow z listy
            lista_miejsc_dostarczania = list(set(lista_miejsc_dostarczania))
            lista_miejsc_dostarczania.remove(miejsce_docelowe['miejscowosc_dostawy'])
            
            if len(lista_miejsc_dostarczania) > 0:
                km_z_miastem_glownym = wyszukanie(zaczynamy='Rzeszow',konczymy=miejsce_docelowe["miejscowosc_dostawy"])[0]['km']
                #tutaj zostaje wprowadzona zmiana, obliczana jest wartosc polaczenia dla wszystkich towarow z danej miejscowosci, dzialanie wynika z usuwania miejscowosci z listy miast posrednich
                filtered_data = nosnik_informacji_transportowych[przewiezienia][nosnik_informacji_transportowych[przewiezienia]['miejscowosc_dostawy'] == miejsce_docelowe['miejscowosc_dostawy']]
                cala_waga = filtered_data['waga'].sum()
                cala_palety = filtered_data['ilosc_dostarczana'].sum()
                koszt_spedycji_z_miasta_glownego = kalkulator_spedycja(km=km_z_miastem_glownym,waga=cala_waga,palety=cala_palety)
                
                punkty_przeniesienia = 0
                #zdobywanie punktów przeniesienia
                for inne_miejscowosci in lista_miejsc_dostarczania:
                    #wyszukanie dziala do 4 polaczenia, dla zalozen normalnego dzialania programu nie bylo problemow. 
                    #Dla dzialania customowego z miejscowoscami ktore dodaje uzytkownik moga sie tworzyc waskie gardla i kalkulator logicznie moze ich nie obsluzyc
                    try:
                        km_pomiedzy_punktami = wyszukanie(zaczynamy=inne_miejscowosci,konczymy=miejsce_docelowe['miejscowosc_dostawy'])[0]['km']
                        km_pomiedzy_punktami += km_z_miastem_glownym
                        km_dla_polaczenia_bezposredniego = wyszukanie(zaczynamy='Rzeszow',konczymy=inne_miejscowosci)[0]['km']
                        km_pomiedzy_punktami = km_pomiedzy_punktami - km_dla_polaczenia_bezposredniego
                    except:
                        km_pomiedzy_punktami = 999

                    if km_pomiedzy_punktami*koszt_km_w_funkcji > koszt_spedycji_z_miasta_glownego[0]:
                        punkty_przeniesienia += 1
                
                punkty_przeniesienia -= len(lista_miejsc_dostarczania)
                #warunek przeniesienia
                if punkty_przeniesienia == 0:
                    warunek_usuniecia = (nosnik_informacji_transportowych[przewiezienia]['nazwa_kontrahenta'] == miejsce_docelowe['nazwa_kontrahenta']) & \
                                    (nosnik_informacji_transportowych[przewiezienia]['miejscowosc_dostawy'] == miejsce_docelowe['miejscowosc_dostawy']) & \
                                    (nosnik_informacji_transportowych[przewiezienia]['ilosc_dostarczana'] == miejsce_docelowe['ilosc_dostarczana']) & \
                                    (nosnik_informacji_transportowych[przewiezienia]['waga'] == miejsce_docelowe['waga'])

                    nosnik_informacji_transportowych[przewiezienia] = nosnik_informacji_transportowych[przewiezienia].drop(nosnik_informacji_transportowych[przewiezienia][warunek_usuniecia].index) # usunięcie wiersza
                    testing_df = pd.DataFrame([miejsce_docelowe], columns=nosnik_informacji_spedycyjnej.columns)
                    #ustalenie nowych kosztow dostawy poniewaz poprzednie byly obliczone sumarycznego towaru dla miejscowosci
                    koszt_spedycji_z_miasta_glownego = kalkulator_spedycja(km=km_z_miastem_glownym,waga=miejsce_docelowe['waga'],palety=miejsce_docelowe['ilosc_dostarczana'])
                    koszt_spedycji_testowy = round(koszt_spedycji_z_miasta_glownego[0])
                    testing_df.reset_index(drop=True, inplace=True)
                    testing_df.loc[0, 'koszt_spedycji'] = koszt_spedycji_testowy
                    nosnik_informacji_spedycyjnej = pd.concat([testing_df, nosnik_informacji_spedycyjnej], ignore_index=True) # wysylka do spedycji

    return nosnik_informacji_spedycyjnej,nosnik_informacji_transportowych

#funkcja sprawa czy jakas miejscowosc nie zablakala sie do innej df a mozna ja zawiezc w innej trasie taniej poniewz auto przejezdza przez ta miejscowosc
def sprawdzenie_czy_nie_taniej_bedzie_przeniesc_pomiedzy_przejazdami(transportowy_df):
    
    for dejtafrejmy in transportowy_df:
        dane_o_aucie = Samochod.dane_auta(nr_rej=dejtafrejmy)
        ile_palet_na_aucie = int(transportowy_df[dejtafrejmy]['ilosc_dostarczana'].sum())
        ile_miejsca_na_aucie = dane_o_aucie - ile_palet_na_aucie

        if ile_miejsca_na_aucie == 0:
            continue
        for dejtafrejmy_do_rozlozenia in transportowy_df:

            if dejtafrejmy == dejtafrejmy_do_rozlozenia:
                continue

            for index,row in transportowy_df[dejtafrejmy_do_rozlozenia].iterrows():
                if ile_miejsca_na_aucie <= row['ilosc_dostarczana']:
                    continue


                if (transportowy_df[dejtafrejmy]==row['miejscowosc_dostawy']).any().any():
                    warunek_usuniecia = (transportowy_df[dejtafrejmy_do_rozlozenia]['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
                                        (transportowy_df[dejtafrejmy_do_rozlozenia]['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
                                        (transportowy_df[dejtafrejmy_do_rozlozenia]['ilosc_dostarczana']== row['ilosc_dostarczana']) & \
                                        (transportowy_df[dejtafrejmy_do_rozlozenia]['waga'] == row['waga'])

                    dataframe_z_usunietym = transportowy_df[dejtafrejmy_do_rozlozenia].drop(transportowy_df[dejtafrejmy_do_rozlozenia][warunek_usuniecia].index)  # usuniecie z df spedycyjnego  

                    dodanie_drobnicy = pd.DataFrame([row],columns=transportowy_df[dejtafrejmy_do_rozlozenia].columns)
                    przejazd = pd.concat([dodanie_drobnicy, transportowy_df[dejtafrejmy]], ignore_index=True)
                    transportowy_df[dejtafrejmy] = przejazd
                    transportowy_df[dejtafrejmy_do_rozlozenia] = dataframe_z_usunietym
                    return transportowy_df
    
    return transportowy_df

@app.route('/trasy_do_realizacji')
def trasy_do_realizacji():
    try:
        os.remove('nowy_2spedycja.csv')
    except:
        pass

    lacza = PolaczenieBazy() # polaczenie z baza danych faktur
    Samochod.odczytaj_z_pliku_wszystkie() # wczytanie danych samochodowych
    #lacza.generowanie_towaru_custome() # tworzenie dokumentow aby moc zaprezentowac dzialanie programu
    dane = lacza.get_values_custome(status='testowania')
    df = pd.DataFrame(dane, columns=['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana','waga'])
    df_do_wyswietlenia = df.copy()
    koszty_pokonania_km = 7
    koszty = przypisywanie_wartosci_bezposredniego_polaczenia(df)

    koszty_dostawy = koszty_odleglosci('Rzeszow',koszty,koszty_pokonania_km) # uzyskanie ceny dostawy przez BOZ

    koszty_dostawy = koszty_spedycji(df,koszty_dostawy)
    pierwotne_koszty_dostawy = koszty_dostawy

    dostawa_boz , dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy,koszty) # uzyskujemy podział na biblioteke i liste zawierajace odpowiednio lista rzeczy do transportu przez boz badz   spedycje
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

        #df = df.drop(df[df['miejscowosc_dostawy'] == miejsce].index, inplace=True)
        df.drop(df[df['miejscowosc_dostawy'] == miejsce].index, inplace=True)

        #df = df.reset_index(drop=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        spedycja_df.reset_index(drop=True, inplace=True)

        if int(df['ilosc_dostarczana'].sum()) <= Samochod.wyswietl_wage_i_palety()[1]: # sprawdzenie czy po usunięciu ostatniej miejscowości nie zostało za dużo miejsca na aucie, jeżeli cos zostało   sprawdza z ostaniej miejscowości możliwości doładunkowe i przenoisi wiersze pomiędzy df
            for y in range (len(x.sort_values(by=['ilosc_dostarczana'],ascending=False))): # wystwietlenie danych z ostatniej miejscowosci w pojedynczych 'wierszach'

                testing = x.iloc[y] # wewnetrzna zmienna, przechowujaca dane o wskazanym wierszu, stworzone dla wygody.
                ilosc_na_series = (x.iloc[y, :]['ilosc_dostarczana'])
                ilosc_do_doladowania = (Samochod.wyswietl_wage_i_palety()[1] - df['ilosc_dostarczana'].sum())

                if ilosc_do_doladowania > 0: # sprawdzenie czy poprzedni rekord w funkcji for nie spełnił warunki, po próbie zmiany warunki if na while generowało zle wyniki
                    warunek_usuniecia = (spedycja_df['nazwa_kontrahenta'] == testing['nazwa_kontrahenta']) & \
                                        (spedycja_df['miejscowosc_dostawy'] == testing['miejscowosc_dostawy']) & \
                                        (spedycja_df['ilosc_dostarczana'] == testing['ilosc_dostarczana']) & \
                                        (spedycja_df['waga'] == testing['waga'])  # potwierdzenie wszystkich zmiennych aby mieć pewność że usuwamy napewno właściwy wiersz


                    if ilosc_na_series > ilosc_do_doladowania: # w przypadku kiedy do jednego klienta jest wiecej towaru niż miejsca na samochodzie, dzieli towar na max wypelnienie samochodu a reszta     do wysylki spedycha

                        doladowanie = ilosc_na_series - ilosc_do_doladowania  # ustalenie ilości przelowowej pomiędzy df
                        # dodanie przeliczaniwa wag
                        nowa_waga_transport = (ilosc_do_doladowania/ilosc_na_series) *(x.iloc[y, :]['waga'])
                        nowa_waga_spedycja = (x.iloc[y, :]['waga']) - nowa_waga_transport
                        
                        spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index) # usunięcie wiersza
                        testing.update(pd.Series([doladowanie], index=['ilosc_dostarczana'])) # ustalenia nowej wartości dla wracjacych danych do spedycji, wprowadziłem zmiane pod importem pandas
                        testing['waga'] = nowa_waga_spedycja
                        # spedycja_df = spedycja_df.append(testing) # wysylka do spedycji
                        testing_df = pd.DataFrame([testing], columns=spedycja_df.columns)
                        spedycja_df = pd.concat([testing_df, spedycja_df], ignore_index=True) # wysylka do spedycji
                        testing['ilosc_dostarczana'] = ilosc_do_doladowania#  ustalenie wartosci dla df transportowego
                        testing['waga'] = nowa_waga_transport

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
                #x_df = pd.DataFrame([x], columns=spedycja_df.columns)
                spedycja_df = pd.concat([x, spedycja_df], ignore_index=True) # przeniesienie wiersza do właściwej df
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

    #transport_df.sort_values(by=['km', 'miejscowosc_dostawy','ilosc_dostarczana'],ascending=False,inplace=True)
    lista_miast_z_najwieksza_iloscia = filtr_najwiekszych_miejscowosci(transport_df)
    transport_df['miejscowosc_dostawy'] = pd.Categorical(transport_df['miejscowosc_dostawy'], categories=lista_miast_z_najwieksza_iloscia, ordered=True)
    # Posortuj DataFrame według kategorii
    transport_df = transport_df.sort_values(by=['miejscowosc_dostawy','ilosc_dostarczana'], ascending=[True, False])
    #transport_df.sort_values(by=['km', 'miejscowosc_dostawy'],ascending=True,inplace=True)
    transport_df.reset_index(drop=True, inplace=True)
    trasy={}

    for index , row in transport_df.iterrows(): # przypisanie drobnicy do transportów#
        transport_df.reset_index(drop=True, inplace=True)

        try:
            for przejazdy in trasy:
                postoje = []
                #warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1])
                #test stworzenia nowego warunku usuniecia
                warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
                                    (transport_df['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
                                    (transport_df['ilosc_dostarczana'] == row['ilosc_dostarczana']) & \
                                    (transport_df['waga'] == row['waga']) 
                #test stworzenia nowego warunku usuniecia
                ilosc_palet_na_zleceniu = int(trasy[przejazdy]['ilosc_dostarczana'].sum())

                if ilosc_palet_na_zleceniu == 0: #  warunek sprawdz ile jest palet do transportu
                    continue

                ciezarowka = Samochod.dane_auta(nr_rej=przejazdy)
                procent_obciazenia = (ciezarowka - ilosc_palet_na_zleceniu)/row.iloc[2]
                #pierwszy warunek sprawdza czy procent obciążenia nie jest równy 0, drugi czy towar nie został wcześniej dodany do innego zlecenia
                #jest to pokrecona logika
                if not transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row['nazwa_kontrahenta']],'miejscowosc_dostawy':[row['miejscowosc_dostawy']],'ilosc_dostarczana':  [row['ilosc_dostarczana']]}).any().all()\
                    or \
                        procent_obciazenia == 0:
                    continue

                else: # tutaj wpadaja wszystkie przypadki mające coś do zawiezienia
                    if procent_obciazenia > 1 :
                        procent_obciazenia = 1.0

                    lista_postoi = trasy[przejazdy]['miejscowosc_dostawy'].tolist()
                    lista_postoi = list(dict.fromkeys(lista_postoi)) # usuniecie duplikatów z listy postoi
                    #if trasy[przejazdy]['miejscowosc_dostawy'].isin([row.iloc[1]])[0].any() or len(trasy) >= Samochod.count_objects(): # pierwszy warunek sprawdza czy wyszukiwana miejscowosc jest w   postojach, drugi czy ilość użytych samochodow nie jest rowna max. Trzeci warunek sprawdza czy analizowany przypadek trasy jest ostatnią trasą.
                    if list(trasy[przejazdy]['miejscowosc_dostawy'].isin([row['miejscowosc_dostawy']]))[0]: # pierwszy warunek sprawdza czy wyszukiwana miejscowosc jest w   postojach.    
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
                            transport_df = pd.concat([transport_df,new_record], ignore_index=True)
                            
                            if row['km']*koszty_pokonania_km < kalkulator_spedycja(row['km'],row['waga'],row['ilosc_dostarczana'])[0]:
                                #warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1])
                                #test stworzenia nowego warunku usuniecia
                                warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
                                    (transport_df['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
                                    (transport_df['ilosc_dostarczana'] == row['ilosc_dostarczana']) & \
                                    (transport_df['waga'] == row['waga'])  
                                #test stworzenia nowego warunku usuniecia
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
                            
                            if polaczenia_z_przystankiem_km < row.iloc[4]: # sprawdzenie czy km z polaczenia z ktorymz punktow sa mniejsze niz bezposrednie polaczenie z Rzeszowa.
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
                            
                        #pierwszy warunek sprawdza czy nie jest to ostatnia możliwa do stworzenia trasa, a inne nie warunki nie stwarzaja mozliwosc utworzenia trasy. Drugi warunek sprawdza czy towar  nie zostal juz dodany do innego zlecenia.
                        if len(trasy) == list(trasy).index(przejazdy)+1 and transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],  'ilosc_dostarczana':[row.iloc[2]]}).any().all():
                                warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
                                    (transport_df['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
                                    (transport_df['ilosc_dostarczana'] == row['ilosc_dostarczana']) & \
                                    (transport_df['waga'] == row['waga']) 
                                raise Exception

            if transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row['nazwa_kontrahenta']],'miejscowosc_dostawy':[row['miejscowosc_dostawy']],'ilosc_dostarczana':  [row['ilosc_dostarczana']]}).any().all(): # warunek sprawdza czy wartosc dalej jest w df_transportowym
                #warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row.iloc[0]) & (transport_df['miejscowosc_dostawy'] == row.iloc[1])  # warunek usunieci musi tez byc utworzony w tym miejscu w    przypadku pierwszej trasy
                #test
                warunek_usuniecia = (transport_df['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
                                    (transport_df['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
                                    (transport_df['ilosc_dostarczana'] == row['ilosc_dostarczana']) & \
                                    (transport_df['waga'] == row['waga']) 
                #test
                postoje = [] # to samo z postojami, czysty wymóg pierwszej trasy
                try:
                    koszt_dostaw_spedycja = wyszukanie(zaczynamy='Rzeszow',konczymy=row['nazwa_kontrahenta'])[0]
                except:
                    koszt_dostaw_spedycja = row['km']*koszty_pokonania_km+1

                if koszt_dostaw_spedycja > row['km']*koszty_pokonania_km:
                    raise Exception

        except RuntimeError as r:
            continue

        except Exception as e:
            
            if len(trasy) == Samochod.count_objects():
                if (transport_df[['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana']].isin({'nazwa_kontrahenta':[row.iloc[0]],'miejscowosc_dostawy':[row.iloc[1]],'ilosc_dostarczana':[row. iloc[2]]}).any().all()) == False: # po odrzuceniu resztki z dolodawanie nie da sie na jej podstawie stworzyc transportu ( maksymalan liczba samochodow ) reszta muszi wrocic do  transportu
                    row_df = pd.DataFrame([row])
                    transport_df = pd.concat([transport_df,row_df], ignore_index=True)
                pass

            else:

                #transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) # usuniecie z df elementu rozwazanego
                #transport_df = transport_df.drop(transport_df[transport_df[warunek_usuniecia]].index)# usuniecie z df elementu rozwazanego
                transport_df = transport_df.drop(transport_df[warunek_usuniecia].index) 
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
        koszt_spedycji = round(kalkulator_spedycja(km=km, waga=waga, palety=palety)[0])
        row['koszt_spedycji'] = koszt_spedycji
        row['km'] = km
        row_df = pd.DataFrame([row])
        spedycja_df = pd.concat([row_df, spedycja_df], ignore_index=True)

    try:
        spedycja_df.dropna(inplace=True)
        spedycja_df.sort_values(by='km',ascending=True,inplace=True)
        spedycja_df.reset_index(drop=True, inplace=True)
    except:
        spedycja_df = spedycja_df


    # ostatnie wirowanie
    bezpiecznik = 0
    
    while True:
        #sprawdzenie aby pętla while nie leciała w nieskończoność
        print(677,trasy,spedycja_df) 
        trasy0 = trasy.copy()
        spedycja0 = spedycja_df.copy()
        trasy, spedycja_df = sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy_do_przyjcia = trasy, spedycje_do_sprawdzenia = spedycja_df, ile_kosztuje_km = koszty_pokonania_km)
        print(684,trasy,spedycja_df) 
        spedycja_df, trasy = model_deflacyjny_dla_stworzonych_tras(nosnik_informacji_transportowych = trasy, nosnik_informacji_spedycyjnej = spedycja_df, koszt_km_w_funkcji = koszty_pokonania_km)
        print(686,trasy,spedycja_df) 
        trasy = sprawdzenie_czy_nie_taniej_bedzie_przeniesc_pomiedzy_przejazdami(trasy)
        print(688,trasy,spedycja_df) 
        if compare_dictionaries(trasy0,trasy) and spedycja0.equals(spedycja_df):
            break
        
        elif bezpiecznik > 5:
            break
        
        else:
            bezpiecznik += 1

    #usuwanie postoi, wag i resetowanie indexow
    for przejazd in trasy:
        trasy[przejazd] = trasy[przejazd][trasy[przejazd]['nazwa_kontrahenta'] != 'Postoj']
        trasy[przejazd] = trasy[przejazd].drop(columns=['waga'])
        trasy[przejazd].reset_index(drop=True, inplace=True)

    trasy = round_column_values_in_dict(trasy)
    #usuniecie kolumny waga
    spedycja_df = spedycja_df.drop(columns=['waga'])
    #lacza.usuniecie_testow()

    spedycja_df = usuwanie_podkreslenia(spedycja_df)

    for odczytanie_dla_usuiecia_podkreslen in trasy:
        trasy[odczytanie_dla_usuiecia_podkreslen] = usuwanie_podkreslenia(trasy[odczytanie_dla_usuiecia_podkreslen])

    return render_template('trasy-flex-aaa.html', towar_wyswietlenie=df_do_wyswietlenia,transportwe_informacje=trasy,spedycyjne_informacje=spedycja_df)
