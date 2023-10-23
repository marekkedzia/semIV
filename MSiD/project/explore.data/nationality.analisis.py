import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json


def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def load_and_prepare_data(data_path):
    df = pd.read_csv(data_path)
    return df


def modify_nationality_data(df, nationality_mapping):
    low_count_nationalities = df['nationality'].value_counts()
    low_count_nationalities = low_count_nationalities[low_count_nationalities <= 3]
    df['nationality_modified'] = df['nationality'].apply(lambda x: 'other' if x in low_count_nationalities.index else x)
    nationality_data = df['nationality_modified'].value_counts()
    plot_data = pd.Series(nationality_data.values,
                          index=[nationality_mapping.get(i, f'Unknown {i}') for i in nationality_data.index])
    return plot_data


def create_nationality_visualization(plot_data, output_image_path):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=plot_data.index, y=plot_data.values, color='red')
    plt.yscale('log')
    plt.title('Wykres częstotliwości dla narodowości (skala logarytmiczna)')
    plt.ylabel('Stracone statki')
    plt.xlabel('Narodowość')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_image_path)
    plt.show()


def main():
    nationality_mapping = load_json('nationality.mapping.json')

    data = load_and_prepare_data('../data/converted_merchants_data.csv')
    plot_data = modify_nationality_data(data, nationality_mapping)
    create_nationality_visualization(plot_data, 'nationality.png')


if __name__ == "__main__":
    main()
