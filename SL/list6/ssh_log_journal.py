from typing import Callable, List

from ssh_log import SSHLogEntry


class SSHLogJournal:
    def __init__(self):
        self._log_entries = []

    def __len__(self):
        return len(self._log_entries)

    def __iter__(self):
        return iter(self._log_entries)

    def __contains__(self, entry: SSHLogEntry):
        return entry in self._log_entries

    def append(self, entry: SSHLogEntry):
        if entry and entry.validate():
            self._log_entries.append(entry)

    def filter_by_criteria(self, criteria: Callable[[SSHLogEntry], bool]) -> List[SSHLogEntry]:
        return list(filter(criteria, self._log_entries))
