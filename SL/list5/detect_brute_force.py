import re
import sys
from collections import Counter
from datetime import datetime, timedelta


def get_logs(log_file_path="logs.txt"):
    def find_ip_address(log_message):
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        return re.search(ip_pattern, log_message).group()

    def match_ssh_log(raw_log):
        ssh_log_pattern = r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+(\w+)\[(\d+)\]:\s+(.+)'
        return re.match(ssh_log_pattern, raw_log).groups()

    def convert_to_dict(line):
        keys = ('timestamp', 'hostname', 'process', 'pid', 'message')
        processed_log = dict(zip(keys, match_ssh_log(line)))
        processed_log['ip'] = find_ip_address(processed_log["message"])
        return processed_log

    processed_logs = []
    with open(log_file_path, 'r') as log_file:
        for log in log_file:
            processed_logs.append(convert_to_dict(log))
    return processed_logs


def find_possible_attacks(logs, time_range_in_seconds):
    attacks = []
    last_log_time = "Jan  1 00:00:00"

    def is_in_range(timestamp):
        ssh_format = "%b %d %H:%M:%S"
        max_range = datetime.strptime(last_log_time, ssh_format) + timedelta(seconds=time_range_in_seconds)
        return datetime.strptime(timestamp, ssh_format) < max_range

    def is_failed(message):
        return re.search(r"Failed password", message)

    for log in logs:
        if is_failed(log["message"]):
            if is_in_range(log["timestamp"]):
                attacks[-1]["failed_logins"].append(log)
            else:
                attacks.append({"failed_logins": [log]})
        last_log_time = log["timestamp"]

    return attacks


def find_ip_addresses(logs):
    return [log["ip"] for log in logs]


def get_suspects(ip_addresses, suspects_count=3):
    suspects = []
    ip_counter = Counter(ip_addresses)
    for ip, occurrences in ip_counter.most_common(suspects_count):
        suspects.append({"ip_address": ip, "failed_logins": occurrences})
    return suspects


def is_brute_force(attack, allowed_logins_attempt=3):
    return attack['suspects'][0]['failed_logins'] > allowed_logins_attempt


def detect_brute_force(logs_file_path, time_range_in_seconds=3):
    attacks = find_possible_attacks(get_logs(logs_file_path), time_range_in_seconds)
    for attack in attacks:
        attack["ip_addresses"] = find_ip_addresses(attack["failed_logins"])
        attack["suspects"] = get_suspects(attack["ip_addresses"])
        if is_brute_force(attack):
            print(f"""Próba nieudanego logowania:
                Wszystkie adresy ip: {attack['ip_addresses']}
                Podejrzane adresy ip: {attack['suspects']}
                """)


if __name__ == '__main__':
    detect_brute_force(sys.argv[1])
