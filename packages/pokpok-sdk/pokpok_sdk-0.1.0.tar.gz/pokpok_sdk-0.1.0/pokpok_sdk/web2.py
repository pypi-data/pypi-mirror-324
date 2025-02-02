from typing import Any

from pydantic import BaseModel
import requests
from pokpok_sdk.constants import BACKEND_BASE_URL, QUOTE_ENDPOINT
from pokpok_sdk.exceptions import PokPokError


class Web2: 
    api_key: str
    base_url: str
    
    def __init__(self, api_key: str, base_url: str = BACKEND_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

    def fetch_quote(self, request: BaseModel, amount: int) -> dict:
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                f"{self.base_url}{QUOTE_ENDPOINT}{amount}",
                headers=headers,
                json=request.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise PokPokError(f"Failed to get quote: {str(e)}")
