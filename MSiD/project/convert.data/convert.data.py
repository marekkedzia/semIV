import pandas as pd

import json


def load_data(csv_file='sunk_ships_data.csv', skip_rows=1):
    return pd.read_csv(csv_file, delimiter=',', header=None, skiprows=skip_rows,
                       names=['date', 'uboat', 'commander', 'ship_name', 'tonnage', 'nationality', 'convoy',
                              'coordinates'])


def transform_data(data):
    data['date'] = pd.to_datetime(data['date'], format='%d %b %Y')
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day'] = data['date'].dt.day

    data['nationality'], nationality_labels = pd.factorize(data['nationality'])
    nationality_mapping = dict(enumerate(nationality_labels))

    data['convoy'], convoy_labels = pd.factorize(data['convoy'])
    convoy_mapping = dict(enumerate(convoy_labels))

    data['coordinates'] = data["coordinates"]
    transformed_data = data.drop(columns=['date'])

    return transformed_data, nationality_mapping, convoy_mapping


def save_mapping(mapping, filename):
    with open(filename, 'w') as f:
        json.dump(mapping, f)


def split_valid_invalid_data(data):
    valid_data = data.dropna()
    invalid_data = data[data.isna().any(axis=1)]

    return valid_data, invalid_data


def save_data(data, filename):
    data.to_csv(filename, index=False)


data = load_data()
data, nationality_mapping, convoy_mapping = transform_data(data)
save_mapping(nationality_mapping, 'nationality_mapping.json')
save_mapping(convoy_mapping, 'convoy_mapping.json')
valid_data, invalid_data = split_valid_invalid_data(data)
save_data(valid_data, 'converted_merchants_data.csv')
save_data(invalid_data, 'invalid_merchants_data.csv')
