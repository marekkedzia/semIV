import random
import re
import sys

from zad2 import get_user_from_logs, get_logs


def get_random_logs(logs_count, logs):
    if logs_count > len(logs):
        return logs
    return random.sample(logs, logs_count)


def get_random_user(users):
    if not users:
        raise ValueError("List cannot be empty")
    return random.choice(users)


def get_logs_for_user(user, logs_file_path):
    logs = get_logs(logs_file_path)
    user_pattern = re.compile(rf"User {user}\b")
    return [log for log in logs if user_pattern.search(log)]


def get_logs_for_random_users(logs_file_path, logs_count=2):
    user = get_random_user(get_user_from_logs(logs_file_path))
    logs = get_logs_for_user(user, logs_file_path)
    return get_random_logs(logs_count, logs)


if __name__ == '__main__':
    print(get_logs_for_random_users(sys.argv[1]))

