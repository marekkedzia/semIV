import sys

from entry_to_dict import entry_to_dict
from read_log import process_nasa_logs, get_ip_address


def log_to_dict(logs):
    dictionary = dict()

    def add_to_dict(host, log):
        dictionary.setdefault(host, []).append(log)

    def fill_dict():
        for log in logs:
            add_to_dict(get_ip_address(log), entry_to_dict(log))

    fill_dict()
    return dictionary


if __name__ == '__main__':
    print(log_to_dict(process_nasa_logs(sys.stdin)))
