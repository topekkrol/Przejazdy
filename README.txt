Dzień dobry, program rozwiązuje problem decyzyjności pomiędzy dwoma możliwymi modelami dostawy, transport własny (całopojazdowy) i spedycja (przesyłki drobnicowe).

        czwarty etap 

Docelowo tutaj będą funkcje które wspomagają formatowanie informacji do kodu html. 

        dane_o_harmonogramie 
Funkcja zwraca informacje o biezacym harmonogramie

     flota.py 

Część programu odpowiadająca za odczytywanie informacji o bieżącej flocie. Wykorzystywana jest biblioteka pickle, która umożliwia odczytywanie z formatu pliku .pkl. Wszystkie funkcje są typem “@classmethod” w związku z tym że nie działają w obrębie danej wartości z pliku .flota.pkl’ tylko na wszystkich wartościach z pliku.

Klasa Samochod:
W klasie samochod zapisane są wszystkie podstawowe informację, o tym jak wygląda struktura informacji w pliku ‘flota.pkl’

        wyswietl_wszystkie
Funkcja odczytuje z pliku obiekt pythona i następnie na zasadzię pętli odczytuje każdy z elementów znajdujących się w obiekcie. Po pod odczytaniu w pętli zwraca wartość w formie dictionary

        zapisz_do_pliku
Funkcja zapisuję biężące dane z dictionary w pliku “flota.pkl”

        odczytaj_z_pliku_wszystkie
Funkcja próbująca otworzyć plik “flota.pkl” znajdujący się w tym samym katologu, w przypadku błędu użytkownik otrzymuje wartość “Nie znaleziono pliku z zapisanymi danymi.”.

        wyswietl_wage_i_palety
Funkcja zwraca sumaryczne wartości odpowiadające możliwościom ładowności dla palet i wagi, dla floty zgromadzonej.

        max_palety
Po posortowaniu od największej wartości w ładowności palet, funkcja zwraca numer rejestracyjny samochodu, wraz z ilością palet jaką może zabrać. Funkcja przyjmuje argument kolejnosc_ladownosci - w którym można zdefiniować które w kolejności auto ma wskazać.

        dane_auta
Funkcja na podstawie argumentu nr_rej - zwraca informację o ładowności palet dla wskazanego pojazdu

        ilosc_pojazdow
Funkcja zwraca informacje o ilości pojazdów dostępnych do realizacji transportów.


    kalkulator_raben

Funkcję znajdujące się w pliku obliczają koszt dostawy dla podanych parametrów: km, waga i ilość palet. Jeżeli użytkownik nie zadeklaruje ilości palet funkcję starają się znaleźć najtańszy możliwy sposób podziału towaru. Ponadto jeżeli użytkownik poda ilość palet niezgodną z możliwymi warunkami realizacji, funkcję podzielą towar zgodnie z możliwymi warunkami realizacji. Zwracane dane są w formie listy

        przypadek_beznadziej
Funkcja dzieli wagę przez ilość palet i na tej podstawie oblicza jaki będzie koszt dostawy

        kalkulator_od_góry
Funkcja stara się podzielić wagę na palety, licząc od wypełnienia najlżejszych możliwych palet w pełni. Funkcja działa w sposób rekurencyjny zwracając listę palet wraz z wagą.

        obliczanie_kosztow
Funkcja oblicza jednostkowy koszt palety z kategoryzacją kilometrów i uwzględnieniem dodatków.

        kalkulator_od_góry
Funkcja stara się podzielić wagę na palety, licząc od wypełnienia najcięższych możliwych palet w pełni. Funkcja działa w sposób rekurencyjny zwracając listę palet wraz z wagą.


        kalulator_500
Funkcja oblicza na ilu palet zmieści się towar i następnie oblicza jaki będzie koszt dostarczenia w takim warunku.

        redukcja
Podczas zaokrąglania wag może dojść do sytuacji kiedy zostanie odjęta zbyt duża wartość w wadze co dalej może prowadzić do błędów w obliczeniach. Funkcja rozwiązuje ten problem odpowiednio redukuję wagę i ilość nośników.

        kalkulator_spedycja
Funkcja oblicza koszt dostawy na trzy możliwe sposoby (kalulator_500, kalkulator_od_góry, kalkulator_od_góry.) Wartosc ‘694201312’ funkcjonuje jako abstrakcyjna wartość mająca zabezpieczyć wartość przed wybraniem wariantu.

    lat_lon
Funkcje w pliku uzyskują współrzędne lat i lon dla wskanego miasta. plik obecnie nie używany pozostawiony dla prezentacji umiejętności obsługi API.

        znalezenie_lokalizacji
Funkcja znajduje współrzędne lat i lon dla miasta wprowadzonego jako argument.

        dodanie_miejscowosci>/h3>
Funkcja zapisuje uzyskany wynik w pliku “latilon.csv” przechowującego informację o współrzędnych dla miejscowości które już były wcześniej wyszukiwane.
    nowa_konsola.py
Plik obsługuje nawigację linkami za pomocą flask, jak i całą obsługę strony internetowej.

        index -  route”/”
Startowa strona pokazująca się po załadowaniu, korzysta z template “konsola.html”

        harmonogram_dostaw - route “/harmonogram_dostaw”
Strona prezentująca aktualny harmonogram dostaw z podziałem na miasta dostawy. Korzysta z template “harmonogram_dostaw.html”

        lista_pojazdow - route “/lista_pojazdow”
Strona prezentuje aktualny stan pojazdów, przeznaczonych do realizacji dostawy. Korzysta z template “lista_samochodow.html”

        dokumentacja - route “/dokumentacja”
Strona prezentuje bieżacy plik xD

        graf - route “/graf”
Strona przekierowuje na figmę, gdzie znajduje się graf głównego procesu podziału towaru pomiędzy możliwe sposoby dostawy,

    odleglosc_api

Plik znajduje dystans dla lokalizacji z Rzeszowa.Plik obecnie nie używany

        get_distance
Funkcja znajduje dystans na podstawie danych lat i lon obydwu punktów. Domyślnie jest ustawiony Rzeszów jako jedne z miejsc.

        get_location
Funkcja znajduje miasto w Polsce, na podstawie nazwy. Wyszukuje lat i lon danego miasta.

    pierwszy_etap
Plik pomocniczy do działania “nowy_main_w_html.py”

        rozwiazywania_rownania_a
Podczas obliczeń w funkcji “koszty_odleglosci” pojawiają się obliczenia w trakcie których nie można ustalić odrazu wartości. Nadawana jest wtedy zmienna, która pod koniec obliczeń jest znana. Jeżeli zajdzie taka sytuacja, funkcja znajduje takie przypadki i w równaniu z zmienną podmienia ją na wartość i zwraca wartość do dictionary.

        sprawdzanie_czy_z_tylu_sie_wszystko_zgadza
Podczas rozwiązywania równania “koszty odległości” może zajść sytuacja kiedy w dalszym ciągu dodawanych miejscowości, pojawią się miejscowości występujące bliżej. W takiej sytuacji dodawana jest lista składająca się z  zmienna i odległość pomiędzy dalszym punktem. Dodana lista jest następnie rozwiązana przez funkcję “rozwiazywania_rownania_a”

        koszty_odleglosci
Funkcja stara się znaleźć realny koszt kilometrów pomiędzy miejscowościami do obslużenia. Wynikiem funkcji jest przypisanie kosztów które następnie się porównywalne do wybrania modelu dostawy.

        koszty_spedycji
Funkcja przypisuje koszty dostawy spedycją dla dane przypadku, korzystając z kalkulatora spedycji.

        wlasny_transport_vs_spedycja
Funkcja na podstawie dostarczonych danych o koszcie dostawy spedycją i transportem własnym, wybiera tańszy sposób dostawy.

        przypisywanie_wartosci_bezposredniego_polaczenia
Funkcja przypisuje kilometry niezbędne do pokonania przy założeniu że transport jest realizowany tylko do tej miejscowości.

    drugi_etap

        sprawdzanie_czy_z_spedycji_cos_sie_zmiesci_w_transporcie_wlasnym
Funkcja sprawdza czy cokolwiek z nośnika informacji spedycyjnej można przenieść do nośnika informacji transportu własnego.

         compare_dictionaries
Funkcja porównuje dwie dictionary, wykorzystana jest do tego aby porównać czy zaszła jakaś zmiana.

        zaokraglanie_i_laczenie_i_sortowanie
Funkcja przygotowuje dane do formatu przyjmowanego przez kod HTML do zaprezentowania na stronie internetowej.

        zaokraglenie_df
Funkcja na podstawie nazwy kolumny zaokrągla wartości we wskazanej kolumnie do liczb całkowitych.

        filtr_najwiekszych_miejscowosci
Funkcja tworzy listę, posortowaną zgodnie z sumaryczną ilością towaru do miejscowości, od największej.

        usuwanie_podkreslenia
Zgodnie z konwencją nazywania zmiennych w pyhtonie, w programie nie występują w nazwach spacje. Kod HTML nie działa na tej samej konwencji i funkcja zamienia określenia na spację, aby tekst był czytelny na stronie internetowej.

        sprawdzenie_czy_nie_taniej_bedzie_przeniesc_pomiedzy_przejazdami
Funkcja sprawdza, czy w obrębie modelu dostawy transport własny, nie można przenieść towaru do innego przejazdu aby było taniej.

        model_deflacyjny_dla_stworzonych_tras
Funkcja kontrolna, czy aby model dostawy wybrany do realizacji dostawy, jest najtańszym możliwym.

    wyszukiwarka_makaronowa
Zadaniem pliku jest znalezienie najkrótszej trasy pomiędzy dwoma punktami.

        sortowanie
Funkcja sortuje uzyskane możliwe drogi dojazdu, wskazująć najkrótszą na zerowym miejscu.

        wyszukanie
Funkcja sprawdza czy dla danej trasy istnieje bezpośrednie połączenie opisane w pliku “Zeszyt1.csv”. Jeżeli nie istnieje, zaczyna sprawdzać miejscowości z jakimi istnieje połączenie z miejscowości startowej, a następnie dla uzyskanej listy miejscowości sprawdza czy w tej liście istnieje miejscowość która łączy się z punktem docelowym. Akcja utworzenia listy miejscowości z jakimi łączy się dany punkt powtarzana jest maksymalnie cztery razy w celu wyszukania żądanej trasy.
