import unittest
import requests
from AirMonitor_App.models.network import get_coordinates, get_air_data, fetch_air_quality


class NetworkInterfaceTest(unittest.TestCase):

    def test_api_availability(self):
        """Проверка доступности сервера API (пингуем хост)"""
        response = requests.get("http://open-meteo.com", timeout=5)
        self.assertEqual(response.status_code, 200, "Сервер API Open-Meteo недоступен по сети")

    def test_geocoding_success(self):
        """Тест сетевого запроса координат: корректный город"""
        # Проверяем, что запрос к Geocoding API возвращает данные
        result = get_coordinates("Minsk")
        self.assertIsNotNone(result, "Сетевой запрос координат для 'Minsk' не удался")
        lat, lon, name = result
        self.assertIsInstance(lat, float)
        self.assertIn("Минск", name)

    def test_geocoding_fail(self):
        """Тест сетевого запроса координат: несуществующий город"""
        # Проверяем обработку ситуации, когда город не найден в облачной базе
        result = get_coordinates("NonExistentCity12345")
        self.assertIsNone(result, "Система должна возвращать None для несуществующего города")

    def test_air_data_fetch(self):
        """Тест сетевого получения JSON с показателями воздуха"""
        # Координаты Парижа
        lat, lon = 48.85, 2.35
        # Запрашиваем данные по сети
        data = get_air_data(lat, lon)

        self.assertIsInstance(data, list, "API должно возвращать данные в формате списка")
        self.assertGreater(len(data), 0, "API вернуло пустой список данных о воздухе")

        # Проверяем структуру полученного JSON-объекта (наличие ключевых полей)
        first_record = data[0]
        self.assertIn('pm10', first_record)
        self.assertIn('co', first_record)
        self.assertIn('date', first_record)

    def test_full_network_cycle(self):
        """Тест полного цикла: от имени города до получения JSON-ответа"""
        measurements, warnings = fetch_air_quality("Berlin")
        self.assertEqual(len(warnings), 0, f"При сетевом запросе возникли предупреждения: {warnings}")
        self.assertGreater(len(measurements), 0, "Данные не были получены в ходе полного цикла")
        self.assertEqual(measurements[0]['city'], "Берлин")


if __name__ == '__main__':
    unittest.main()