import sys

from read_log import process_nasa_logs, get_http_code


def get_entries_by_status(log_list, http_code):
    def validate(): return 100 <= http_code < 1000
    if not validate():
        raise Exception("Http code must be an integer from range 100-999")
    try:
        filtered_list = filter(lambda log: get_http_code(log) == http_code, log_list)
        return list(filtered_list)
    except IndexError:
        print("Cannot filter provided list. Action cannot be executed, list wasn't filtered")
        return filtered_list


if __name__ == "__main__":
    not_found_http_status = 404
    print(get_entries_by_status(process_nasa_logs(sys.stdin), not_found_http_status))
