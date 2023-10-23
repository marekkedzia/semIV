import json
import os
import sys
import zipfile

BACKUP_DIR = "./backups"
DEFAULT_RESTORE_LOCATION = './restored'


def set_path_to_restore():
    args = sys.argv
    if len(args) <= 1:
        return DEFAULT_RESTORE_LOCATION
    else:
        return args[1]


PATH_TO_RESTORE = set_path_to_restore()


def restore_file(backup_path):
    with zipfile.ZipFile(backup_path, 'r') as zip_ref:
        zip_ref.extractall(PATH_TO_RESTORE)
    print(f'Restored backup: {backup_path}')


def restore_directory(logs_file='backup_logs', logs_file_extension='json'):
    def generate_backup_path(file):
        return os.path.join(BACKUP_DIR, file)

    def get_logs(file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def print_logs(logs):
        numerated_logs = {}
        for log_number, log in enumerate(logs, start=1):
            numerated_logs[log_number] = log["backup_created"]
            print(f"{log_number}. {log}")
        return numerated_logs

    logs = get_logs(generate_backup_path(f"{logs_file}.{logs_file_extension}"))
    logs = print_logs(logs)
    file_index = int(input('Choose backup number to restore: '))
    restore_file(os.path.join(BACKUP_DIR, logs[file_index]["file_name"]))


if __name__ == '__main__':
    args = sys.argv
    restore_directory()
