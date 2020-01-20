import requests
import sqlite3
import csv
import daemon
import fire
import time
import datetime

API_KEY = '85b6c7a69e371c6820aa44273521292f'

base_url = 'https://api.darksky.net/forecast/{}/{},{}?exclude=hourly,daily,minutely'


# def get_all_information():
#     try:
#         database = sqlite3.connect("data.db")
#         cursor = database.cursor()
#         sql_select_query = "SELECT * FROM weather;"
#         cursor.execute(sql_select_query, )
#         cities = cursor.fetchall()
#         cursor.close()
#         database.close()
#
#         return cities
#     except Exception as e:
#         print(e)


def get_city_by_id(city_id):
    try:
        database = sqlite3.connect("data.db")
        cursor = database.cursor()
        sql_select_query = "SELECT * FROM cities where id = ?;"
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
            return data

        cursor.close()
        database.close()

    except Exception as e:
        print(e)


def current_weather(city_id):
    result = get_city_by_id(city_id)
    data = {}
    data['Time'] = result['currently']['time']
    data['Summary'] = result['currently']['summary']
    data['Wind Speed'] = result['currently']['windSpeed']
    data['Temperature'] = result['currently']['temperature']
    data['uvIndex'] = result['currently']['uvIndex']
    data['Visibility'] = result['currently']['visibility']
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO weather (time, summary, windSpeed, temperature, uvIndex, visibility) VALUES (?, ?, ?, ?, ?, ?);",
        (result['currently']['time'], result['currently']['summary'], result['currently']['windSpeed'],
         result['currently']['temperature'], result['currently']['uvIndex'], result['currently']['visibility']))
    database.commit()
    database.close()

    return data


def convert(fname):
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM weather;")

    if fname.endswith('.csv'):
        with open(fname, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([i[0] for i in cursor.description])
            for data in cursor:
                writer.writerow(data)
            database.close()
        return fname
    return f'{fname} is not expected file type. Try with csv please!'


# def run():
#     with daemon.DaemonContext():
#         print(get_all_information())


if __name__ == '__main__':
    # run()
    fire.Fire({
        'current': current_weather,
        'convert': convert,
    })
