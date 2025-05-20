from dash import html


def render(map_mode, color_mode, style_info):
    if map_mode == "base":
        return None

    # TODO: implement map_mode title for legends once needed
    # # Create title based on map mode
    # if map_mode == "total":
    #     title = "Total Climate Finance ($)"
    # elif map_mode == "rio_oecd":
    #     title = "Rio Marker-based"
    # elif map_mode == "rio_climfinbert":
    #     title = "Legend"  # TODO: rework titles for all map modi
    # elif map_mode == "rio_diff":
    #     title = "Difference (pp)"
    # else:
    #     title = map_mode.replace("_", " ").title()

    if color_mode == "continuous":
        # For continuous color scale, display a gradient bar
        min_val = style_info["min"]
        max_val = style_info["max"]
        colorscale = style_info["colorscale"]

        # Format numbers without decimal places if they're large
        if min_val >= 1000:
            min_text = f"{int(min_val):,}"
            max_text = f"{int(max_val):,}"
        else:
            min_text = f"{min_val:.2f}"
            max_text = f"{max_val:.2f}"

        # Create a CSS gradient for the legend
        gradient = ", ".join(
            [
                f"{color} {i / (len(colorscale) - 1) * 100}%"
                for i, color in enumerate(colorscale)
            ]
        )

        # Return a single parent div containing all elements
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
                                "background": f"linear-gradient(to right, {gradient})",
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

    else:  # quartile mode
        # For quartile color scale, show each quartile as a block
        breaks = style_info["quartile_breaks"]
        colors = style_info["quartile_colors"]

        if not breaks or len(breaks) < 2:
            return html.Div()  # Return empty div instead of None

        items = []
        for i in range(len(breaks) - 1):
            start = breaks[i]
            end = breaks[i + 1]

            # Format numbers
            if start >= 1000:
                start_text = f"{int(start):,}"
                end_text = f"{int(end):,}"
            else:
                start_text = f"{start:.2f}"
                end_text = f"{end:.2f}"

            # Handle edge case for last quartile to be inclusive
            range_text = (
                f"{start_text} - {end_text}"
                if i < len(breaks) - 2
                else f"{start_text} - {end_text}"
            )

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

        # Return a single parent div containing all elements
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
