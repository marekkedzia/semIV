import re
from datetime import datetime

from ssh_log import SSHLogPasswordAccepted, SSHLogPasswordRejected


class SSHUser:
    def __init__(self, username: str, last_login: datetime):
        self.username = username
        self.last_login = last_login

    def validate(self) -> bool:
        valid_username = re.match(r'^[\w-]{1,32}$', self.username)
        return bool(valid_username)


log_entry_1 = SSHLogPasswordRejected(
    timestamp=datetime(2023, 12, 10, 6, 55, 48),
    raw_content="Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2",
    pid=24200,
    hostname="LabSZ"
)

log_entry_2 = SSHLogPasswordAccepted(
    timestamp=datetime(2023, 12, 10, 9, 32, 20),
    raw_content="Accepted password for fztu from 119.137.62.142 port 49116 ssh2",
    pid=24680,
    hostname="LabSZ"
)

user_1 = SSHUser("john_doe", datetime.now())
user_2 = SSHUser("jane_doe", datetime.now())

mixed_list = [log_entry_1, log_entry_2, user_1, user_2]

for item in mixed_list:
    print(f"Item: {item}")
    print(f"Valid: {item.validate()}\n")

