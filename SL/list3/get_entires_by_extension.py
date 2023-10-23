import sys

from read_log import process_nasa_logs


def get_image_extension(log):
    def contains_extensions(path):
        return len(path) > 1

    splitted_request_path = log[2].split('.')
    extension = splitted_request_path[1].split(" ")[0] if contains_extensions(splitted_request_path) else None
    return extension


def get_entries_by_extension(log_list, extension):
    return list(filter(lambda log: get_image_extension(log) == extension, log_list))


if __name__ == "__main__":
    jpg_extension = "jpg"
    print(get_entries_by_extension(process_nasa_logs(sys.stdin), jpg_extension))
