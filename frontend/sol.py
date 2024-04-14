import solara
import pandas as pd
from pathlib import Path

from frontend.comp import ReusableComponent
from frontend.api_utils import fetch_series_data


@solara.component()
def Page():
    # solara.lab.theme.themes.dark.primary = "#1e1248"
    # solara.lab.theme.dark = True
    solara.Style(Path("frontend/assets/style.css"))
    # solara.Theme(Path("frontend/assets/theme.js"))

    series_id = "CBBTCUSD"
    data = fetch_series_data(series_id)
    df = pd.DataFrame(data)

    with solara.Column(gap="10px", align="center"):
        with solara.Card(
            title="Card title", subtitle="Card subtitle", elevation=4, classes=["card"]
        ):
            solara.DataFrame(df, items_per_page=5)
