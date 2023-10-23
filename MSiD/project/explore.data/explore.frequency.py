import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/converted_merchants_data.csv')

df = df.drop(columns=['commander', 'ship_name', 'convoy', 'coordinates', 'tonnage', 'year', 'month', 'day'])

uboat_data = df['uboat'].value_counts().nlargest(50)

plt.figure(figsize=(10, 5))
sns.barplot(x=uboat_data.index, y=uboat_data.values, color='red')
plt.title('50 Uboatów z największą liczbą zatopień')
plt.ylabel('Zatopienia')
plt.xlabel('Uboat')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.2)  # Dodajemy trochę więcej przestrzeni na dole wykresu
plt.savefig('uboat_hits.png')
plt.show()

# Tworzenie przykładowego mapowania
nationality_mapping = {
    0: "Great Britain",
    1: "Belgium",
    2: "Finland",
    3: "France",
    4: "Estonia",
    5: "Sweden",
    6: "Norway",
    7: "Denmark",
    8: "Greece",
    9: "Netherlands",
    10: "Lithia",
    11: "Yugoslavia",
    12: "German",
    13: "Latvia",
    14: "Spain",
    15: "Panama",
    16: "Italy",
    17: "Iran",
    18: "Argentina",
    19: "Canada",
    20: "Egypt",
    21: "Hungary",
    22: "Faroe",
    23: "Portugal",
    24: "Iceland",
    25: "Armenia",
    26: "Soviet Union",
    27: "Australia",
    28: "Poland",
    29: "Belize",
    30: "Venezuela",
    31: "Georgia",
    32: "Saudi Arabia",
    33: "Chile",
    34: "Honduras",
    35: "Dominican Republic",
    36: "Nicaragua",
    37: "Montenegro",
    38: "Jamaica",
    39: "Colombia",
    40: "New Zealand",
    41: "Syria",
    42: "Uruguay",
    43: "Cuba",
    44: "Lebanon",
    45: "India",
    46: "Switzerland"
}

# Wyszukujemy narodowości z liczbą wystąpień <= 3
low_count_nationalities = df['nationality'].value_counts()
low_count_nationalities = low_count_nationalities[low_count_nationalities <= 3]

# Tworzymy nową kolumnę 'nationality_modified', zastępując narodowości o liczbie wystąpień <= 3 jako 'other'
df['nationality_modified'] = df['nationality'].apply(lambda x: 'other' if x in low_count_nationalities.index else x)

# Aktualizujemy nationality_data, usuwając te, które zostały zastąpione przez 'other'
nationality_data = df['nationality_modified'].value_counts()

plt.figure(figsize=(10, 5))

# Utwórz serię danych do wykresu, gdzie indeksy są zastąpione etykietami z mapowania
plot_data = pd.Series(nationality_data.values,
                      index=[nationality_mapping.get(i, f'Unknown {i}') for i in nationality_data.index])

sns.barplot(x=plot_data.index, y=plot_data.values, color='red')

plt.yscale('log')
plt.title('Wykres częstotliwości dla narodowości (skala logarytmiczna)')
plt.ylabel('Stracone statki')
plt.xlabel('Narodowość')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('nationality.png')
plt.show()




