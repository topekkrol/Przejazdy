import matplotlib.pyplot as plt

# Wczytanie obrazu jako tło
img = plt.imread(r"Trasy-zmiana_przypisywania_do_coru\airlines")

# Dane dla pierwszej linii
x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]

# Dane dla drugiej linii
x2 = [1, 2, 3, 4, 5]
y2 = [1, 2, 1, 2, 1]

# Rysowanie pierwszej linii
plt.plot(x1, y1, label='Linia 1', color='blue', linestyle='-')

# Rysowanie drugiej linii
plt.plot(x2, y2, label='Linia 2', color='red', linestyle='--')

# Dodanie nazw punktów dla pierwszej linii
# for i, txt in enumerate(y1):
#     plt.text(x1[i], y1[i], f'({x1[i]}, {y1[i]})', color='blue')

# Dodanie nazw punktów dla drugiej linii
test_labels = ['test0', 'test1', 'test2', 'test3', 'test4']

plt.scatter(4, 4, color='blue', label='Punkt')

# Dodanie nazwy dla jednego punktu
plt.text(4, 4, 'test',)

for i, txt in enumerate(y2):
    plt.text(x2[i], y2[i], test_labels[i], color='red')

# Dodanie tytułu wykresu
plt.title('Dwie linie w Matplotlib')

# Dodanie etykiet do osi x i y
plt.xlabel('Oś X')
plt.ylabel('Oś Y')

# Dodanie legendy
plt.legend()

# Wyświetlenie obrazu jako tła
plt.imshow(img, extent=[min(x1 + x2), max(x1 + x2), min(y1 + y2), max(y1 + y2)], alpha=0.5, aspect='auto')

# Wyświetlenie wykresu
plt.show()
