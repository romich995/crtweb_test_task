import requests


WEATHER_API_KEY = '99ba78ee79a2a24bc507362c5288a81b'


class API():
    def __init__():
        
        """
        Инициализирует класс
        """
        self.session = requests.Session()


    def _get(self, url, raise_for_status=False):
        """
        Отправляет запрос на сервер
        Args:
            url: Адрес запроса
            raise_for_status: флаг, необходимо ли 
                создать исключение при ответе со статусом кода 
                отличным от 200 до 300 невключительно 
        Returns:

        """
        r = self.session.get(url)

        if raise_for_status and not (200 <= r.status_code < 300):
            r.raise_for_status()
        
        return r
        
class OpenWeatherMapAPI(API):
    """"""
    base_url = 'https://api.openweathermap.org'

    def _get_weather_url(self, city):
        """
        Генерирует url включая в него необходимые параметры
        Args:
            city: Город
        Returns:

        """
        url = base_url
        url += '?units=metric'
        url += '&q=' + city
        url += '&appid=' + WEATHER_API_KEY
        return url 

    def _get_weather_from_response(self, response):
        """
        Достает погоду из ответа
        Args:
            response: Ответ, пришедший с сервера
        Returns:

        """
        data = response.json()
        return data['main']['temp']():

    def get_weather(self, city):
        """
        Делает запрос на получение погоды
        Args:
            city: Город
        Returns:

        """
        url = self._get_weather_url(city)
        r = self._get(url, 
                       raise_for_status=True)
        if r is None:
            return None
        else:
            weather = self.get_weather_from_response(r)
            return weather

    def check_existing(self, city):
        """
        Проверяет наличие города
        Args:
            city: Название города
        Returns:

        """
        url = self._get_weather_url(city)
        r = self._get(url)
        if r.status_code == 404:
            return False
        if r.status_code == 200:
            return True
    