import sys


def print_entries(logs):
    for log in logs:
        print(log)


if __name__ == "__main__":
    print_entries(sys.stdin)
