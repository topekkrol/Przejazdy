koszty_spedycji = {
    '120x80': {
        500: {100: 98.18, 200: 102.37, 300: 118.79, 500: 124.48, 600: 147.69},
        800: {100: 129.05, 200: 135.84, 300: 156.21, 500: 163.13, 600: 196.06},
        1200: {100: 147.45, 200: 155.35, 300: 175.84, 500: 184.50, 600: 208.70}
    },
    '80x60': {
        200: {100: 80.51, 200: 87.06, 300: 87.67, 500: 94.35, 600: 106.07},
        300: {100: 93.11, 200: 104.59, 300: 106.20, 500: 114.60, 600: 129.05}
    },
    '120x120': {
        600: {100: 117.20, 200: 123.49, 300: 144.91, 500: 165.94, 600: 204.12},
        800: {100: 127.51, 200: 134.74, 300: 158.44, 500: 181.48, 600: 223.28},
        1200: {100: 141.43, 200: 152.45, 300: 175.60, 500: 201.43, 600: 234.39}
    },
    '80x180': {
        600: {100: 117.20, 200: 123.49, 300: 144.91, 500: 165.94, 600: 204.12},
        800: {100: 127.51, 200: 134.74, 300: 158.44, 500: 181.48, 600: 223.28},
        1200: {100: 141.43, 200: 152.45, 300: 175.60, 500: 201.43, 600: 234.39}
    }
}

dodatek_paliwowy = 0.15
dodatek_drogowy = 0.0846

def przypadek_beznadziejmy(palety,waga):
    srednia_waga = (waga/palety)
    if srednia_waga <= 500:
        srednia_waga = 500
    elif srednia_waga <= 800:
        srednia_waga = 800
    else:
        srednia_waga=1200

    palcie = []
    for _ in range(palety):
        palcie.append(srednia_waga)

    return palcie
def Kalkulator_od_dolu(km, waga, palety, lista_palet=None):
    if lista_palet is None:
        lista_palet = []


    if waga < 0:
        lista_palet.remove(1200)
        lista_palet.append(800)
        waga = 500

    if palety == 1:
        waga = int(waga / 100)

        if waga <= 5:
            waga = 500
        elif waga <= 8:
            waga = 800
        elif waga <= 12:
            waga = 1200
        elif waga > 12:
            return Kalkulator_od_dolu(km, waga * 100, palety=2, lista_palet=lista_palet)

        if waga > 100:
            lista_palet.append(waga)
            return lista_palet
    else:
        if waga % 500 == 0 or waga % 500 == 800 or waga % 500 == 1200:
            lista_palet.append(500)
            return Kalkulator_od_dolu(km, waga - 500, palety - 1, lista_palet=lista_palet)
        elif waga % 800 == 0 or waga % 800 == 500 or waga % 800 == 1200:
            lista_palet.append(800)
            return Kalkulator_od_dolu(km, waga - 800, palety - 1, lista_palet=lista_palet)
        elif waga % 1200 == 0 or waga % 1200 == 500 or waga % 1200 == 800:
            lista_palet.append(1200)
            return Kalkulator_od_dolu(km, waga - 1200, palety - 1, lista_palet=lista_palet)
        else:
            if waga < 800:
                lista_palet.append(500)
                return Kalkulator_od_dolu(km, waga - 500, palety - 1, lista_palet=lista_palet)
            elif waga < 1200:
                lista_palet.append(800)
                return Kalkulator_od_dolu(km, waga - 800, palety - 1, lista_palet=lista_palet)
            else:
                lista_palet.append(1200)
                return Kalkulator_od_dolu(km, waga - 1200, palety - 1, lista_palet=lista_palet)

    return (0, [])

def ObliczanieKosztow(lista,km):
    koszt = 0
    if km %100 == 0:
        km = km
    else:
        km = (int(km/100)+1)*100
    if km == 400:
        km = 300
    elif km > 600:
        km =600

    for waga in lista:
        koszt += (1+dodatek_paliwowy+dodatek_drogowy) * koszty_spedycji['120x80'][waga][km]

    return koszt


def Kalkulator_od_góry (km, waga, palety, lista_palet=None):
    if lista_palet is None:
        lista_palet = []



    if waga < 0:
        lista_palet.remove(1200)
        lista_palet.append(800)
        waga = 500

    if palety == 1:
        waga = int(waga / 100)

        if waga <= 5:
            waga = 500
        elif waga <= 8:
            waga = 800
        elif waga <= 12:
            waga = 1200
        elif waga > 12:
            return Kalkulator_od_góry(km, waga * 100, palety=2, lista_palet=lista_palet)

        if waga > 100:
            lista_palet.append(waga)
            return lista_palet
    else:
        if waga % 1200 == 0 or waga % 1200 == 500 or waga % 1200 == 800:
            lista_palet.append(1200)
            return Kalkulator_od_góry(km, waga - 1200, palety - 1, lista_palet=lista_palet)
        elif (waga % 800 == 0 or waga % 800 == 500 or waga % 800 == 1200) and waga < 2400:
            lista_palet.append(800)
            return Kalkulator_od_góry(km, waga - 800, palety - 1, lista_palet=lista_palet)
        elif (waga % 500 == 0 or waga % 500 == 800 or waga % 500 == 1200) and waga < 1500:
            lista_palet.append(500)
            return Kalkulator_od_góry(km, waga - 500, palety - 1, lista_palet=lista_palet)
        else:
            lista_palet.append(1200)
            return Kalkulator_od_góry(km, waga - 1200, palety - 1, lista_palet=lista_palet)


    return (0, [])

def Kalulator_500 (waga, palety):
    lista_palet = []
    if waga/palety < 500:
        for _ in range(palety):
            lista_palet.append(500)
    return lista_palet

def redukcja(lista_redukcji,ile_zredukowac):
    if ile_zredukowac < -300:
        for palcie in lista_redukcji:
            if palcie == 1200 and ile_zredukowac < -400:
                lista_redukcji.remove(1200)
                lista_redukcji.append(800)
                ile_zredukowac += 400
            if palcie == 800 and ile_zredukowac < -300:
                lista_redukcji.remove(800)
                lista_redukcji.append(500)
                ile_zredukowac += 300

    return lista_redukcji

def kalkulator_spedycja(km, waga, palety=1):
    try:
        gora = Kalkulator_od_góry(km,waga,palety)
    except:
        gora = przypadek_beznadziejmy(palety=palety,waga=waga)
    try:
        dol = Kalkulator_od_dolu(km,waga,palety)
    except:
        dol = przypadek_beznadziejmy(palety=palety, waga=waga)

    palety500 = Kalulator_500(waga,palety)
    roznica_gora = waga - sum(gora)
    gora = redukcja(gora,roznica_gora)
    if len(gora) > 0:
        koszt_gora = ObliczanieKosztow(gora, km)
    else:
        koszt_gora = 694201312
    roznice_dol = waga - sum(dol)
    dol = redukcja(dol,roznice_dol)
    if len(dol) > 0:
        koszt_dol = ObliczanieKosztow(dol, km)
    else:
        koszt_dol = 694201312

    roznica_500 = waga - sum(palety500)
    palety500  = redukcja(palety500,roznica_500)
    if len(palety500) > 0:
        koszt_500 = ObliczanieKosztow(palety500, km)
    else:
        koszt_500 = 694201312

    return min([(koszt_gora,gora),(koszt_dol,dol),(koszt_500,palety500)], key=lambda x:x[0])


