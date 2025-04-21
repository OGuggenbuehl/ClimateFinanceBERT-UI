from typing import Literal

from dash_extensions.javascript import assign


def style_map(
    map_mode: Literal[
        "base",
        "total",
        "rio_oecd",
        "rio_climfinbert",
        "rio_diff",
    ],
):
    """Return style config for map rendering."""
    if map_mode == "base":
        return {
            "style": {"fillColor": "dodgerblue", "color": "dodgerblue"},
            "style_handle": None,
            "colorscale": [],
            "classes": [],
            "min": None,
            "max": None,
        }

    # Define continuous color gradients
    if map_mode == "total":
        colorscale = ["#00BFFF", "#FFFF00", "#FF4500"]  # Blue → Yellow → Red
    elif map_mode == "rio_oecd":
        colorscale = ["#d9f0a3", "#addd8e", "#31a354"]  # Light → Mid → Dark Green
    elif map_mode == "rio_climfinbert":
        colorscale = ["#ffffcc", "#ffeda0", "#f03b20"]  # Yellow → Orange → Red
    elif map_mode == "rio_diff":
        colorscale = ["#0571b0", "#f7f7f7", "#ca0020"]  # Blue → White → Red

    # Example static values (can be dynamic based on data)
    min_val = 0
    max_val = 1000

    style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)

    style_handle = assign("""function(feature, context) {
        const { min, max, colorscale, style, polyColoring } = context.hideout;
        const value = feature.properties[polyColoring];
        if (value === null || value === undefined) {
            style.fillColor = "#A9A9A9";
            return style;
        }
        const normalized = Math.min(Math.max((value - min) / (max - min), 0), 1);
        const color = chroma.scale(colorscale).domain([0, 1])(normalized).hex();
        style.fillColor = color;
        return style;
    }""")

    return {
        "style": style,
        "style_handle": style_handle,
        "colorscale": colorscale,
        "classes": [],  # Not used, included for compatibility
        "min": min_val,
        "max": max_val,
    }
