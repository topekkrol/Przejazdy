import pandas as pd

def czy_mamy_tak_miejscowosc(koniec):
    dane = pd.read_csv('Zeszyt1.csv',delimiter=';')
    plyk = pd.DataFrame(dane)

    t1 = (len(plyk.where(plyk['Rozpoczecie'] == koniec).dropna()))
    t2 = (len(plyk.where(plyk['Zakonczenie'] == koniec).dropna()))

    return t1+t2
