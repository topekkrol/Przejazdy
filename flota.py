import datetime
import pickle
from DoPSGl import PolaczenieBazy

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

    def dodaj_przejechane_km(self, km):
        self.przejechane_km += km
        self.zapisz_do_pliku()

    def wyswietl_info(self):
        print("Marka:", self.marka)
        print("Ladowosc palet:", self.ladowosc_palety)
        print("Ladownosc waga:", self.ladownosc_waga)
        print("Numer rejestracyjny:", self.nr_rejestracyjny)
        try:
            print("Przebieg:", self.przejechane_km+PolaczenieBazy().km_samochod(self.nr_rejestracyjny))
        except:
            print("Przebieg:", self.przejechane_km)
        print("Data przeglądu:", self.data_przegladu.strftime("%d"),self.data_przegladu.strftime("%B"),'\n')

    @classmethod
    def wyswietl_wszystkie(cls):
        cls.odczytaj_z_pliku_wszystkie()
        for samochod in cls.lista_samochodow:
            samochod.wyswietl_info()
    @classmethod
    def zapisz_do_pliku(cls):
        with open('flota.pkl', 'wb') as plik:
            pickle.dump(cls.lista_samochodow, plik)

    # @classmethod
    # def odczytaj_z_pliku(cls):
    #     cls.odczytaj_z_pliku_wszystkie()
    #     samochody = []
    #     with open('flota.pkl', 'rb') as plik:
    #         while True:
    #             try:
    #                 obj = pickle.load(plik)
    #                 for obiekt in obj:
    #                     samochody.append(obiekt)
    #             except EOFError:
    #                 break
    #     return samochody

    @classmethod
    def odczytaj_z_pliku_wszystkie(cls):
        try:
            with open(r'Trasy-zmiana_przypisywania_do_coru\flota.pkl', 'rb') as plik:
                cls.lista_samochodow = pickle.load(plik)
        except FileNotFoundError:
            print("Nie znaleziono pliku z zapisanymi danymi.")


    @classmethod
    def usun_obiekt(cls, nr_rej):
        for obj in cls.lista_samochodow:
            if obj.nr_rejestracyjny == nr_rej:
                cls.lista_samochodow.remove(obj)
                cls.zapisz_do_pliku()
                # Samochod.num_object -= 1
                return True
        return False


    @classmethod
    def usun_wszystkie(cls):
        cls.lista_samochodow.clear()
        cls.zapisz_do_pliku()
        # Samochod.num_object = 0

    @classmethod
    def wyswietl_wage_i_palety(cls):
        wewnetrzne_waga = 0
        wewnetrzne_palety = 0
        for s in cls.lista_samochodow:
            wewnetrzne_waga += int(s.ladownosc_waga)
            wewnetrzne_palety += int(s.ladowosc_palety)
        return wewnetrzne_waga , wewnetrzne_palety

    @classmethod
    def max_palety(cls, x=0):
        sorted_list = sorted(cls.lista_samochodow, key=lambda s: int(s.ladowosc_palety), reverse=True)
        if x < len(sorted_list):
            return sorted_list[x].nr_rejestracyjny, sorted_list[x].ladowosc_palety
        else:
            return None

    @classmethod
    def dane_auta(cls,nr_rej):
        for nr_reje in cls.lista_samochodow:
            if nr_reje.nr_rejestracyjny == nr_rej:
                return (nr_reje.ladowosc_palety)

    @staticmethod
    def count_objects():
        return len(Samochod.lista_samochodow)

    @classmethod
    def przeglady(cls):
        cls.odczytaj_z_pliku_wszystkie()
        # dane = PolaczenieBazy()
        dane_km = dict(PolaczenieBazy().km_samochodow())
        for samochody in cls.lista_samochodow:
            if samochody.nr_rejestracyjny in dane_km:
                nr_zmiany_oleju = int((dane_km[samochody.nr_rejestracyjny] + samochody.przejechane_km) / 1000)
                if nr_zmiany_oleju ==0:
                    continue
                else:
                    try:
                        PolaczenieBazy().dodanie_tabeli_samochod(samochody.nr_rejestracyjny,nr_zmiany_oleju,'wymiana_oleju')

                    except:
                        continue

    @classmethod
    def alert_przeglady(cls):
        cls.odczytaj_z_pliku_wszystkie()

        for samochody in cls.lista_samochodow: # sprawdzenie przegladu samochodu
            data_przegladu = datetime.date(day=int(samochody.data_przegladu.strftime("%d")), month=int(samochody.data_przegladu.strftime("%m")), year=int(datetime.datetime.now().strftime("%Y")))
            data_dzis = datetime.date(day=int(datetime.datetime.now().strftime("%d")) , month=int(datetime.datetime.now().strftime("%m")), year=int(datetime.datetime.now().strftime("%Y")))
            # print("flota 140",date(samochody.data_przegladu.strftime("%d"), datetime.datetime.now().strftime("%d"), samochody.data_przegladu.strftime("%m"), datetime.datetime.now().strftime("%m"))
            if data_dzis > data_przegladu:
                PolaczenieBazy().dodanie_tabeli_samochod(nr_rejestracyjny=samochody.nr_rejestracyjny,wielekrotnosc=0,opis="przeglad",data=samochody.data_przegladu.date())

        dane_print = PolaczenieBazy().nierozliczone_pozycje_kosztowe_transport()
        if len(dane_print) > 0: # wyswietlanie nierozliczonych pozycji w transporcie
            print("Konieczne jest wykonanie seriwsu:")
            print("nr rejestracyjny","data","usługa")
            for _ in dane_print:
                print(str(_[1:3]).replace("(","").replace(")","").replace(", datetime.date"," ").replace(","," -"),_[-2])