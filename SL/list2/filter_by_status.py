import sys

from process_nasa_logs import process_nasa_logs, get_http_code


def filter_by_status(logs, status):
    def filter_func(log):
        if get_http_code(log) == status:
            print(log)
            return True
        else:
            return False
    return list(filter(filter_func, logs))


def filter_by_ok_status(logs):
    return filter_by_status(logs, "200")


if __name__ == "__main__":
    filter_by_ok_status(process_nasa_logs(sys.stdin))

