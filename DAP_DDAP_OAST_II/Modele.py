# Plik z modelami składającymi się na sieć

from typing import List

# Klasa, która reprezentuje pojedyncze zapotrzebowanie
class Zapotrzebowanie:
    
    def __init__(self, dane_o_zapotrzebowaniu, nr_zapotrzebowania):
        self.wezel_poczatkowy = dane_o_zapotrzebowaniu[0]
        self.wezel_koncowy = dane_o_zapotrzebowaniu[1]
        self.wielkosc_zapotrzebowania = int(dane_o_zapotrzebowaniu[2])
        self.nr_zapotrzebowania = nr_zapotrzebowania
        self.lista_sciezek_w_zapotrzebowaniach = []

    def pobierz_ilosc_sciezek(self):
        return len(self.lista_sciezek_w_zapotrzebowaniach)

# Klasa, która reprezentuje pojedyncze łącze
class Lacze:
    
    def __init__(self, dane_o_laczu):
        self.wezel_poczatkowy = dane_o_laczu[0]
        self.wezel_koncowy = dane_o_laczu[1]
        self.max_liczba_modulow = int(dane_o_laczu[2])
        self.koszt_jednostkowy = int(dane_o_laczu[3])
        self.modul_lacza = int(dane_o_laczu[4])

# Klasa, która reprezentuje pojedynczą ścieżkę w zapotrzebowaniu
class SciezkaWZapotrzebowaniu:
    
    def __init__(self, dane_o_sciezce, nr_zapotrzebowania):
        self.nr_sciezki = int(dane_o_sciezce[0])
        self.nr_zapotrzebowania = nr_zapotrzebowania
        self.lacza_w_sciezce = [int(nr_lacza) for nr_lacza in dane_o_sciezce[1:]]

# Klasa, która reprezentuje topologię sieci
class TopologiaSieci:
    
    def __init__(self):
        self.lacza = []
        self.zapotrzebowania = []

    def wyluskaj_lacze(self, nr_lacza):
        pojedyncze_lacze = self.lacza[nr_lacza-1]
        return pojedyncze_lacze

    def wyluskaj_zapotrzebowanie(self, nr_zapotrzebowania):
        pojedyncze_zapotrzebowanie = self.zapotrzebowania[nr_zapotrzebowania-1]
        return pojedyncze_zapotrzebowanie

    def wyluskaj_sciezki_w_zapotrzebowaniach(self) -> List[SciezkaWZapotrzebowaniu]:

        sciezki_w_zapotrzebowaniach = []
        for zapotrzebowanie in self.zapotrzebowania:
            sciezki = zapotrzebowanie.lista_sciezek_w_zapotrzebowaniach
            sciezki_w_zapotrzebowaniach.append(sciezki)

        lista_sciezek = []
        for sciezka in sciezki_w_zapotrzebowaniach:
            for pojedyncza_sciezka in sciezka:
                lista_sciezek.append(pojedyncza_sciezka)

        return lista_sciezek

# Klasa, która reprezentuje pojedynczy gen
class Gen:
    
    @staticmethod
    def utworz_gen(kombinacja, zapotrzebowanie: Zapotrzebowanie):
        alokacje_przeplywow = {}

        for sciezka_w_zapotrzebowaniu in zapotrzebowanie.lista_sciezek_w_zapotrzebowaniach:
            nr_sciezki = sciezka_w_zapotrzebowaniu.nr_sciezki
            przeplyw = (zapotrzebowanie.nr_zapotrzebowania, nr_sciezki)
            alokacje_przeplywow[przeplyw] = kombinacja[nr_sciezki-1]

        return alokacje_przeplywow
