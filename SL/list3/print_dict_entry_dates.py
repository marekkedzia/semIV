import sys
from functools import reduce

from log_to_dict import log_to_dict
from read_log import process_nasa_logs


def print_dict_entry_dates(dictionary):
    def has_ok_status(log):
        return log["status code"] == 200

    for addr, logs in dictionary.items():
        requests = len(logs)
        first_request = logs[0]["datetime"]
        last_request = logs[-1]["datetime"]
        successful_requests = reduce(lambda acc, log: acc + 1 if has_ok_status(log) else acc, logs, 0)

        successful_request_ratio = successful_requests / requests if requests != 0 else 0

        print("Address: {}".format(addr))
        print("Number of requests: {}".format(requests))
        print("First request date: {}".format(first_request))
        print("Last request date: {}".format(last_request))
        print("Successful request ratio: {:.2f}%".format(successful_request_ratio * 100))
        print()


if __name__ == '__main__':
    print(print_dict_entry_dates(log_to_dict(process_nasa_logs(sys.stdin))))
