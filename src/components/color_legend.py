from typing import Optional

from dash import html


def format_value(value: float) -> str:
    """Format a numeric value for display in the legend as $ Mio USD."""
    if value >= 1000:
        formatted = f"{int(value):,}"
    else:
        formatted = f"{value:.2f}"
    return f"${formatted} M"


def create_gradient_style(colorscale: list[str]) -> str:
    """Create a CSS gradient string from a colorscale.

    Args:
        colorscale: List of color codes

    Returns:
        CSS linear-gradient string
    """
    gradient_stops = ", ".join(
        [
            f"{color} {i / (len(colorscale) - 1) * 100}%"
            for i, color in enumerate(colorscale)
        ]
    )
    return f"linear-gradient(to right, {gradient_stops})"


def render_continuous_legend(
    min_val: float, max_val: float, colorscale: list[str]
) -> html.Div:
    """Render a continuous color legend with a gradient bar."""
    min_text = format_value(min_val)
    max_text = format_value(max_val)
    gradient = create_gradient_style(colorscale)

    return html.Div(
        [
            html.Div(
                "Color Legend:",
                style={"font-weight": "bold", "margin-bottom": "8px"},
            ),
            html.Div(
                [
                    html.Div(
                        style={
                            "height": "10px",
                            "background": gradient,
                            "marginBottom": "5px",
                        }
                    ),
                    html.Div(
                        [
                            html.Span(min_text, style={"float": "left"}),
                            html.Span(max_text, style={"float": "right"}),
                        ]
                    ),
                ]
            ),
        ]
    )


def create_quartile_items(breaks: list[float], colors: list[str]) -> list[html.Div]:
    """Create items for the quartile legend.

    Args:
        breaks: List of quartile break points
        colors: List of colors for quartiles

    Returns:
        List of Div components for each quartile
    """
    items = []

    for i in range(len(breaks) - 1):
        start = breaks[i]
        end = breaks[i + 1]

        # Format numbers
        start_text = format_value(start)
        end_text = format_value(end)
        range_text = f"{start_text} - {end_text}"

        items.append(
            html.Div(
                [
                    html.Span(
                        style={
                            "display": "inline-block",
                            "width": "15px",
                            "height": "15px",
                            "margin-right": "5px",
                            "background-color": colors[i],
                        }
                    ),
                    html.Span(f"Q{i + 1}: {range_text}"),
                ],
                style={"margin-bottom": "2px"},
            )
        )

    return items


def render_quartile_legend(breaks: list[float], colors: list[str]) -> html.Div:
    """Render a quartile-based color legend with color blocks."""
    if not breaks or len(breaks) < 2:
        return html.Div()  # Return empty div

    items = create_quartile_items(breaks, colors)

    return html.Div(
        [
            html.H6(
                "Color Legend:",
                style={
                    "font-weight": "bold",
                    "margin-bottom": "8px",
                },
            ),
            html.Div(items),
        ]
    )


def render(map_mode: str, color_mode: str, style_info: dict) -> Optional[html.Div]:
    if map_mode == "base":
        return None

    if color_mode == "continuous":
        return render_continuous_legend(
            min_val=style_info["min"],
            max_val=style_info["max"],
            colorscale=style_info["colorscale"],
        )
    else:  # quartile mode
        return render_quartile_legend(
            breaks=style_info["quartile_breaks"],
            colors=style_info["quartile_colors"],
        )
