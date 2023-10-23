import re
import statistics
from datetime import datetime


def parse_log_line(line):
    start_pattern = r'session opened for user'
    end_pattern = r'session closed for user'
    timestamp_pattern = r'\w{3} \d{1,2} \d{2}:\d{2}:\d{2}'

    start_match = re.search(start_pattern, line)
    end_match = re.search(end_pattern, line)
    timestamp_match = re.search(timestamp_pattern, line)

    return start_match, end_match, timestamp_match


def update_start_times(start_times, line, timestamp_match):
    user = line.split()[-1]
    timestamp = datetime.strptime(timestamp_match.group(), '%b %d %H:%M:%S')
    start_times[user] = timestamp


def update_durations(start_times, durations, line, timestamp_match):
    user = line.split()[-1]
    timestamp = datetime.strptime(timestamp_match.group(), '%b %d %H:%M:%S')
    if user in start_times:
        duration = (timestamp - start_times[user]).total_seconds()
        durations.append(duration)
        del start_times[user]


def calculate_duration_and_std(log_file):
    start_times = {}
    durations = []

    with open(log_file, 'r') as file:
        for line in file:
            start_match, end_match, timestamp_match = parse_log_line(line)

            if start_match and timestamp_match:
                update_start_times(start_times, line, timestamp_match)
            elif end_match and timestamp_match:
                update_durations(start_times, durations, line, timestamp_match)

    avg_duration = statistics.mean(durations)
    std_dev = statistics.stdev(durations)

    return avg_duration, std_dev


log_file = "logs.txt"
avg_duration, std_dev = calculate_duration_and_std(log_file)

print(f"Średni czas trwania: {avg_duration} sekund")
print(f"Odchylenie standardowe: {std_dev} sekund")
