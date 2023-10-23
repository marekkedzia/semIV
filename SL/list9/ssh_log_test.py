import pytest
from ipaddress import IPv4Address
from ssh_log import SSHLogEntry, SSHLogPasswordRejected, SSHLogPasswordAccepted, SSHLogError, SSHLogOther
from ssh_log_journal import SSHLogJournal


# test weryfikujący poprawność ekstrakcji czasu tworzonego obiektu klasy SSHLogEntry
def test_ssh_log_other_timestamp():
    log_entry = SSHLogOther("Dec 10 06:55:48", "raw_content", 24200)
    assert log_entry.timestamp == "Dec 10 06:55:48"

# testy weryfikujące poprawność ekstrakcji adresu IPv4
def test_ssh_log_other_valid_ipv4_extraction():
    log_entry = SSHLogOther("Dec 10 06:55:48", "Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2", 24200)
    assert log_entry.extract_ipv4() == IPv4Address('173.234.31.186')

def test_ssh_log_other_invalid_ipv4_extraction():
    log_entry = SSHLogOther("Dec 10 06:55:48", "Failed password for invalid user webmaster from 666.777.88.213 port 38926 ssh2", 24200)
    assert log_entry.extract_ipv4() is None

def test_ssh_log_other_no_ipv4_extraction():
    log_entry = SSHLogOther("Dec 10 06:55:48", "Failed password for invalid user webmaster from port 38926 ssh2", 24200)
    assert log_entry.extract_ipv4() is None

@pytest.mark.parametrize("log_entry_type, args", [
    (SSHLogPasswordRejected, ["Dec 10 06:55:48", "Failed password for invalid user user from 192.0.2.0 port 22 ssh2", 24200, "user", "192.0.2.0", 22]),
    (SSHLogPasswordAccepted, ["Dec 10 06:55:48", "Accepted password for user from 192.0.2.0 port 22 ssh2", 24200, "user", "192.0.2.0", 22]),
    (SSHLogError, ["Dec 10 06:55:48", "error_msg", 24200, "error_msg", "192.0.2.0"]),
    (SSHLogOther, ["Dec 10 06:55:48", "raw_content", 24200])
])
def test_ssh_journal_append(log_entry_type, args):
    journal = SSHLogJournal()
    log_entry = log_entry_type(*args)
    journal.append(log_entry)
    assert len(journal) > 0
    assert isinstance(journal._log_entries[0], log_entry_type)