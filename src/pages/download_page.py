import dash_bootstrap_components as dbc
from dash import html

from components import datatable, ids
from components.widgets import (
    action_button,
    categories,
    donor_type,
    flow_type,
    sub_categories,
    timespan,
)


def render() -> html.Div:
    return html.Div(
        id="download-page",
        children=[
            _create_title_section(),
            _create_description_section(),
            html.Br(),
            _create_filters_section(),
            _create_buttons_section(),
            _create_datatable_section(),
        ],
    )


def _create_title_section() -> dbc.Row:
    """
    Create the title section of the download page.

    Returns:
        dbc.Row: A Bootstrap row containing the page title
    """
    return dbc.Row(
        dbc.Col(
            [
                html.H1("Download Data", className="text-center my-4"),
            ],
            width=12,
        )
    )


def _create_description_section() -> dbc.Row:
    """
    Create the description section with instructions.

    Returns:
        dbc.Row: A Bootstrap row containing the page description
    """
    return dbc.Row(
        dbc.Col(
            [
                html.P(
                    "Download the data in CSV format. You can filter the data "
                    "by selecting the type of flow, the donor type, the categories, "
                    "and the subcategories. Once you're ready, click 'Query' to pull the data and 'Download' to get it in CSV format.",
                    className="lead text-center",
                ),
            ],
            width={"size": 8, "offset": 2},
        )
    )


def _create_filters_section() -> dbc.Row:
    """
    Create the filters section with all filter widgets.

    Returns:
        dbc.Row: A Bootstrap row containing filter widgets in three columns
    """
    return dbc.Row(
        children=[
            _create_donor_flow_column(),
            _create_timespan_column(),
            _create_categories_column(),
        ],
        className="mb-4",
    )


def _create_donor_flow_column() -> dbc.Col:
    """
    Create the column with donor type and flow type filters.

    Returns:
        dbc.Col: A Bootstrap column with donor and flow type widgets
    """
    return dbc.Col(
        [
            donor_type.render(
                id=ids.DONORTYPE_DROPDOWN_DOWNLOAD,
                style={"color": "black"},
            ),
            flow_type.render(
                id=ids.FLOW_TYPE_DROPDOWN_DOWNLOAD,
                style={"color": "black"},
            ),
        ],
        width={"size": 2, "offset": 2},
        className="mb-4",
    )


def _create_timespan_column() -> dbc.Col:
    """
    Create the column with timespan (year range) filter.

    Returns:
        dbc.Col: A Bootstrap column with the timespan widget
    """
    return dbc.Col(
        [
            timespan.render(id=ids.YEAR_SLIDER_DOWNLOAD),
        ],
        width={"size": 4, "offset": 0},
        className="mb-4",
    )


def _create_categories_column() -> dbc.Col:
    """
    Create the column with categories and subcategories filters.

    Returns:
        dbc.Col: A Bootstrap column with category widgets
    """
    return dbc.Col(
        [
            categories.render(
                id=ids.CATEGORIES_DROPDOWN_DOWNLOAD,
                style={"color": "black"},
            ),
            sub_categories.render(
                id=ids.CATEGORIES_SUB_DROPDOWN_DOWNLOAD,
                style={"color": "black"},
            ),
        ],
        width={"size": 2, "offset": 0},
        className="mb-4",
    )


def _create_buttons_section() -> dbc.Row:
    """
    Create the section with query and download buttons.

    Returns:
        dbc.Row: A Bootstrap row containing the action buttons
    """
    return dbc.Row(
        dbc.Col(
            dbc.Row(
                [
                    _create_query_button_column(),
                    _create_download_button_column(),
                ],
                className="g-3",
            ),
            width=12,
        ),
        className="mb-4",
    )


def _create_query_button_column() -> dbc.Col:
    """
    Create the column with the query button.

    Returns:
        dbc.Col: A Bootstrap column with the query button
    """
    return dbc.Col(
        action_button.render(
            "Query",
            id=ids.QUERY_BTN,
            class_name="w-100",
        ),
        width={"size": 2, "offset": 4},
    )


def _create_download_button_column() -> dbc.Col:
    """
    Create the column with the download button.

    Returns:
        dbc.Col: A Bootstrap column with the download button
    """
    return dbc.Col(
        action_button.render(
            "Download",
            id=ids.DOWNLOAD_BTN,
            color="success",
            class_name="w-100",
        ),
        width=2,
    )


def _create_datatable_section() -> dbc.Row:
    """
    Create the section with the data table.

    Returns:
        dbc.Row: A Bootstrap row containing the data table
    """
    return dbc.Row(
        dbc.Col(
            html.Div(
                children=[
                    dbc.Card(
                        datatable.render(id=ids.DOWNLOAD_DATATABLE),
                        body=False,
                        id=ids.DATATABLE_CARD_DOWNLOAD,
                        className="shadow-sm",
                    )
                ],
            ),
            width={"size": 8, "offset": 2},
        ),
        className="mt-4",
    )
