import zad4b
import zad4c
import argparse


def main(logs):
    parser = argparse.ArgumentParser(description="Analiza logów SSH")
    parser.add_argument("log_file", help="ścieżka do pliku z logami")
    parser.add_argument("-m", "--min-log-level", type=int, help="minimalny poziom logowania (opcjonalny)")

    args = parser.parse_args()

    if args.command == "task2":
        avg_duration, std_dev = zad4b.calculate_duration_and_std(args.log_file)
        print(f"Średni czas trwania: {avg_duration} sekund")
        print(f"Odchylenie standardowe: {std_dev} sekund")
    elif args.command == "task4":
        most_common = zad4c.find_max_logins_username(logs)
        smallest_number = zad4c.find_min_logins_username(logs)

        print(f"Najczęstszy element na liście: {most_common}")
        print(f"Najmniejsza liczba na liście: {smallest_number}")
