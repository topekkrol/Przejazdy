import csv

def sortowanie(sortowanie_lista):
    lista8=[]
    try:
        y = 999
        for trasy in sortowanie_lista:
            if y > trasy['km']:
                y = trasy['km']

        for trasy in sortowanie_lista:
            if trasy['km'] == y:
                lista8.append(trasy)

        return (lista8)
    except:
        return None

def wyszukanie(zaczynamy,konczymy,glebokosc=4,obowiazkowy_przystanek=''):
    lista = []  #Lista gotowych tras#
    lista1 = {}  #Lista miast pośrednich między etapem 1-2#
    lista2 = {}  #Formularz dodawania trasy#
    lista3 = {}  #Lista miast pośrednih między etapem 2-3#
    lista4 = []  #Lista tras wygenerowanych z lista3#
    lista5 = {}  #Lista miast pośrednih między etapem 3-4#
    lista6 = []  #Lista tras wygenerowanych z lista1#
    lista7 = []  #Lista tras wygenerowanych z lista 5#
    # lista8 = [] #Lista gotowych tras
    x = 0

    with open('Zeszyt1.csv') as csv_file:
        if glebokosc >= 1:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                if row['Rozpoczecie'] == zaczynamy:
                    if row['Zakonczenie'] == konczymy:
                        x += int(row['km'])
                        lista2 = {
                            'Start': zaczynamy,
                            'Przystanek':'',
                            'Koniec': konczymy,
                            'km': x
                        }
                        lista.append(lista2)

                    else:
                        lista1={
                            'Start': zaczynamy,
                            'Przystanek': row['Zakonczenie'],
                            'km': row['km']
                        }
                        lista6.append(lista1)

                elif row['Zakonczenie'] == zaczynamy:
                    if row['Rozpoczecie'] == konczymy:
                        x += int(row['km'])
                        lista2 = {
                            'Start': zaczynamy,
                            'Przystanek': '',
                            'Koniec': konczymy,
                            'km': x
                        }
                        lista.append(lista2)

                    else:
                        lista1 = {
                            'Start': zaczynamy,
                            'Przystanek': row['Rozpoczecie'],
                            'km': row['km']
                        }
                        lista6.append(lista1)


    # ## Koniec pierwszego etapu ##
    if glebokosc >= 2:
        with open('Zeszyt1.csv') as csv_file:
            csv_reader_1 = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader_1:
               for miasta in lista6:
                   x = 0
                   if row['Rozpoczecie'] == miasta['Przystanek']:
                       if row['Zakonczenie'] == konczymy:

                           x += int(row['km'])
                           x += int(miasta['km'])
                           lista2 = {
                               'Start' : zaczynamy,
                               'Przystanek' : miasta['Przystanek'],
                               'Koniec' : konczymy,
                               'km' : x
                           }
                           lista.append(lista2)

                       else:
                           x += int(row['km'])
                           x += int(miasta['km'])
                           lista3={
                               'Start' : zaczynamy,
                               'Przystanek_1' : miasta['Przystanek'],
                               'Przystanek_2' : row['Zakonczenie'],
                               'km' : x
                           }
                           lista4.append(lista3)

                   elif row['Zakonczenie'] == miasta['Przystanek']:
                       if row['Rozpoczecie'] == konczymy:
                           x += int(row['km'])
                           x += int(miasta['km'])
                           lista2 = {
                               'Start': zaczynamy,
                               'Przystanek': miasta['Przystanek'],
                               'Koniec': konczymy,
                               'km': x
                           }
                           lista.append(lista2)
                       else:
                           x += int(row['km'])
                           x += int(miasta['km'])
                           lista3 = {
                               'Start': zaczynamy,
                               'Przystanek_1': miasta['Przystanek'],
                               'Przystanek_2': row['Rozpoczecie'],
                               'km': x
                           }
                           lista4.append(lista3)

    ## Koniec drugiego etapu ##
    if glebokosc >= 3:
        with open('Zeszyt1.csv') as csv_file:
            csv_reader_1 = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader_1:
               for miasta in lista4:
                   x = 0
                   if row['Rozpoczecie'] == miasta['Przystanek_2']:
                       if row['Zakonczenie'] == konczymy:
                           x += int(miasta['km'])
                           x += int(row['km'])
                           lista2 = {
                               'Start': zaczynamy,
                               'Przystanek_1': miasta['Przystanek_1'],
                               'Przystanek_2': miasta['Przystanek_2'],
                               'Koniec': konczymy,
                               'km': x
                           }
                           lista.append(lista2)
                       else:
                           x += int(row['km'])
                           x += int(miasta['km'])
                           lista5 = {
                               'Start': zaczynamy,
                               'Przystanek_1': miasta['Przystanek_1'],
                               'Przystanek_2': miasta['Przystanek_2'],
                               'Przystanek_3' : row['Zakonczenie'],
                               'km': x
                           }
                           lista7.append(lista5)
                   elif row['Zakonczenie'] == miasta['Przystanek_2'] :
                       if row['Rozpoczecie'] == konczymy:
                           x += int(miasta['km'])
                           x += int(row['km'])
                           lista2 = {
                               'Start': zaczynamy,
                               'Przystanek_1': miasta['Przystanek_1'],
                               'Przystanek_2': miasta['Przystanek_2'],
                               'Koniec': konczymy,
                               'km': x
                           }
                           lista.append(lista2)
                       else:
                           x += int(row['km'])
                           x += int(miasta['km'])
                           lista5 = {
                               'Start': zaczynamy,
                               'Przystanek_1': miasta['Przystanek_1'],
                               'Przystanek_2': miasta['Przystanek_2'],
                               'Przystanek_3' : row['Rozpoczecie'],
                               'km': x
                           }
                           lista7.append(lista5)

    ## Koniec trzeciego etapu ##
    if glebokosc >= 4:
        with open('Zeszyt1.csv') as csv_file:
            csv_reader_1 = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader_1:
               for miasta in lista7:
                   x = 0
                   if row['Rozpoczecie'] == miasta['Przystanek_3']:
                       if row['Zakonczenie'] == konczymy:
                           x += int(miasta['km'])
                           x += int(row['km'])
                           lista2 = {
                               'Start': zaczynamy,
                               'Przystanek_1': miasta['Przystanek_1'],
                               'Przystanek_2': miasta['Przystanek_2'],
                               'Przystanek_3': miasta['Przystanek_3'],
                               'Koniec': konczymy,
                               'km': x
                           }
                           lista.append(lista2)


                   elif row['Zakonczenie'] == miasta['Przystanek_3']:
                       if row['Rozpoczecie'] == konczymy:
                           x += int(miasta['km'])
                           x += int(row['km'])
                           lista2 = {
                               'Start': zaczynamy,
                               'Przystanek_1': miasta['Przystanek_1'],
                               'Przystanek_2': miasta['Przystanek_2'],
                               'Przystanek_3': miasta['Przystanek_3'],
                               'Koniec': konczymy,
                               'km': x
                           }
                           lista.append(lista2)

    if len(obowiazkowy_przystanek) > 1:
        selected_dicts =[]
        for d in lista:
            if 'Przystanek' in d and d['Przystanek'] == obowiazkowy_przystanek or 'Przystanek_1' in d and d['Przystanek_1'] == obowiazkowy_przystanek or 'Przystanek_2' in d and d['Przystanek_2'] == obowiazkowy_przystanek or 'Przystanek_3' in d and d['Przystanek_3'] == obowiazkowy_przystanek:
                selected_dicts.append(d)

        return sortowanie(selected_dicts)



    return sortowanie(lista)



