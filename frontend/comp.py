from matplotlib.pyplot import subplots, Figure
import matplotlib.pyplot as plt
import mplcyberpunk
from pandas import DataFrame
from solara import component, FigureMatplotlib, Reactive, Button

plt.style.use("cyberpunk")

from frontend.api_utils import get_observations, get_predictions


def get_df_observations(series_id: str) -> DataFrame:
    """
    Consume backend API for observations and initialize DataFrame.
    """
    return DataFrame(get_observations(series_id))


def get_df_predictions(series_id: str, model: str) -> DataFrame:
    """
    Consume backend API for predictions and initialize DataFrame.
    """
    return DataFrame(get_predictions(series_id, model))


def get_empty_figure() -> Figure:
    """
    Initialize empty matplotlib figure.
    """
    figure, _axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
    return figure


def set_reactive_figure(
    reactive_object: Reactive, series: str, model: str, title: str
) -> None:
    """
    Update reactive object with complete figure.
    """
    df_observations = get_df_observations(series)
    df_predictions = get_df_predictions(series, model)
    figure, axes = subplots(nrows=1, ncols=1, figsize=(20, 10))
    df_predictions.plot(
        x="date",
        y="value",
        ax=axes,
        title=f"{title}{series}",
        label="Forecast",
        color="red",
    )
    df_observations.plot(
        x="date", y="value", ax=axes, title=f"{title}{series}", label="Realized"
    )
    mplcyberpunk.add_glow_effects(axes, gradient_fill=True)
    reactive_object.set(figure)


@component
def SemiconductorButtonClick(reactive_object: Reactive[Figure]):
    """
    Semiconductor button component which updates figure with semiconductor series on click.
    """
    return Button(
        label="Semiconductor",
        on_click=lambda: set_reactive_figure(
            reactive_object=reactive_object,
            series="IPG3344S",
            model="semiconductor",
            title="Manufacturing: Semiconductor and Other Electronic Component - ",
        ),
        icon_name="mdi-chart-timeline-variant",
        click_event="click",
        classes=["button-64"],
    )


@component
def CryptocurrencyButtonClick(reactive_object: Reactive[Figure]):
    """
    Cryptocurrency button component which updates figure with cryptocurrency series on click.
    """
    return Button(
        label="Cryptocurrency",
        on_click=lambda: set_reactive_figure(
            reactive_object=reactive_object,
            series="CBBTCUSD",
            model="cryptocurrency",
            title="Coinbase Bitcoin (USD) - ",
        ),
        icon_name="mdi-chart-timeline-variant",
        click_event="click",
        classes=["button-64"],
    )


@component
def PlotFigure(reactive_figure: Reactive[Figure]) -> FigureMatplotlib:
    """
    Child component of Card in main Column component on Page,
    which returns the updated matplotlib figure.
    """
    return FigureMatplotlib(reactive_figure.value)
