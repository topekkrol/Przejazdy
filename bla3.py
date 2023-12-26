import datetime
import click
import importlib
from tabulate import tabulate
from datetime import date
import subprocess

from flota import Samochod
from DoPSGl import PolaczenieBazy
from sprawdzenie_csv import czy_mamy_tak_miejscowosc
from LatandLon import dodanie_miejscowosci

def validate_input(value):
    try:
        value = int(value)
    except:
        value = value
    if type(value) != int:

        raise click.BadParameter(f"'{value}' nie jest obslugiwana przez program.")
    return value

def validate_day(day):
    dni_tydzien = ['0','Poniedzialek', 'Wtorek', 'Sroda', 'Czwartek', 'Piatek']
    day = day. capitalize()
    if day in dni_tydzien:
        return day
    else:
        raise click.BadParameter(f"Program nie obslguje dany wejsciowych takich jak: {day}")
@click.command()
def color_cli():
    ilosc_wykonanych_podzialow = 0
    while True:

        user_input = click.prompt(text='Wybierz do chcesz zrobic: \n1. Zakoncz\n2. Podziel towar na transport\n3. Wyswietl flote pojazdow \n4. Wyswietl towar do transportu\n5. Wyswietl zlecenia transportwe\n6. Wyswietl harmonogram tras\n7. Koszt kilometra\nWybor', value_proc=validate_input)

        if user_input == 1:
            break

        elif user_input == 2:
            subprocess.call(['python', 'main.py'])

        elif user_input == 3:
            Samochod.odczytaj_z_pliku_wszystkie()
            Samochod.wyswietl_wszystkie()
            wybor3 = click.prompt(
                    "Wybierz do chcesz zrobic: \n1. Wyjsc\n2. Dodać nowy samochod\n3. Usunac samochod\n4. Przejść do  kosztów samochodów\nWybor ", value_proc=validate_input)

            if wybor3 == 1:
                continue
            if wybor3 == 2:
                nr_rejestracyjny = input("Wprowadz numer rejestracyjny pojazdu: ").upper()
                marka = input("Jakie marki jest samochod: ")
                ladowosc_pal = input("Wprowdza ile palet Euro miesci sie na samochod: ")
                ladowosc_waga = input("Wprowadz kilogranow moze zaladowac samochod maksymalnie: ")
                przeglad = input('Wprowadz date w formacie RRRR-MM-DD: ').split('-')
                rok, miesiac, dzien = [int(item) for item in przeglad]

                data_przeladu = date(rok, miesiac, dzien)
                datetime_przelad = datetime.datetime.combine(data_przeladu,
                                                                 datetime.time())  # uzyskanie wlasciwego formatu dla pozostałych obiektow w klasie
                nr_rejestracyjny = Samochod(nr_rejestracyjny=nr_rejestracyjny, ladownosc_waga=ladowosc_waga,
                                                    ladowosc_palety=ladowosc_pal, marka=marka, przeglad=datetime_przelad)

                Samochod.zapisz_do_pliku()

            if wybor3 == 3:
                nr_rejestracyjny = input("Wprowadz numer rejestracyjny pojazdu: ").upper()
                try:
                    Samochod.usun_obiekt(nr_rejestracyjny)
                    print("Samochod usuniety")
                except:
                    print("Samochod o takim numerze rejestracyjnym nie istnieje w flocie.")
            if wybor3 == 4:
                PolaczenieBazy().wyswietl_tabele_kosztow()
                wybor2 = input(
                            'Jeżeli chcesz zaktualizować pozycje z listy wybierz 1, jeżeli chcesz dodać nową pozycje wybierz 2.')
                if wybor2 == str(1):
                        wprowadz_id = input("Wprowadz id kosztu: ")
                        koszt_1 = input('Wprowadz ile kosztowała usługa')
                        PolaczenieBazy().update_tabeli_samochod(wprowadz_id, koszt_1)

                if wybor2 == str(2):

                    nr_rej = input("Wprowadz numer rejestracyjny pojazdu: ").upper()
                    if Samochod.dane_auta(nr_rej=nr_rej) == None:
                        print("Proszę numeru rejestracyjnego nie ma w bazie, proszę wprowadzić poprawny")
                        continue
                    usluga = input('Wprowadz opis uslugi (serwis/wynagrodzenie/inne): ')
                    usluga = usluga.replace(" ", "_").lower()
                    while usluga == "wymiana_oleju" or usluga == "przeglad":
                        print("Zastrzeżona nazwa, wprowadz inną")
                        usluga = input('Wprowadz opis uslugi')
                    if usluga == "wynagrodzenie":
                        prawcownik = input("Wprowadz imię i nazwisko pracownika: ")
                        prawcownik = prawcownik.replace(" ", "_").lower()
                        usluga = usluga + " :" + prawcownik
                    elif usluga == 'inne' or usluga == 'serwis':
                        cd_uslugi = input("wprowadz dalszy opis: ")
                        cd_uslugi = cd_uslugi.replace(" ", "_").lower()
                        usluga = usluga + " :" + cd_uslugi
                    else:
                        print("Wprowadzona nazwa jest błędna, spróbuj jeszcze raz.")
                        continue
                    koszt_2 = input('Wprowadz ile kosztowała usługa')
                    PolaczenieBazy().dodanie_do_tabeli_kosztow(nr_rej, usluga, koszt_2)

            else:
                click.echo('Niepoprawna wartosc.')

        elif user_input == 4:
            dane_do_wyswietlenia = PolaczenieBazy().get_values(status='planowana')
            if len(dane_do_wyswietlenia) == 0.0:
                brak_dokumentow = click.prompt(
                    "Nie ma zadnych dokumentow do transportu, jeżeli chcesz wygenerować dokumenty wciśnij 1, jeżeli nie wciśnij 0", value_proc=validate_input)
                if brak_dokumentow == 1:
                    PolaczenieBazy().generowanie_towaru()
                    dane_do_wyswietlenia = PolaczenieBazy().get_values(status='planowana')
            click.echo("Klient , Miasto dostawy , Ilosc palet, Waga")
            for _ in dane_do_wyswietlenia:
                click.echo(_)


            while click.confirm("Chcesz dodac nowy dokuemnt?", default=False):
                miejscowosc_dostawy = input("Miejsce dostawy : ")
                if czy_mamy_tak_miejscowosc(miejscowosc_dostawy) == 0:
                    dodanie_miejscowosci(miejscowosc_dostawy)

                nazwa_kontrahenta = input("Nazwa kontrahenta : ")
                symbol_dokumentu = input("Symbol dokumentu : ")
                data_dostawy = input("Data dostawy (yyyy-mm-dd) : ")
                ilosc = input("Ile palet euro jest dostarczanych ( liczby calkowite ) : ")
                waga = input("Jaka jest waga dostarczanego towaru (kg) : ")
                wartosc = input("Wartosc dokumentu netto : ")
                PolaczenieBazy().dodanie_faktury(nazwa_kontrahenta, symbol_dokumentu, data_dostawy, data_dostawy, ilosc,
                                                 waga, wartosc,
                                                 miejscowosc_dostawy)  # bazana danych jest przygotowana na przyjecie planowanej daty dostawy i statusu, ale na obecnym etapie ustawiamy domyślne.
                click.echo("Dokument dodany do transportu")

        elif user_input == 5:
            dane = PolaczenieBazy()
            dane_do_przedstawienia = dane.wszystkie_trasy()
            naglowek = ['nr_zlecenia', 'miejscowosci_dostawy', 'kontrachenci','ilosc_dostarczana', 'samochod', 'data_dostawy', 'km']
            click.echo(tabulate(dane_do_przedstawienia,tablefmt='fancy_grid',headers=naglowek))

            trasa = click.prompt(text='Jeżeli chcesz zaktualizowac km na zleceniu ,wpisz numer zlecenia. Jezeli nie chcesz to wpisz 0.',value_proc=validate_input,)
            if trasa != 0:
                km = click.prompt(text='Ilosc pokonanych przez samochod kilometrow podczas trasy',type=int)
                wykonanie_aktualizacji_km = dane.update_km(nr_trasy=trasa,km=km)
                if wykonanie_aktualizacji_km == None:
                    click.echo("Niepoprawne wartosci")
                else:
                    click.echo(tabulate(wykonanie_aktualizacji_km,tablefmt='fancy_grid',headers=naglowek))

                Samochod.przeglady()

        elif user_input == 6:
            dane = PolaczenieBazy()
            harmonogram = dane.tydzien()
            dni_tydzien = ['Poniedzialek','Wtorek','Sroda','Czwartek','Piatek']
            click.echo(tabulate(harmonogram,headers=dni_tydzien,tablefmt='grid'))

            dzien = click.prompt("Jezeli chcesz zaktualizować harmonogram wprowadz ktory dzien",value_proc=validate_day,default='0',show_default=False)
            if dzien in dni_tydzien:
                miejscowosc = click.prompt("Wprowadz nazwe miejscowosci jaką chcesz dodać: ")
                try:
                    dodanie_miejscowosci(miejscowosc)
                    dane.tydzien(nowe_miasto=miejscowosc, trasa=dni_tydzien.index(dzien)+1)
                    click.echo("Pomyślnie udalo się dodać miejscowosc do trasy")
                except Exception as e:
                    click.echo("Nie udalo się dodać trasy spróbuj ponownie.")

        elif user_input == 7:
            wybor5 = click.prompt(
                "Jeżeli chcesz sprawdzić koszt dla konkretnego samochodu wprowadź numer rejestracyjny, jeżeli chcesz uzyskać koszt ogólny pozostaw miejsce puste i wciśnij Enter",default="",show_default=False)
            wybor_miesiac = click.prompt("Wprowadz po przecinku za jakie miesiące chcesz dane ")

            try:
                lista_miesiecy = [int(num) for num in wybor_miesiac.split(",")]
            except:
                click.echo("Wprowadzono nie poprawne wartosci, spróbuj jeszcze raz w poprawnymi wartosciami")
                continue

            if wybor5 == "":
                click.echo(PolaczenieBazy().koszty_przejechania_km(miesiac=lista_miesiecy))
                click.echo("zł/km średnio")
            else:
                click.echo("Kilometry samochodu")
                click.echo(wybor5)
                click.echo("kosztowowal")
                click.echo(PolaczenieBazy().koszty_przejechania_km(miesiac=lista_miesiecy, nr_rejestracyjny=wybor5))
    else:
        click.echo('Niepoprawna wartosc.')


if __name__ == '__main__':
    color_cli()
