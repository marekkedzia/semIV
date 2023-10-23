import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_prepare_data(data_path):
    df = pd.read_csv(data_path)
    df = df.drop(columns=['commander', 'ship_name', 'convoy', 'coordinates', 'tonnage', 'year', 'month', 'day'])
    return df


def count_uboat_hits(data):
    uboat_data = data['uboat'].value_counts().nlargest(50)
    return uboat_data


def create_uboat_visualization(uboat_data, output_image_path):
    plt.figure(figsize=(10, 5))
    sns.barplot(x=uboat_data.index, y=uboat_data.values, color='red')
    plt.title('50 Uboatów z największą liczbą zatopień')
    plt.ylabel('Zatopienia')
    plt.xlabel('Uboat')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(output_image_path)
    plt.show()


def calculate_time_between_sinks(df):
    df['time_between_sinks'] = df['date'].diff()
    zero_diffs = df[df['time_between_sinks'].dt.total_seconds() == 0].shape[0]
    print(f"Liczba odstępów równych zero: {zero_diffs}")
    df = df[df['time_between_sinks'].dt.total_seconds() != 0]
    average_time_between_sinks = df['time_between_sinks'].mean()
    print(average_time_between_sinks)


def main():
    data = load_and_prepare_data('../data/converted_merchants_data.csv')
    uboat_data = count_uboat_hits(data)
    create_uboat_visualization(uboat_data, 'uboat_hits.png')
    calculate_time_between_sinks(data)


if __name__ == "__main__":
    main()
