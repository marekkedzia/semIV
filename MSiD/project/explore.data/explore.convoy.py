import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(data_path, mapping_path):
    df = pd.read_csv(data_path)
    with open(mapping_path) as json_file:
        mapping = json.load(json_file)
    return df, mapping


def clean_and_convert_tonnage(df):
    df['tonnage'] = df['tonnage'].str.replace(',', '').astype(float)
    return df


def calculate_convoy_losses(df):
    return df[df['convoy'] != '-'].groupby('convoy').size()


def get_top_convoys(convoy_losses, mapping, top_n=30):
    top_convoy_indices = convoy_losses.nlargest(top_n + 1).index
    top_convoy_losses = pd.Series([mapping[str(i)] for i in top_convoy_indices], index=top_convoy_indices)
    return top_convoy_losses


def plot_data(x, y, title, xlabel, ylabel, rotation=90):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=x, y=y, color='red')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=rotation)
    plt.tight_layout()


def main():
    data, mapping = load_data('../data/converted_merchants_data.csv', '../data/mappings/convoy_mapping.json')
    data = clean_and_convert_tonnage(data)
    convoy_losses = calculate_convoy_losses(data)
    top_30_convoy_losses = get_top_convoys(convoy_losses, mapping, 30)
    plot_data(top_30_convoy_losses.index, top_30_convoy_losses.values, 'Top 30 konwojów z największymi stratami', 'Konwój', 'Straty (liczba statków)')
    plt.show()


if __name__ == '__main__':
    main()
