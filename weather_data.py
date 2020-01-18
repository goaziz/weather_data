import requests, sqlite3



API_KEY = '85b6c7a69e371c6820aa44273521292f'

base_url = 'https://api.darksky.net/forecast/{}/{},{}?exclude=hourly,daily,minutely'

lat = input('Enter latitude: ')
lon = input('Enter longitude: ')

final_url = base_url.format(
    API_KEY,
    lat,
    lon
)

database = sqlite3.connect("data.db")
cursor = database.cursor()
cursor.execute('DROP TABLE IF EXISTS weather')

cursor.execute("CREATE TABLE weather (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  time TIMESTAMP, summary VARCHAR,"
               "windSpeed FLOAT, temperature FLOAT, uvIndex INTEGER, visibility FLOAT);")

data = requests.get(final_url).json()

# time, summary, windSpeed, temperature, uvIndex, visibility
if data:
    time = data['currently']['time']
    summary = data['currently']['summary']
    wind_speed = data['currently']['windSpeed']
    temp = data['currently']['temperature']
    uv_index = data['currently']['uvIndex']
    visibility = data['currently']['visibility']

    cursor.execute("INSERT INTO weather (time, summary, windSpeed, temperature, uvIndex, visibility) VALUES (?, ?, ?, ?, ?, ?);",
                   (time, summary, wind_speed, temp, uv_index, visibility))
    database.commit()
    database.close()

    print("Time: {}\nSummary: {}\nwindSpeed: {}\nTemperature: {}\nuvIndex: {}\nVisibility: {}".format(
        time, summary, wind_speed, temp, uv_index, visibility
    ))
else:
    print("City not found")