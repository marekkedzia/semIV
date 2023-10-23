import sys

from read_log import process_nasa_logs, get_ip_address


def get_entries_by_addr(log_list, ip_addr):
    try:
        filtered_list = filter(lambda log: get_ip_address(log) == ip_addr, log_list)
        return list(filtered_list)
    except IndexError:
        print("Cannot filter provided list. Action cannot be executed, list wasn't filtered")
        return filtered_list


if __name__ == "__main__":
    default_ip_address = "lmsmith.tezcat.com"
    print(get_entries_by_addr(process_nasa_logs(sys.stdin), default_ip_address))
