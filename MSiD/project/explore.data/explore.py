import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_prepare_data(filepath):
    data = pd.read_csv(filepath, skiprows=1, header=None,
                 names=["uboat", "commander", "ship_name", "tonnage", "nationality", "convoy", "coordinates", "year",
                        "month", "day"])
    data["tonnage"] = data["tonnage"].str.replace(',', '').astype(float)
    return data


def create_directory_if_not_exists(directory):
    os.makedirs(directory, exist_ok=True)


def plot_histogram(data, column, bins, title, xlabel, ylabel, filename, kde=False, xticks=None, yscale=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data=data, x=column, bins=bins, kde=kde, ax=ax, color='red')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if xticks:
        ax.set_xticks(xticks)
    if yscale:
        ax.set_yscale(yscale)
    fig.savefig(filename)
    min_value = data[column].min()
    max_value = data[column].max()

    print(f"Minimum value in {column}: {min_value}")
    print(f"Maximum value in {column}: {max_value}")


def explore_data(df):
    df = df[df["tonnage"] > 0]
    plot_histogram(df, "tonnage", 100, "Rozkład tonażu zatopionych statków", " Tonaż", "Liczba zatopionych", "data/conclusions/tonnage.png", kde=False)
    plot_histogram(df, "day", 31, "Dzienny rozkład liczby zatopień", "Dzień miesiąca", "Liczba zatopień", "data/conclusions/day_histogram.png", kde=False, xticks=range(1, 32))
    plot_histogram(df, "month", 12, "Miesięczny rozkład liczby zatopień", "Miesiąc", "Liczba zatopień", "data/conclusions/month_histogram.png", kde=False, xticks=range(1, 13))
    plot_histogram(df, "year", 20, "Roczny rozkład liczby zatopień", "Rok", "Liczba zatopień", "data/conclusions/year_histogram.png", kde=True)

    plt.show()


def main():
    data_filepath = "../data/converted_merchants_data.csv"
    data = load_and_prepare_data(data_filepath)
    create_directory_if_not_exists("data/conclusions")
    explore_data(data)


if __name__ == "__main__":
    main()
