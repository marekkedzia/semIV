import sys

from list2 import process_nasa_logs


def filter_by_hours(logs, hour_from, hour_to):
    def filter_func(log):
        req_hour = process_nasa_logs.get_hour(log)
        if req_hour > hour_from or hour_from < hour_to:
            print(log)
            return True
        else:
            return False
    return list(filter(filter_func, logs))


def filter_from_22_to_6(logs):
    return filter_by_hours(logs, 22, 6)


if __name__ == "__main__":
    filter_from_22_to_6(process_nasa_logs(sys.stdin))

