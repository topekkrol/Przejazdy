from do_psql import PolaczenieBazy
import calendar
import locale

def dane_o_harmonogramie():
    locale.setlocale(locale.LC_ALL, 'pl_PL')
    nazwa_dni_tygodnia = list(calendar.day_name)

    harmonogram_dostaw = {}
    dane = PolaczenieBazy().tydzien()
    for dni_tygodnia in dane:
        harmonogram_dostaw[nazwa_dni_tygodnia[dni_tygodnia-1].title()] = str(dane[dni_tygodnia]).replace("[","").replace("]","").replace("'","")

    return harmonogram_dostaw
