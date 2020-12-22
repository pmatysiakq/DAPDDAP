from Modele import Lacze
from Modele import TopologiaSieci
from Modele import Zapotrzebowanie
from Modele import SciezkaWZapotrzebowaniu


SEPARATOR = ' '  # Ustawienie separatora do odczytywania pliku


class Parsowanie:

    def parsuj_plik(self, nazwa_pliku):

        siec = TopologiaSieci()

        with open(nazwa_pliku) as plik_sieci:

            # -> Wyłuskaj łącza:
            lacza_ilosc = int(plik_sieci.readline())            # czyta pierwszą linię pliku = ilość łączy
            
            for linia in range(lacza_ilosc):                    # tyle razy (linijek), ile jest łączy
                dane_o_laczu = self.utworz_liste_z_linii(plik_sieci.readline())
                # ^ przeczytaj kolejną linię i zapisuj do listy wartości zgodnie z separatorem ' '
                #  w ten sposób uzyskujemy dane o poszczególnym łączu
                
                lacze = Lacze(dane_o_laczu=dane_o_laczu)
                # ^ po kolei przypisz te dane do odpowiednich pól zdefiniowanych w klasie Lacze

                siec.lacza.append(lacze)                        # dodaj to łącze do listy

            for x in range(2):
                plik_sieci.readline()                           # przeczytaj kolejne 2 linie pliku

            # -> Wyłuskaj zapotrzebowania:
            ilosc_zapotrzebowan = int(plik_sieci.readline())    # czyta kolejną linię pliku = ilość zapotrzebowań
            plik_sieci.readline()

            for nr_zapotrzebowania in range(ilosc_zapotrzebowan):
                dane_o_zapotrzebowaniu = self.utworz_liste_z_linii(plik_sieci.readline())
                # ^ uzyskujemy dane o zapotrzebowaniu

                zapotrzebowanie = Zapotrzebowanie(dane_o_zapotrzebowaniu=dane_o_zapotrzebowaniu,
                                                  nr_zapotrzebowania=nr_zapotrzebowania+1)
                # ^ po kolei przypisz te dane do odpowiednich pól zdefiniowanych w klasie Zapotrzebowanie,
                #  zwiększ nr zapotrzebowania o 1

                ilosc_sciezek_w_zapotrzebowaniu = int(plik_sieci.readline())  # kolejna linia = ilość ścieżek w zapotrzebowaniu

                for nr_sciezki_w_zapotrzebowaniu in range(ilosc_sciezek_w_zapotrzebowaniu):
                    dane_o_sciezce = self.utworz_liste_z_linii(plik_sieci.readline())
                    # ^ uzyskujemy dane o ścieżce

                    sciezka_w_zapotrzebowaniu = SciezkaWZapotrzebowaniu(dane_o_sciezce=dane_o_sciezce,
                                                                        nr_zapotrzebowania=nr_zapotrzebowania + 1)
                    # ^ po kolei przypisz te dane do odpowiednich pól zdefiniowanych w klasie SciezkaWZapotrzebowaniu,
                    #  zwiększ nr zapotrzebowania o 1

                    zapotrzebowanie.lista_sciezek_w_zapotrzebowaniach.append(sciezka_w_zapotrzebowaniu)

                siec.zapotrzebowania.append(zapotrzebowanie)    # dodaj to zapotrzebowanie do listy

                plik_sieci.readline()                           # przeczytaj kolejną linię (pusta)

        return siec

    @staticmethod
    def utworz_liste_z_linii(linia):
        return linia.strip().split(SEPARATOR)  # strip() - by usunąć początkowe i końcowe białe znaki, ' ' - separator
