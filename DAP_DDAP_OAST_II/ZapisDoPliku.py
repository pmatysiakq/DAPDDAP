from pathlib import Path
from Chromosom import Chromosom

class ZapisDoPliku:

    def __init__(self, siec):
        self.siec = siec


    def zapisz_do_pliku(self, trajektoria, naj_rozwiazanie: Chromosom, nazwa_pliku):   # Metoda statyczna, bo nie zależy od atrybutu 'siec'


        with open(nazwa_pliku, "w+") as plik:

            plik.write("\t\t\t---> NAJLEPSZE ROZWIĄZANIE <---\n")

            # -> Zapis dla zapotrzebowań
            zapotrzebowania_ilosc = len(self.siec.zapotrzebowania)
            plik.write("{}\n\n".format(zapotrzebowania_ilosc))

            for nr_zapotrzebowania in range(zapotrzebowania_ilosc):     # dla każdego zapotrzebowania zapisz:

                gen = naj_rozwiazanie.pobierz_gen(nr_zapotrzebowania+1)
                uzyte_przeplywy = {numer: przeplyw for numer, przeplyw in gen.items() if przeplyw > 0}

                plik.write("{} ".format(nr_zapotrzebowania+1))   # 1) numer zapotrzebowania po kolei
                plik.write("{}\n".format(len(uzyte_przeplywy)))
                # ^ 2) w tej samej linii co nr zapotrzebowania zapisz ilość użytych przepływów + przejdź do kolejnej linii

                for numer in uzyte_przeplywy.keys():                               # dla każdego numeru użytego przepływu
                    plik.write("{} {}\n".format((numer[1]), (uzyte_przeplywy[numer])))
                    # zapisujemy po kolei numery użytych przepływów + ' ' + przepływ dla tego numeru,
                    #  te sekwencje powtarzają się w zależności od tego ile jest przepływów

                plik.write("\n")
            plik.write("\t\t\t---> KOLEJNE GENERACJE W ALGORYTMIE EWOLUCYJNYM <---\n\n")

            for generacja, generacja_rozwiazanie in enumerate(trajektoria):     # Numerujemy trajektorie
                # ^ zwraca generacje danej iteracji + jej rozwiązanie jako wartość

                plik.write("-> Generacja numer {}".format(generacja+1) + "\n\n")
                plik.write("{}".format(generacja_rozwiazanie))
                plik.write("\n\n\n")

            # -> Zapis dla łączy
            lacza_ilosc = len(self.siec.lacza)

            plik.write("{}".format(lacza_ilosc) + "\n\n")  # zapisz całkowitą ilość łączy, przejdź 2 linie dalej

            for nr_lacza in range(lacza_ilosc):                         # dla każdego łącza zapisz:
                plik.write("{} ".format(nr_lacza+1))    # 1) numer łącza po kolei
                plik.write("{} ".format(naj_rozwiazanie.lacze_obciazenia[nr_lacza]))  # 2) obciążenie łącza
                plik.write("{}\n".format(naj_rozwiazanie.lacze_rozmiary[nr_lacza]))   # 3) rozmiar łącza + przejdź do kolejnej linii

            plik.write("\n")                            # dodaj linię przerwy

            print("Zapis wyników w pliku {}:\n  - obliczenia najlepszego rozwiązania: "
                  "zapis_najlepszego_rozwiazania2.txt,\n  - trajektoria procesu optymalizacji: zapis_trajektorii2.txt.".format(nazwa_pliku))
