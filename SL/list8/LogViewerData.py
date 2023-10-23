from typing import List, Dict, Any


class LogViewerData:
    def __init__(self, rows: List[Dict[str, Any]]):
        self.rows = rows

    def filter_data(self, ship_name: str, commander: str, uboat: str, tonnage_min: int, tonnage_max: int) -> List[Dict[str, Any]]:
        filtered_data = [row for row in self.rows if
                         (not ship_name or ship_name.lower() in row['ship_name'].lower()) and
                         (not commander or commander.lower() in row['commander'].lower()) and
                         (not uboat or uboat.lower() in row['uboat'].lower()) and
                         (tonnage_min <= int(row['tonnage'].replace(',', '')) <= tonnage_max)
                         ]
        return filtered_data
