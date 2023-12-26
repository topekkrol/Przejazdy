import csv
import pandas as pd

# Tworzenie pierwszego DataFrame
data1 = {
    'nazwa_kontrahenta': ['U', 'A', 'E', 'D'],
    'miejscowosc_dostawy': ['Bilgoraj', 'Bilgoraj', 'Janow Lubelski', 'Janow Lubelski'],
    'ilosc_dostarczana': [4.0, 2.0, 6.0, 6.0],
    'waga': [7135.0, 2596.0, 3906.0, 7584.0],
    'km': [110, 110, 111, 111]
}

df1 = pd.DataFrame(data1)

# Tworzenie drugiego DataFrame
data2 = {
    'nazwa_kontrahenta': ['L'],
    'miejscowosc_dostawy': ['Lezajsk'],
    'ilosc_dostarczana': [18.0],
    'waga': [1000.0],
    'km': [50]
}

df2 = pd.DataFrame(data2)

# Połączenie DataFrame w jednym słowniku
df_dict = {
    0 : df1,
    1 : df2
}

Spedycja =  {
        'nazwa_kontrahenta': ['U', 'Top-gres', 'M', 'Romax'],
        'miejscowosc_dostawy': ['Bilgoraj', 'Kielce', 'Zamosc', 'Warszawa'],
        'ilosc_dostarczana': [1.0, 1.0, 1.0, 4.0],
        'waga': [1426.0, 800.0, 688.0, 3453.0],
        'km': [110.0, 168.0, 170.0, 318.0],
        'koszt_spedycji': [318.181112, 167.708064, 167.708064, 773.699128]
    }
df_spedycja = pd.DataFrame(Spedycja)

print(df_spedycja,df_dict)

nazwa_pliku = 'your_data.csv'
szukana_wartosc = 'mieszany'
wykorzystanie_danych = 0
wykorzystanie_danych_spedycja = 1
# Otwórz plik CSV w trybie do odczytu
with open(nazwa_pliku, 'r') as plik:
    czytnik_csv = csv.reader(plik)
    for poszukiwany in czytnik_csv:
        if poszukiwany[-1] == "mieszany":
            print(poszukiwany)

            if wykorzystanie_danych == 1 and wykorzystanie_danych_spedycja == 1:
                print(1)
            elif wykorzystanie_danych == 1 and wykorzystanie_danych_spedycja == 0: # wysylam transport, spedycje nie
            #spedycja musi wrócić do dokumentów
                wynik = df_spedycja[(df_spedycja['nazwa_kontrahenta'] == poszukiwany[3]) & (df_spedycja['miejscowosc_dostawy'] == poszukiwany[2])]
                print(wynik)
            elif wykorzystanie_danych == 0 and wykorzystanie_danych_spedycja == 1:#wysylamy spedycje, transport nie
            #transport musi wrócic do dokumentow
                print(63)
                for dejty in df_dict:
                    wynik = df_dict[dejty][(df_dict[dejty]['nazwa_kontrahenta'] == poszukiwany[3]) & (df_dict[dejty]['miejscowosc_dostawy'] == poszukiwany[2])]
                    if len(wynik) > 0:
                        print(wynik)
            else:
                print("leci else")
