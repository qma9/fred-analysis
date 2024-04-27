from matplotlib.pyplot import subplots
import matplotlib.pyplot as plt
import mplcyberpunk
from pandas import DataFrame
from solara import component, FigureMatplotlib

from frontend.api_utils import get_observations, get_predictions

plt.style.use("cyberpunk")


def get_df_observations(series_id: str) -> DataFrame:
    return DataFrame(get_observations(series_id))


def get_df_predictions(series_id: str) -> DataFrame:
    return DataFrame(get_predictions(series_id))


@component
def PlotObservations() -> FigureMatplotlib:
    series = "CBBTCUSD"
    df = get_df_observations(series)
    fig, axes = subplots(nrows=1, ncols=1, figsize=(12, 10))
    df.plot(x="date", y="value", ax=axes, title=series)
    mplcyberpunk.add_glow_effects(axes, gradient_fill=True)
    # fig = Figure(figsize=(20, 12))
    # axes = fig.subplots(nrows=1, ncols=1)
    # axes.plot(df["value"], data=df)  # color="#0a9396"
    return FigureMatplotlib(fig)
