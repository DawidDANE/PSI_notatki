# ============================================
# ZADANIE 1
# Pobranie danych meteorologicznych
# ============================================

# (Dane zostały zapisane ręcznie do pliku dane.txt)

# ============================================
# ZADANIE 2
# Załadowanie danych do DataFrame
# ============================================

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

dane = pd.read_csv("dane.txt", sep=r"\s+", header=None)

# ============================================
# ZADANIE 3
# Preparacja danych
# ============================================

# nadanie nazw kolumn
dane.columns = [
    "Rok", "Sty", "Lut", "Mar", "Kwi", "Maj", "Cze",
    "Lip", "Sie", "Wrz", "Paz", "Lis", "Gru"
]

# wybór stycznia
dane = dane[["Rok", "Sty"]]

# zmiana nazw kolumn (po polsku)
dane.columns = ["Data", "Temperatura"]

# konwersja do Celsjusza (jeśli dane są w Fahrenheit)
dane["Temperatura"] = (dane["Temperatura"] - 32) * 5/9

# pokazanie WSZYSTKICH danych
pd.set_option('display.max_rows', None)

print("\n--- ZADANIE 3: Dane po przygotowaniu ---")
print(dane)

# zapis danych
dane.to_csv("dane_styczen.txt", sep="\t", index=False)

# ============================================
# ZADANIE 4
# Statystyki opisowe
# ============================================

print("\n--- ZADANIE 4: Statystyki opisowe ---")
print(dane.describe())

# ============================================
# ZADANIE 5
# Regresja liniowa i prognoza
# ============================================

x = dane['Data']
y = dane['Temperatura']

linear_regression = stats.linregress(x, y)

print("\n--- ZADANIE 5: Regresja liniowa ---")
print("Nachylenie (slope):", linear_regression.slope)
print("Przecięcie (intercept):", linear_regression.intercept)

# prognoza na 2026
prognoza_2026 = linear_regression.slope * 2026 + linear_regression.intercept

print("\nPrognoza temperatury na styczeń 2026:")
print(prognoza_2026)

# ocena błędu
print("\nOcena modelu:")
print("R-value:", linear_regression.rvalue)
print("P-value:", linear_regression.pvalue)
print("Std error:", linear_regression.stderr)

# ============================================
# ZADANIE 6
# Wizualizacja regresji liniowej
# ============================================

plt.figure(figsize=(10, 6))

# wykres punktowy
sns.scatterplot(x='Data', y='Temperatura', data=dane)

# linia regresji
plt.plot(
    dane['Data'],
    linear_regression.slope * dane['Data'] + linear_regression.intercept,
    color='red'
)

plt.title("ZADANIE 6: Regresja liniowa temperatury styczniowej")
plt.xlabel("Rok")
plt.ylabel("Temperatura (°C)")

plt.grid(True)

# zapis wykresu
plt.savefig("wykres_regresji.png")

plt.show()

# ============================================
# KONIEC
# ============================================