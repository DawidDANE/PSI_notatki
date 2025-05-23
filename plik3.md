# Warsztat samochodowy - Dokumentacja

## Opis projektu

Projekt zawiera implementację systemu zarządzania warsztatem samochodowym. Główna klasa `Warsztat` pozwala na zarządzanie pojazdami, klientami oraz procesem napraw.

## Struktura klasy Warsztat

### Konstruktor `__init__`

Inicjalizuje nową instancję warsztatu z podaną nazwą i adresem. 

```python
def __init__(self, nazwa: str, adres: str) -> None:
nazwa - nazwa warsztatu.

adres - adres warsztatu.

Inicjalizuje puste słowniki dla pojazdów i klientów oraz ustawia datę utworzenia na aktualny czas.

Metoda dodaj_pojazd
Dodaje pojazd do warsztatu pod warunkiem, że numer rejestracyjny jest unikalny i nie pusty.


def dodaj_pojazd(self, pojazd: Pojazd) -> bool:
Sprawdza, czy pojazd ma niepusty numer rejestracyjny.

Jeśli pojazd z tym numerem już istnieje, wyrzuca błąd.

Dodaje pojazd do słownika pojazdy.

Zwraca True w przypadku powodzenia.

Metoda klienci_aktywni
Zwraca listę aktywnych klientów.


def klienci_aktywni(self):
Przeszukuje słownik klientów i filtruje tych, którzy mają atrybut aktywny ustawiony na True.

Metoda znajdz_pojazd_po_rejestracji
Znajduje pojazd po numerze rejestracyjnym.


def znajdz_pojazd_po_rejestracji(self, nr_rejestracyjny: str):
Zwraca obiekt pojazdu lub None, jeśli nie znaleziono.

Metoda zglos_naprawe
Dodaje zgłoszenie naprawy dla klienta i pojazdu.


def zglos_naprawe(self, klient_id: int, pojazd_id: str, opis_usterki: str) -> None:
Pobiera klienta i pojazd po ID.

Jeśli któregokolwiek nie ma, rzuca wyjątek.

Dodaje zgłoszenie do klienta.

Ustawia pojazd w stan naprawy.

Metoda usun_pojazd
Usuwa pojazd z warsztatu, o ile nie jest w trakcie naprawy.


def usun_pojazd(self, nr_rejestracyjny):
Sprawdza istnienie pojazdu.

Sprawdza czy pojazd nie jest w naprawie.

Usuwa pojazd i zwraca go.

Metoda znajdz_pojazd
Alternatywna metoda do wyszukania pojazdu po numerze rejestracyjnym.


def znajdz_pojazd(self, nr_rejestracyjny: str) -> Optional[Pojazd]:
Zwraca pojazd lub None.

Metoda pojazdy_w_naprawie
Zwraca listę pojazdów obecnie w naprawie.

def pojazdy_w_naprawie(self) -> List[Pojazd]:
Filtruje pojazdy po stanie W_naprawie.

Metoda zarejestruj_klienta
Dodaje klienta do warsztatu, jeśli klient o takim ID jeszcze nie istnieje.


def zarejestruj_klienta(self, klient: Klient) -> bool:
Sprawdza istnienie klienta.

Dodaje klienta i zwraca True.

Metoda znajdz_klienta
Wyszukuje klienta po ID.


def znajdz_klienta(self, id_klienta: str) -> Optional[Klient]:
Zwraca klienta lub None.

Metoda zakoncz_naprawe
Kończy naprawę pojazdu, aktualizując stan i datę zakończenia.


def zakoncz_naprawe(self, nr_rejestracyjny):
Wyszukuje pojazd i wywołuje metodę kończącą naprawę.

Metoda zapisz_do_pliku
Zapisuje aktualny stan warsztatu do pliku JSON.


def zapisz_do_pliku(self, plik: str) -> bool:
Tworzy słownik z danymi warsztatu.

Konwertuje pojazdy i klientów do formatu JSON.

Zapisuje do wskazanego pliku.

Zwraca True.

Metoda wczytaj_z_pliku
Tworzy obiekt Warsztat na podstawie danych z pliku JSON.


@classmethod
def wczytaj_z_pliku(cls, plik: str) -> "Warsztat":
Sprawdza istnienie pliku.

Ładuje dane JSON.

Odtwarza obiekty pojazdów i klientów.

Zwraca nowy obiekt Warsztat.

def usun_pojazd(self, nr_rejestracyjny):
    if nr_rejestracyjny not in self.pojazdy:
        raise ValueError("Nie znaleziono pojazdu.")
    pojazd = self.pojazdy[nr_rejestracyjny]
    if pojazd.stan == StanPojazdu.W_naprawie:
        raise ValueError("Nie można usunąć pojazdu będącego w naprawie.")
    del self.pojazdy[nr_rejestracyjny]
    return pojazd
Sprawdza czy pojazd o podanym numerze istnieje.

Nie pozwala usunąć pojazdu, który jest aktualnie w naprawie.

Usuwa pojazd z warsztatu i zwraca usunięty obiekt.

Metoda znajdz_pojazd

def znajdz_pojazd(self, nr_rejestracyjny: str) -> Optional[Pojazd]:
    return self.pojazdy.get(nr_rejestracyjny)
Metoda identyczna do znajdz_pojazd_po_rejestracji, pobiera pojazd po numerze.

Metoda pojazdy_w_naprawie

def pojazdy_w_naprawie(self) -> List[Pojazd]:
    return [p for p in self.pojazdy.values() if p.stan == StanPojazdu.W_naprawie]
Zwraca listę pojazdów, które aktualnie są oznaczone jako „w naprawie”.

Metoda zarejestruj_klienta

def zarejestruj_klienta(self, klient: Klient) -> bool:
    if klient.id in self.klienci:
        raise ValueError("Klient o tym ID już istnieje.")
    self.klienci[klient.id] = klient
    return True
Dodaje nowego klienta, jeśli jego ID jeszcze nie istnieje.

Rzuca wyjątek, jeśli klient o takim ID jest już zarejestrowany.

Zwraca True na potwierdzenie.

Metoda znajdz_klienta

def znajdz_klienta(self, id_klienta: str) -> Optional[Klient]:
    return self.klienci.get(id_klienta)
Pobiera klienta po jego ID lub zwraca None, jeśli go nie ma.

Metoda zakoncz_naprawe

def zakoncz_naprawe(self, nr_rejestracyjny):
    pojazd = self.pojazdy.get(nr_rejestracyjny)
    if not pojazd:
        raise ValueError("Pojazd nie istnieje")
    pojazd.zakoncz_naprawe(datetime.now())
Pobiera pojazd i kończy jego naprawę, zapisując datę zakończenia.

Rzuca błąd, jeśli pojazd o takim numerze nie istnieje.

Metoda zapisz_do_pliku

def zapisz_do_pliku(self, plik: str) -> bool:
    dane = {
        "nazwa": self.nazwa,
        "adres": self.adres,
        "data_utworzenia": self.data_utworzenia.isoformat(),
        "pojazdy": {
            nr: json.loads(pojazd.to_json()) for nr, pojazd in self.pojazdy.items()
        },
        "klienci": {
            kid: json.loads(klient.to_json())
            for kid, klient in self.klienci.items()
        },
    }
    with open(plik, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=2)
    return True
Tworzy słownik ze wszystkimi danymi warsztatu.

Serializuje pojazdy i klientów do formatu JSON.

Zapisuje dane do pliku o podanej nazwie.
Metoda wczytaj_z_pliku
Tworzy obiekt Warsztat na podstawie danych z pliku JSON.


@classmethod
def wczytaj_z_pliku(cls, plik: str) -> "Warsztat":
Sprawdza istnienie pliku.

Ładuje dane JSON.

Odtwarza obiekty pojazdów i klientów.

Zwraca nowy obiekt Warsztat.