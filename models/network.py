import requests
from urllib.parse import quote
from datetime import datetime


def get_coordinates(city: str):
    try:
        safe_city = quote(city.strip())
        geo_url = f"http://geocoding-api.open-meteo.com/v1/search?name={safe_city}&count=1&language=ru&format=json"

        geo_res = requests.get(geo_url, timeout=10).json()
        results = geo_res.get('results')
        if not results: return None

        loc = results[0]
        return loc['latitude'], loc['longitude'], loc['name']
    except Exception as e:
        print(f"Ошибка Geocoding: {e}")
        return None


def get_air_data(lat: float, lon: float, start_date=None, end_date=None):
    try:
        aq_url = (
            f"http://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={lat}&longitude={lon}&hourly=pm10,pm2_5,nitrogen_dioxide,carbon_monoxide&timezone=auto"
        )
        if start_date and end_date:
            aq_url += f"&start_date={start_date}&end_date={end_date}"

        res = requests.get(aq_url, timeout=10).json()
        h = res.get('hourly', {})

        measurements = []
        now = datetime.now()

        for i in range(len(h.get('time', []))):
            dt = datetime.fromisoformat(h['time'][i])
            if dt > now: continue

            measurements.append({
                "date": dt.strftime("%d-%m-%Y %H:%M"),
                "pm10": h['pm10'][i] if h['pm10'][i] is not None else 0,
                "pm25": h['pm2_5'][i] if h['pm2_5'][i] is not None else 0,
                "no2": h['nitrogen_dioxide'][i] if h['nitrogen_dioxide'][i] is not None else 0,
                "co": h['carbon_monoxide'][i] if h['carbon_monoxide'][i] is not None else 0,
            })
        return measurements
    except Exception as e:
        print(f"Ошибка Air API: {e}")
        return []


def fetch_air_quality(city: str, start_date=None, end_date=None):
    warnings = []
    coords = get_coordinates(city)
    if not coords:
        warnings.append(f"Город '{city}' не найден")
        return [], warnings

    lat, lon, city_name = coords
    if start_date and not end_date:
        end_date = start_date

    raw_list = get_air_data(lat, lon, start_date, end_date)
    if not raw_list:
        warnings.append(f"Данные для {city_name} не получены")
        return [], warnings

    for m in raw_list: m['city'] = city_name
    return raw_list, warnings