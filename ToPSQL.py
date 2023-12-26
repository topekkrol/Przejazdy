import psycopg2
from datetime import datetime



def polaczenie(zadanie='get_values'):
    hostname = 'localhost'
    database = 'Transport'
    username = 'postgres'
    pwd = 'Wisnia12'
    port_id = 5432
    conn = None
    cur = None

    warunek_dniowy = teskt()
    create_script_dokumenty = ''' CREATE TABLE IF NOT EXISTS Dokumenty1 (
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
                             nr_zlecenia VARCHAR(200),
                             miejscowosc_dostawy VARCHAR(200),
                             nazwa_kontrahenta VARCHAR(200),
                             ilosc_dostarczana REAL,
                             data_utworzenia DATE)'''


    copy_value_test = "copy Dokumenty (nazwa_kontrahenta, symbol_dokumentu, data_utworzenia,	planowana_data_dostawy,	ilosc_dostarczana, waga, wartosc_dokumentu, miejscowosc_dostawy, status  ) FROM 'C:/Nowy_folder/dane_do_karmienia.csv' DELIMITER ';' ENCODING 'UTF8' CSV HEADER"

    get_values = F"SELECT nazwa_kontrahenta,miejscowosc_dostawy,sum(ilosc_dostarczana),sum(waga) FROM dokumenty WHERE Status = 'planowana' AND {warunek_dniowy} GROUP BY nazwa_kontrahenta,miejscowosc_dostawy;"

    ilosc_tras = "SELECT count(*) FROM trasy;"
    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)

        cur = conn.cursor()
        # cur.execute(create_script_trasy)
        # cur.execute(copy_value_test)
        if zadanie =='get_values':
            cur.execute(get_values)
            dane = cur.fetchall()
        if zadanie == 'ile_tras':
            cur.execute(ilosc_tras)
            dane = cur.fetchall()

        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    try:
        return dane
    except:
        return None
def teskt():
    d = datetime.now().date()
    dzis = int(d.strftime('%w'))

    dzis =1  # test

    tydzien ={
        1 : ['Lezajsk','Bilgoraj','Zamosc','Strzyzow','Jaslo','Krosno','Kolbuszowa'],
        2 : ['Lezajsk','Bilgoraj','Zamosc','Strzyzow','Jaslo','Krosno'],
        3 : ['Bilgoraj','Zamosc','Stalowa Wola','Tarnobrzeg'],
        4 : ['Lezajsk','Stalowa Wola','Nisko','Rudnik nad Sanem','Kolbuszowa','Mielec','Tarnobrzeg','Debica'],
        5 : ['Bilgoraj','Zamosc','Stalowa Wola','Mielec','Lezajsk'],
    }
    zwrot=''
    for dni in tydzien[dzis]:
        zwrot += "miejscowosc_dostawy='"+dni+"' OR "
    zwrot = zwrot[:-3]
    return zwrot