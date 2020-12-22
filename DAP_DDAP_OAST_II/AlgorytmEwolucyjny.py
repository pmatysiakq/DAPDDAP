import copy, random
from time import time

from Modele import TopologiaSieci
from Chromosom import Chromosom, pobierz_chromosomy_z_jednym_genem

# Klasa, która reprezentuje pojedyncze uruchomienie algorytmu AE
class AlgorytmEwolucyjny:
    
    def __init__(self, problem, ziarno, siec: TopologiaSieci, ilosc_chromosomow, max_czas,
                 max_liczba_generacji, max_liczba_mutacji, max_liczba_niepoprawionych_generacji, krzyzowanie_prawdopodobienstwo: float,
                 mutacja_prawdopodobienstwo: float, kryterium_stopu):

        self.problem = problem
        random.seed(ziarno)
        self.siec = siec
        self.ilosc_chromosomow = ilosc_chromosomow
        self.generacja = 0
        self.brak_poprawy = 0
        self.liczba_mutacji = 0
        self.max_czas = max_czas
        self.max_liczba_generacji = max_liczba_generacji
        self.max_liczba_mutacji = max_liczba_mutacji
        self.max_liczba_niepoprawionych_generacji = max_liczba_niepoprawionych_generacji
        self.krzyzowanie_prawdopodobienstwo = krzyzowanie_prawdopodobienstwo
        self.mutacja_prawdopodobienstwo = mutacja_prawdopodobienstwo
        self.kryterium_stopu = kryterium_stopu
        self.czas_poczatkowy = 0
        self.wszystkie_generacje = []
        self.ilosc_najlepszych_chromosomow = round(ilosc_chromosomow * 0.6)
        self.wypelnienie_populacji = ilosc_chromosomow - self.ilosc_najlepszych_chromosomow


    def generuj_pierwsza_populacje(self):      # pierwsza populacja jako tablica chromosomów

        kombinacje_genow = list()
        for zapotrzebowanie in self.siec.zapotrzebowania:
            kombinacje_genow.append(pobierz_chromosomy_z_jednym_genem(zapotrzebowanie))

        pierwsza_populacja = []

        for element_chrom in range(self.ilosc_chromosomow):
            chromosom = Chromosom({})       # Tworzymy chromosom jako słownik; chromosom będzie miał wartości
            for kombinacja_genow in kombinacje_genow:
                gen = random.choice(kombinacja_genow).alokacja_zasobow_zapotrzebowania
                chromosom.dodaj_gen(gen)        # funkcja z Chromosom.py

            chromosom.oblicz_lacza(self.siec, problem=self.problem)     # Oblicz łącza dla danego problemu
            pierwsza_populacja.append(chromosom)

        random.shuffle(pierwsza_populacja)

        return pierwsza_populacja

    def wybierz_najlepsze_dopasowanie(self, populacja):

        populacja.sort(key=lambda element_populacja: element_populacja.wartosc_funkcji_kosztu)  # TODO !!!

        najlepsze_chromosomy = populacja[:self.ilosc_najlepszych_chromosomow]

        uzupelnienie_najlepszymi = list()
        for element_populacji in range(self.wypelnienie_populacji):
            uzupelnienie_najlepszymi.append(copy.deepcopy(najlepsze_chromosomy[element_populacji]))
        # Dopełniamy najlepszymi chromosomami, żeby populacja nie zmalała

        najlepsze_dopasowanie = najlepsze_chromosomy + uzupelnienie_najlepszymi

        return najlepsze_dopasowanie

    @staticmethod
    def prawda_falsz():
        return bool(random.getrandbits(1))

    def krzyzuj_chromosomy(self, rodzice):
        rodzic_pierwszy = rodzice[0]
        rodzic_drugi = rodzice[1]
        potomek_pierwszy = Chromosom({})
        potomek_drugi = Chromosom({})
        ilosc_genow = rodzic_pierwszy.ilosc_genow

        for numer_genu in range(ilosc_genow):  # Decydujemy, który gen zostaje pobrany od którego rodzica
            if self.prawda_falsz():
                potomek_pierwszy.dodaj_gen(rodzic_pierwszy.pobierz_gen(numer_genu+1))
                potomek_drugi.dodaj_gen(rodzic_drugi.pobierz_gen(numer_genu+1))
                # ^ Przypisz 1-mu potomkowi gen pierwszego rodzica, 2-mu drugiego
            else:
                potomek_pierwszy.dodaj_gen(rodzic_drugi.pobierz_gen(numer_genu+1))
                potomek_drugi.dodaj_gen(rodzic_pierwszy.pobierz_gen(numer_genu+1))
                # ^ Przypisz 1-mu potomkowi gen drugiego rodzica, 2-mu pierwszego

        potomkowie = [potomek_pierwszy, potomek_drugi]

        return potomkowie

    def krzyzowanie_wystapienie(self):      # na podstawie prawdopodobieństwa [0-1]
        return random.random() < self.krzyzowanie_prawdopodobienstwo

    def mutacja_wystapienie(self):          # na podstawie prawdopodobieństwa [0-1]
        return random.random() < self.mutacja_prawdopodobienstwo

    def uruchom_algorytm_ewolucyjny(self) -> Chromosom:
        populacja = self.generuj_pierwsza_populacje()  # Wygeneruj pierwszą populację jako tablicę chromosomów
        rozwiazanie_algorytmu = Chromosom({})           # Inicjujemy rozwiązanie algorytmu obiektem Chromosom
        self.czas_poczatkowy = time()

        while not self.zakoncz_obliczenia():
            self.generacja += 1                         # Tworzymy kolejną generację dopóki niespełniony warunek stopu
            naj_chromosom_w_generacji = Chromosom({})

            for chromosom in populacja:                 # Oblicz funkcję kosztu dla utworzonej generacji
                chromosom.oblicz_lacza(self.siec, self.problem)
                if chromosom.oblicz_funkcje_kosztu(self.siec, self.problem) < naj_chromosom_w_generacji.wartosc_funkcji_kosztu:
                    naj_chromosom_w_generacji = copy.deepcopy(chromosom)

            self.wszystkie_generacje.append(naj_chromosom_w_generacji)
            print("Numer generacji: {}.".format(self.generacja)
                  + " Wartość funkcji kosztu: {}".format(naj_chromosom_w_generacji.wartosc_funkcji_kosztu))

            if naj_chromosom_w_generacji.wartosc_funkcji_kosztu < rozwiazanie_algorytmu.wartosc_funkcji_kosztu:
                rozwiazanie_algorytmu = copy.deepcopy(naj_chromosom_w_generacji)
                self.brak_poprawy = 0
            else:
                self.brak_poprawy += 1

            populacja = self.wybierz_najlepsze_dopasowanie(populacja)

            # -> Wykonaj krzyżowanie
            populacja_po_krzyzowaniu = []

            while len(populacja) > 1:
                rodzice = random.sample(populacja, 2)
                populacja.remove(rodzice[0])        # Usuwamy rodziców z listy, aby wybrać innych
                populacja.remove(rodzice[1])

                populacja_po_krzyzowaniu += (self.krzyzuj_chromosomy(rodzice)
                                             if self.krzyzowanie_wystapienie() else rodzice)
                # ^ jeśli krzyzowanie występuje, to do tablicy 'populacja_po_krzyzowaniu' dodajemy potomków,
                #   jeśli nie to do tablicy dodajemy samych rodziców

            populacja += populacja_po_krzyzowaniu   # aktualizacja populacji

            # -> Wykonaj mutację
            for chromosom in populacja:
                if self.mutacja_wystapienie():             # Jeśli mutacja chromosomów wystepuje (wartość True/False)
                    for gen in range(chromosom.ilosc_genow):
                        if self.mutacja_wystapienie():     # Jeśli mutacja genów występuje
                            chromosom.mutuj_gen(gen+1)
                            self.liczba_mutacji += 1

        print("\nCzas optymalizacji: {} [s]\n".format(round(time() - self.czas_poczatkowy, 3)))
        # ^ Zaokrąglamy czas optymalizacji do 3 miejsc po przecinku

        for rozwiazanie in self.wszystkie_generacje:
            rozwiazanie.oblicz_lacza_w_problemach(self.siec)  # Oblicz wartości łączy - dla trajektorii procesu

        rozwiazanie_algorytmu.oblicz_lacza_w_problemach(self.siec)

        return rozwiazanie_algorytmu

    # Sprawdzenie kryterium stopu
    def zakoncz_obliczenia(self):
        if self.kryterium_stopu == 1 and (time() - self.czas_poczatkowy >= self.max_czas):
            print("Obliczenia zakończone ze względu na przekroczenie maksymalnego czasu.")
            return True
        if self.kryterium_stopu == 2 and (self.generacja >= self.max_liczba_generacji):
            print("Obliczenia zakończone ze względu na osiągnięcie maksymalnej liczby generacji.")
            return True
        if self.kryterium_stopu == 3 and (self.liczba_mutacji >= self.max_liczba_mutacji):
            print("Obliczenia zakończone ze względu na osiągnięcie maksymalnej liczby mutacji.")
            return True
        if self.kryterium_stopu == 4 and (self.brak_poprawy >= self.max_liczba_niepoprawionych_generacji):
            print("Obliczenia zakończone ze względu na brak poprawy rozwiązania w kolejnych generacjach.")
            return True
        else:
            return False
