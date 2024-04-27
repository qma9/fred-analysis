from solara import component, Style, Card, Column, DataFrame
from solara.lab import theme
import pandas as pd
from pathlib import Path

from frontend.comp import PlotObservations
from frontend.api_utils import get_observations


@component()
def Page():
    # solara.lab.theme.themes.dark.primary = "#1e1248"
    theme.dark = True
    Style(Path("frontend/assets/style.css"))
    # solara.Theme(Path("frontend/assets/theme.js"))

    with Column(
        align="center",
        gap="12px",
    ):
        with Card(
            title="Card title",
            subtitle="Card subtitle",
            elevation=10,
            margin=10,
            classes=["card"],
        ):
            PlotObservations()
