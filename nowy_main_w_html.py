
import pandas as pd
import os
import operator
from flask import render_template, request
from __main__ import app

from kalkulator_raben import kalkulator_spedycja
from do_psql import PolaczenieBazy
from flota import Samochod
from wyszukiwarka_makaronowa import wyszukanie
from pierwszy_etap import koszty_odleglosci, koszty_spedycji, wlasny_transport_vs_spedycja, przypisywanie_wartosci_bezposredniego_polaczenia
from drugi_etap import sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym, compare_dictionaries, zaokraglanie_i_laczenie_i_sortowanie,filtr_najwiekszych_miejscowosci, usuwanie_podkreslenia, sprawdzenie_czy_nie_taniej_bedzie_przeniesc_pomiedzy_przejazdami,model_deflacyjny_dla_stworzonych_tras, zmien_kolejnosc

@app.route('/trasy_do_realizacji')
def trasy_do_realizacji():
    try:
        os.remove('nowy_2spedycja.csv')
    except:
        pass

    lacza = PolaczenieBazy() # polaczenie z baza danych faktur
    lacza.generowanie_towaru_custome() # tworzenie dokumentow aby moc zaprezentowac dzialanie programu
    Samochod.odczytaj_z_pliku_wszystkie() # wczytanie danych samochodowych
    dane = lacza.get_values_custome()
    df = pd.DataFrame(dane, columns=['nazwa_kontrahenta','miejscowosc_dostawy','ilosc_dostarczana','waga'])
    df_do_wyswietlenia = df.copy()
    koszty_pokonania_km = 7
    koszty = przypisywanie_wartosci_bezposredniego_polaczenia(df)

    koszty_dostawy = koszty_odleglosci('Rzeszow',koszty,koszty_pokonania_km) # uzyskanie ceny dostawy przez BOZ z uwzglednieniem punktow ktore sa w realizacji

    koszty_dostawy = koszty_spedycji(df,koszty_dostawy)

    dostawa_boz , dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy,koszty) # uzyskujemy podział na biblioteke i liste zawierajace odpowiednio lista rzeczy do transportu przez boz badz   spedycje
    spedycja_df =pd.DataFrame(columns=['nazwa_kontrahenta', 'miejscowosc_dostawy', 'ilosc_dostarczana', 'waga'])
    pierwszy_rekord_do_uruchamienia_tworzenia_df = 0

    while int(df['ilosc_dostarczana'].sum()) > Samochod.wyswietl_wage_i_palety()[1]: # sprawdzenie czy potrzeby transportowe nie są większe niż możliwości
        
        miejsce = (max(dostawa_boz.items(), key=operator.itemgetter(1))[0])
        x = df.where(df['miejscowosc_dostawy'] == miejsce).dropna() # wyszukanie miejscowości najdalej położonej od punktu startowego w df transportowej
        x = x.sort_values(by='ilosc_dostarczana')
        dostawa_boz.pop(miejsce) # usuniecie z dict miejscowości transportowej

        if len(spedycja_df) >0:
            spedycja_df = pd.concat([spedycja_df,x], ignore_index=True) # przeniesienie miejscowosći to df spedycyjnej
        else:
            spedycja_df = x

        df.drop(df[df['miejscowosc_dostawy'] == miejsce].index, inplace=True) #usuniecie z df transportowego
        df.reset_index(drop=True, inplace=True) 
        spedycja_df.reset_index(drop=True, inplace=True)

        if int(df['ilosc_dostarczana'].sum()) <= Samochod.wyswietl_wage_i_palety()[1]: # sprawdzenie czy po usunięciu ostatniej miejscowości nie zostało za dużo miejsca na aucie, jeżeli cos zostało   sprawdza z ostaniej miejscowości możliwości doładunkowe i przenoisi wiersze pomiędzy df
            for index, testing in x.iterrows(): # wystwietlenie danych z ostatniej miejscowosci w pojedynczych 'wierszach'

                ilosc_do_doladowania = (Samochod.wyswietl_wage_i_palety()[1] - df['ilosc_dostarczana'].sum())

                if ilosc_do_doladowania > 0: # sprawdzenie czy poprzedni rekord w funkcji for nie spełnił warunki, po próbie zmiany warunki if na while generowało zle wyniki
                    warunek_usuniecia = (spedycja_df['nazwa_kontrahenta'] == testing['nazwa_kontrahenta']) & \
                                        (spedycja_df['miejscowosc_dostawy'] == testing['miejscowosc_dostawy']) & \
                                        (spedycja_df['ilosc_dostarczana'] == testing['ilosc_dostarczana']) & \
                                        (spedycja_df['waga'] == testing['waga'])  # potwierdzenie wszystkich zmiennych aby mieć pewność że usuwamy napewno właściwy wiersz


                    if testing['ilosc_dostarczana'] > ilosc_do_doladowania: # w przypadku kiedy do jednego klienta jest wiecej towaru niż miejsca na samochodzie, dzieli towar na max wypelnienie samochodu a reszta     do wysylki spedycja
                        doladowanie = testing['ilosc_dostarczana'] - ilosc_do_doladowania  # ustalenie ilości przelowowej pomiędzy df do spedycji
                        # dodanie przeliczaniwa wag
                        nowa_waga_transport = (ilosc_do_doladowania/testing['ilosc_dostarczana']) *(testing['waga'])
                        nowa_waga_spedycja = (testing['waga']) - nowa_waga_transport
                        
                        spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index) # usunięcie wiersza

                        testing['ilosc_dostarczana'] = doladowanie # ustalenia nowej wartości dla wracjacych danych do spedycji, wprowadziłem zmiane pod importem pandas
                        testing['waga'] = nowa_waga_spedycja
                        # spedycja_df = spedycja_df.append(testing) # wysylka do spedycji
                        testing_df = pd.DataFrame([testing], columns=spedycja_df.columns)
                        spedycja_df = pd.concat([testing_df, spedycja_df], ignore_index=True) # wysylka do spedycji
                        testing['ilosc_dostarczana'] = ilosc_do_doladowania#  ustalenie wartosci dla df transportowego
                        testing['waga'] = nowa_waga_transport

                    elif testing['ilosc_dostarczana'] <= df['ilosc_dostarczana'].sum(): # w przypadku kiedy do jednego klienta nie jest wiecej towaru niz wolnego miejsca na samochodzie
                        spedycja_df = spedycja_df.drop(spedycja_df[warunek_usuniecia].index) # usunięcie wiersza

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
    
    #while musi byc  poniewaz na kazdym koncu petli jes
    while len(dostawa_spedycja) > 0:
        for spedycyjne in dostawa_spedycja: # przeniesienie elementów pomiedzy df wysyłanych spedycją
            
            x =df.where(df['miejscowosc_dostawy'] == spedycyjne).dropna() # wycięcie wiersza do przeniesienia
            if len(spedycja_df) == 0:
                spedycja_df =pd.DataFrame(x)
            else:
                spedycja_df = pd.concat([x, spedycja_df], ignore_index=True) # przeniesienie wiersza do właściwej df
            df.drop(df[df['miejscowosc_dostawy'] == spedycyjne].index, inplace=True) # usunięcie wiersza z tramsportowej df
            df.reset_index(drop=True, inplace=True) # usunięcie powstałej luki po usunięciu z df miejscowości wysłanych spedycją
            spedycja_df.reset_index(drop=True, inplace=True)
        koszty_dostawy = koszty_odleglosci('Rzeszow',dostawa_boz,koszty_pokonania_km)
        koszty_dostawy = koszty_spedycji(df,koszty_dostawy)
        dostawa_boz, dostawa_spedycja = wlasny_transport_vs_spedycja(koszty_dostawy, koszty)
    
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
            
            if len(trasy) == Samochod.ilosc_pojazdow():
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
            km = wyszukanie('Rzeszow',row['miejscowosc_dostawy'])[0]['km']

        palety = row['ilosc_dostarczana']
        waga = row['waga']
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
    print(373,spedycja_df,trasy)
    trasy = zmien_kolejnosc(trasy)
    while True:
        #sprawdzenie aby pętla while nie leciała w nieskończoność
        trasy0 = trasy.copy()
        spedycja0 = spedycja_df.copy()
        trasy, spedycja_df = sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy_do_przyjcia = trasy, spedycje_do_sprawdzenia = spedycja_df, ile_kosztuje_km = koszty_pokonania_km)
        spedycja_df, trasy = model_deflacyjny_dla_stworzonych_tras(nosnik_informacji_transportowych = trasy, nosnik_informacji_spedycyjnej = spedycja_df, koszt_km_w_funkcji = koszty_pokonania_km)
        print(381,trasy, spedycja_df)
        trasy = sprawdzenie_czy_nie_taniej_bedzie_przeniesc_pomiedzy_przejazdami(trasy)
        print(383,trasy)
        #funkcja porownuje czy w trasach zaszla jakas zmiana
        if compare_dictionaries(trasy0,trasy) and spedycja0.equals(spedycja_df) and bezpiecznik > 2:
            break

        elif bezpiecznik > 5:
            break
        
        else:
            print("test - 390")
            bezpiecznik += 1

    #usuwanie postoi, wag i resetowanie indexow
    for przejazd in trasy:
        trasy[przejazd] = trasy[przejazd][trasy[przejazd]['nazwa_kontrahenta'] != 'Postoj']
        trasy[przejazd] = trasy[przejazd].drop(columns=['waga'])
        trasy[przejazd].reset_index(drop=True, inplace=True)

    trasy = zaokraglanie_i_laczenie_i_sortowanie(trasy)
    #usuniecie kolumny waga
    spedycja_df = spedycja_df.drop(columns=['waga'])
    lacza.usuniecie_testow()

    spedycja_df = usuwanie_podkreslenia(spedycja_df)

    for odczytanie_dla_usuiecia_podkreslen in trasy:
        trasy[odczytanie_dla_usuiecia_podkreslen] = usuwanie_podkreslenia(trasy[odczytanie_dla_usuiecia_podkreslen])

    return render_template('trasy-flex.html', towar_wyswietlenie=df_do_wyswietlenia,transportwe_informacje=trasy,spedycyjne_informacje=spedycja_df)
