def process_ssh_logs(process_func=print, log_file_path='logs.txt'):
    def process_log(process, log):
        process(log)

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            process_log(process_func, line)


if __name__ == '__main__':
    process_ssh_logs()
