from typing import Literal

from dash_extensions.javascript import assign


def style_map(
    map_mode: Literal["base", "total", "rio_oecd", "rio_climfinbert", "rio_diff"],
):
    """Style the map based on the selected map mode.

    Args:
        map_mode (Literal["base", "total", "rio_oecd", "rio_climfinbert", "rio_diff"]): The selected map mode.

    Returns:
        list: A list of Dash Leaflet components representing the styled map.
    """
    if map_mode == "base":
        return {"fillColor": "dodgerblue", "color": "dodgerblue"}

    if map_mode == "total":
        colorscale = [
            "#A9A9A9",
            "#FED976",
            "#FEB24C",
            "#FD8D3C",
            "#FC4E2A",
            "#E31A1C",
            "#BD0026",
            "#800026",
        ]

    elif map_mode == "rio_oecd":
        colorscale = [
            "#A9A9A9",
            "#9ad219",
            "#a5d732",
            "#b0dc4c",
            "#bbe166",
            "#c7e67f",
            "#d2eb99",
            "#ddf0b2",
        ]

    elif map_mode == "rio_climfinbert":
        colorscale = [
            "#A9A9A9",
            "#FFF700",
            "#FFEA00",
            "#FFDD00",
            "#FFD000",
            "#FFC300",
            "#FFB600",
            "#FFAA00",
        ]

    elif map_mode == "rio_diff":
        colorscale = [
            "#A9A9A9",
            "#FF0000",
            "#FF1919",
            "#FF3232",
            "#FF4C4C",
            "#FF6666",
            "#FF7F7F",
            "#FF9999",
        ]

    classes = [0, 10, 20, 50, 100, 200, 500, 1000]
    style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)
    # Geojson rendering logic, must be JavaScript as it is executed in clientside.
    style_handle = assign("""function(feature, context){
        const {classes, colorscale, style, polyColoring} = context.hideout;  // get props from hideout
        const value = feature.properties[polyColoring];  // get value the determines the color
        for (let i = 0; i < classes.length; ++i) {
            if (value > classes[i]) {
                style.fillColor = colorscale[i];  // set the fill color according to the class
            }
        }
        return style;
    }""")
    return classes, colorscale, style, style_handle
