from dotenv import load_dotenv

from time import perf_counter
import asyncio
import sys
import os

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from api import (
    build_urls,
    get_responses,
    interpolate_data,
)
from api.database import (
    populate_series,
    populate_observations,
    create_tables,
    fetch_observations,
    populate_predictions,
)
from api.analysis import (
    pivot_data,
    select_series,
    unit_root_test,
    difference_series,
    cointegration_rank,
    get_lag_order,
    vecm_wrapper,
    get_predictions,
    inverse_difference_series,
    melt_data,
)
from api.config import (
    BASE_URL,
    SERIES_ENDPOINT,
    OBSERVATIONS_ENDPOINT,
    SERIES_IDS,
    SEMICONDUCTOR_SERIES,
    CRYPTOCURRENCY_SERIES,
)


async def main() -> None:
    # Build series URLs, about 10 years of data is requested
    series_urls = build_urls(
        BASE_URL, SERIES_ENDPOINT, SERIES_IDS, observation_start="2014-12-01"
    )

    # Build observations URLs, about 10 years of data is requested
    observations_urls = build_urls(
        BASE_URL, OBSERVATIONS_ENDPOINT, SERIES_IDS, observation_start="2014-12-01"
    )

    start_time = perf_counter()  # benchmarking

    # Send get requests to series URLs and receive JSON response
    series_responses = await get_responses(series_urls)

    # Send get requests to observations URLs and receive JSON response
    observations_responses = await get_responses(observations_urls)

    end_time = perf_counter()  # benchmarking

    print(f"\nTime: {end_time - start_time} seconds\n")  # benchmarking

    # Transform nonlinear series to daily frequency with cubic spline interpolation
    transformed_observations = interpolate_data(observations_responses, "cubicspline")

    # Create Series and Observations tables in database
    create_tables()

    # Populate Series table with series responses
    populate_series(series_responses, SERIES_IDS)

    # Populate Observations table with observations including untouched and transformed series
    populate_observations(transformed_observations)

    # Fetch Observations from database
    data = fetch_observations()

    ##############################################
    ################## Analysis ##################
    ##############################################
    # Pivot data to have dates as index and series as columns
    df = pivot_data(data)

    # Select groups of series for analyses
    df_semiconductor = select_series(df, SEMICONDUCTOR_SERIES)
    df_cryptocurrency = select_series(df, CRYPTOCURRENCY_SERIES)

    # Test for unit root to check if series are stationary
    semiconductor_p_values_before = unit_root_test(df_semiconductor)
    cryptocurrency_p_values_before = unit_root_test(df_cryptocurrency)

    # Difference non-stationary series and re-test with adfuller
    df_semiconductor_differenced, _semiconductor_p_values_after = difference_series(
        df_semiconductor, semiconductor_p_values_before
    )
    df_cryptocurrency_differenced, _cryptocurrency_p_values_after = difference_series(
        df_cryptocurrency, cryptocurrency_p_values_before
    )

    # Get cointegration rank for series
    semiconductor_rank = cointegration_rank(df_semiconductor_differenced)
    cryptocurrency_rank = cointegration_rank(df_cryptocurrency_differenced)

    # Get lag order for VECM
    semiconductor_lag_order = get_lag_order(df_semiconductor_differenced)
    cryptocurrency_lag_order = get_lag_order(df_semiconductor_differenced)

    # Get VECM models
    semiconductor_model = vecm_wrapper(
        df_semiconductor_differenced,
        semiconductor_rank,
        semiconductor_lag_order,
    )
    cryptocurrency_model = vecm_wrapper(
        df_cryptocurrency_differenced,
        cryptocurrency_rank,
        cryptocurrency_lag_order,
    )

    # Fit VECM models
    semiconductor_result = semiconductor_model.fit()
    cryptocurrency_result = cryptocurrency_model.fit()

    # Get predictions from VECM models
    df_semiconductor_predictions = get_predictions(
        df_semiconductor_differenced,
        semiconductor_result,
        steps=365,  # adjust steps for forecast length
    )
    df_cryptocurrency_predictions = get_predictions(
        df_cryptocurrency_differenced,
        cryptocurrency_result,
        steps=365,  # adjust steps for forecast length
    )

    # Inverse series differencing to get predictions in original scale
    df_semiconductor_forecast = inverse_difference_series(
        df_semiconductor_predictions, df_semiconductor, semiconductor_p_values_before
    )
    df_cryptocurrency_forecast = inverse_difference_series(
        df_cryptocurrency_predictions, df_cryptocurrency, cryptocurrency_p_values_before
    )

    # Inverse pivoting of dataframes back to original long schema
    df_semiconductor_forecast_long = melt_data(df_semiconductor_forecast)
    df_cryptocurrency_forecast_long = melt_data(df_cryptocurrency_forecast)

    # Insert categorical model column
    df_semiconductor_forecast_long["model"] = "semiconductor"
    df_cryptocurrency_forecast_long["model"] = "cryptocurrency"

    # Populate predictions table
    populate_predictions(df_semiconductor_forecast_long)
    populate_predictions(df_cryptocurrency_forecast_long)


if __name__ == "__main__":
    asyncio.run(main())
