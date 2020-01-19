import sqlite3
import daemon

def get_all_information():
    try:
        database = sqlite3.connect("data.db")
        cursor = database.cursor()
        sql_select_query = "SELECT * FROM weather"
        cursor.execute(sql_select_query,)
        cities = cursor.fetchall()
        cursor.close()
        database.close()

        return cities
    except Exception as e:
        print(e)

def run():
    with daemon.DaemonContext():
        print(get_all_information())

if __name__ == '__main__':
    run()