import sys

from filter_by_country import filter_by_pl_domain
from filter_by_day import filter_by_friday
from filter_by_hour import filter_from_22_to_6
from filter_by_status import filter_by_ok_status
from find_biggest_data_transfer import find_biggest_data_transfer
from find_data_transfer import find_total_data_transfer_in_gb
from find_http_occurrences import find_200_status_occurrences, find_302_status_occurrences, find_404_status_occurrences
from find_images_requests import find_images_requests_count

if __name__ == "__main__":
    filter_by_pl_domain(sys.stdin)
    filter_by_friday(sys.stdin)
    filter_from_22_to_6(sys.stdin)
    filter_by_ok_status(sys.stdin)
    find_biggest_data_transfer(sys.stdin)
    find_total_data_transfer_in_gb(sys.stdin)
    find_404_status_occurrences(sys.stdin)
    find_200_status_occurrences(sys.stdin)
    find_302_status_occurrences(sys.stdin)
    find_images_requests_count(sys.stdin)

# cat NASA | python filter_by_day.py | python filter_by_country.py
