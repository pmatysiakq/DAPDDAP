# Klasa, która reprezentuje pojedynczy chromosom

import math
import random
from typing import List
from pprint import pformat
from itertools import product

from Modele import Gen, TopologiaSieci, Zapotrzebowanie

class Chromosom(object):
    def __init__(self, alokacja_zasobow_zapotrzebowania):
        self.rozmiary_laczy = []
        self.obciazenia_laczy = []
        self.alokacja_zasobow_zapotrzebowania = alokacja_zasobow_zapotrzebowania
        self.ilosc_genow = 0
        self.wartosc_funkcji_kosztu = float('inf')      # inicjalizacja dużą wartością początkową na start

    def pobierz_gen(self, nr_zapotrzebowania):
        geny_slownik = {}
        for numer, gen in self.alokacja_zasobow_zapotrzebowania.items():
            if numer[0] == nr_zapotrzebowania:
                geny_slownik.update({numer: gen})
        return geny_slownik

    def dodaj_wartosci_przeplywow(self, pozycje_alokacji):
        wartosci_alokacji = self.alokacja_zasobow_zapotrzebowania.copy()  # kopia listy alokacji bez zmiany oryginalnej
        wartosci_alokacji.update(pozycje_alokacji)
        self.alokacja_zasobow_zapotrzebowania = wartosci_alokacji

    def dodaj_gen(self, gen):
        self.dodaj_wartosci_przeplywow(gen)
        self.ilosc_genow += 1

    def oblicz_lacza(self, siec, problem):
        lacza = siec.lacza
        lacza_wartosci = [0]*len(siec.lacza)  # Początkowo uzupełnij tablicę wartości łączy zerami; inicjalizacja
        sciezki = siec.wyluskaj_sciezki_w_zapotrzebowaniach()   # Pobieramy ścieżki

        problem = problem.lower()

        for nr_lacza, lacze in enumerate(lacza):    # Od razu numerujemy łącza za pomocą enumerate()
            suma_wielkosci_zap = 0                  # Suma wielkości zapotrzebowania (demand volume)
            kolejny_nr_lacza = (nr_lacza+1)

            for sciezka in sciezki:
                if kolejny_nr_lacza in sciezka.lacza_w_sciezce:
                    wielkosc_zapotrzebowania = (sciezka.nr_zapotrzebowania, sciezka.nr_sciezki)
                    wartosc_wielkosci_zap = self.alokacja_zasobow_zapotrzebowania.get(wielkosc_zapotrzebowania)
                    suma_wielkosci_zap += wartosc_wielkosci_zap

            if problem.lower() == "ddap":
                lacza_wartosci[nr_lacza] = math.ceil(suma_wielkosci_zap/lacze.modul_lacza)
            else:
                lacza_wartosci[nr_lacza] = suma_wielkosci_zap

        if problem.lower() == "ddap":
            self.rozmiary_laczy = lacza_wartosci
        elif problem.lower() == "dap":
            self.obciazenia_laczy = lacza_wartosci
        else:
            print("Nieprawidłowy rodzaj problemu.")

    def oblicz_funkcje_kosztu(self, siec: TopologiaSieci, problem):
        if problem.lower() == "ddap":
            wartosc_funkcji_kosztu_DDAP = 0  # inicjalizacja wartością początkową 0

            for nr_lacza, lacze_rozmiar in enumerate(self.rozmiary_laczy):  # Od razu numerujemy rozmiary
                wartosc_funkcji_kosztu_DDAP += siec.lacza[nr_lacza].koszt_jednostkowy*lacze_rozmiar

            self.wartosc_funkcji_kosztu = wartosc_funkcji_kosztu_DDAP

            return wartosc_funkcji_kosztu_DDAP

        elif problem.lower() == "dap":
            wartosc_funkcji_kosztu_DAP = float('-inf')  # inicjalizacja małą wartością początkową

            for nr_obciazenia, lacze_obciazenie in enumerate(self.obciazenia_laczy):  # Od razu numerujemy obciążenia
                wartosc_funkcji_kosztu = lacze_obciazenie - \
                                         (siec.lacza[nr_obciazenia].max_liczba_modulow*siec.lacza[nr_obciazenia].modul_lacza)
                if wartosc_funkcji_kosztu > wartosc_funkcji_kosztu_DAP:
                    wartosc_funkcji_kosztu_DAP = wartosc_funkcji_kosztu

            self.wartosc_funkcji_kosztu = wartosc_funkcji_kosztu_DAP

            return wartosc_funkcji_kosztu_DAP
        else:
            print("Nie udało się obliczyć funkcji kosztu.")

    def mutuj_gen(self, nr_genu):

        gen = self.pobierz_gen(nr_genu)

        if len(gen) > 1:
            wartosci_genu_do_mutacji = random.sample(list(gen), 2)
            # ^ Zwraca 2 wartości losowo wybrane do mutacji z listy wartości w danym genie

            # Jeśli pierwsza z wylosowanych wartości genu wybranego do mutacji jest > 0, to...
            if self.alokacja_zasobow_zapotrzebowania[wartosci_genu_do_mutacji[0]] > 0:
                self.alokacja_zasobow_zapotrzebowania[wartosci_genu_do_mutacji[0]] -= 1
                self.alokacja_zasobow_zapotrzebowania[wartosci_genu_do_mutacji[1]] += 1
                # ^ ...dla tego genu przenosimy jedną jednostkę zapotrzebowania z jednego miejsca na inne

    def __repr__(self):
        global obciazenia_laczy, rozmiary_laczy

        przeplywy = ("Przepływy dla konfiguracji (numer zapotrzebowania, numer ścieżki):\n"
                     + pformat(self.alokacja_zasobow_zapotrzebowania, width=20))

        if self.obciazenia_laczy:
            obciazenia_laczy = ("\nObciążenia łączy: {}".format(self.obciazenia_laczy))
        if self.rozmiary_laczy:
            rozmiary_laczy = ("\nRozmiary łączy: {}".format(self.rozmiary_laczy))

        wartosc_funkcji_kosztu = ("\nWartość funkcji kosztu dla rozwiązania: {}".format(self.wartosc_funkcji_kosztu))

        zapis_rozwiazania = przeplywy + obciazenia_laczy + rozmiary_laczy + wartosc_funkcji_kosztu

        return zapis_rozwiazania

    def oblicz_lacza_w_problemach(self, siec: TopologiaSieci):  # Dla zapisu trajektorii procesu
        self.oblicz_lacza(siec, "ddap")
        self.oblicz_lacza(siec, "dap")


# Funkcja pomocnicza - do generacji pierwszej populacji
def pobierz_chromosomy_z_jednym_genem(zapotrzebowanie: Zapotrzebowanie) -> List[Chromosom]:

    pojedyncza_wielkosc_zapotrzebowania = range(zapotrzebowanie.wielkosc_zapotrzebowania + 1)
    # ^ Rozkładamy wielkości zapotrzebowania pojedynczo; '+1' bo numerujemy od 0

    kombinacje_przeplywow = list()
    poj_wlk_zapo_dla_kazdej_sciezki = list()
    pojedyncza_wielkosc_zapotrzebowania_kombinacje = list()

    for i in range(zapotrzebowanie.pobierz_ilosc_sciezek()):
        poj_wlk_zapo_dla_kazdej_sciezki.append(pojedyncza_wielkosc_zapotrzebowania)

    for kombinacja in product(*poj_wlk_zapo_dla_kazdej_sciezki):
        if sum(kombinacja) == zapotrzebowanie.wielkosc_zapotrzebowania:
            pojedyncza_wielkosc_zapotrzebowania_kombinacje.append(kombinacja)

    for kombinacja in pojedyncza_wielkosc_zapotrzebowania_kombinacje:
        kombinacje_przeplywow.append(Chromosom(Gen.utworz_gen(kombinacja, zapotrzebowanie)))

    return kombinacje_przeplywow
