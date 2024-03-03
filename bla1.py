import pandas as pd
from flota import Samochod

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

                    print('do tego',transportowy_df[dejtafrejmy])
                    print('mozna przenisc to',row['miejscowosc_dostawy'])
                    dataframe_z_usunietym = transportowy_df[dejtafrejmy_do_rozlozenia].drop(transportowy_df[dejtafrejmy_do_rozlozenia][warunek_usuniecia].index)  # usuniecie z df spedycyjnego  

                    dodanie_drobnicy = pd.DataFrame([row],columns=transportowy_df[dejtafrejmy_do_rozlozenia].columns)
                    przejazd = pd.concat([dodanie_drobnicy, transportowy_df[dejtafrejmy]], ignore_index=True)
                    transportowy_df[dejtafrejmy] = przejazd
                    transportowy_df[dejtafrejmy_do_rozlozenia] = dataframe_z_usunietym
                    return transportowy_df


dane = {
    'RZ8554N': {
        'nazwa_kontrahenta': ['R', 'J', 'G'],
        'miejscowosc_dostawy': ['Zamosc', 'Zamosc', 'Zamosc'],
        'ilosc_dostarczana': [5.0, 8.0, 5.0],
        'waga': [5185.0, 7708.0, 0.0],
        'km': [170, 170, 170]
    },
    'RZ8367R': {
        'nazwa_kontrahenta': ['N', 'Y', 'O', 'J','P'],
        'miejscowosc_dostawy': ['Tarnobrzeg', 'Stalowa Wola', 'Stalowa Wola', 'Bilgoraj','Janow Lubelski'],
        'ilosc_dostarczana': [3.0, 2.0, 1.0, 8.0,4.0],
        'waga': [1741.0, 6020.0, 3150.0, 0.0, 0.0],
        'km': [85, 85, 85, 0, 0]
    },
    'RZ0535W': {
        'nazwa_kontrahenta': ['N', 'Y', 'N'],
        'miejscowosc_dostawy': ['Tarnobrzeg', 'Tarnobrzeg', 'Tarnobrzeg'],
        'ilosc_dostarczana': [2.0, 9.0, 2.0],
        'waga': [848.0, 5656.0, 9488.0],
        'km': [85, 85, 85]
    }
}
# Tworzenie słownika zawierającego DataFrame
trasy = {}
for klucz, wartosc in dane.items():
    trasy[klucz] = pd.DataFrame(wartosc)
Samochod.odczytaj_z_pliku_wszystkie() # wczytanie danych samochodowych

print(trasy)
trasy = sprawdzenie_czy_nie_taniej_bedzie_przeniesc_pomiedzy_przejazdami(trasy)
print(trasy)