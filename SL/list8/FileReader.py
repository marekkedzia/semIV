import csv
from typing import List, Dict


class CSVReaderService:
    def read_csv(self, file_name: str) -> List[Dict[str, str]]:
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
        return data
