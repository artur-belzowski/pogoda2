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
        return self.get_weather_forecast(key)

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()

    def get_weather_forecast(self, searched_date):
        # wczytanie wynikow z pliku, jeśli istnieją
        try:
            with open("prognoza.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

        # wynik juz zapisany
        if str(searched_date) in self.data:
            return self.data[str(searched_date)]

        url = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"

        # pobieranie danych z API
        resp = requests.get(
            url.format(
                latitude=self.latitude, longitude=self.longitude, searched_date=searched_date
            )
        )
        api_data = resp.json()

        # wydrukuj dane
        if "daily" not in api_data:
            print("Nie ma informacji o opadach dla podanej daty.")
            result = "Nie wiadomo."
        else:
            rain = api_data["daily"]["rain_sum"]
            rain = float(rain[0])
            if rain > 0.0:
                result = "Będzie padać."
            elif rain == 0.0:
                result = "Nie będzie padać."
            else:
                result = "Nie wiem."

        # zapisz wynik zapytania do pliku
        self.data[searched_date.strftime("%Y-%m-%d")] = result
        with open("prognoza.json", "w") as f:
            json.dump(self.data, f)

        return result


latitude = 52.237049
longitude = 21.017532
wf = WeatherForecast(latitude, longitude)

# pobieranie pogody dla konkretnej daty
searched_date_str = input(
    "Podaj datę w formacie RRRR-MM-DD (lub zostaw puste dla daty jutrzejszej): "
)
if searched_date_str == "":
    searched_date = datetime.date.today() + datetime.timedelta(days=1)
else:
    searched_date = datetime.datetime.strptime(searched_date_str, "%Y-%m-%d").date()

result = wf[searched_date]
print("Pogoda dla daty {}: {}".format(searched_date, result))

# zwracanie wszystkich zapisanych rezultatów
print('Dotychczasowe rezultaty: ')
for date, weather in wf.items():
    print(" {}: {}".format(date, weather))

# iterator zwracający wszystkie daty, dla których znana jest pogoda
print('Dostępna pogoda :')
for date in wf:
    print(" -  {}".format(date))
