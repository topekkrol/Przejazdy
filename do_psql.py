import psycopg2
from datetime import datetime
import pickle
import random
import string
import csv
from hasla import haslo_psql,db_psql
class PolaczenieBazy:
    def __init__(self):
        self.hostname = 'localhost'
        self.database = db_psql
        self.username = 'postgres'
        self.pwd = haslo_psql
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

    def get_values_custome(self): # dodać sprawdzanie dnia >= data_utworzenia i dodac sprawdzanie wartosci. Stworzenia warunku status do pobierania danych i sprawdzania ich
        warunek_dniowy = "Status = 'testowania' AND ("+self.teskt()+")"
        get_values_query = f"SELECT nazwa_kontrahenta,miejscowosc_dostawy,sum(ilosc_dostarczana),sum(waga) FROM dokumenty WHERE {warunek_dniowy} GROUP BY nazwa_kontrahenta,miejscowosc_dostawy;"
        self.cur.execute(get_values_query)
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

        self.cur.execute(create_script_dokumenty)
        self.cur.execute(create_script_trasy)
        self.cur.execute(create_script_koszty_samochodow)
        self.cur.execute(create_script_nowe_trasy)
        self.conn.commit()

    def tydzien(self,nowe_miasto="",trasa=""):

        tydzien = {
            1: ['Jaroslaw', 'Przeworsk', 'Lubaczow', 'Tomaszow', 'Sanok', 'Brzozow','Stalowa Wola','Nisko','Rudnik nad Sanem'], 
            2: ['Lezajsk', 'Bilgoraj', 'Janow Lubelski', 'Strzyzow', 'Jaslo', 'Stalowa Wola', 'Kolbuszowa', 'Mielec',
                'Debica', 'Tarnobrzeg'],  
            3: ['Bilgoraj', 'Zamosc', 'Stalowa Wola', 'Tarnobrzeg','Janow Lubelski'], 
            4: ["Staszow","Debica","Gorlice","Jaslo","Krosno","Strzyzow"], 
            5: ['Bilgoraj', 'Zamosc', 'Stalowa Wola', 'Mielec', 'Lezajsk'],
        }
        if nowe_miasto == 3: # zapisywania defoltowych tras, przywrocenie ustawien do 
            with open("tydzien.pkl", 'wb') as file:
                pickle.dump(tydzien, file)

        elif len(nowe_miasto)>2: # dodawania nowej miejscowsci
            try:
                with open("tydzien.pkl", 'rb') as plik:
                    x = pickle.load(plik)
                    miasta_do_transportu = x[int(trasa)]
                    miasta_do_transportu.append(nowe_miasto)
                    x[int(trasa)] = miasta_do_transportu

                    with open("tydzien.pkl", 'wb') as file:
                        pickle.dump(x, file)
            except:
                print("Niepoprawne dane, proszę spróbować jeszcze raz.")

        else: # wyswietlania miast do transporti
            with open("tydzien.pkl", 'rb') as plik:
                x = pickle.load(plik)
                return x

    def teskt(self):
        d = datetime.now().date()
        dzis = int(d.strftime('%w'))
        if dzis == 0 or dzis ==6:
            dzis = 1
        #dzis = 3  # test
        tydzien = self.tydzien()
        zwrot = ''
        for dni in tydzien[dzis]:
            zwrot += "miejscowosc_dostawy='" + dni + "' OR "
        zwrot += f"planowana_data_dostawy <= '{d}'"
        # zwrot = zwrot[:-3]
        return zwrot

    def dodanie_faktury(self,nazwa_kontrahenta,symbol_dokumentu,data_utworzenia,planowana_data_dostawy, ilosc_dostarczana,waga,wartosc_dokumentu,miejscowosc_dostawy,status="planowana"):
        # status odrazu ustawiamy na 'planowana'
        if planowana_data_dostawy == None:
            add_value = f"INSERT INTO dokumenty (nazwa_kontrahenta, symbol_dokumentu, data_utworzenia, ilosc_dostarczana, waga, wartosc_dokumentu, miejscowosc_dostawy, status) VALUES ('{nazwa_kontrahenta}', '{symbol_dokumentu}', '{data_utworzenia}', {ilosc_dostarczana}, {waga}, {wartosc_dokumentu}, '{miejscowosc_dostawy}', '{status}');"
        else:
            add_value = f"INSERT INTO dokumenty (nazwa_kontrahenta, symbol_dokumentu, data_utworzenia, planowana_data_dostawy, ilosc_dostarczana, waga, wartosc_dokumentu, miejscowosc_dostawy, status) VALUES ('{nazwa_kontrahenta}', '{symbol_dokumentu}', '{data_utworzenia}', '{planowana_data_dostawy}', {ilosc_dostarczana}, {waga}, {wartosc_dokumentu}, '{miejscowosc_dostawy}', '{status}');"

        try:
            self.cur.execute(add_value)
            self.conn.commit()

        except:
            print("Wprowadzono nie poprawne danie, spróbuj jeszcze raz w poprawnymi danymi")

    def update_tabeli_samochod(self,nr_id,koszt): # aktualizowanie tabeli kosztow
        d1 = datetime.now().date() # uzyskanie daty
        update_kosztow_transportu = f"UPDATE koszty_samochodow SET koszt = {koszt}, data_wykonania = '{d1}' WHERE id= '{nr_id}';"
        self.cur.execute(update_kosztow_transportu)
        self.conn.commit()

    def generowanie_towaru_custome(self):
        d = datetime.now().date()
        dzis = int(d.strftime('%w'))

        if dzis == 0 or dzis ==6:
            dzis = 1

        #dzis = 3  # test
        x = self.tydzien()[dzis]
  
        for _ in range(len(x)):
            palety = random.randint(1,10)
            id_dokumentu = random.choices(string.ascii_letters, k=5)
            id_dokumentu = "".join(id_dokumentu).lower()
            # lista_generat.append((id_dokumentu,random.choice(string.ascii_letters).upper(), random.choice(x),palety, palety*random.randint(500,1500)))
            self.dodanie_faktury(nazwa_kontrahenta=random.choice(string.ascii_letters).upper(),symbol_dokumentu=id_dokumentu,data_utworzenia=datetime.now().date(),planowana_data_dostawy=None,ilosc_dostarczana=str(palety),waga=str(palety*random.randint(500,1500)),wartosc_dokumentu='997',miejscowosc_dostawy=random.choice(x),status="testowania")

    def usuniecie_testow(self):
        dzis = datetime.now().strftime("%Y-%m-%d %H:%M")
        testy_do_usuniecia = f"UPDATE dokumenty set status = 'zrealizowane {dzis} ' where status = 'testowania';"
        self.cur.execute(testy_do_usuniecia)
        self.conn.commit()