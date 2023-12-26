import psycopg2
from datetime import datetime
import pickle
import random
import string
import csv

class PolaczenieBazy:
    def __init__(self):
        self.hostname = 'localhost'
        self.database = 'test'
        self.username = 'postgres'
        self.pwd = 'Wisnia12'
        self.port_id = 5432
        self.conn = None
        self.cur = None
        try:
            self.conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.database,
                user=self.username,
                password=self.pwd,
                port=self.port_id)
            self.cur = self.conn.cursor()
        except Exception as error:
            print(error)

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def get_values(self,status="przetwarzanie_danych"): # dodać sprawdzanie dnia >= data_utworzenia i dodac sprawdzanie wartosci. Stworzenia warunku status do pobierania danych i sprawdzania ich
        warunek_dniowy = "Status = 'planowana' AND ("+self.teskt()+")"
        get_values_query = f"SELECT nazwa_kontrahenta,miejscowosc_dostawy,sum(ilosc_dostarczana),sum(waga) FROM dokumenty WHERE {warunek_dniowy} GROUP BY nazwa_kontrahenta,miejscowosc_dostawy;"
        self.cur.execute(get_values_query)
        dane = self.cur.fetchall()
        if status != 'planowana':
            self.zmiana_statusu(warunek_dniowy=warunek_dniowy)
        return dane


    def zmiana_statusu(self,warunek_dniowy,status="przetwarzanie_danych"):
        zmiana_statusu = f"UPDATE dokumenty SET status = '{status}' WHERE {warunek_dniowy}"
        self.cur.execute(zmiana_statusu)
        if status != "przetwarzanie_danych":
            dane = self.cur.rowcount
            self.conn.commit()
            return dane
        else:
            self.conn.commit()

    def ile_tras(self):
        ilosc_tras_query = "select max(nr_zlecenia) from trasy;"
        self.cur.execute(ilosc_tras_query)
        dane = self.cur.fetchall()
        return dane[0][0]
    
    def gwiazda(self):
        ilosc_tras_query = "select * from dokumenty order by id limit 10;"
        self.cur.execute(ilosc_tras_query)
        dane = self.cur.fetchall()
        return dane


    def create_script(self):
        create_script_dokumenty = ''' CREATE TABLE IF NOT EXISTS Dokumenty (
                                id SERIAL PRIMARY KEY,
                                nazwa_kontrahenta VARCHAR(200),
                                symbol_dokumentu VARCHAR(200),
                                data_utworzenia DATE,
                                planowana_data_dostawy DATE,
                                ilosc_dostarczana REAL,
                                waga REAL,
                                wartosc_dokumentu REAL,
                                miejscowosc_dostawy VARCHAR(200),
                                status VARCHAR(50))'''

        create_script_trasy = ''' CREATE TABLE IF NOT EXISTS Trasy (
                                 id SERIAL PRIMARY KEY,
                                 nr_zlecenia REAL,
                                 miejscowosci_dostawy VARCHAR(200),
                                 kontrachenci VARCHAR(200),
                                 ilosc_dostarczana REAL,
                                 samochod VARCHAR(50),
                                 data_dostawy DATE,
                                 km REAL)'''

        create_script_nowe_trasy = ''' CREATE TABLE IF NOT EXISTS nowe_trasy (
                                 id SERIAL PRIMARY KEY,
                                 nr_zlecenia VARCHAR(200),
                                 data_dostawy DATE,
                                 miejscowosci VARCHAR(200),
                                 firma VARCHAR(200),
                                 ilosc_dostarczana REAL,
                                 samochod VARCHAR(50),
                                 koszt REAL,
                                 km REAL,
                                 model_dostawy VARCHAR(200) )'''

        create_script_koszty_samochodow = ''' CREATE TABLE IF NOT EXISTS koszty_samochodow (
                                         id SERIAL PRIMARY KEY,
                                         samochod VARCHAR(50),
                                         planowana_data_wykonania DATE,
                                         data_wykonania DATE,
                                         koszt REAL,
                                         opis VARCHAR(500),
                                         oznaczenie_stale REAL)''' # Oznaczenie stale przekazuje informacje o wielokrotnosci przy ktorej zostal wykonany poprzedni przeglad

        #self.cur.execute(create_script_dokumenty)
        #self.cur.execute(create_script_trasy)
        #self.cur.execute(create_script_koszty_samochodow)
        self.cur.execute(create_script_nowe_trasy)
        self.conn.commit()

    def tydzien(self,nowe_miasto="",trasa=""):

        tydzien = {
            1: ['Jaroslaw', 'Przeworsk', 'Lubaczow', 'Tomaszow', 'Sanok', 'Brzozow','Stalowa Wola','Nisko','Rudnik nad Sanem'], # gotowa baza testowa
            2: ['Lezajsk', 'Bilgoraj', 'Janow Lubelski', 'Strzyzow', 'Jaslo', 'Stalowa Wola', 'Kolbuszowa', 'Mielec',
                'Debica', 'Tarnobrzeg'],  # gotowa baza testowa
            3: ['Bilgoraj', 'Zamosc', 'Stalowa Wola', 'Tarnobrzeg','Janow Lubelski'], # gotowa baza testowa
            4: ["Staszow","Debica","Gorlice","Jaslo","Krosno","Strzyzow"], # gotowa baza testowa
            5: ['Bilgoraj', 'Zamosc', 'Stalowa Wola', 'Mielec', 'Lezajsk'],
        }
        if nowe_miasto == 3: # zapisywania defoltowych tras
            with open(r"Trasy-zmiana_przypisywania_do_coru\tydzien.pkl", 'wb') as file:
                pickle.dump(tydzien, file)

        elif len(nowe_miasto)>2: # dodawania nowej miejscowsci
            try:
                with open(r"Trasy-zmiana_przypisywania_do_coru\tydzien.pkl", 'rb') as plik:
                    x = pickle.load(plik)
                    miasta_do_transportu = x[int(trasa)]
                    miasta_do_transportu.append(nowe_miasto)
                    x[int(trasa)] = miasta_do_transportu

                    with open(r"Trasy-zmiana_przypisywania_do_coru\tydzien.pkl", 'wb') as file:
                        pickle.dump(x, file)
            except:
                print("Niepoprawne dane, proszę spróbować jeszcze raz.")

        else: # wyswietlania miast do transporti
            with open(r"Trasy-zmiana_przypisywania_do_coru\tydzien.pkl", 'rb') as plik:
                x = pickle.load(plik)
                return x

    def teskt(self):
        d = datetime.now().date()
        # dzis = int(d.strftime('%w'))

        dzis = 3  # test
        tydzien = self.tydzien()
        zwrot = ''
        for dni in tydzien[dzis]:
            zwrot += "miejscowosc_dostawy='" + dni + "' OR "
        zwrot += f"planowana_data_dostawy <= '{d}'"
        # zwrot = zwrot[:-3]
        return zwrot

    def przesylka(self,plyk):

        zapytanie = f"copy trasy (nr_zlecenia,data_dostawy,miejscowosci_dostawy,kontrachenci,ilosc_dostarczana,samochod,km) FROM '{plyk}' DELIMITER ',' ENCODING 'UTF8';"
        self.cur.execute(zapytanie)
        self.conn.commit()

    def wszystkie_trasy(self):
        trasy ="select nr_zlecenia, miejscowosci_dostawy, kontrachenci, ilosc_dostarczana, samochod, data_dostawy, km from trasy order by id;"
        self.cur.execute(trasy)
        dane = self.cur.fetchall()
        return dane

    def update_km(self,nr_trasy,km):
        update =f"UPDATE trasy SET km = {km}  WHERE nr_zlecenia = {nr_trasy}"
        self.cur.execute(update)
        self.conn.commit()
        nowy_wiersz =f"SELECT nr_zlecenia, miejscowosci_dostawy, kontrachenci, ilosc_dostarczana, samochod, data_dostawy, km FROM trasy WHERE nr_zlecenia = {nr_trasy}"
        self.cur.execute(nowy_wiersz)

        komunikat = self.cur.fetchall()
        if len(komunikat) < 1:
            komunikat = None

        return komunikat

    def dodanie_faktur(self):
        copy_value_test = "copy Dokumenty (nazwa_kontrahenta, symbol_dokumentu, data_utworzenia,planowana_data_dostawy,	ilosc_dostarczana, waga, wartosc_dokumentu, miejscowosc_dostawy, status  ) FROM 'C:/Nowy_folder/dane_do_karmienia.csv' DELIMITER ';' ENCODING 'UTF8' CSV HEADER"
        self.cur.execute(copy_value_test)
        self.conn.commit()

    def dodanie_faktury(self,nazwa_kontrahenta,symbol_dokumentu,data_utworzenia,planowana_data_dostawy, ilosc_dostarczana,waga,wartosc_dokumentu,miejscowosc_dostawy):
        # status odrazu ustawiamy na 'planowana'
        if planowana_data_dostawy == None:
            add_value = f"INSERT INTO dokumenty (nazwa_kontrahenta, symbol_dokumentu, data_utworzenia, ilosc_dostarczana, waga, wartosc_dokumentu, miejscowosc_dostawy, status) VALUES ('{nazwa_kontrahenta}', '{symbol_dokumentu}', '{data_utworzenia}', {ilosc_dostarczana}, {waga}, {wartosc_dokumentu}, '{miejscowosc_dostawy}', 'planowana');"
        else:
            add_value = f"INSERT INTO dokumenty (nazwa_kontrahenta, symbol_dokumentu, data_utworzenia, planowana_data_dostawy, ilosc_dostarczana, waga, wartosc_dokumentu, miejscowosc_dostawy, status) VALUES ('{nazwa_kontrahenta}', '{symbol_dokumentu}', '{data_utworzenia}', '{planowana_data_dostawy}', {ilosc_dostarczana}, {waga}, {wartosc_dokumentu}, '{miejscowosc_dostawy}', 'planowana');"
        try:
            self.cur.execute(add_value)
            self.conn.commit()

        except:
            print("Wprowadzono nie poprawne danie, spróbuj jeszcze raz w poprawnymi danymi")

    def km_samochodow(self): # uzyskanie km wszystkich samochodow
        km_value = "select samochod, sum(km) from trasy group by samochod;" # statment uzyskania km
        self.cur.execute(km_value) # wykananie statmentu
        dane_km = self.cur.fetchall() # uzyskanei km
        return dane_km # zwrot danych

    def km_samochod(self,nr_rej):
        km_sum = f"select sum(km) from trasy WHERE samochod = '{nr_rej}' ;" # statment uzyskania km
        self.cur.execute(km_sum) # wykananie statmentu
        dane_km = self.cur.fetchall() # uzyskanei km
        return dane_km[0][0] # zwrot danych

    def dodanie_tabeli_samochod(self,nr_rejestracyjny,wielekrotnosc,opis,data=None): #automatyczne dodawanie pozycji do bazy danych transportow
        if data == None:
            d = datetime.now().date()
        else:
            d = data

        if opis == 'wymiana_oleju':
            sprawdzenie_czy_istnieje = f"SELECT * FROM koszty_samochodow WHERE samochod = '{nr_rejestracyjny}' AND oznaczenie_stale = {wielekrotnosc};"
        elif opis == 'przeglad':
            sprawdzenie_czy_istnieje = f"SELECT * from koszty_samochodow WHERE samochod = '{nr_rejestracyjny}' AND  opis = '{opis}' AND planowana_data_wykonania = '{d}'"

        self.cur.execute(sprawdzenie_czy_istnieje)
        dane_samochodu = self.cur.fetchall()

        if len(dane_samochodu) == 0: # sprawdzenie czy obiekt znajduje sie w bazie
            # if dane_samochodu[0][4] == 0.0: # sprawdzenie czy usluga juz nie zostala wykonana
                # print(f'\nKonieczne jest wykonanie {opis} w samochodzie {nr_rejestracyjny}.\nPowinno być wykonane {dane_samochodu[0][2]}. Jeżeli zostało już wykonane porszę dodać pozycje kosztową.\n')
        # else:
            new_row = f"INSERT INTO koszty_samochodow (samochod, planowana_data_wykonania, koszt, opis,oznaczenie_stale) VALUES ('{nr_rejestracyjny}', '{d}', 0, '{opis}', {wielekrotnosc});"
            self.cur.execute(new_row)
            self.conn.commit()
            print(f"Konieczna wymiana oleju w {nr_rejestracyjny}")

    def update_tabeli_samochod(self,nr_id,koszt): # aktualizowanie tabeli kosztow
        d1 = datetime.now().date() # uzyskanie daty
        update_kosztow_transportu = f"UPDATE koszty_samochodow SET koszt = {koszt}, data_wykonania = '{d1}' WHERE id= '{nr_id}';"
        self.cur.execute(update_kosztow_transportu)
        self.conn.commit()

    def wyswietl_tabele_kosztow(self): # wyswietlanie tabeli kosztow
        wyswietlenie ='SELECT * FROM koszty_samochodow ORDER BY id'
        self.cur.execute(wyswietlenie)
        dane_kosztow = self.cur.fetchall()
        print('id, samochod,planowana_data_wykonania,koszt,opis,oznaczenie_stale')
        for koszty in dane_kosztow:
            print(koszty)

    def dodanie_do_tabeli_kosztow(self,nr_rejestracyjny,usluga,koszt): # dodawanie nowych pozycji do bazy danych transportów
        d1 = datetime.now().date() # uzyskanie daty
        ilosc_rekordow_statment = f"SELECT COUNT(*) FROM koszty_samochodow WHERE samochod = '{nr_rejestracyjny}' AND opis = '{usluga}';" # sprawdzenie czy jest juz taki opis w tabeli
        self.cur.execute(ilosc_rekordow_statment) #wykonanie ilości rekordow statment
        ilosc_rekordow = self.cur.fetchall() # uzyskanie ilości rekordow
        statment = f"INSERT INTO koszty_samochodow (samochod, planowana_data_wykonania, data_wykonania, koszt, opis, oznaczenie_stale)  VALUES ( '{nr_rejestracyjny}' , '{d1}' , '{d1}' , {koszt} , '{usluga}' , {ilosc_rekordow[0][0]+1});" # pełny statment dodający
        self.cur.execute(statment) # wykonanie statmentu
        self.conn.commit()

    def koszty_przejechania_km(self,miesiac,rok=datetime.now().year,nr_rejestracyjny=None): # defoltowo wprowadzonych jest aktualny rok
        warunek_miesiac ="" # warunek dniowy wchodzi jako lista
        for m in miesiac:
            warunek_miesiac += f"EXTRACT(MONTH FROM planowana_data_wykonania) = {m} OR "

        warunek_miesiac = warunek_miesiac[:-3]
        if nr_rejestracyjny == None:
            warunek_auta =""

        else:
            warunek_auta =f" AND samochod = '{nr_rejestracyjny}'"

        wszystkie_auta = f"SELECT SUM(koszt) FROM koszty_samochodow WHERE {warunek_miesiac}AND EXTRACT(YEAR FROM planowana_data_wykonania) = {rok}{warunek_auta};"
        self.cur.execute(wszystkie_auta)
        koszt_samochod = self.cur.fetchall()

        wszystkie_km = f"SELECT SUM(km) FROM trasy WHERE {warunek_miesiac}AND EXTRACT(YEAR FROM planowana_data_wykonania) = {rok}{warunek_auta};"
        self.cur.execute(wszystkie_km.replace("planowana_data_wykonania","data_dostawy"))
        suma_km = self.cur.fetchall()
        if type(koszt_samochod[0][0]) == float and type(suma_km[0][0]) == float :
            koszt_km = koszt_samochod[0][0]/suma_km[0][0]
            return (round(koszt_km,2))
        else:
            return "Niepoprawne dane"

    def nierozliczone_pozycje_kosztowe_transport(self):
        puste_wiersze = "SELECT * from koszty_samochodow WHERE data_wykonania IS NULL;"  # uzyskanie wierszow z pustym wierszem data wykonania
        self.cur.execute(puste_wiersze)  # wykananie statmentu
        wiersze_do_wyjasnienia = self.cur.fetchall()  # uzyskanei km
        return wiersze_do_wyjasnienia  # zwrot danych

    def generowanie_towaru(self):
        d = datetime.now().date()
        # dzis = int(d.strftime('%w'))

        dzis = 3  # test
        x = self.tydzien()[dzis]
        lista_generat = []
        for _ in range(len(x)):
            palety = random.randint(1,10)
            id_dokumentu = random.choices(string.ascii_letters, k=5)
            id_dokumentu = "".join(id_dokumentu).lower()
            # lista_generat.append((id_dokumentu,random.choice(string.ascii_letters).upper(), random.choice(x),palety, palety*random.randint(500,1500)))
            self.dodanie_faktury(nazwa_kontrahenta=random.choice(string.ascii_letters).upper(),symbol_dokumentu=id_dokumentu,data_utworzenia=datetime.now().date(),planowana_data_dostawy=None,ilosc_dostarczana=str(palety),waga=str(palety*random.randint(500,1500)),wartosc_dokumentu='997',miejscowosc_dostawy=random.choice(x))
        # print(lista_generat)

    def ile_tras_nowe_trasy(self):
        ilosc_tras_query = r"SELECT MAX(nr_zlecenia::float) AS max_value FROM nowe_trasy WHERE nr_zlecenia ~ E'^\\d+(\\.\\d+)?$'"  
        self.cur.execute(ilosc_tras_query)
        dane = self.cur.fetchall()
        
        return int(dane[0][0])
        
    def przesylka_nowe_trasy(self,przesylka): #zmiana z copy na insert into z wzgledu na problem z deplomentem, koniecznosc dostosowania do kazdego komputera
        
        with open(przesylka, 'r', newline='') as file:
            reader = csv.reader(file)
            for rrr in reader:
                #wyslanie danych
                tekst_dodania = str(rrr).replace("[","(").replace("]",")")
                zapytanie = f'''INSERT INTO nowe_trasy( nr_zlecenia ,data_dostawy ,miejscowosci ,firma ,ilosc_dostarczana ,samochod ,koszt ,km, model_dostawy ) 
                VALUES 
                {tekst_dodania};'''
                self.cur.execute(zapytanie)
                self.conn.commit()

                #zmiana statusu dokumenty
                zmiana_statusu_warunek_planowana = f"miejscowosc_dostawy = '{rrr[2]}' AND nazwa_kontrahenta = '{rrr[3]}' AND status = 'planowana';"
                self.zmiana_statusu(warunek_dniowy=zmiana_statusu_warunek_planowana,status="test"+rrr[8])