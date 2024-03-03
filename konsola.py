import datetime
import time
from datetime import date
from flota import Samochod
from DoPSGl import PolaczenieBazy
from sprawdzenie_csv import czy_mamy_tak_miejscowosc
from LatandLon import dodanie_miejscowosci
import importlib
Samochod.alert_przeglady()
print('\n')
ilosc_wykonanych_podzialow = 0
while __name__ =='__main__':

    wybor = input("Wybierz do chcesz zrobic: \n1. Zakoncz\n2. Podziel towar na transport\n3. Wyswietl flote pojazdow \n4. Wyswietl towar do transportu\n5. Wyswietl zlecenia transportwe\n6. Wyswietl harmonogram tras\nWybor: ")

    try:
        wybor = int(wybor)
    except:
        print("Prosze wybrac poprawna odpowiedz")
        time.sleep(3)
        continue

    match wybor:
        case 1:
            break
        case 2:
            import nowy_main_light
            if ilosc_wykonanych_podzialow >0:
                importlib.reload(nowy_main_light)
            ilosc_wykonanych_podzialow += 1
        case 3:
            Samochod.odczytaj_z_pliku_wszystkie()
            Samochod.wyswietl_wszystkie()
            wybor3 = input("Wybierz do chcesz zrobic: \n1.Dodać nowy samochod\n2.Usunac samochod\n3.Przejść do  kosztów samochodów\n4.Koszt kilometra")
            try:
                wybor3 = int(wybor3)
            except:
                print("Prosze wybrac poprawna odpowiedz")
                time.sleep(3)
                continue
            print("wybor",wybor3)
            match wybor3:
                case 1:
                    nr_rejestracyjny =input("Wprowadz numer rejestracyjny pojazdu: ").upper()
                    marka = input("Jakie marki jest samochod: ")
                    ladowosc_pal = input("Wprowdza ile palet Euro miesci sie na samochod: ")
                    ladowosc_waga = input("Wprowadz kilogranow moze zaladowac samochod maksymalnie: ")
                    przeglad = input('Wprowadz date w formacie RRRR-MM-DD: ').split('-')
                    rok, miesiac, dzien = [int(item) for item in przeglad]

                    data_przeladu = date(rok, miesiac, dzien)
                    datetime_przelad = datetime.datetime.combine(data_przeladu, datetime.time()) # uzyskanie wlasciwego formatu dla pozostałych obiektow w klasie
                    nr_rejestracyjny = Samochod(nr_rejestracyjny=nr_rejestracyjny,ladownosc_waga=ladowosc_waga,ladowosc_palety=ladowosc_pal, marka=marka,przeglad=datetime_przelad)

                    Samochod.zapisz_do_pliku()
                    # Samochod.wyswietl_wszystkie()
                case 2:
                    nr_rejestracyjny =input("Wprowadz numer rejestracyjny pojazdu: ").upper()
                    try:
                        Samochod.usun_obiekt(nr_rejestracyjny)
                        print("Samochod usuniety")
                    except:
                        print("Samochod o takim numerze rejestracyjnym nie istnieje w flocie.")
                case 3:
                    PolaczenieBazy().wyswietl_tabele_kosztow()
                    wybor2 = input('Jeżeli chcesz zaktualizować pozycje z listy wybierz 1, jeżeli chcesz dodać nową pozycje wybierz 2.')
                    if wybor2 == str(1):
                        wprowadz_id = input("Wprowadz id kosztu: ")
                        koszt_1 = input('Wprowadz ile kosztowała usługa')
                        PolaczenieBazy().update_tabeli_samochod(wprowadz_id,koszt_1)

                    if wybor2 == str(2):

                        nr_rej =input("Wprowadz numer rejestracyjny pojazdu: ").upper()
                        if Samochod.dane_auta(nr_rej=nr_rej) == None:
                            print("Proszę numeru rejestracyjnego nie ma w bazie, proszę wprowadzić poprawny")
                            continue
                        usluga = input('Wprowadz opis uslugi (serwis/wynagrodzenie/inne): ')
                        usluga = usluga.replace(" ","_").lower()
                        while usluga == "wymiana_oleju" or usluga =="przeglad":
                            print("Zastrzeżona nazwa, wprowadz inną")
                            usluga = input('Wprowadz opis uslugi')
                        if usluga == "wynagrodzenie":
                            prawcownik = input("Wprowadz imię i nazwisko pracownika: ")
                            prawcownik = prawcownik.replace(" ", "_").lower()
                            usluga = usluga+" :"+prawcownik
                        elif usluga == 'inne' or usluga == 'serwis':
                            cd_uslugi = input("wprowadz dalszy opis: ")
                            cd_uslugi = cd_uslugi.replace(" ", "_").lower()
                            usluga = usluga + " :" + cd_uslugi
                        else:
                            print("Wprowadzona nazwa jest błędna, spróbuj jeszcze raz.")
                            continue
                        koszt_2 = input('Wprowadz ile kosztowała usługa')

                        PolaczenieBazy().dodanie_do_tabeli_kosztow(nr_rej,usluga,koszt_2)

                case 4:
                    wybor5 = input("Jeżeli chcesz sprawdzić koszt dla konkretnego samochodu wprowadź numer rejestracyjny, jeżeli chcesz uzyskać koszt ogólny pozostaw miejsce puste i wciśnij Enter.")
                    wybor_miesiac = input("Wprowadz po przecinku za jakie miesiące chcesz dane :")
                    # print(wybor_miesiac)
                    try:
                        lista_miesiecy = [int(num) for num in wybor_miesiac.split(",")]
                    except:
                        print("Wprowadzono nie poprawne wartosci, spróbuj jeszcze raz w poprawnymi wartosciami")
                        continue
                    print(lista_miesiecy)
                    if wybor5 == "":
                        print(PolaczenieBazy().koszty_przejechania_km(miesiac=lista_miesiecy),"zł/km średnio")
                    else:
                        print(PolaczenieBazy().koszty_przejechania_km(miesiac=lista_miesiecy,nr_rejestracyjny=wybor5))
                case _:
                    continue
        case 4:
            dane_do_wyswietlenia = PolaczenieBazy().get_values( status='planowana')
            if len(dane_do_wyswietlenia) == 0.0:
                brak_dokumentow = input("Nie ma zadnych dokumentow do transportu, jeżeli chcesz wygenerować dokumenty wciśnij 1, jeżeli nie wciśnij 0: ")
                if brak_dokumentow == str(1):
                    PolaczenieBazy().generowanie_towaru()
                    dane_do_wyswietlenia = PolaczenieBazy().get_values( status='planowana')
            print("Klient",'Miasto dostawy','Ilosc palet','Waga')
            for _ in dane_do_wyswietlenia:
                print(_)

            nowy_record = input("Jezeli chcesz dodac nowy dokument wcisnij 1")

            while nowy_record == "1":
                miejscowosc_dostawy = input("Miejsce dostawy : ")
                if czy_mamy_tak_miejscowosc(miejscowosc_dostawy) == 0:
                    dodanie_miejscowosci(miejscowosc_dostawy)

                nazwa_kontrahenta = input("Nazwa kontrahenta : ")
                symbol_dokumentu = input("Symbol dokumentu : ")
                data_dostawy = input("Data dostawy (yyyy-mm-dd) : ")
                ilosc = input("Ile palet euro jest dostarczanych ( liczby calkowite ) : ")
                waga =input("Jaka jest waga dostarczanego towaru (kg) : ")
                wartosc = input("Wartosc dokumentu netto : ")
                PolaczenieBazy().dodanie_faktury(nazwa_kontrahenta,symbol_dokumentu,data_dostawy,data_dostawy,ilosc,waga,wartosc,miejscowosc_dostawy) # bazana danych jest przygotowana na przyjecie planowanej daty dostawy i statusu, ale na obecnym etapie ustawiamy domyślne.
                print("Dokument dodany do transportu")

                nowy_record =input("Jezeli chcesz dodac kolejny dokument, wcisnij 1")

        case 5:
            dane = PolaczenieBazy()
            dane_do_przedstawienia = dane.wszystkie_trasy()
            for _ in dane_do_przedstawienia:
                print(_)

            update_km = input("Jeżeli chcesz zaktualizowac km na ktorys zleceniu ,wpisz numer zlecenia. Jezeli nie chcesz to wpisz Q.")

            try:
                update_km = int(update_km)
                km = input("Ilosc pokonanych przez samochod kilometrow podczas trasy : ")
                dane.update_km(nr_trasy=update_km, km=km)
            except:
                print("Wprowadzono niepoprawny znak")

            Samochod.przeglady()

        case 6:
            dane = PolaczenieBazy()
            harmonogram = dane.tydzien()
            day_names = ['',"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

            for _ in harmonogram:

                print(day_names[_],harmonogram[_])
            wybor4 = input("Jeżeli chcesz dodać nową miejscowość do harmonogramu transportowego wciśnij 1")
            if wybor4 == "1":
                miejscowosc = input("Wprowadz nazwe miejscowosci jaką chcesz dodać: ")
                nr_trasy = input("Wprowadz numer trasy do której ma zostać dodana: ")
                try:
                    dodanie_miejscowosci(miejscowosc)
                    dane.tydzien(nowe_miasto=miejscowosc,trasa=nr_trasy)
                    print("Pomyślnie udalo się dodać miejscowosc do trasy")
                except Exception as e:
                    print(e,"Nie udalo się dodać trasy spróbuj ponownie.")
            else:
                continue

        case _:
            print("Prosze wybrac poprawna odpowiedz")
            time.sleep(3)
            continue
