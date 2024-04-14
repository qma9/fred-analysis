# api_utils.py
import requests

import os


def fetch_series_data(series_id: str) -> dict:
    try:
        # Get the root URL from an environment variable
        root_domain = os.getenv("BACKEND_URL", "http://localhost:8000")
        response = requests.get(f"{root_domain}/api/series/{series_id}")
        if response.status_code != 200:
            raise Exception(f"Error: Received status code {response.status_code}")
        data = response.json()
        return data
    except Exception as e:
        print(f"Failed to fetch series data: {e}")
        return None
