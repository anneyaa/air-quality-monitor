import os
import json
from datetime import datetime
from AirMonitor_App.constants import DATA_FILE

class Measurement:
    def __init__(self, city, date, pm10, pm25, no2, co, **kwargs):
        self.city = city
        self.date = date
        self.pm10 = float(pm10)
        self.pm25 = float(pm25)
        self.no2 = float(no2)
        self.co = float(co)

    def to_dict(self):
        return self.__dict__

class AirQualityMonitor:
    def __init__(self):
        self.data = []
        self.data_file = DATA_FILE

    def fetch_from_api(self, city='Berlin', start_date=None, end_date=None):
        from AirMonitor_App.models.network import fetch_air_quality
        raw_list, warnings = fetch_air_quality(city, start_date, end_date)
        if raw_list:
            self.data = [Measurement(**m) for m in raw_list]
            self.append_to_database(self.data)
            return True, warnings
        return False, warnings

    def fetch_for_comparison(self, cities, target_date):
        from AirMonitor_App.models.network import fetch_air_quality
        results = {}
        for city in cities:
            if city and city.strip():
                raw_list, warnings = fetch_air_quality(city, target_date, target_date)
                if raw_list:
                    measurements = [Measurement(**m) for m in raw_list]
                    results[city] = measurements
                    self.append_to_database(measurements)
        return results

    def fetch_and_analyze(self, city, start_d, end_d, f_type, f_min, f_max, s_by, s_order):
        from AirMonitor_App.models.network import get_coordinates, get_air_data
        coords = get_coordinates(city)
        if not coords: return [], ["Город не найден"]

        raw = get_air_data(coords[0], coords[1], start_d, end_d)
        if not raw: return [], ["Нет данных за этот период"]

        res = [Measurement(city=coords[2], **m) for m in raw]

        if f_type and (f_min or f_max):
            temp = []
            for m in res:
                val = getattr(m, f_type)
                if f_min and val < float(f_min): continue
                if f_max and val > float(f_max): continue
                temp.append(m)
            res = temp

        is_rev = (s_order == 'desc')
        try:
            if s_by == 'date':
                res.sort(key=lambda x: datetime.strptime(x.date, "%d-%m-%Y %H:%M"), reverse=is_rev)
            else:
                res.sort(key=lambda x: getattr(x, s_by), reverse=is_rev)
        except: pass
        return res, []

    def append_to_database(self, new_items):
        existing = []
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except: pass

        seen = {f"{d['city']}_{d['date']}" for d in existing}
        for item in new_items:
            d = item.to_dict()
            if f"{d['city']}_{d['date']}" not in seen:
                existing.append(d)

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=4, ensure_ascii=False)

    def load_from_json(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    items = json.load(f)
                    self.data = [Measurement(**item) for item in items]
            except: self.data = []

    def get_all_cities(self):
        self.load_from_json()
        return sorted(list(set(m.city for m in self.data)))