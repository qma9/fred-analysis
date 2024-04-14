from statsmodels.tsa.vector_ar.vecm import (
    select_coint_rank,
    select_order,
    VECM,
    VECMResults,
)
from statsmodels.tsa.statespace.tools import diff
from statsmodels.tsa.stattools import adfuller
from pandas import DataFrame, Series, date_range, concat
from pandas.tseries.offsets import Day

from typing import Dict, Tuple


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
    for series, p_value in p_values.items():
        if p_value > 0.05:
            df.loc[:, series] = diff(
                df[series], k_diff=1, k_seasonal_diff=None, seasonal_periods=1
            )
        else:
            pass
    df_differenced = df.dropna()

    return df_differenced, unit_root_test(df_differenced)


def cointegration_rank(df: DataFrame) -> int:
    """
    Perform Johansen cointegration test.
    """
    result = select_coint_rank(
        df, det_order=0, k_ar_diff=1, method="trace", signif=0.05
    )

    return result.rank


def get_lag_order(df: DataFrame):
    """
    Get the lag order for the VECM model.
    """
    result = select_order(
        df, maxlags=15, deterministic="cili", seasons=4, exog=None, exog_coint=None
    )
    return (result.aic + result.bic + result.fpe + result.hqic) // 4


def vecm_wrapper(
    df_endog: DataFrame, exog: DataFrame | Series, rank: int, lag_order: int
) -> VECM:
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


def inverse_difference_series(df: DataFrame) -> DataFrame:
    """
    Reverse differencing to get original series.
    """
    return df.cumsum()
