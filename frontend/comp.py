import solara


@solara.component
def ReusableComponent():
    color = solara.use_reactive("red")  # another possibility
    solara.Select(label="Color", values=["red", "green", "blue", "orange"], value=color)
    solara.Markdown("### Solara is awesome", style={"color": color.value})

