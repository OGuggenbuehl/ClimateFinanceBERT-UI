from typing import Any, Literal, Optional

import numpy as np
from dash_extensions.javascript import assign


def get_colorscale_for_mode(map_mode: str) -> list[str]:
    """Get the appropriate color scale for a given map mode.

    Args:
        map_mode: The visualization mode of the map

    Returns:
        List of color codes for the gradient
    """
    mode_colorscales = {
        "total": ["#00BFFF", "#FFFF00", "#FF4500"],  # Blue → Yellow → Red
        "rio_oecd": ["#d9f0a3", "#addd8e", "#31a354"],  # Light → Mid → Dark Green
        "rio_climfinbert": ["#ffffcc", "#ffeda0", "#f03b20"],  # Yellow → Orange → Red
        "rio_diff": ["#0571b0", "#f7f7f7", "#ca0020"],  # Blue → White → Red
    }

    return mode_colorscales.get(
        map_mode, ["#d3d3d3", "#808080", "#000000"]
    )  # Default grayscale


def calculate_quartiles(geojson_data: dict) -> dict[str, Any]:
    """Calculate quartile breakpoints and corresponding colors from GeoJSON data.

    Args:
        geojson_data: GeoJSON data with values to analyze

    Returns:
        Dictionary with quartile breaks and colors
    """
    # Extract values from GeoJSON features
    values = [
        feature["properties"].get("value")
        for feature in geojson_data["features"]
        if feature["properties"].get("value") is not None
    ]

    if not values:
        return {
            "min_val": 0,
            "max_val": 1000,
            "quartile_breaks": [],
            "quartile_colors": [],
        }

    # Calculate value range and quartiles
    min_val = min(values)
    max_val = max(values)
    q1 = np.percentile(values, 25)
    q2 = np.percentile(values, 50)
    q3 = np.percentile(values, 75)

    return {
        "min_val": min_val,
        "max_val": max_val,
        "quartile_breaks": [min_val, q1, q2, q3, max_val],
        "quartile_colors": [],  # To be filled by caller
    }


def create_continuous_style_handler() -> Any:
    """Create a JavaScript function for continuous color styling.

    Returns:
        JavaScript function for continuous color styling
    """
    return assign("""function(feature, context) {
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


def create_quartile_style_handler() -> Any:
    """Create a JavaScript function for quartile-based color styling.

    Returns:
        JavaScript function for quartile-based color styling
    """
    return assign("""function(feature, context) {
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


def style_map(
    map_mode: Literal["base", "total", "rio_oecd", "rio_climfinbert", "rio_diff"],
    color_mode: Literal["continuous", "quartile"] = "continuous",
    geojson_data: Optional[dict] = None,
) -> dict[str, Any]:
    """Generate style configuration for map rendering.

    Args:
        map_mode: The mode of the map visualization
        color_mode: Whether to use continuous or quartile-based coloring
        geojson_data: The GeoJSON data used to calculate quartiles

    Returns:
        Dictionary containing style configuration
    """
    # Handle base map mode (no data visualization)
    if map_mode == "base":
        return {
            "style": {"fillColor": "dodgerblue", "color": "dodgerblue"},
            "style_handle": None,
            "colorscale": [],
            "classes": [],
            "min": None,
            "max": None,
        }

    # Get the color scale for this visualization mode
    colorscale = get_colorscale_for_mode(map_mode)

    # Default values (will be overridden if data is provided)
    min_val = 0
    max_val = 1000
    quartile_breaks = []
    quartile_colors = []

    # Calculate quartiles if we have data and are using quartile coloring
    if geojson_data and color_mode == "quartile":
        quartile_data = calculate_quartiles(geojson_data)
        min_val = quartile_data["min_val"]
        max_val = quartile_data["max_val"]
        quartile_breaks = quartile_data["quartile_breaks"]

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

    # Base style for all features
    style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)

    # Different style handlers for continuous vs. quartile coloring
    style_handle = (
        create_continuous_style_handler()
        if color_mode == "continuous"
        else create_quartile_style_handler()
    )

    # Return the complete style configuration
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
