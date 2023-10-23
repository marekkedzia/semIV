import sys

from read_log import process_nasa_logs


def sort_logs(logs, sort_by):
    try:
        return sorted(logs, key=lambda element: element[sort_by])
    except IndexError:
        print(f"Incorrect sorting index (must be smaller then {len(logs[0])}).")
        return logs


if __name__ == "__main__":
    gb_transfer_index = 4
    print(sort_logs(process_nasa_logs(sys.stdin), gb_transfer_index))
