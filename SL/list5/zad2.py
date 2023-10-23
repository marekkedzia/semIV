import re
import sys


def match_ssh_log(log):
    ssh_log_pattern = r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+(\w+)\[(\d+)\]:\s+(.+)'
    return re.match(ssh_log_pattern, log).groups()


def convert_to_tuple(line):
    return match_ssh_log(line)[1:6]


def convert_to_dict(line):
    keys = ('timestamp', 'hostname', 'process', 'pid', 'message')
    return dict(zip(keys, match_ssh_log(line)))


def filter_logs(log_file_path, reducer_func):
    with open(log_file_path, 'r') as log_file:
        filtered_outcome = []

        for log in log_file:
            filtered_outcome.append(reducer_func(log))

    return filtered_outcome


def get_ipv4_from_logs(logs_file_path):
    ipv4_pattern = re.compile(
        r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')

    def reduce_by_ipv4(log):
        match = ipv4_pattern.search(log)
        return match.group() if match else None

    return filter_logs(logs_file_path, reduce_by_ipv4)


def get_user_from_logs(logs_file_path):
    user_pattern = re.compile(r'User (\w+)')

    def reduce_by_user(log):
        match = user_pattern.search(log)
        return match.group(1) if match else None

    return filter_logs(logs_file_path, reduce_by_user)


def get_event_type(log):
    unrecognised_event_code = "inne"

    event_types = {
        "udane logowanie": r"User (\w+) logged in",
        "nieudane logowanie": r"Failed password for",
        "zamknięcie połączenia": r"Connection closed by",
        "błędne hasło": r"Invalid password for",
        "błędna nazwa użytkownika": r"Invalid user (\w+)",
        "próba włamania": r"Possible break-in attempt"
    }

    for message_type, pattern in event_types.items():
        if re.search(pattern, log):
            return message_type

    return unrecognised_event_code


def get_events_type(logs_file_path):
    return filter_logs(logs_file_path, get_event_type)


def get_logs(log_file_path="logs.txt"):
    with open(log_file_path, 'r') as log_file:
        return log_file.readlines()


if __name__ == '__main__':
    print(get_ipv4_from_logs(sys.argv[1]))
    print(get_user_from_logs(sys.argv[1]))
    print(get_events_type(sys.argv[1]))
