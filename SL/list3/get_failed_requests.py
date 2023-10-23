import sys
from read_log import get_http_code, process_nasa_logs


def get_failed_requests(logs, store_in_one_list=True):
    def is_failed(request):
        return get_http_code(request) > 400

    def is_server_error(request):
        return get_http_code(request) > 500

    def is_client_error(request):
        return 400 < get_http_code(request) < 500

    if store_in_one_list:
        return list(filter(lambda request: is_failed(request), logs))
    else:
        errors = {
            "client_errors": [],
            "server_errors": []
        }
        for log in logs:
            if is_client_error(log):
                errors["client_errors"].append(log)
            elif is_server_error(log):
                errors["server_errors"].append(log)
        return errors


if __name__ == "__main__":
    print(get_failed_requests(process_nasa_logs(sys.stdin), False)["server_errors"])
