import pandas as pd

df = pd.read_csv('commanders_time_between_sinks.csv')

df = df.dropna()

print(df['time_between_sinks'].mean())
