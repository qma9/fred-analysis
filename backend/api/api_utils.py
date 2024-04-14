from urllib.parse import urlencode, urlparse, parse_qs
from requests.exceptions import RequestException
from aiohttp import ClientSession
from dateutil.parser import parse
import pandas as pd
import numpy as np

from datetime import datetime, date
from typing import List, Dict
import asyncio
from json import JSONEncoder
import os


class DateEncoder(JSONEncoder):
    def default(self: JSONEncoder, obj: List[Dict[str, str | int | float]]) -> str:
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def build_url(base_url: str, endpoint: str, **kwargs) -> str:
    url = f"{base_url}/{endpoint}"
    if kwargs:
        url += f"?{urlencode(kwargs)}"
    return url


def build_urls(
    base_url: str,
    endpoint: str,
    series_ids: List[str],
    api_key: str = None,
    file_type: str = "json",
    observation_start: str = None,
) -> List[str]:
    if api_key is None:
        api_key = os.getenv("FRED_API_KEY")

    return [
        build_url(
            base_url,
            endpoint,
            api_key=api_key,
            series_id=series_id,
            file_type=file_type,
            observation_start=observation_start,
        )
        for series_id in series_ids
    ]


async def get_json(session: ClientSession, url: str) -> dict:
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except RequestException as e:
        if response:
            print(f"Error occurred: {e}, status code: {response.status_code}")
        else:
            print(f"Error occurred: {e}")
        return None


async def get_responses(urls: List[str]) -> List[Dict[str, str | int | float]]:
    responses = []
    async with ClientSession() as session:
        tasks = [get_json(session, url) for url in urls]
        await asyncio.sleep(0.05)
        results = await asyncio.gather(*tasks)  # added
        for url, response in zip(
            urls, results
        ):  # removed as second argument: asyncio.as_completed(tasks)
            # response = await task
            if response is not None:
                if "seriess" in response:
                    response = response["seriess"][0]
                    # Convert dates to date objects
                    for date_field in [
                        "realtime_start",
                        "realtime_end",
                        "observation_start",
                        "observation_end",
                    ]:
                        response[date_field] = datetime.strptime(
                            response[date_field], "%Y-%m-%d"
                        ).date()
                    # Parse last_updated to datetime
                    response["last_updated"] = parse(response["last_updated"])
                    responses.append(response)
                elif "observations" in response:
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query)
                    series_id = query_params.get("series_id", [None])[0]
                    for observation in response["observations"]:
                        # Add series_id to observation data
                        observation["series_id"] = series_id
                        # Convert value to float if it's not a period
                        if observation["value"] != ".":
                            observation["value"] = float(observation["value"])
                        else:
                            observation["value"] = None
                        # Convert dates to date objects
                        for date_field in ["realtime_start", "realtime_end", "date"]:
                            observation[date_field] = datetime.strptime(
                                observation[date_field], "%Y-%m-%d"
                            ).date()
                        responses.append(observation)
    return responses


def select_target_responses(
    responses: List[Dict[str, str | int | float]], targets: List[str]
) -> List[Dict[str, str | int | float]]:

    return [response for response in responses if response["series_id"] in targets]


def increase_frequency(
    data: List[Dict[str, str | int | float]]
) -> List[Dict[str, str | int | float]]:

    # Get unique series_id values
    series_ids = set(item["series_id"] for item in data)

    result = []
    for series_id in series_ids:
        # Filter data for current series_id
        filtered_data = [item for item in data if item["series_id"] == series_id]

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(filtered_data)

        # Convert 'date' and 'value' columns to datetime and float respectively
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = df["value"].astype(float)

        # Set 'date' as index
        df.set_index("date", inplace=True)

        # Calculate the differences and daily increments
        df["diffs"] = df["value"].diff()
        df["interval"] = df.index.to_series().diff().dt.days
        df["daily_increments"] = df["diffs"] / df["interval"]

        # Resample to daily frequency, backward filling the values
        increments = df["daily_increments"].resample("D").asfreq().bfill()
        increments.iloc[0] = np.nan

        # Resample the DataFrame to daily frequency
        df_daily = df.resample("D").asfreq()
        df_daily.iloc[1:] = np.nan

        # Fill the NaN values in df_daily['value'] with the corresponding values in increments
        df_daily["value"] = df_daily["value"].fillna(increments)

        # Get the cumulative sum of the values
        df_daily["value"] = df_daily["value"].cumsum()

        # Forward fill the other columns
        df_daily = df_daily.ffill()

        # Drop unnecessary columns
        df_daily.drop(columns=["diffs", "interval", "daily_increments"], inplace=True)

        # Convert the series back to a list of dictionaries
        transformed_data = df_daily.reset_index().to_dict("records")

        # Append transformed data to result
        result.extend(transformed_data)

    return result


def backwards_fill(
    data: List[Dict[str, str | int | float]]
) -> List[Dict[str, str | int | float]]:

    # Get unique series_id values
    series_ids = set(item["series_id"] for item in data)

    result = []
    for series_id in series_ids:

        # Filter data for current series_id
        filtered_data = [item for item in data if item["series_id"] == series_id]

        # Convert filtered data to a DataFrame
        df = pd.DataFrame(filtered_data)

        # Convert 'date' and 'value' columns to datetime and float respectively
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = df["value"].astype(float)

        # Set 'date' as index
        df.set_index("date", inplace=True)

        # Resample into daily time series and back fill values
        df_daily = df.resample("D").asfreq().bfill()

        # Convert the series back to a list of dictionaries
        transformed_data = df_daily.reset_index().to_dict("records")

        # Append transformed data to result
        result.extend(transformed_data)

    return result


def interpolate_data(
    data: List[Dict[str, str | int | float]],
    method: str,
) -> List[Dict[str, str | int | float]]:

    # Get unique series_id values
    series_ids = set(item["series_id"] for item in data)

    result = []
    for series_id in series_ids:

        # Filter data for current series_id
        filtered_data = [item for item in data if item["series_id"] == series_id]

        # Convert the data to a DataFrame
        df = pd.DataFrame(filtered_data)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = df["value"].astype(float)
        df.set_index("date", inplace=True)

        # Resample the data to fill in missing days
        df_daily = df.resample("D").asfreq()

        # Interpolate the missing values
        df_daily["value"] = df_daily["value"].interpolate(method=method)

        # Backwards fill the remaining nans
        df_daily.bfill(inplace=True)

        # Convert the series back to a list of dictionaries
        transformed_data = df_daily.reset_index().to_dict("records")

        # Append transformed data to result
        result.extend(transformed_data)

    return result


def recombine_data(
    untouched_data: List[Dict[str, str | int | float]],
    transformed_data: List[List[Dict[str, str | int | float]]],
) -> List[Dict[str, str | int | float]]:

    for data in transformed_data:
        untouched_data.extend(data)

    return untouched_data


if __name__ == "__main__":
    print("This is a module, and should not be run directly")
    exit(1)
