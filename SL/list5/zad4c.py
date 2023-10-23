from zad2 import get_user_from_logs


def find_max_logins_username(logs_file_path):
    users = get_user_from_logs(logs_file_path)
    return max(users)

def find_min_logins_username(logs_file_path):
    users = get_user_from_logs(logs_file_path)
    return min(users)


if __name__ == '__main__':
    print(find_min_logins_username("logs.txt"))
    print(find_max_logins_username("logs.txt"))
