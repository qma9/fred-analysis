from dotenv import load_dotenv

from time import time
import asyncio
from json import dump
import sys
import os

# Add root directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from api import (
    build_urls,
    get_responses,
    DateEncoder,
    select_target_responses,
    backwards_fill,
    interpolate_data,
    recombine_data,
)
from api.database import (
    populate_series,
    populate_observations,
    create_tables,
)
from api.analysis import (
    unit_root_test,
    difference_series,
    cointegration_rank,
    get_lag_order,
    vecm_wrapper,
    get_predictions,
    inverse_difference_series,
)
from api.config import (
    BASE_URL,
    SERIES_ENDPOINT,
    OBSERVATIONS_ENDPOINT,
    SERIES_IDS,
    SIMPLE_TARGETS,
    INTERPOLATION_TARGETS,
)


async def main() -> None:
    # Build series URLs, about 10 years of data is requested
    series_urls = build_urls(
        BASE_URL, SERIES_ENDPOINT, SERIES_IDS, observation_start="2014-01-12"
    )

    # Build observations URLs, about 10 years of data is requested
    observations_urls = build_urls(
        BASE_URL, OBSERVATIONS_ENDPOINT, SERIES_IDS, observation_start="2014-01-12"
    )

    print(f"\nURL:\n{observations_urls}\n")  # benchmarking

    start_time = time()  # benchmarking

    # Make get requests to series URLs and receive JSON response
    series_responses = await get_responses(series_urls)

    # Make get requests to observations URLs and receive JSON response
    observations_responses = await get_responses(observations_urls)

    end_time = time()  # benchmarking

    print(f"\nTime: {end_time - start_time} seconds\n")  # benchmarking

    # print(f"\nSeries Responses:\n{series_responses}\n")  # testing

    ################## Testing ##################
    with open("backend/output/observations.json", "w") as f:
        dump(observations_responses, f, cls=DateEncoder)

    # Select accumulating series with lesser than daily frequency
    # accumulating_targets = select_target_responses(
    #     observations_responses, ACCUMULATING_TARGETS
    # )

    # Select binary or index series with lesser than daily frequency
    simple_targets = select_target_responses(observations_responses, SIMPLE_TARGETS)

    # Select nonlinear non-stationary series with lesser than daily frequency
    interpolation_targets = select_target_responses(
        observations_responses, INTERPOLATION_TARGETS
    )

    # Select all other series
    other_observations = [
        response
        for response in observations_responses
        if response["series_id"]
        not in SIMPLE_TARGETS + INTERPOLATION_TARGETS  # + ACCUMULATING_TARGETS
    ]

    # Transform accumulating series to daily frequency with proportional incrementing
    # transformed_accumulating_targets = increase_frequency(accumulating_targets)

    # Transform binary or index series to daily frequency with backwards filling
    transformed_simple_targets = backwards_fill(simple_targets)

    # Transform nonlinear series to daily frequency with cubic spline interpolation
    transformed_interpolation_targets = interpolate_data(
        interpolation_targets, "cubicspline"
    )

    # Recombine transformed series with other untouched daily series
    transformed_observations = recombine_data(
        other_observations,
        [
            # transformed_accumulating_targets,
            transformed_simple_targets,
            transformed_interpolation_targets,
        ],
    )

    ################## Testing ##################
    with open("transformations.json", "w") as f:
        dump(transformed_observations, f, cls=DateEncoder)

    # Create Series and Observations tables in database
    create_tables()

    # Populate Series table with series responses
    populate_series(series_responses)

    # Populate Observations table with observations including untouched and transformed series
    populate_observations(transformed_observations)

    # Analysis

    exit(0)


if __name__ == "__main__":
    asyncio.run(main())
