## Weather Information from Dark Sky

This is a script to collect weather information from Dark Sky https://darksky.net/dev

In order to run this script firstly clone your own system with this url

```
https://github.com/goaziz/weather_data.git
```

The next step: create virtual environment in your working space by this command ``python3.x -m venv venv`` then install all dependencies from `pip install -r requirements.txt` file.

Now you're all set. This is the useful commands to run the script

```
python main.py run &
```
this command does background task where data is collected and saved into the database every 1 minute

```
python main.py city_id id
```

this command collects weather information for the specified city which you should enter from 1 to 5 numbers instead of id  

```
python main.py convert cities.csv
```

this exports all weather table information to csv