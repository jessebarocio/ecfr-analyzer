import requests

class ECFRAPI:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    def get_agencies(self):
        response = requests.get(f"{self.api_base_url}/api/admin/v1/agencies.json")
        return response.json()['agencies']

    def get_titles(self):
        response = requests.get(f"{self.api_base_url}/api/versioner/v1/titles.json")
        return response.json()['titles']
