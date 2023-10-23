from typing import List, Dict


class FilterService:
    def filter_data(self, data: List[Dict[str, str]], ship_name_search_text: str, commander_search_text: str,
                    uboat_search_text: str, tonnage_min: int, tonnage_max: int) -> List[Dict[str, str]]:

        filtered_data = [row for row in data if
                         (not ship_name_search_text or ship_name_search_text in row['ship_name'].lower()) and
                         (not commander_search_text or commander_search_text in row['commander'].lower()) and
                         (not uboat_search_text or uboat_search_text in row['uboat'].lower()) and
                         (tonnage_min <= int(row['tonnage'].replace(',', '')) <= tonnage_max)
                         ]

        return filtered_data
