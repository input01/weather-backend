import pytest
import requests

def test_suggest():
    r = requests.get("http://localhost/api/weather/suggest/"+"北")
    result = r.json().get("result")
    assert {"value": "北京市", "city_geocode": "110100"} in result
    assert {"value": "北海市", "city_geocode": "450500"} in result

def test_get_weather_by_id():
    r = requests.get("http://localhost/api/weather/info/" + "110100")
    result = r.json().get("result")
    assert result.get("location") is not None
    assert result.get("now").get("temp") is not None

def test_get_weather_by_name():
    r = requests.get("http://localhost/api/weather/info/byname/" + "上海市")
    result = r.json().get("result")
    assert result.get("location") is not None
    assert result.get("now").get("temp") is not None


if __name__ == '__main__':
    pytest.main()
