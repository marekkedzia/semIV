import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

ship_data = []
coordinates_pattern = re.compile(r'\[([-+]?\d+\.\d+),\s*([-+]?\d+\.\d+)\]')

def scrape_ship_data(date):
    url = f'https://uboat.net/allies/merchants/losses_year.html?qdate={date}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'id': 'table2'})

        for row in table.find_all('tr')[2:]:
            cells = row.find_all('td')
            if cells and len(cells) == 9:
                ship_info = {
                    'date': cells[0].text.strip(),
                    'uboat': cells[1].text.strip(),
                    'commander': cells[2].text.strip(),
                    'ship_name': cells[4].text.strip(),
                    'tonnage': cells[5].text.strip(),
                    'nationality': cells[7].text.strip(),
                    'convoy': cells[8].text.strip() if cells[8].text.strip() else "-"
                }
                ship_data.append(ship_info)

        locations = soup.find('script', {'charset': 'utf-8', 'type': 'text/javascript'})
        lines = locations.string.split('\n')

        results = []

        for line in lines:
            if 'var marker =' in line:
                coordinates = coordinates_pattern.findall(line)

                soup = BeautifulSoup(line, 'html.parser')
                strong_tag = soup.find('strong')
                ship_name = strong_tag.text

                results.append({'ship_name': ship_name, 'coordinates': coordinates})
        for result in results:
            for ship_info in ship_data:
                if result['ship_name'] == ship_info['ship_name']:
                    ship_info['coordinates'] = result['coordinates']
                    break
        print(f'Dane zostały dodane dla daty: {date}')
    else:
        print(f'Wystąpił problem z pobraniem danych dla daty: {date}')


start_date = datetime(1939, 9, 1)
end_date = datetime(1945, 5, 31)


delta = timedelta(days=30)

while start_date <= end_date:
    date_str = start_date.strftime("%Y-%m")
    scrape_ship_data(date_str)
    start_date += delta

df = pd.DataFrame(ship_data)
df.to_csv('sunk_ships_data.csv', index=False, encoding='utf-8')

print('Dane zostały zapisane do pliku sunk_ships_data.csv.')
