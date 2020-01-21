import requests
import sqlite3
import csv
import fire
import time

API_KEY = '85b6c7a69e371c6820aa44273521292f'

base_url = 'https://api.darksky.net/forecast/{}/{},{}'


def get_all_information():
    """
    Comment: this does background task which every minute collects information
    and saves into weather table in the database
    """
    database = sqlite3.connect("data.db")
    cursor = database.cursor()
    sql_select_query = "SELECT * FROM cities;"
    cursor.execute(sql_select_query, )
    cities = cursor.fetchall()
    for city in cities:
        lat = city[2]
        lon = city[3]
        request_url = base_url.format(
            API_KEY,
            lat,
            lon
        )
        result = requests.get(request_url).json()
        data = {}
        data['Time'] = result['currently']['time']
        data['Summary'] = result['currently']['summary']
        data['Wind Speed'] = result['currently']['windSpeed']
        data['Temperature'] = result['currently']['temperature']
        data['uvIndex'] = result['currently']['uvIndex']
        data['Visibility'] = result['currently']['visibility']

        cursor.execute(
            "INSERT INTO weather (updated_at, summary, windSpeed, temperature, uvIndex, visibility, city_id) VALUES (?, ?, ?, ?, ?, ?, ?);",
            (result['currently']['time'], result['currently']['summary'], result['currently']['windSpeed'],
             result['currently']['temperature'], result['currently']['uvIndex'], result['currently']['visibility'],
             city[0]))

        database.commit()


def get_weather_by_city_id(city_id):
    """
    Comment: this retrieves weather information for specified city
    :param city_id:
    :return:
    """
    try:
        database = sqlite3.connect("data.db")
        cursor = database.cursor()
        sql_select_query = "SELECT * FROM weather where city_id = ? AND updated_at < DATETIME('now', '-10 minute');"
        cursor.execute(sql_select_query, (city_id,))
        cities_weather = cursor.fetchall()
        database.commit()
        return cities_weather

    except Exception as e:
        return f'Error: {e}'


def convert(fname):
    """
    Comment: this function export all data from weather table into csv file
    :param fname:
    :return:
    """
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


def run():
    while True:
        time.sleep(60)
        get_all_information()


if __name__ == '__main__':
    fire.Fire({
        'run': run,
        'city_id': get_weather_by_city_id,
        'convert': convert
    })
