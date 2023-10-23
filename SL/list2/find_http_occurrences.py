import sys
from functools import reduce
from process_nasa_logs import process_nasa_logs

NOT_FOUND = "404"
OK = "200"
FOUND = "302"


def find_http_status(status, logs):
    return reduce(lambda acc, log: acc + (process_nasa_logs.get_http_code(log) == status), logs, 0)


def print_http_occurrences(status, occurrences):
    print('Http status ' + str(status) + ' occurs ' + str(occurrences) + ' times')


def find_404_status_occurrences(logs):
    print_http_occurrences(NOT_FOUND, find_http_status(NOT_FOUND, logs))


def find_200_status_occurrences(logs):
    print_http_occurrences(OK, find_http_status(OK, logs))


def find_302_status_occurrences(logs):
    print_http_occurrences(FOUND, find_http_status(FOUND, logs))


if __name__ == "__main__":
    logs = process_nasa_logs(sys.stdin)
    find_200_status_occurrences(logs)
    find_302_status_occurrences(logs)
    find_404_status_occurrences(logs)

