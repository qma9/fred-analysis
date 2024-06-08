# api_utils.py
from requests import HTTPError
import requests

import os


def get_observations(series_id: str) -> dict:
    try:
        # Get the root URL from an environment variable
        root_domain = os.getenv("BACKEND_URL", "http://localhost:8000")
        response = requests.get(f"{root_domain}/api/series/{series_id}")
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        data = response.json()
        return data
    except HTTPError as e:
        print(f"Failed to fetch series data: {e}")
        return None


def get_predictions(series_id: str, model: str) -> dict:
    try:
        # Get the root URL from an environment variable
        root_domain = os.getenv("BACKEND_URL", "http://localhost:8000")
        response = requests.get(f"{root_domain}/api/predictions/{series_id}/{model}")
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        data = response.json()
        return data
    except HTTPError as e:
        print(f"Failed to fetch series data: {e}")
        return None
