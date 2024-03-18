from flota import Samochod
import pandas as pd
from WyszukiwarkaMakaronowa import wyszukanie
import time
import traceback
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
                if row['miejscowosc_dostawy'] == "Brzozow":
                    print("bingo",trasy_do_przyjcia)
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
                            if row['miejscowosc_dostawy'] == "Brzozow":
                                print(50,"bingo")
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
                        if row['miejscowosc_dostawy'] == "Brzozow":
                            print(65,"bingo",dodatkowe_km_dla_punktu * ile_kosztuje_km, row['koszt_spedycji']*procent_wypelnienia_auta)
                        if dodatkowe_km_dla_punktu * ile_kosztuje_km < row['koszt_spedycji']*procent_wypelnienia_auta: # sprawdzenie czy tańsze jest połączenie z którymś z punktow czy bezpośrednio z Rzeszowa 
                            if row['miejscowosc_dostawy'] == "Brzozow":
                                print(67,"bingo")
                            spedycje_do_sprawdzenia = spedycje_do_sprawdzenia.drop(spedycje_do_sprawdzenia[warunek_usuniecia].index)  # usuniecie z df spedycyjnego  
                            row.update(pd.Series([row['ilosc_dostarczana']*procent_wypelnienia_auta],index=['ilosc_dostarczana']))
                            row.update(pd.Series([row['waga']*procent_wypelnienia_auta],index=['waga']))
                            dodanie_drobnicy = pd.DataFrame([row],columns=trasy_do_przyjcia[powrot_z_trasy].columns)
                            przejazd = pd.concat([dodanie_drobnicy, trasy_do_przyjcia[powrot_z_trasy]], ignore_index=True)
                            trasy_do_przyjcia[powrot_z_trasy] = przejazd

                            if procent_wypelnienia_auta < 1:
                                if row['miejscowosc_dostawy'] == "Brzozow":
                                    print(78,"bingo")
                                row['ilosc_dostarczana'] = row['ilosc_dostarczana'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['ilosc_dostarczana'] / procent_wypelnienia_auta))  # ustawienowej nowej ilosci dostarczanych palet
                                row['waga'] = row['waga'] / procent_wypelnienia_auta - (procent_wypelnienia_auta * (row['waga'] / procent_wypelnienia_auta))  # analogiczne ustawienie wagi
                                dodanie_spadkow = pd.DataFrame([row],columns=spedycje_do_sprawdzenia.columns)
                                print(dodanie_spadkow)
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

def sprawdzenie_czy_nie_taniej_bedzie_przeniesc_pomiedzy_przejazdami(transportowy_df):
    
    for dejtafrejmy in transportowy_df:
        dane_o_aucie = Samochod.dane_auta(nr_rej=dejtafrejmy)
        ile_palet_na_aucie = int(transportowy_df[dejtafrejmy]['ilosc_dostarczana'].sum())
        procent_wypelnienia_auta = ile_palet_na_aucie / dane_o_aucie

        if procent_wypelnienia_auta == 1:
            continue

        for dejtafrejmy_do_rozlozenia in transportowy_df:

            if dejtafrejmy == dejtafrejmy_do_rozlozenia:
                continue
            for index,row in transportowy_df[dejtafrejmy_do_rozlozenia].iterrows():

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

def round_column_values_in_dict(data_dict):
    # Iterujemy po elementach słownika
    for key, df in data_dict.items():
        # Sprawdzamy, czy podana nazwa kolumny istnieje w danym DataFrame
        df = zaokraglenie_df(df,'waga')
        data_dict[key] = df

    
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
