import sys

from read_log import process_nasa_logs
from log_to_dict import log_to_dict


def get_addrs(dictionary):
    return list(dictionary.keys())


if __name__ == '__main__':
    print(get_addrs(log_to_dict(process_nasa_logs(sys.stdin))))
