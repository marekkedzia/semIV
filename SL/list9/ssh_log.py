import re
from ipaddress import IPv4Address, AddressValueError
from abc import ABC, abstractmethod
from typing import Optional, Union


class SSHLogEntry(ABC):
    def __init__(self, timestamp: str, raw_content: str, pid: int, hostname: Optional[str] = None) -> None:
        self.timestamp: str = timestamp
        self.hostname: Optional[str] = hostname
        self._raw_content: str = raw_content
        self.pid: int = pid

    def __str__(self) -> str:
        if self.hostname:
            return f"[{self.timestamp}] {self.hostname} (PID: {self.pid}): {self._raw_content}"
        else:
            return f"[{self.timestamp}] (PID: {self.pid}): {self._raw_content}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(timestamp='{self.timestamp}', raw_content='{self._raw_content}', pid={self.pid}, hostname='{self.hostname}')"

    def __eq__(self, other: 'SSHLogEntry') -> bool:
        return (self.timestamp == other.timestamp and
                self.hostname == other.hostname and
                self._raw_content == other._raw_content and
                self.pid == other.pid)

    def __lt__(self, other: 'SSHLogEntry') -> bool:
        return self.timestamp < other.timestamp

    def __gt__(self, other: 'SSHLogEntry') -> bool:
        return self.timestamp > other.timestamp

    def extract_ipv4(self) -> Optional[IPv4Address]:
        ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        ip_address = re.findall(ip_regex, self._raw_content)[0]
        try:
            return IPv4Address(ip_address)
        except AddressValueError:
            return None

    @property
    def has_ip(self) -> bool:
        return self.extract_ipv4() is not None

    @abstractmethod
    def validate(self) -> bool:
        pass


class SSHLogPasswordRejected(SSHLogEntry):
    def __init__(self, timestamp: str, raw_content: str, pid: int, hostname: Optional[str] = None,
                 user: Optional[str] = None, ip_address: Optional[Union[str, IPv4Address]] = None,
                 port: Optional[Union[str, int]] = None) -> None:
        super().__init__(timestamp, raw_content, pid, hostname)
        self.user: Optional[str] = user
        self.ip_address: Optional[Union[str, IPv4Address]] = ip_address
        self.port: Optional[int] = int(port) if port else None

    def validate(self) -> bool:
        pattern = rf"Failed password for invalid user {re.escape(self.user)} from {re.escape(str(self.ip_address))} port {self.port} ssh2"
        return bool(re.search(pattern, self._raw_content))


class SSHLogPasswordAccepted(SSHLogEntry):
    def __init__(self, timestamp: str, raw_content: str, pid: int, hostname: Optional[str] = None,
                 user: Optional[str] = None, ip_address: Optional[Union[str, IPv4Address]] = None,
                 port: Optional[Union[str, int]] = None) -> None:
        super().__init__(timestamp, raw_content, pid, hostname)
        self.user: Optional[str] = user
        self.ip_address: Optional[Union[str, IPv4Address]] = ip_address
        self.port: Optional[int] = int(port) if port else None

    def validate(self) -> bool:
        pattern = rf"Accepted password for {re.escape(self.user)} from {re.escape(str(self.ip_address))} port {self.port} ssh2"
        return bool(re.search(pattern, self._raw_content))

class SSHLogError(SSHLogEntry):
    def __init__(self, timestamp: str, raw_content: str, pid: int, hostname: Optional[str] = None,
                 error_msg: Optional[str] = None, ip_address: Optional[Union[str, IPv4Address]] = None) -> None:
        super().__init__(timestamp, raw_content, pid, hostname)
        self.error_msg: Optional[str] = error_msg
        self.ip_address: Optional[Union[str, IPv4Address]] = ip_address

    def validate(self) -> bool:
        pattern = rf"error: {re.escape(self.error_msg)}\[{re.escape(str(self.ip_address))}\]"
        return bool(re.search(pattern, self._raw_content))


class SSHLogOther(SSHLogEntry):
    def extract_ipv4(self) -> Optional[IPv4Address]:
        ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        ip_addresses = re.findall(ip_regex, self._raw_content)
        if ip_addresses:
            return IPv4Address(ip_addresses[0])
        else:
            return None

    def validate(self) -> bool:
        return True  # Assuming all other logs are valid

