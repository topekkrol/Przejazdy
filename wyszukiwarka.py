from WyszukiwarkaRekurencyjna import Trasa
from WyszukiwarkaMakaronowa import wyszukanie
from WyszukiwarkaSpecjalistyczna import find_route
import datetime

t1 = datetime.datetime.now()
trasa = Trasa()
wynik = trasa.znajdz_trase('Rzeszow', 'Bilgoraj',max_depth=2)
print(wynik[0]) # wyświetli 110
t2 = datetime.datetime.now()

w1 = t2-t1

t3 = datetime.datetime.now()
print(wyszukanie('Rzeszow','Bilgoraj',2))
t4 = datetime.datetime.now()

w2 = t4-t3

# if w1 > w2:
#     wynik ='Metoda makaronowa'
#     wynik2 = w1/w2
# else:
#     wynik ='Rekurencja'
#     wynik2 = w2/w1
#
# print(f'Szybsza jest metowa{wynik}, ok {wynik2} szybciej działa')

t5 = datetime.datetime.now()
start = 'Rzeszow'
end = 'Bilgoraj'

cost, path = find_route(start, end)
print(cost,path)
t6 = datetime.datetime.now()
w3 = t6-t5

print(w1,'x',w2,'x',w3)