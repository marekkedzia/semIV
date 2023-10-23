import matplotlib.pyplot as plt
import pandas as pd


def load_and_clean_ship_data(filepath):
    ship_data = pd.read_csv(filepath, header=0,
                            names=["uboat", "commander", "ship_name", "tonnage", "nationality", "convoy", "coordinates",
                                   "year", "month", "day"])

    ship_data[["year", "month", "day"]] = ship_data[["year", "month", "day"]].apply(pd.to_numeric, errors='coerce')

    ship_data.dropna(subset=["year", "month", "day"], inplace=True)

    ship_data["date"] = pd.to_datetime(ship_data[["year", "month", "day"]])
    return ship_data


def load_battle_data(filepath):
    return pd.read_csv(filepath, names=["Battle", "Start", "End", "Location", "Result"], header=0,
                       parse_dates=["Start", "End"])


def merge_data(ship_data, battle_data):
    merged_data = ship_data.merge(battle_data, left_on="date", right_on="Start", how="outer")
    merged_data["is_battle"] = ~merged_data["Battle"].isna()
    merged_data["month_year"] = pd.to_datetime(merged_data["date"]).dt.to_period("M")
    return merged_data


def monthly_ship_count(merged_data):
    ship_count_monthly = merged_data.groupby(["month_year", "is_battle"]).size().reset_index(name="count")
    ship_count_monthly_pivot = ship_count_monthly.pivot(index="month_year", columns="is_battle", values="count")

    ship_count_monthly_pivot.fillna(0, inplace=True)
    return ship_count_monthly_pivot


def visualize_data(ship_count_monthly_pivot):
    fig, ax = plt.subplots(figsize=(15, 7))

    start_date = pd.to_datetime('1939-09-01')
    end_date = pd.to_datetime('1945-05-01')
    ax.set_xlim(start_date, end_date)

    ship_count_monthly_pivot.plot(ax=ax)

    ax.set_title("Liczba zatopionych okrętów podczas bitw (miesięcznie)")
    ax.set_xlabel("Miesiąc i rok")
    ax.set_ylabel("Liczba zatopionych okrętów")
    ax.legend(["Bez bitwy", "Podczas bitwy"])
    plt.xticks(rotation=45)

    plt.savefig("sunk_day_by_day.png")

    plt.show()


def main():
    ship_data_filepath = "../data/converted_merchants_data.csv"
    battle_data_filepath = "../data/raw/battles.csv"

    ship_data = load_and_clean_ship_data(ship_data_filepath)
    battle_data = load_battle_data(battle_data_filepath)

    merged_data = merge_data(ship_data, battle_data)
    ship_count_monthly_pivot = monthly_ship_count(merged_data)

    visualize_data(ship_count_monthly_pivot)


if __name__ == "__main__":
    main()

