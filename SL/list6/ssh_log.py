import re
from ipaddress import IPv4Address, AddressValueError
from abc import ABC, abstractmethod


class SSHLogEntry(ABC):
    def __init__(self, timestamp, raw_content, pid, hostname=None):
        self.timestamp = timestamp
        self.hostname = hostname
        self._raw_content = raw_content
        self.pid = pid

    def __str__(self):
        if self.hostname:
            return f"[{self.timestamp}] {self.hostname} (PID: {self.pid}): {self._raw_content}"
        else:
            return f"[{self.timestamp}] (PID: {self.pid}): {self._raw_content}"

    def __repr__(self):
        return f"{self.__class__.__name__}(timestamp='{self.timestamp}', raw_content='{self._raw_content}', pid={self.pid}, hostname='{self.hostname}')"

    def __eq__(self, other):
        return (self.timestamp == other.timestamp and
                self.hostname == other.hostname and
                self._raw_content == other._raw_content and
                self.pid == other.pid)

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __gt__(self, other):
        return self.timestamp > other.timestamp

    def extract_ipv4(self):
        ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        ip_address = re.findall(ip_regex, self._raw_content)[0]
        try:
            return IPv4Address(ip_address)
        except AddressValueError:
            return None

    @property
    def has_ip(self):
        return self.extract_ipv4() is not None

    @abstractmethod
    def validate(self):
        pass


class SSHLogPasswordRejected(SSHLogEntry):
    def __init__(self, timestamp, raw_content, pid, hostname=None, user=None, ip_address=None, port=None):
        super().__init__(timestamp, raw_content, pid, hostname)
        self.user = user
        self.ip_address = ip_address
        self.port = int(port) if port else None

    def validate(self):
        pattern = rf"Failed password for invalid user {re.escape(self.user)} from {re.escape(str(self.ip_address))} port {self.port} ssh2"
        return bool(re.search(pattern, self._raw_content))


class SSHLogPasswordAccepted(SSHLogEntry):
    def __init__(self, timestamp, raw_content, pid, hostname=None, user=None, ip_address=None, port=None):
        super().__init__(timestamp, raw_content, pid, hostname)
        self.user = user
        self.ip_address = ip_address
        self.port = int(port) if port else None

    def validate(self):
        pattern = rf"Accepted password for {re.escape(self.user)} from {re.escape(str(self.ip_address))} port {self.port} ssh2"
        return bool(re.search(pattern, self._raw_content))


class SSHLogError(SSHLogEntry):
    def __init__(self, timestamp, raw_content, pid, hostname=None, error_msg=None, ip_address=None):
        super().__init__(timestamp, raw_content, pid, hostname)
        self.error_msg = error_msg
        self.ip_address = ip_address

    def validate(self):
        pattern = rf"error: {re.escape(self.error_msg)}\[{re.escape(str(self.ip_address))}\]"
        return bool(re.search(pattern, self._raw_content))


class SSHLogOther(SSHLogEntry):
    def validate(self):
        return True
