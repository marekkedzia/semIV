import pandas as pd

# wczytanie pliku CSV
df = pd.read_csv("dane.csv")

# wyświetlenie kilku pierwszych wierszy
print(df.head())

# obliczenie podstawowych statystyk opisowych
print(df.describe())
