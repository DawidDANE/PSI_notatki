import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# ==========================================================
# WCZYTANIE DANYCH
# ==========================================================

plik = "Projekt_Koncowy_MMS.xlsx"

df = pd.read_excel(plik)

# ==========================================================
# CZYSZCZENIE KOLUMN
# ==========================================================

df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

df.columns = df.columns.str.strip()

print("KOLUMNY:")
print(df.columns.tolist())

# ==========================================================
# KOLUMNY LICZBOWE
# ==========================================================

numeric_cols = [
    "Overall Score",
    "Research Environment",
    "Research Quality",
    "Industry Impact",
    "Teaching"
]

# ==========================================================
# CZYSZCZENIE LICZB
# ==========================================================

for col in numeric_cols:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# ==========================================================
# USUWANIE BRAKÓW
# ==========================================================

df = df.dropna()

print("\nLICZBA WIERSZY:")
print(len(df))

# ==========================================================
# ZMIENNA OBJAŚNIANA
# ==========================================================

y = df["Overall Score"]

# ==========================================================
# ZMIENNE OBJAŚNIAJĄCE
# ==========================================================

variables = [
    "Research Environment",
    "Research Quality",
    "Industry Impact",
    "Teaching"
]

# ==========================================================
# ANALIZA KORELACJI
# ==========================================================

print("\nANALIZA WSPÓŁCZYNNIKÓW KORELACJI")
print("=" * 70)

istotne = []

wyniki = []

wyniki.append(
    "ANALIZA WSPÓŁCZYNNIKÓW KORELACJI"
)

wyniki.append("=" * 70)

for col in variables:

    corr, pval = pearsonr(df[col], y)

    # tylko istotne statystycznie
    if pval < 0.05:

        istotne.append(col)

        # siła korelacji
        if abs(corr) >= 0.7:
            sila = "silna"

        elif abs(corr) >= 0.3:
            sila = "umiarkowana"

        else:
            sila = "slaba"

        print("\n" + "-" * 70)
        print(f"Zmienna: {col}")
        print(f"Korelacja Pearsona: {corr:.6f}")
        print(f"P-value: {pval:.15f}")

        print(
            f"Wniosek: "
            f"ISTOTNA statystycznie "
            f"({sila} korelacja)"
        )

        wyniki.append("\n" + "-" * 70)

        wyniki.append(
            f"Zmienna: {col}"
        )

        wyniki.append(
            f"Korelacja Pearsona: "
            f"{corr:.6f}"
        )

        wyniki.append(
            f"P-value: "
            f"{pval:.15f}"
        )

        wyniki.append(
            f"Wniosek: "
            f"ISTOTNA statystycznie "
            f"({sila} korelacja)"
        )

# ==========================================================
# WYBRANE ZMIENNE
# ==========================================================

print("\nWYBRANE ZMIENNE")
print("=" * 70)

wyniki.append("\nWYBRANE ZMIENNE")
wyniki.append("=" * 70)

for x in istotne:

    print(x)

    wyniki.append(x)

# ==========================================================
# INTERPRETACJA
# ==========================================================

print("\nINTERPRETACJA")
print("=" * 70)

interpretacja = (
    "Do dalszej analizy wybrano zmienne "
    "istotne statystycznie "
    "(p-value < 0.05). "
    "Zmienne te wykazują "
    "największy wpływ na Overall Score."
)

print(interpretacja)

wyniki.append("\nINTERPRETACJA")
wyniki.append("=" * 70)
wyniki.append(interpretacja)

# ==========================================================
# MACIERZ KORELACJI
# ==========================================================

corr_matrix = df[
    variables + ["Overall Score"]
].corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title(
    "Macierz korelacji"
)

plt.tight_layout()

plt.savefig(
    "macierz_korelacji.png"
)

plt.close()

# ==========================================================
# ZAPIS DO PLIKU
# ==========================================================

with open(
    "analiza_korelacji.txt",
    "w",
    encoding="utf-8"
) as f:

    for line in wyniki:

        f.write(str(line))
        f.write("\n")

# ==========================================================
# KONIEC
# ==========================================================

print("\nZAPISANO:")
print("analiza_korelacji.txt")

print("\nWYGNEROWANO:")
print("macierz_korelacji.png")