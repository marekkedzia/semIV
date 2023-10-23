from typing import Callable, List, Iterator

from ssh_log import SSHLogEntry


class SSHLogJournal:
    def __init__(self) -> None:
        self._log_entries: List[SSHLogEntry] = []

    def __len__(self) -> int:
        return len(self._log_entries)

    def __iter__(self) -> Iterator[SSHLogEntry]:
        return iter(self._log_entries)

    def __contains__(self, entry: SSHLogEntry) -> bool:
        return entry in self._log_entries

    def append(self, entry: SSHLogEntry) -> None:
        if entry and entry.validate():
            self._log_entries.append(entry)

    def filter_by_criteria(self, criteria: Callable[[SSHLogEntry], bool]) -> List[SSHLogEntry]:
        return list(filter(criteria, self._log_entries))
