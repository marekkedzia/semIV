import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_prepare_ship_data(data_path):
    ship_data = pd.read_csv(
        data_path,
        header=0,
        names=["uboat", "commander", "ship_name", "tonnage", "nationality", "convoy", "coordinates", "year", "month", "day"]
    )
    ship_data[["year", "month", "day"]] = ship_data[["year", "month", "day"]].apply(pd.to_numeric, errors='coerce')
    ship_data.dropna(subset=["year", "month", "day"], inplace=True)
    ship_data["date"] = pd.to_datetime(ship_data[["year", "month", "day"]])

    return ship_data


def load_and_prepare_battle_data(battle_data_path):
    battle_data = pd.read_csv(battle_data_path)
    battle_data["Start"] = pd.to_datetime(battle_data["Start"], errors="coerce")
    battle_data["End"] = pd.to_datetime(battle_data["End"], errors="coerce")

    return battle_data


def merge_data(ship_data, battle_data):
    merged_data = ship_data.merge(battle_data, left_on="date", right_on="Start", how="outer")
    merged_data["is_battle"] = ~merged_data["Battle"].isna()
    merged_data["month_year"] = pd.to_datetime(merged_data["date"]).dt.to_period("M")

    return merged_data


def create_visualization(merged_data, output_image_path):
    ship_count = merged_data.groupby(["month_year", "is_battle"]).size().reset_index(name="count")
    ship_count_pivot = ship_count.pivot(index="month_year", columns="is_battle", values="count")
    ship_count_pivot["ratio"] = ship_count_pivot[True] / (ship_count_pivot[True] + ship_count_pivot[False])

    plt.figure(figsize=(10, 5))
    sns.set_style("whitegrid")
    bar_plot = sns.barplot(x=ship_count_pivot.index, y=ship_count_pivot["ratio"])
    bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=90)

    plt.title("Liczba zatopionych okrętów podczas bitw")
    plt.xlabel("Miesiąc i rok")
    plt.ylabel("Stosunek liczby zatopionych okrętów podczas bitw do ogólnej liczby zatopień")
    plt.savefig(output_image_path)
    plt.show()


def main():
    ship_data = load_and_prepare_ship_data("../data/converted_merchants_data.csv")
    battle_data = load_and_prepare_battle_data("../data/raw/battles.csv")
    merged_data = merge_data(ship_data, battle_data)
    create_visualization(merged_data, "../data/conclusions/sunk.to.battles.png")


if __name__ == "__main__":
    main()
