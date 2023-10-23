import logging
import sys

from zad2 import get_event_type
from zad1 import process_ssh_logs

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)
    ]
)


def process_log_line(log_line):
    bytes_read = len(log_line)
    logging.debug(f"Przeczytano {bytes_read} bajtów")

    message_type = get_event_type(log_line)

    log_actions = {
        "udane logowanie": logging.info,
        "zamknięcie połączenia": logging.info,
        "nieudane logowanie": logging.warning,
        "błędne hasło": logging.error,
        "błędna nazwa użytkownika": logging.error,
        "próba włamania": logging.critical,
    }

    action = log_actions.get(message_type, logging.debug)
    action(f"{message_type}: {log_line}")


if __name__ == '__main__':
    process_ssh_logs(process_func=process_log_line)

