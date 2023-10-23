import sys

from process_nasa_logs import get_day, process_nasa_logs


def filter_by_day(logs, day):
    def filter_func(log):
        if get_day(log) == day:
            print(log)
            return True
        else:
            return False

    return list(filter(filter_func, logs))


def filter_by_friday(logs):
    friday = 4
    return filter_by_day(logs, friday)


if __name__ == "__main__":
    filter_by_friday(process_nasa_logs(sys.stdin))
