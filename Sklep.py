from abc import ABC, abstractmethod
import re


class Sklep(ABC):
    @abstractmethod
    def wartosc_magazynu(self):
        pass


class E_leclerc:
    def __init__(self, produkty, kasa):
        if not isinstance(produkty, list):
            raise TypeError('Produkty muszą być listą')
        if not isinstance(kasa, Kasa):
            raise TypeError('Kasa musi być obiektem klasy Kasa')
        for produkt in produkty:
            if not isinstance(produkt, Produkt):
                raise TypeError('Produkty muszą być listą obiektów klasy Produkt')
        self.produkty = produkty
        self._kasa = kasa

    def wartosc_magazynu(self):
        """
        Zwraca sumę wartości wszystkich produktów w magazynie
        """
        return sum([produkt.wartosc() for produkt in self.produkty])

    @staticmethod
    def wypisz_wartosc(wartosc):
        print(f'Wartość magazynu to: {wartosc:.2f}zł')


class Kasa:
    def __init__(self, gotowka, otwarta):
        if not isinstance(gotowka, (int, float)):
            raise TypeError('Gotówka musi być liczbą')
        if not isinstance(otwarta, bool):
            raise TypeError('Otwarta musi być wartością logiczną')
        self._gotowka = gotowka
        self.__otwarta = otwarta

    def transakcja(self, kwota):
        """
        Dodaje kwotę do gotówki w kasie
        """
        if not isinstance(kwota, (int, float)):
            raise TypeError('Kwota musi być liczbą')
        self._gotowka += kwota

    @classmethod
    def utworz(cls):
        """
        Funkcja otwiera kasę na początku dnia
        ze stanem gotówki 2000zł i stanem otwarta
        """
        return cls(2000, True)


class Produkt:
    def __init__(self, cena, ilosc, kod_kreskowy):
        if not isinstance(cena, (int, float)):
            raise TypeError('Cena musi być liczbą')
        if not isinstance(ilosc, int):
            raise TypeError('Ilość musi być liczbą całkowitą')
        if not isinstance(kod_kreskowy, str):
            raise TypeError('Kod kreskowy musi być ciągiem znaków')
        if not re.match(r'^\d{13}$', kod_kreskowy):
            raise ValueError('Kod kreskowy musi składać się z 13 cyfr')
        self.cena = cena
        self.ilosc = ilosc
        self.__kod_kreskowy = kod_kreskowy

    def wartosc(self):
        """
        Funkcja zwraca wartość produktów
        """
        return self.cena * self.ilosc


class Wyprzedany(Produkt):
    def __init__(self, cena, ilosc, kod_kreskowy, data_dostawy):
        super().__init__(cena, ilosc, kod_kreskowy)
        self._data_dostawy = data_dostawy

    def dostawa(self):
        """
        Funkcja informuje, kiedy odbędzie się dostawa danego produktu
        """
        return f"Dostawa oczekiwana jest na dzień: {self._data_dostawy}"


class Dostepny(Produkt):
    def __init__(self, cena, ilosc, kod_kreskowy, data_przydatnosci):
        super().__init__(cena, ilosc, kod_kreskowy)
        self._data_przydatnosci = data_przydatnosci
        if not self._sprawdz_date():
            raise ValueError('Data jest niepoprawnego formatu')

    def _sprawdz_date(self):
        """
        Funkcja sprawdza, czy data jest w poprawnym formacie
        """
        return re.fullmatch(r'[0-3][0-9]-[0-1][0-9]-20[0-9][0-9]', self._data_przydatnosci)


Sklep.register(E_leclerc)

if __name__ == '__main__':
    kasa = Kasa.utworz()
    produkty = [Dostepny(10, 10, '1234567890123', '01-01-2020'),
                Dostepny(20, 20, '1234567890124', '01-01-2020'),
                Wyprzedany(30, 30, '1234567890125', '01-01-2020'),
                Wyprzedany(40, 40, '1234567890126', '01-01-2020')]
    sklep = E_leclerc(produkty, kasa)
    E_leclerc.wypisz_wartosc(sklep.wartosc_magazynu())
