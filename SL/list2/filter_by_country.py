import sys

from process_nasa_logs import process_nasa_logs, get_country


def filter_by_country(logs, country_code):
    def filter_func(log):
        if get_country(log) == country_code:
            print(log)
            return True
        else:
            return False
    return list(filter(filter_func, logs))


def filter_by_pl_domain(logs):
    return filter_by_country(logs, "pl")


if __name__ == "__main__":
    filter_by_pl_domain(process_nasa_logs(sys.stdin))

