# Dokumentacja klas `StanPojazdu` i `Pojazd`

## Importy

```python
import json
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Optional
```

- `json` – do serializacji i deserializacji danych JSON.  
- `datetime` – do pracy z datami i czasem.  
- `Enum` i `auto` – do definiowania enumeracji (stałych wartości).  
- `typing` – podpowiedzi typów (lista, słownik, opcjonalny typ).  

---

## Klasa `StanPojazdu`

Reprezentuje możliwe stany pojazdu w warsztacie.

```python
class StanPojazdu(Enum):
    """Stan pojazdów w naprawie."""

    Dostepny = auto()
    W_naprawie = auto()
    Naprawiony = auto()
    Niedostepny = auto()
```

- `Dostepny` – pojazd jest dostępny do użytku lub naprawy.  
- `W_naprawie` – pojazd jest aktualnie w naprawie.  
- `Naprawiony` – pojazd zakończył naprawę.  
- `Niedostepny` – pojazd jest niedostępny (np. wycofany).  

---

## Klasa `Pojazd`

Opisuje pojazd w warsztacie wraz z jego danymi i historią napraw.

### Konstruktor

```python
def __init__(
    self,
    identyfikator: str,
    marka: str,
    nr_rejestracyjny: str,
    model: str,
    rok_produkcji: int,
    stan: StanPojazdu,
    historia: Optional[List[Dict]] = None,
) -> None:
```

Argumenty:

- `identyfikator` – unikalny ID pojazdu.  
- `marka` – marka pojazdu (np. Toyota).  
- `nr_rejestracyjny` – numer rejestracyjny.  
- `model` – model pojazdu (np. Corolla).  
- `rok_produkcji` – rok produkcji (nie może być z przyszłości).  
- `stan` – aktualny stan pojazdu (z `StanPojazdu`).  
- `historia` – lista słowników opisujących historię napraw (opcjonalne).  

Walidacje:

- `rok_produkcji` nie może być większy niż bieżący rok.  
- `model` nie może być pusty.  
- `marka` musi być typu `str`.  
- Jeśli historia nie zostanie podana, tworzona jest pusta lista.  

---

### Metoda `wstaw_do_naprawy`

```python
def wstaw_do_naprawy(self, data_rozpoczecia: datetime) -> None:
```

- Zmienia stan pojazdu na `W_naprawie`.  
- Dodaje do historii wpis z datą rozpoczęcia naprawy i statusem "Naprawa rozpoczęta".  
- Sprawdza, czy pojazd jest w stanie `Dostepny` przed rozpoczęciem naprawy.  
- Jeśli stan jest inny lub historia nie jest listą, rzuca wyjątek.  

---

### Metoda `zakoncz_naprawe`

```python
def zakoncz_naprawe(self, data_zakonczenia: datetime) -> None:
```

- Zmienia stan pojazdu na `Naprawiony`.  
- Dodaje do historii wpis z datą zakończenia naprawy i statusem "Naprawa zakończona".  
- Sprawdza, czy pojazd jest aktualnie w stanie `W_naprawie`.  
- Jeśli data zakończenia jest `None` lub pojazd nie jest w naprawie, rzuca wyjątek.  

---

### Metoda `oznacz_jako_niedostepny`

```python
def oznacz_jako_niedostepny(self):
```

- Ustawia stan pojazdu na `Niedostepny`.  
- Jeśli pojazd już jest niedostępny, nic nie robi.  

---

### Metoda `wydaj_klientowi`

```python
def wydaj_klientowi(self) -> None:
```

- Ustawia stan pojazdu na `Dostepny`.  
- Dodaje do historii wpis z aktualną datą i statusem "Pojazd wydany klientowi".  
- Jeśli pojazd nie jest naprawiony, rzuca wyjątek.  

---

### Metoda `to_json`

```python
def to_json(self):
```

- Serializuje obiekt `Pojazd` do JSON (string).  

---

### Metoda `from_json`

```python
@classmethod
def from_json(cls, dane: str) -> "Pojazd":
```

- Tworzy obiekt `Pojazd` z danych JSON (string).  
