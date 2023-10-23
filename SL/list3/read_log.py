import re
import datetime
import sys

nasa_log_length = 5
nasa_no_transfer_code = "-"


def process_nasa_logs(file):
    def process_nasa_log(line):
        properties = re.match(r"(.+) - - \[(.+) \"(.+)\" (.+) (.+)", line)
        return properties.groups() if properties else []

    def is_nasa_log(log):
        return len(log) == nasa_log_length

    def process():
        processed_logs = []
        for raw_log in file:
            log = process_nasa_log(raw_log)
            if is_nasa_log(log):
                processed_logs.append(
                    (get_ip_address(log), get_date(log), get_request_path(log), get_http_code(log),
                     get_transfer_size(log)
                     ))
            # else:
            # raise Exception('Line does not meet NASA standards')

        return processed_logs

    return process()


def get_ip_address(log):
    return log[0]


def get_date(log):
    date = log[1].split()[0]
    converted_date = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S')
    return converted_date


def get_request_path(log):
    return log[2]


def get_http_code(log):
    return int(log[3])


def get_transfer_size(log):
    return int(log[4]) if log[4] != nasa_no_transfer_code else 0


if __name__ == "__main__":
    print(process_nasa_logs(sys.stdin))
