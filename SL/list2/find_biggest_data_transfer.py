import sys

from process_nasa_logs import get_transfer_size, process_nasa_logs
from functools import reduce

nasa_no_transfer_code = '-'
default_nasa_log = ["No NASA log with any transfer found", "-", "-", "-", "0"]


def find_biggest_data_transfer(logs):
    def compare_transfers(log1, log2):
        log1_transfer = get_transfer_size(log1)
        log2_transfer = get_transfer_size(log2)
        return log1 if log1_transfer != nasa_no_transfer_code and int(log1_transfer) > int(log2_transfer) else log2

    print(
        'The biggest data transfer: ' + str(
            reduce(lambda acc, log: compare_transfers(log, acc), logs, default_nasa_log)))


if __name__ == "__main__":
    find_biggest_data_transfer(process_nasa_logs(sys.stdin))
