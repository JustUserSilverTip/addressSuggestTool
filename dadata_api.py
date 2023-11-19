import requests
from database import Database

class DadataAPI:
    def __init__(self, api_key, base_url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"):
        self.api_key = api_key
        self.base_url = base_url

    def suggest_address(self, query, language="ru"):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        }

        params = {
            "query": query,
            "language": language
        }

        response = requests.post(self.base_url, json=params, headers=headers)
        if response.status_code == 200:
            return response.json().get('suggestions', [])
        elif response.status_code == 403:
            print("Несуществующий API ключ")

    def get_coordinates(self, dadata_query):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}"
        }

        params = {
            "query": dadata_query,
            "count": 1
        }

        response = requests.post(self.base_url, json=params, headers=headers)
        data = response.json().get("suggestions", [])[0].get("data", {})
        
        latitude = data.get("geo_lat")
        longitude = data.get("geo_lon")

        return latitude, longitude