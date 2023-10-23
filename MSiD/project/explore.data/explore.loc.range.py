import pandas as pd
import folium
from ast import literal_eval


def load_data(file_path):
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    df = df.sort_values('date')
    return df


def create_map(df, output_file):
    map = folium.Map(location=[0, 0], zoom_start=2)
    for idx, row in df.iterrows():
        coordinates = literal_eval(row['coordinates'])[0]
        folium.CircleMarker(
            location=[float(coordinates[0]), float(coordinates[1])],
            radius=0.1,
            color='red',
            fill=True,
            fill_opacity=0.7
        ).add_to(map)
    map.save(output_file)


def main():
    df = load_data('../data/converted_merchants_data.csv')
    create_map(df, 'sinking_map.html')


if __name__ == "__main__":
    main()
