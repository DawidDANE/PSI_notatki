### Pełna analiza kodu klasy `Klient` (z wyjaśnieniami każdej linijki)

```python
import json
import re
from enum import Enum, auto
from datetime import datetime
from typing import List, Dict, Any
from src.pojazd_naprawa import Pojazd, StanPojazdu
```

* **import json**: pozwala zamieniać dane na tekst JSON i odwrotnie.
* **import re**: narzędzie do sprawdzania wzorców w tekście (np. emaila).
* **Enum, auto**: do tworzenia listy opcji (np. typ klienta).
* **datetime**: do obsługi daty i czasu.
* **typing**: podpowiedzi typów (List, Dict, Any).
* **z innego pliku importujemy klasy Pojazd i StanPojazdu**.

```python
class TypKlienta(Enum):
    INDYWIDUALNY = auto()
    FIRMOWY = auto()
```

* Tworzymy typ wyliczeniowy z dwoma opcjami: INDYWIDUALNY i FIRMOWY.
* `auto()` automatycznie nadaje wartość (np. 1, 2).

```python
class Klient:
    def __init__(self, id: int, imie_nazwisko: str, email: str, typ: TypKlienta, aktywny: bool = True) -> None:
```

* ****init****: konstruktor klasy (tworzy klienta).
* Przyjmuje dane klienta: id, imie i nazwisko, email, typ klienta i czy aktywny.

```python
        if not email or "@" not in email:
            raise ValueError("Email musi być poprawny i zawierać '@'")
```

* Sprawdzenie czy email nie jest pusty i zawiera `@`.
* **raise**: rzuć wyjątek (błąd).
* **ValueError**: błąd niepoprawnej wartości.

```python
        if not imie_nazwisko:
            raise ValueError("Imię i nazwisko nie może być puste")
```

* Sprawdzenie czy podano imie i nazwisko.

```python
        if not email or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", email):
            raise ValueError("Niepoprawny adres email")
```

* Dokładniejsze sprawdzenie emaila przy pomocy wyrażeń regularnych (**re.match**).

```python
        self.id = id
        self.imie_nazwisko = imie_nazwisko
        self.email = email
        self.typ = typ
        self.aktywny = aktywny
        self.historia_zgloszen: List[Dict[str, Any]] = []
```

* Przypisujemy dane do obiektu (self = ten konkretny klient).
* `historia_zgloszen` to lista zgłoszeń dotyczących naprawy pojazdu.

### Metoda: dodaj zgłoszenie

```python
def dodaj_zgloszenie(self, pojazd_id: str, opis_usterki: str) -> None:
```

* Dodaje nowe zgłoszenie do listy zgłoszeń klienta.

```python
    if not isinstance(pojazd_id, str) or not pojazd_id:
        raise TypeError("ID pojazdu musi być niepustym stringiem")
```

* **isinstance()** sprawdza, czy `pojazd_id` to napis.
* **TypeError**: błąd typu (np. jakby podać liczbę zamiast tekstu).

```python
    if not isinstance(opis_usterki, str) or not opis_usterki:
        raise ValueError("Opis usterki nie może być pusty")
```

* Sprawdza czy opis jest poprawnym tekstem.

```python
    self.historia_zgloszen.append({"pojazd_id": pojazd_id, "opis_usterki": opis_usterki})
```

* Dodaje zgłoszenie (jako słownik) do listy.

### Metoda: usuń zgłoszenie

```python
def usun_zgloszenie(self, pojazd_id: str, opis_usterki: str) -> None:
```

* Szuka i usuwa zgłoszenie z listy.

```python
    for i, zgloszenie in enumerate(self.historia_zgloszen):
        if zgloszenie["pojazd_id"] == pojazd_id and zgloszenie["opis_usterki"] == opis_usterki:
            del self.historia_zgloszen[i]
            return
    raise ValueError("Nie znaleziono zgłoszenia do usunięcia")
```

* Szuka zgłoszenia pasującego do pojazdu i opisu. Jeśli znajdzie, usuwa. Jak nie, rzuca błąd.

### Metoda: wstaw pojazd do naprawy

```python
def wstaw_pojazd_do_naprawy(self, pojazd: Pojazd, opis_usterki: str) -> None:
```

* Dodaje zgłoszenie i oznacza pojazd jako w naprawie.

```python
    if not isinstance(opis_usterki, str) or not opis_usterki:
        raise ValueError("Opis usterki musi być niepustym stringiem")
    if pojazd.stan != StanPojazdu.Dostepny:
        raise ValueError(f"Pojazd {pojazd.identyfikator} nie jest dostępny.")
    self.dodaj_zgloszenie(pojazd.identyfikator, opis_usterki)
    pojazd.wstaw_do_naprawy(datetime.now())
```

* Sprawdza czy opis usterki jest poprawny.
* Sprawdza czy pojazd jest dostępny.
* Dodaje zgłoszenie i rozpoczyna naprawę.

### Metoda: odbierz pojazd po naprawie

```python
def odbierz_pojazd_po_naprawie(self, pojazd: Pojazd) -> None:
```

* Zamyka naprawę i aktualizuje dane pojazdu.

```python
    if not self.aktywny:
        raise PermissionError("Klient nie jest aktywny")
    if pojazd.stan != StanPojazdu.W_naprawie:
        raise ValueError(f"Pojazd {pojazd.identyfikator} nie jest w naprawie.")
    if not any(z["pojazd_id"] == pojazd.identyfikator for z in self.historia_zgloszen):
        raise ValueError("Klient nie ma zgłoszenia dla tego pojazdu.")
    if not pojazd.historia:
        raise ValueError("Historia pojazdu jest pusta, nie można zakończyć naprawy")
    pojazd.zakoncz_naprawe(datetime.now())
```

* Sprawdza:

  * Czy klient aktywny
  * Czy pojazd jest w naprawie
  * Czy klient zgłosił ten pojazd
  * Czy naprawa została rozpoczetą

### Metoda: dezaktywuj klienta

```python
def dezaktywuj(self):
    self.aktywny = False
```

* Ustawia klienta jako nieaktywnego.

### Zapisz do JSON

```python
def to_json(self) -> str:
    return json.dumps({
        "id": self.id,
        "imie_nazwisko": self.imie_nazwisko,
        "email": self.email,
        "typ": self.typ.name,
        "aktywny": self.aktywny,
        "historia_zgloszen": self.historia_zgloszen,
    }, ensure_ascii=False, indent=2)
```

* Tworzy JSON z obiektu klienta.
* `typ.name` zamienia enum na jego nazwę np. "FIRMOWY".

### Wczytaj klienta z JSON

```python
@classmethod
def from_json(cls, dane: str) -> "Klient":
    obj = json.loads(dane)
    typ_klienta = TypKlienta[obj["typ"]]
    klient = cls(id=obj["id"], imie_nazwisko=obj["imie_nazwisko"], email=obj["email"], typ=typ_klienta)
    klient.aktywny = obj["aktywny"]
    klient.historia_zgloszen = obj.get("historia_zgloszen", [])
    return klient
```

* Odtwarza klienta z danych JSON.
* **@classmethod**: metoda należy do klasy, a nie do konkretnego obiektu.
* Używa `cls(...)` zamiast `Klient(...)`, by działało nawet gdy klasa się nazywa inaczej.
