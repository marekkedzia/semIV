import sys
from functools import reduce
from process_nasa_logs import get_transfer_size, process_nasa_logs

nasa_no_transfer_code = '-'
default_nasa_log = ["No NASA log with any transfer found", "-", "-", "-", "0"]


def find_total_data_transfer_in_gb(logs):
    def convert_b_to_gb(number):
        return number / 1024 * 1024 * 1024

    total_b_number = reduce(lambda acc, log: acc + (
        int(get_transfer_size(log)) if get_transfer_size(
            log) != nasa_no_transfer_code else 0), logs,
                            0)
    print('Data transfer: ' + str(convert_b_to_gb(total_b_number)) + ' GB')


if __name__ == "__main__":
    find_total_data_transfer_in_gb(process_nasa_logs(sys.stdin))
