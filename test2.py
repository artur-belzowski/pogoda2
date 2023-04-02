import json
import requests
import datetime

class WeatherForecast:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()

    def get_weather_forecast(self, searched_date):
        searched_date = datetime.datetime.strptime(searched_date, '%Y-%m-%d').date()

        # wczytanie wynikow z pliku, jeśli istnieją
        try:
            with open('prognoza.json', 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = self.data.get(key, {})


        # wynik juz zapisany
        if str(searched_date) in self.data:
            print("Wynik dla daty", searched_date, "został już pobrany:")
            print("Opady deszczu:", self.data[str(searched_date)])
            return


        url = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"

        # pobieranie danych z API
        resp = requests.get(url.format(latitude=self.latitude, longitude=self.longitude, searched_date=searched_date))
        api_data = resp.json()

        # wydrukuj dane
        if 'daily' not in api_data:
            print("Nie ma informacji o opadach dla podanej daty.")
            result = "Nie wiadomo."
        else:
            rain = api_data['daily']['rain_sum']
            rain = float(rain[0])
            if rain > 0.0:
                print("Będzie padać.")
                result = "Będzie padać."
            elif rain == 0.0:
                print("Nie będzie padać.")
                result = "Nie będzie padać."

        # zapisz wynik zapytania do pliku
        self.data[searched_date.strftime('%Y-%m-%d')] = result
        with open('prognoza.json', 'w') as f:
            json.dump(self.data, f)


latitude = 52.237049
longitude = 21.017532
wf = WeatherForecast(latitude, longitude)

# pobieranie pogody dla konkretnej daty
searched_date_str = input("Podaj datę w formacie RRRR-MM-DD (lub zostaw puste dla daty jutrzejszej): ")
if searched_date_str == "":
    searched_date = datetime.date.today() + datetime.timedelta(days=1)
else:
    searched_date = datetime.datetime.strptime(searched_date_str, '%Y-%m-%d').date()
result = wf[searched_date]
print("Pogoda dla daty {}: {}".format(searched_date, result))

# zwracanie wszystkich zapisanych rezultatów
for date, weather in wf.items():
    print("Pogoda dla daty {}: {}".format(date, weather))

# iterator zwracający wszystkie daty, dla których znana jest pogoda
for date in wf:
    print("Dostępna pogoda dla daty: {}".format(date))
