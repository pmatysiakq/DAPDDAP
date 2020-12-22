from time import time

from Parsowanie import Parsowanie
from ZapisDoPliku import ZapisDoPliku
from AlgorytmEwolucyjny import AlgorytmEwolucyjny


if __name__ == "__main__":

    # Parametry domyślne - używane, jeśli nie zostaną wprowadzone inne
    MAX_CZAS = 500
    MAX_LICZBA_GENERACJI = 100
    MAX_LICZBA_MUTACJI = 1000000
    MAX_LICZBA_NIEPOPRAWIONYCH_GENERACJI = 40
    KRZYZOWANIE_PRAWDOPODOBIENSTWO = 0.6
    MUTACJA_PRAWDOPODOBIENSTWO = 0.01
    ZIARNO_GENERATORA = 7

    rozwiazanie_problemu = None

    # Start programu - wprowadzanie przez użytkownika parametrów algorytmu
    print(" === ALGORYTM EWOLUCYJNY ROZWIĄZUJĄCY PROBLEMY DAP I DDAP ===")

    # Wybór problemu do rozwiązania
    problem = "None"
    while problem.lower() not in ["dap", "ddap"]:
        problem = str(input("\n1. Proszę wpisać nazwę problemu do rozwiązania (DAP lub DDAP): "))
        if problem.lower() in ["dap", "ddap"]:
            print("Rozwiązuję problem: {}".format(problem.upper()))
        else:
            print("Wprowadzono nieprawidłowy problem. Proszę spróbować ponownie.")

    # Wybór pliku z topologią sieci + parsowanie pliku za pomocą klasy Parsowanie()
    parser_sieci = Parsowanie()
    siec = ''

    plik_wejsciowy = -1
    while plik_wejsciowy not in [1, 2, 3]:
        plik_wejsciowy = int(input("2. Proszę wpisać liczbę {1, 2, 3} odpowiadającą plikowi z określoną topologią, gdzie:\n"
                               "   1) Plik net4.txt  2) Plik net12_1.txt  3) Plik net12_2.txt: "))
        if plik_wejsciowy == 1:
            siec = parser_sieci.parsuj_plik('net4.txt')
        elif plik_wejsciowy == 2:
            siec = parser_sieci.parsuj_plik('net12_1.txt')
        elif plik_wejsciowy == 3:
            siec = parser_sieci.parsuj_plik('net12_2.txt')
        else:
            print("Wprowadzono nieprawidłowy numer pliku. Proszę spróbować ponownie.")

    zapis_do_pliku = ZapisDoPliku(siec=siec)  # Przypisanie odpowiednim parametrom wartości ze sparsowanego pliku

    # Wybór kolejnych parametrów algorytmu
    ziarno_generatora_liczb_losowych = int(input("3. Proszę wskazać ziarno generatora liczb losowych do generacji "
                                                 "chromosomów: "))
    licznosc_populacji_startowej = int(input("4. Proszę określić liczność populacji startowej: "))

    krzyzowanie_prawdopodobienstwo = -1
    while 1 <= krzyzowanie_prawdopodobienstwo or krzyzowanie_prawdopodobienstwo <= 0:
        krzyzowanie_prawdopodobienstwo = float(input("5. Proszę podać prawdopodobieństwo wystąpienia krzyżowania: "))
        if 0 <= krzyzowanie_prawdopodobienstwo <= 1:
            print("Prawdopodobieństwo krzyżowania ustawiono na: {}".format(krzyzowanie_prawdopodobienstwo))
        else:
            print("Nieprawidłowa wartość prawdopodobieństwa wystąpienia krzyżowania (poza przedziałem (0, 1)).")

    mutacja_prawdopodobienstwo = -1
    while 1 <= mutacja_prawdopodobienstwo or mutacja_prawdopodobienstwo <= 0:
        mutacja_prawdopodobienstwo = float(input("6. Proszę podać prawdopodobieństwo wystąpienia mutacji: "))
        if 0 <= mutacja_prawdopodobienstwo <= 1:
            print("Prawdopodobieństwo mutacji ustawiono na: {}".format(mutacja_prawdopodobienstwo))
        else:
            print("Nieprawidłowa wartość prawdopodobieństwa wystąpienia mutacji (poza przedziałem (0, 1)).")

    # najlepsze_chromosomy_procent = float(input("7. Proszę podać procent najlepszych chromosomów (0, 1): "))

    # Wybór kryterium stopu
    kryterium_stopu = -1
    while kryterium_stopu not in [1, 2, 3, 4]:
        kryterium_stopu = int(input("8. Proszę wpisać liczbę odpowiadającą wybranemu kryterium stopu, gdzie:\n 1) Zadany "
                                "czas  2) Zadana liczba generacji  3) Zadana liczba mutacji  4) Maksymalna liczba prób "
                                "poprawy najlepszego znanago rozwiązania: "))
        if kryterium_stopu == 1:
            MAX_CZAS = int(input("   Proszę podać maksymalny czas szukania rozwiązania w sekundach: "))
        elif kryterium_stopu == 2:
            MAX_LICZBA_GENERACJI = int(input("  Proszę podać maksymalną liczbę generacji: "))
        elif kryterium_stopu == 3:
            MAX_LICZBA_MUTACJI = int(input("    Proszę podać maksymalną liczbę mutacji: "))
        elif kryterium_stopu == 4:
            MAX_LICZBA_NIEPOPRAWIONYCH_GENERACJI = int(input("    Proszę podać maksymalną liczbę prób poprawy "))
        else:
            print("Wybrano nieprawidłowy numer kryterium stopu. Proszę spróbować ponownie.")

    # Instancja klasy AlgorytmEwolucyjny
    AlgEwol = AlgorytmEwolucyjny(
        problem=problem,
        siec=siec,
        ziarno=ziarno_generatora_liczb_losowych,
        ilosc_chromosomow=licznosc_populacji_startowej,
        max_liczba_niepoprawionych_generacji=MAX_LICZBA_NIEPOPRAWIONYCH_GENERACJI,
        max_liczba_generacji=MAX_LICZBA_GENERACJI,
        max_liczba_mutacji=MAX_LICZBA_MUTACJI,
        max_czas=MAX_CZAS,
        krzyzowanie_prawdopodobienstwo=krzyzowanie_prawdopodobienstwo,
        mutacja_prawdopodobienstwo=mutacja_prawdopodobienstwo,
        kryterium_stopu=kryterium_stopu
    )

    # Uruchomienie algorytmu
    rozwiazanie_problemu = AlgEwol.uruchom_algorytm_ewolucyjny()

    # Wyświetlenie rozwiązań, zapis do plików
    zapis_do_pliku.zapisz_do_pliku(AlgEwol.wszystkie_generacje,  naj_rozwiazanie=rozwiazanie_problemu,
                                                                    nazwa_pliku='Wyniki.txt')
    # ^ zapis trajektorii procesu optymalizacji do pliku
    
    print("Wartość funkcji kosztu najlepszego rozwiązania: {}\n".format(rozwiazanie_problemu.wartosc_funkcji_kosztu))

