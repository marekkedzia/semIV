import requests

url = "https://api.coindesk.com/v1/bpi/currentprice.json" # przykładowy URL dla API z informacjami o cenach Bitcoin

response = requests.get(url) # wysłanie zapytania GET

if response.status_code == 200: # sprawdzenie, czy odpowiedź jest poprawna
    data = response.json() # pobranie danych z odpowiedzi w formacie JSON
    print(data) # wyświetlenie danych w konsoli
else:
    print("Nie udało się pobrać danych z API.") # wyświetlenie informacji o błędzie, jeśli odpowiedź jest niepoprawna
