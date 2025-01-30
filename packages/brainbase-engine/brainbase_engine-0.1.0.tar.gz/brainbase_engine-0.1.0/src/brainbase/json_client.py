import requests
from typing import Dict, Optional
from urllib.parse import urljoin
from .utils import get_api_url
class JsonApiClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = get_api_url(),
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
        }

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict:
        url = urljoin(f"{self.base_url}/api/", endpoint.lstrip("/"))
        print("Making request to", url)
        response = requests.request(method, url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str) -> Dict:
        return self._make_request("GET", endpoint)

    def post(self, endpoint: str, data: Dict) -> Dict:
        return self._make_request("POST", endpoint, data)

