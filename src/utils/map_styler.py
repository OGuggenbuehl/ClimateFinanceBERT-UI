from typing import Dict, Literal, Optional

import numpy as np
from dash_extensions.javascript import assign


def style_map(
    map_mode: Literal[
        "base",
        "total",
        "rio_oecd",
        "rio_climfinbert",
        "rio_diff",
    ],
    color_mode: Literal["continuous", "quartile"] = "continuous",
    geojson_data: Optional[Dict] = None,
):
    """Return style config for map rendering.

    Args:
        map_mode: The mode of the map
        color_mode: Whether to use continuous or quartile-based coloring
        geojson_data: The GeoJSON data used to calculate quartiles
    """
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

    # Default values (will be overridden if data is provided)
    min_val = 0
    max_val = 1000
    quartile_breaks = []
    quartile_colors = []

    # Calculate quartiles if we have data
    if geojson_data and color_mode == "quartile":
        values = [
            feature["properties"].get("value")
            for feature in geojson_data["features"]
            if feature["properties"].get("value") is not None
        ]

        if values:
            min_val = min(values)
            max_val = max(values)

            # Calculate quartile breakpoints
            q1 = np.percentile(values, 25)
            q2 = np.percentile(values, 50)
            q3 = np.percentile(values, 75)
            quartile_breaks = [min_val, q1, q2, q3, max_val]

            # Extract colors for quartiles from colorscale
            if len(colorscale) >= 4:
                quartile_colors = colorscale[:4]
            else:
                # Create 4 colors from our colorscale
                quartile_colors = [
                    colorscale[0],  # First quartile: first color
                    colorscale[min(1, len(colorscale) - 1)],  # Second quartile
                    colorscale[min(1, len(colorscale) - 1)],  # Third quartile
                    colorscale[-1],  # Fourth quartile: last color
                ]

    style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)

    # Different style handlers for continuous vs. quartile coloring
    if color_mode == "continuous":
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
    else:  # quartile coloring
        style_handle = assign("""function(feature, context) {
            const { min, max, style, polyColoring, quartile_breaks, quartile_colors } = context.hideout;
            const value = feature.properties[polyColoring];
            
            if (value === null || value === undefined) {
                style.fillColor = "#A9A9A9";
                return style;
            }
            
            // Find which quartile the value belongs to
            let colorIndex = 0;
            for (let i = 1; i < quartile_breaks.length; i++) {
                if (value <= quartile_breaks[i]) {
                    colorIndex = i - 1;
                    break;
                }
            }
            
            style.fillColor = quartile_colors[colorIndex];
            return style;
        }""")

    return {
        "style": style,
        "style_handle": style_handle,
        "colorscale": colorscale,
        "classes": [],
        "min": min_val,
        "max": max_val,
        "quartile_breaks": quartile_breaks,
        "quartile_colors": quartile_colors,
    }
