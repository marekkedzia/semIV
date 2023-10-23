import re
import datetime
import sys

nasa_log_length = 5


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
                processed_logs.append(log)
            # else:
            # raise Exception('Line does not meet NASA standards')

        return processed_logs

    return process()


def get_transfer_size(log):
    return log[4]


def get_hour(log):
    date = log[1].split(":")
    hour = int(date[1])
    return hour


def get_http_code(log):
    return log[3]


def get_day(log):
    date = log[1].split()[0]
    converted_date = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S')
    return converted_date.weekday()


def get_country(log):
    host = log[0]
    domain = host.split(".")[-1]
    return domain


def get_image_extension(log):
    def contains_extensions(path):
        return len(path) > 1

    splitted_request_path = log[2].split('.')
    extension = splitted_request_path[1].split(" ")[0] if contains_extensions(splitted_request_path) else None
    return extension


if __name__ == "__main__":
    print(process_nasa_logs(process_nasa_logs(sys.stdin)))
