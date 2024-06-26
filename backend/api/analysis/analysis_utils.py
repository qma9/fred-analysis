from sqlalchemy.engine import Row
from statsmodels.tsa.vector_ar.vecm import (
    select_coint_rank,
    select_order,
    VECM,
    VECMResults,
)
from statsmodels.tsa.statespace.tools import diff
from statsmodels.tsa.stattools import adfuller
from pandas import DataFrame, Series, date_range, concat, to_datetime
from pandas.tseries.offsets import Day

from typing import Dict, Tuple, List


def pivot_data(data: List[Row]) -> DataFrame:
    """
    Pivot the DataFrame to have dates as index and series as columns.
    """
    df = DataFrame(data)
    df["date"] = to_datetime(df["date"])
    df["value"] = df["value"].astype(float)
    return df.pivot(index="date", columns="series_id", values="value")


def select_series(df: DataFrame, series_ids: List[str]) -> DataFrame:
    """
    Select series for semiconductor and cryptocurrency analysis.
    """
    df_select = df.copy()
    return (
        df_select[series_ids].bfill(limit_area="inside").ffill(limit_area="outside")
    )  # Filling any nans, TODO: Not the most preferable way to deal with nans


def unit_root_test(df: DataFrame) -> Dict[str, float]:
    """
    Get p-value for Augmented Dickey-Fuller unit root test,
    to check if series are stationary.
    """
    result = {}
    for series in df.columns:
        p_value = adfuller(
            df[series],
            maxlag=None,
            regression="ctt",
            autolag="AIC",
            store=False,
            regresults=False,
        )
        result[series] = p_value[1]
    return result


def difference_series(
    df: DataFrame, p_values: Dict[str, float]
) -> Tuple[DataFrame, Dict[str, float]]:
    """
    Difference non-stationary series and re-test with adfuller.
    """
    df_copy = df.copy()
    for series, p_value in p_values.items():
        if p_value > 0.05:
            df_copy.loc[:, series] = diff(
                df[series], k_diff=1, k_seasonal_diff=None, seasonal_periods=1
            )
        else:
            pass
    df_differenced = df_copy.bfill(
        limit_area="outside"
    )  # Filling any Nans, TODO: Not the most preferable way to deal with nans
    return df_differenced, unit_root_test(df_differenced)


def cointegration_rank(df: DataFrame) -> int:
    """
    Perform Johansen cointegration test.
    """
    result = select_coint_rank(
        df, det_order=0, k_ar_diff=1, method="trace", signif=0.05
    )
    return result.rank


def get_lag_order(df: DataFrame) -> int:
    """
    Get the lag order for the VECM model.
    """
    result = select_order(
        df, maxlags=15, deterministic="cili", seasons=4, exog=None, exog_coint=None
    )
    return (result.aic + result.bic + result.fpe + result.hqic) // 4


def vecm_wrapper(df_endog: DataFrame, rank: int, lag_order: int) -> VECM:
    """
    Wrapper function for VECM model.
    """
    vecm = VECM(
        endog=df_endog,
        exog=None,
        exog_coint=None,
        dates=None,
        freq=None,
        missing="none",
        k_ar_diff=lag_order,
        coint_rank=rank,
        deterministic="cili",
        seasons=0,
        first_season=0,
    )
    return vecm


def get_predictions(df: DataFrame, vecm_result: VECMResults, steps: int) -> DataFrame:
    """
    Get predictions for the next n days and concatenate with the original series.
    """
    predictions = vecm_result.predict(steps=steps)
    df_predictions = DataFrame(predictions, columns=df.columns)
    next_n_days = date_range(start=df.index[-1] + Day(), periods=steps)
    df_predictions.index = next_n_days
    return concat([df, df_predictions])


def inverse_difference_series(
    df: DataFrame, df_original: DataFrame, p_values: Dict[str, float]
) -> DataFrame:
    """
    Reverse differencing to get original series.
    """
    df_inverse = df.copy()
    for series, p_value in p_values.items():
        if p_value > 0.05:
            df_inverse.iloc[0, df.columns.get_loc(series)] = df_original.iloc[
                0, df_original.columns.get_loc(series)
            ]
            df_inverse.loc[:, series] = df_inverse.loc[:, series].cumsum()
        else:
            pass
    return df_inverse


def melt_data(df: DataFrame) -> DataFrame:
    """
    Inverse pivoting of dataframe back to original long schema.
    """
    df_long = df.copy()
    return df_long.reset_index(names="date").melt(id_vars=["date"])
