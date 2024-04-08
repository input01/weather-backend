from apiflask import APIFlask
from flask import abort
import requests
import csv
from logging.config import dictConfig
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = APIFlask(__name__, docs_ui='swagger-ui')
city_geocode_map = {}
with open('weather_district_id.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        city_geocode_map.setdefault(row['city'], row['city_geocode'])
app.logger.info('baidu city geocode csv dic load OK')
app.logger.debug(city_geocode_map)


@app.get("/api/weather/suggest/<city>")
def weather_suggest(city):
    result = []
    for (city_name, city_geocode) in city_geocode_map.items():
        if city in city_name:
            result.append({"value": city_name, "city_geocode": city_geocode})
    return {'status': 0, 'message': 'success', 'result': result}


@app.get("/api/weather/info/<district_id>")
def weather_info(district_id):
    url = "https://api.map.baidu.com/weather/v1/"
    ak = "dxeW95iEqktXPSy964HwJZfzVMzDRN7q"
    params = {
        "district_id": district_id,
        "data_type": "now",
        "ak": ak,
    }
    response = requests.get(url=url, params=params)
    return response.json()


@app.get("/api/weather/info/byname/<city>")
def weather_info_byname(city):
    url = "https://api.map.baidu.com/weather/v1/"
    ak = "dxeW95iEqktXPSy964HwJZfzVMzDRN7q"
    params = {
        "district_id": city_geocode_map.get(city),
        "data_type": "now",
        "ak": ak,
    }
    response = requests.get(url=url, params=params)
    return response.json()


if __name__ == '__main__':
    app.run(port=80, debug=True)
