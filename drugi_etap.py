from flota import Samochod
import pandas as pd
from wyszukiwarka_makaronowa import wyszukanie
from kalkulator_raben import kalkulator_spedycja
from flota import Samochod

def sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym(trasy_do_przyjcia,spedycje_do_sprawdzenia,ile_kosztuje_km):
    dl_speydcji = len(spedycje_do_sprawdzenia)
    x = 0

    while dl_speydcji > 0: # sprawdzanie czy pozycje z spedycji nie są możliwe do doładowaniaI
        x += 1 
        dl_speydcji = len(spedycje_do_sprawdzenia) # ustalanie długosci, sprawdza czy petla wykonala operacje

        for powrot_z_trasy in trasy_do_przyjcia: # czytanie tras

            for index, row in spedycje_do_sprawdzenia.iterrows():       
                lista_postoi = trasy_do_przyjcia[powrot_z_trasy]['miejscowosc_dostawy'].tolist() #uzyskanie listy miejscowosci ktore odwiedza auto
                postoje_lista = list(dict.fromkeys(lista_postoi)) #usuniecie duplikatow
                palety_na_powrocie = int(Samochod.dane_auta(powrot_z_trasy)) - int(trasy_do_przyjcia[powrot_z_trasy]['ilosc_dostarczana'].sum()) # obliczenie palet na powrocie, dla kazdego klient musi zostac obliczona na nowo
                if palety_na_powrocie == 0:
                    continue
 
                try:
                    if  row['ilosc_dostarczana'] <= palety_na_powrocie : # obliczenie ilości do doładowania
                        procent_wypelnienia_auta =1 #procent wyplnienia auta w rozumieniu procent w jakim towar w zamowieniu jest w stanie zmiesci sie na aucie
                    else:
                        procent_wypelnienia_auta =  palety_na_powrocie / row['ilosc_dostarczana'] 

                    warunek_usuniecia = (spedycje_do_sprawdzenia['nazwa_kontrahenta'] == row['nazwa_kontrahenta']) & \
                                        (spedycje_do_sprawdzenia['miejscowosc_dostawy'] == row['miejscowosc_dostawy']) & \
                                        (spedycje_do_sprawdzenia['ilosc_dostarczana'] == row['ilosc_dostarczana']) & \
                                        (spedycje_do_sprawdzenia['waga'] == row['waga'])

                    if row['miejscowosc_dostawy'] in postoje_lista: # sprawdzenie czy miejscowosc nie wystepuje w postojach

                        spedycje_do_sprawdzenia = spedycje_do_sprawdzenia.drop(spedycje_do_sprawdzenia[warunek_usuniecia].index)  # usuniecie z df spedycyjnego  
                        row.update(pd.Series([row['ilosc_dostarczana']*procent_wypelnienia_auta],index=['ilosc_dostarczana']))
                        row.update(pd.Series([row['waga']*procent_wypelnienia_auta],index=['waga']))
                        dodanie_drobnicy = pd.DataFrame([row],columns=trasy_do_przyjcia[powrot_z_trasy].columns)
                        przejazd = pd.concat([dodanie_drobnicy, trasy_do_przyjcia[powrot_z_trasy]], ignore_index=True)
                        trasy_do_przyjcia[powrot_z_trasy] = przejazd

                        if procent_wypelnienia_auta < 1:
                            row['ilosc_dostarczana'] = row['ilosc_dostarczana'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['ilosc_dostarczana'] / procent_wypelnienia_auta))  # ustawienowej nowej ilosci dostarczanych palet
                            row['waga'] = row['waga'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['waga'] / procent_wypelnienia_auta))  # analogiczne ustawienie wagi
                            dodanie_spadkow = pd.DataFrame([row],columns=spedycje_do_sprawdzenia.columns)
                            spedycje_do_sprawdzenia = pd.concat([dodanie_spadkow, spedycje_do_sprawdzenia], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df

                        continue
                        # dodanie

                    try: # sprawdzenie czy dołożenie miejsca dostawy nie jest tańsze niż wysyłka spedycja
                        km_pomiedzy_miastem_glownym = wyszukanie(zaczynamy=row['miejscowosc_dostawy'], konczymy='Rzeszow')[0]['km']
                        km_pomiedzy_punktami = wyszukanie(zaczynamy=postoje_lista[0], konczymy=row['miejscowosc_dostawy'])[0]['km']
                        km_dla_polaczenia_bezposredniego = wyszukanie(zaczynamy=postoje_lista[0], konczymy='Rzeszow')[0]['km']
                        dodatkowe_km_dla_punktu = (km_pomiedzy_punktami + km_pomiedzy_miastem_glownym)- km_dla_polaczenia_bezposredniego

                        if dodatkowe_km_dla_punktu * ile_kosztuje_km < row['koszt_spedycji']*procent_wypelnienia_auta: # sprawdzenie czy tańsze jest połączenie z którymś z punktow czy bezpośrednio z Rzeszowa 

                            spedycje_do_sprawdzenia = spedycje_do_sprawdzenia.drop(spedycje_do_sprawdzenia[warunek_usuniecia].index)  # usuniecie z df spedycyjnego  
                            row.update(pd.Series([row['ilosc_dostarczana']*procent_wypelnienia_auta],index=['ilosc_dostarczana']))
                            row.update(pd.Series([row['waga']*procent_wypelnienia_auta],index=['waga']))
                            dodanie_drobnicy = pd.DataFrame([row],columns=trasy_do_przyjcia[powrot_z_trasy].columns)
                            przejazd = pd.concat([dodanie_drobnicy, trasy_do_przyjcia[powrot_z_trasy]], ignore_index=True)
                            trasy_do_przyjcia[powrot_z_trasy] = przejazd

                            if procent_wypelnienia_auta < 1:

                                row['ilosc_dostarczana'] = row['ilosc_dostarczana'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['ilosc_dostarczana'] / procent_wypelnienia_auta))  # ustawienowej nowej ilosci dostarczanych palet
                                row['waga'] = row['waga'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['waga'] / procent_wypelnienia_auta))  # analogiczne ustawienie wagi
                                row['koszt_spedycji'] = round(kalkulator_spedycja(row['km'],row['waga'],row['ilosc_dostarczana'])[0])
                                dodanie_spadkow = pd.DataFrame([row],columns=spedycje_do_sprawdzenia.columns)
                                spedycje_do_sprawdzenia = pd.concat([dodanie_spadkow, spedycje_do_sprawdzenia], ignore_index=True) # dodanie palet ktore sie nie zmiescily do df

                    except Exception as e:
                        continue

                except ZeroDivisionError as e:
                    continue

                except Exception as e:
                    continue
                    
        dl_speydcji -= len(spedycje_do_sprawdzenia)

    return trasy_do_przyjcia,spedycje_do_sprawdzenia

def compare_dictionaries(dict1, dict2):
    # Sprawdź, czy klucze się zgadzają
    if set(dict1.keys()) != set(dict2.keys()):
        return False
    
    # Iteruj po kluczach i porównuj DataFrame'y
    for key in dict1.keys():
        if not dict1[key].equals(dict2[key]):
            return False
    
    return True

def zaokraglanie_i_laczenie_i_sortowanie(data_dict):
    # Iterujemy po elementach słownika
    for key, df in data_dict.items():
        # Sprawdzamy, czy podana nazwa kolumny istnieje w danym DataFrame
        df = zaokraglenie_df(df,'waga')

        # laczymy z soba te same elementy identyfikując po nazwie i miejscowosci
        grouped = df.groupby(['nazwa_kontrahenta', 'miejscowosc_dostawy']).agg({'ilosc_dostarczana': 'sum'}).reset_index()
        lista_miejscowosci = filtr_najwiekszych_miejscowosci(grouped)
        df['miejscowosc_dostawy'] = pd.Categorical(df['miejscowosc_dostawy'], categories=lista_miejscowosci, ordered=True)
        # Posortuj DataFrame według kategorii
        df_gotowa = df.sort_values(by=['miejscowosc_dostawy','ilosc_dostarczana'], ascending=[True, False])
        data_dict[key] = df_gotowa

    return data_dict

def zaokraglenie_df(df, column_name):
    if column_name in df.columns:
        #polaczenia wartosci z takimi samymi wartosciami w calosc
        df = df.groupby(['nazwa_kontrahenta', 'miejscowosc_dostawy']).sum().reset_index()
        # Zaokrąglamy wartości w kolumnie do określonej liczby miejsc po przecinku
        df[column_name] = df[column_name].round(0)
        # Aktualizujemy DataFrame w słowniku
        df = df.sort_values(by=['miejscowosc_dostawy', 'ilosc_dostarczana'])

    return df

def filtr_najwiekszych_miejscowosci(frame_do_uporzadkowania):
    frame_do_uporzadkowania = frame_do_uporzadkowania.groupby(['miejscowosc_dostawy']).sum().reset_index()
    frame_do_uporzadkowania.sort_values(by=['ilosc_dostarczana'],ascending=False,inplace=True)
    pozadana_kolejnosc = frame_do_uporzadkowania['miejscowosc_dostawy'].tolist()

    return pozadana_kolejnosc

def usuwanie_podkreslenia(df_z_pokresleniem):
    for nazwa_kolumny in df_z_pokresleniem.columns:
        df_z_pokresleniem.rename(columns={nazwa_kolumny:nazwa_kolumny.replace("_"," ").title()},inplace=True)

    return df_z_pokresleniem

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


#funkcja sprawdza czy dla stworzonego modelu nie zachodzi sytuacja gdzie taniej jest dostarczyc towar innym modelem transportu.
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
                        print(219,km_pomiedzy_punktami)
                        km_pomiedzy_punktami += km_z_miastem_glownym
                        print(221,km_pomiedzy_punktami,km_z_miastem_glownym)
                        km_dla_polaczenia_bezposredniego = wyszukanie(zaczynamy='Rzeszow',konczymy=inne_miejscowosci)[0]['km']
                        print(223,km_dla_polaczenia_bezposredniego)
                        km_pomiedzy_punktami = km_pomiedzy_punktami - km_dla_polaczenia_bezposredniego
                        print(km_pomiedzy_punktami)
                    except:
                        km_pomiedzy_punktami = 999

                    if km_pomiedzy_punktami*koszt_km_w_funkcji > koszt_spedycji_z_miasta_glownego[0]:
                        print(km_pomiedzy_punktami*koszt_km_w_funkcji, koszt_spedycji_z_miasta_glownego[0],"+1")
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

def sort_dataframes_by_weight(dataframes_dict):
    sorted_dataframes = dict(sorted(dataframes_dict.items(), key=lambda x: x[1]['waga'].sum(), reverse=False))
    return sorted_dataframes

def zmien_kolejnosc(dictionary):
    lista_kluczy = list(sort_dataframes_by_weight(dictionary))
    nowy_słownik = {}
    for klucz in lista_kluczy:
        if klucz in dictionary:
            nowy_słownik[klucz] = dictionary[klucz]
    return nowy_słownik