import requests
import sqlite3
import time
import datetime

API_KEY = '85b6c7a69e371c6820aa44273521292f'

base_url = 'https://api.darksky.net/forecast/{}/{},{}?exclude=hourly,daily,minutely'

def get_city_by_id(city_id):
    try:
        database = sqlite3.connect("data.db")
        cursor = database.cursor()
        sql_select_query = "SELECT * FROM cities where id = ?"
        cursor.execute(sql_select_query, (city_id,))
        cities = cursor.fetchall()

        for city in cities:
            lat = city[2]
            lon = city[3]
            request_url = base_url.format(
                API_KEY,
                lon,
                lat
            )
            data = requests.get(request_url).json()
            # print(data)
            return data


        cursor.close()
        database.close()

    except Exception as e:
        print(e)


def current_weather(city_id):
    result = get_city_by_id(city_id)
    dict = {}
    dict['Time'] = result['currently']['time']
    dict['Summary'] = result['currently']['summary']
    dict['Wind Speed'] = result['currently']['windSpeed']
    dict['Temperature'] = result['currently']['temperature']
    dict['uvIndex'] = result['currently']['uvIndex']
    dict['Visibility'] = result['currently']['visibility']
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    t = datetime.datetime.now()
    minute_count = 0
    delta_minutes = (datetime.datetime.now() - t).seconds / 60
    if delta_minutes and delta_minutes != minute_count:
        cursor.execute("INSERT INTO weather (time, summary, windSpeed, temperature, uvIndex, visibility) VALUES (?, ?, ?, ?, ?, ?);",
            (result['currently']['time'], result['currently']['summary'], result['currently']['windSpeed'],
             result['currently']['temperature'], result['currently']['uvIndex'], result['currently']['visibility']))
        minute_count = delta_minutes
        database.commit()
    time.sleep(60)
    database.close()

    return dict

if __name__ == '__main__':
    city_id = int(input("Enter a city id: "))
    print(current_weather(city_id))
