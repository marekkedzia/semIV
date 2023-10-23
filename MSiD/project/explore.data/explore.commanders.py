import pandas as pd
import matplotlib.pyplot as plt


def load_data(filepath):
    return pd.read_csv(filepath)


def calculate_commander_counts(data):
    return data['commander'].value_counts()


def get_top_commanders(commander_counts, top_n=3):
    return commander_counts[:top_n]


def get_commanders_with_min_sinkings(commander_counts, min_sinkings=5):
    return commander_counts[commander_counts >= min_sinkings]


def plot_data(data, title, xlabel, ylabel, ax):
    ax.bar(data.index, data.values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def main():
    data = load_data('../data/converted_merchants_data.csv')

    commander_counts = calculate_commander_counts(data)
    top3_commanders = get_top_commanders(commander_counts, 3)
    five_or_more = get_commanders_with_min_sinkings(commander_counts, 5)

    print("Trzech dowódców z największą liczbą zatopień:")
    print(top3_commanders)
    print("\nDowódcy z 5 lub więcej zatopień:")
    print(five_or_more)
    print("\nLiczba wszystkich dowodcow:")
    print(commander_counts)

    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    plot_data(top3_commanders, 'Trzech dowódców z największą liczbą zatopień', 'Dowódca', 'Liczba zatopień', axs[0])
    plot_data(five_or_more, 'Dowódcy z 5 lub więcej zatopień', 'Dowódca', 'Liczba zatopień', axs[1])

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
