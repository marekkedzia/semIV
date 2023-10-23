import json
import shutil
import sys
import time
import os

BACKUP_DIR = "./backups"


def save_json_object(file_path, json_object):
    data = []

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

    data.append(json_object)

    with open(file_path, 'w') as file:
        json.dump(data, file)


def create_backup(path, backup_extension='zip'):
    timestamp = int(time.time())

    def get_backup_filename():
        return f"{timestamp}-{path}"

    def create_backup_directory():
        shutil.make_archive(os.path.join(BACKUP_DIR, get_backup_filename()), backup_extension, path)

    def generate_logs_path(logs_file='backup_logs', logs_file_extension='json'):
        return os.path.join(BACKUP_DIR, f"{logs_file}.{logs_file_extension}")

    def create_log():
        log = {
            "timestamp": timestamp,
            "source_directory": os.path.join(os.getcwd(), get_backup_filename()),
            "file_name": f"{get_backup_filename()}.{backup_extension}"
        }
        return {"backup_created": log}

    create_backup_directory()
    save_json_object(generate_logs_path(), create_log())


if __name__ == '__main__':
    args = sys.argv
    create_backup(args[1])
