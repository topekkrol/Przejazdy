import pandas as pd


class Trasa:
    def __init__(self):
        self.trasy = pd.read_csv('Zeszyt1.csv', delimiter=';')

    def znajdz_trase(self, zaczynamy, konczymy, odwiedzone=None, dystans=0, max_depth=4):
        if odwiedzone is None:
            odwiedzone = set()
        if zaczynamy == konczymy:
            return [{'Start': zaczynamy, 'Koniec': konczymy, 'Miejscowosci': [zaczynamy], 'km': dystans}]
        if max_depth == 0:
            return []
        odwiedzone.add(zaczynamy)
        trasy = []
        for _, row in self.trasy.iterrows():
            if row['Rozpoczecie'] == zaczynamy and row['Zakonczenie'] not in odwiedzone:
                sub_trasy = self.znajdz_trase(row['Zakonczenie'], konczymy, odwiedzone.copy(), dystans=int(row['km']),
                                              max_depth=max_depth - 1)
                for sub_trasa in sub_trasy:
                    trasy.append({'Start': zaczynamy, 'Koniec': sub_trasa['Koniec'],
                                  'Miejscowosci': [zaczynamy] + sub_trasa['Miejscowosci'],
                                  'km': dystans + sub_trasa['km']})
            elif row['Zakonczenie'] == zaczynamy and row['Rozpoczecie'] not in odwiedzone:
                sub_trasy = self.znajdz_trase(row['Rozpoczecie'], konczymy, odwiedzone.copy(), dystans=int(row['km']),
                                              max_depth=max_depth - 1)
                for sub_trasa in sub_trasy:
                    trasy.append({'Start': zaczynamy, 'Koniec': sub_trasa['Koniec'],
                                  'Miejscowosci': [zaczynamy] + sub_trasa['Miejscowosci'],
                                  'km': dystans + sub_trasa['km']})
        return sorted(trasy, key=lambda x: x['km'])
