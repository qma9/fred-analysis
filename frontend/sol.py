from solara import component, Style, Card, Column, Row, reactive
from solara.lab import theme
from pathlib import Path

from frontend.comp import (
    SemiconductorButtonClick,
    CryptocurrencyButtonClick,
    PlotFigure,
    get_empty_figure,
)


@component()
def Page():
    # Dark theme and style sheet
    theme.dark = True
    Style(Path("frontend/assets/style.css"))

    # Initialize empty reactive object for plot
    reactive_object = reactive(get_empty_figure())

    # Main column component on page
    # Contains row with two buttons and card with plot
    with Column(align="center", gap="0px"):
        with Row(gap="10px", margin=10, justify="space-around"):
            SemiconductorButtonClick(reactive_object)
            CryptocurrencyButtonClick(reactive_object)
        with Card(
            elevation=10,
            classes=["card"],
        ):
            PlotFigure(reactive_object)
