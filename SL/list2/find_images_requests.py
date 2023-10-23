import sys
from functools import reduce
from process_nasa_logs import process_nasa_logs

supported_image_extensions = ['gif', 'jpg', 'jpeg', 'xbm']


def is_image_request(log):
    return process_nasa_logs.get_image_extension(log) in supported_image_extensions


def compare_counts(images_requests_count, overall_count):
    print("Images requests represent " + str(images_requests_count / overall_count * 100) + "% of all requests(" + str(
        images_requests_count) + "/" + str(overall_count) + ")")


def find_images_requests_count(logs):
    return reduce(lambda acc, log: acc + 1 if is_image_request(log) else acc, logs, 0)


if __name__ == "__main__":
    find_images_requests_count(process_nasa_logs(sys.stdin))

