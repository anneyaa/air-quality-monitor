from datetime import datetime

def format_date(iso_str):
    try:
        return datetime.fromisoformat(iso_str).strftime("%d-%m-%Y %H:%M")
    except Exception:
        return iso_str

def param_to_display(param):
    mapping = {'pm25': 'PM2.5', 'pm10': 'PM10', 'no2': 'NO2', 'co': 'CO'}
    return mapping.get(param.lower(), param)