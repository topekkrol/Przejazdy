from wyszukiwarka_makaronowa import wyszukanie
from kalkulator_raben import kalkulator_spedycja

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

#funkcja przypisuje koszty dla wykonania polaczenia z uwzgleniedniem jakie miejscowosci rozwniez znajduja sie na trasie
def koszty_odleglosci(start, koszty,koszt_km):
    a = []
    for miejscowosci in koszty:
        poleczenie1 = wyszukanie(start,miejscowosci,glebokosc=1)
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
    for index, miejscowosci_spedycyjne in data_frame.iterrows(): # s jako zmienna bo x jest zbyt powszechne        
        
        km = wewnetrzne_koszty_dostawy[miejscowosci_spedycyjne['miejscowosc_dostawy']]['km']
        try:
            spedycja = wewnetrzne_koszty_dostawy[miejscowosci_spedycyjne['miejscowosc_dostawy']]['spedycja']
            spedycja += kalkulator_spedycja(km,miejscowosci_spedycyjne['waga'],miejscowosci_spedycyjne['ilosc_dostarczana'])[0]
            wewnetrzne_koszty_dostawy[miejscowosci_spedycyjne['miejscowosc_dostawy']]['spedycja'] = spedycja
        except:

            wewnetrzne_koszty_dostawy[miejscowosci_spedycyjne['miejscowosc_dostawy']]['spedycja'] = kalkulator_spedycja(km,miejscowosci_spedycyjne['waga'],miejscowosci_spedycyjne['ilosc_dostarczana'])[0]

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

#funkcja przypisuje dla miejscowosc wartosc bezposredniego polaczenia
def przypisywanie_wartosci_bezposredniego_polaczenia(df):

    koszty = {}
    wewnetrzne_pogrupowane = df[['miejscowosc_dostawy']].drop_duplicates()

    for index, miejscowsc in wewnetrzne_pogrupowane.iterrows():
        koszty[miejscowsc['miejscowosc_dostawy']] = [wyszukanie('Rzeszow',miejscowsc['miejscowosc_dostawy'])[0]['km']]

    return koszty
