from typing import List, Dict


class StatisticsService:
    def calculate_statistics(self, table_data: List[Dict[str, str]]) -> Dict[str, str]:
        total_ships = len(table_data)
        total_tonnage = 0
        nationality_count = {}
        uboat_count = {}
        commander_count = {}

        for row in table_data:
            tonnage = int(row['tonnage'].replace(',', ''))
            total_tonnage += tonnage

            nationality = row['nationality']
            if nationality in nationality_count:
                nationality_count[nationality] += 1
            else:
                nationality_count[nationality] = 1

            uboat = row['uboat']
            if uboat in uboat_count:
                uboat_count[uboat] += 1
            else:
                uboat_count[uboat] = 1

            commander = row['commander']
            if commander in commander_count:
                commander_count[commander] += 1
            else:
                commander_count[commander] = 1

        most_common_nationality = max(nationality_count, key=nationality_count.get) if nationality_count else None
        most_common_uboat = max(uboat_count, key=uboat_count.get) if uboat_count else None
        most_common_commander = max(commander_count, key=commander_count.get) if commander_count else None

        return {
            "total_ships": total_ships,
            "total_tonnage": total_tonnage,
            "most_common_nationality": most_common_nationality,
            "nationality_count": nationality_count.get(most_common_nationality, 0),
            "most_common_uboat": most_common_uboat,
            "uboat_count": uboat_count.get(most_common_uboat, 0),
            "most_common_commander": most_common_commander,
            "commander_count": commander_count.get(most_common_commander, 0)
        }
