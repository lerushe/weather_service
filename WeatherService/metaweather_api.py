"""
This is a module to get data from external application
"""
import grequests
import requests
import datetime
import logging

from WeatherService.load_config import Config

logger = logging.getLogger('WeatherService.metaweather_api')


class MetaWeatherAPI:

    def __init__(self):
        self._config = Config()
        self._address = self._config.api_address
        self._city = self._config.city
        self._city_id = self.get_city_id()

    def get_city_id(self):
        """
        Method for get location id
        :return: location id
        """
        response = requests.get(self._address+f'search/?query={self._city}')
        data = response.json()
        return data[0]['woeid']

    def get_data_for_days(self, num_days):
        """
        Method for get weather data from api for a certain number of days
        :param num_days: days number
        :return: list data for some days, each element in json format
        """
        end_date = datetime.datetime.today()
        date_list = [end_date - datetime.timedelta(days=x) for x in range(0, num_days)]
        base = self._address+str(self._city_id)+'/{}'
        rs = (grequests.get(u) for u in [base.format(t.strftime("%Y/%m/%d")) for t in date_list])
        data = []
        for r in grequests.map(rs):
            data.extend(r.json())
        return data

    def get_data_for_day(self):
        """
        Method for get weather data from api for one day
        :return: list data for day, each element in json format
        """
        date = datetime.datetime.today().strftime("%Y/%m/%d")
        response = requests.get(f'https://www.metaweather.com/api/location/{self._city_id}/{date}')
        data = response.json()
        return data


if __name__ == '__main__':
    Weather = MetaWeatherAPI()