import datetime


def entry_to_dict(entry):
    keys = ['ip', 'datetime', 'request', 'status_code', 'size']
    return dict(zip(keys, entry))


if __name__ == '__main__':
    dummy_log = ('dynip42.efn.org', datetime.datetime(1995, 7, 1, 0, 2, 28), 'GET /icons/text.xbm HTTP/1.0', 200, 527)
    print(entry_to_dict(dummy_log))
