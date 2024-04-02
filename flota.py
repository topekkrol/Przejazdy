import pickle

class Samochod:
    lista_samochodow = []
    # num_object = 0

    def __init__(self, nr_rejestracyjny, marka, ladowosc_palety, ladownosc_waga,przeglad,przejechane_km = 0):
        # Samochod.num_object += 1
        self.nr_rejestracyjny = nr_rejestracyjny
        self.marka = marka
        self.ladowosc_palety = ladowosc_palety
        self.ladownosc_waga = ladownosc_waga
        self.przejechane_km = przejechane_km
        self.data_przegladu = przeglad
        Samochod.lista_samochodow.append(self)

    def __str__(self):
        return str({
             'nr_rejestracyjny': self.nr_rejestracyjny,
             'marka': self.marka,
             'ladowosc_palety': self.ladowosc_palety,
             'ladownosc_waga': self.ladownosc_waga,
             'przejechane_km': self.przejechane_km,
             'data przegladu': self.data_przegladu
        })

    @classmethod
    def wyswietl_wszystkie(cls):
        lista_samochodow = {}

        for samochod in cls.lista_samochodow:
            lista_samochodow[samochod.nr_rejestracyjny] = [samochod.ladowosc_palety,'{:,.0f}'.format(samochod.ladownosc_waga).replace(',', ' ')]

        return lista_samochodow
    
    @classmethod
    def zapisz_do_pliku(cls):
        with open('flota.pkl', 'wb') as plik:
            pickle.dump(cls.lista_samochodow, plik)

    @classmethod
    def odczytaj_z_pliku_wszystkie(cls):
        try:
            with open('flota.pkl', 'rb') as plik:
                cls.lista_samochodow = pickle.load(plik)
        except FileNotFoundError:
            print("Nie znaleziono pliku z zapisanymi danymi.")

    @classmethod
    def wyswietl_wage_i_palety(cls):
        wewnetrzne_waga = 0
        wewnetrzne_palety = 0
        for s in cls.lista_samochodow:
            wewnetrzne_waga += int(s.ladownosc_waga)
            wewnetrzne_palety += int(s.ladowosc_palety)
        return wewnetrzne_waga , wewnetrzne_palety

    @classmethod
    def max_palety(cls, kolejnosc_ladownosci=0):
        sorted_list = sorted(cls.lista_samochodow, key=lambda s: int(s.ladowosc_palety), reverse=True)
        if kolejnosc_ladownosci < len(sorted_list):

            return sorted_list[kolejnosc_ladownosci].nr_rejestracyjny, sorted_list[kolejnosc_ladownosci].ladowosc_palety
        else:
            return None

    @classmethod
    def dane_auta(cls,nr_rej):
        for nr_reje in cls.lista_samochodow:
            if nr_reje.nr_rejestracyjny == nr_rej:
                return nr_reje.ladowosc_palety

    @staticmethod
    def ilosc_pojazdow():
        return len(Samochod.lista_samochodow)
