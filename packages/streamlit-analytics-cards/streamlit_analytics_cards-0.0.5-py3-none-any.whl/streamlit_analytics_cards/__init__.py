import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component("streamlit_analytics_cards", url="http://localhost:3000")
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "streamlit_analytics_cards", path=build_dir
    )


def card(
    template: str,
    title: str = "",
    subtitle: str = "",
    main_value: str = "",
    secondary_value: str = "",
    delta: str = "",
    chart_data: list = None,
    x_axis_label: str = "",
    insights: list = None,
    table_data: list = None,
    bars: list = None,
    marker: float = None,
    marker_label: str = "",
    dot_plots: list = None,
    color_scheme: dict = None,
    key: str = None,
):
    """
    Streamlit custom component.

    Parameters
    ----------
    template : str
        The type of card to render.
    title : str, optional
        Card title.
    subtitle : str, optional
        Card subtitle.
    main_value : str, optional
        Main value displayed on the card.
    secondary_value : str, optional
        Secondary value displayed.
    delta : str, optional
        Trend or comparison value.
    chart_data : list, optional
        Data for charts.
    x_axis_label : str, optional
        Label for x-axis of the chart.
    insights : list, optional
        Insights for the card.
    table_data : list, optional
        Table data.
    bars : list, optional
        Bar chart data.
    marker : float, optional
        Marker value for comparison.
    marker_label : str, optional
        Label for marker.
    dot_plots : list, optional
        Dot plot data.
    color_scheme : dict, optional
        Color settings for the card.
    key : str, optional
        Unique Streamlit key.

    Returns
    -------
    Any
        Value returned by the component.
    """
    data = {
        "template": template,
        "title": title,
        "subtitle": subtitle,
        "mainValue": main_value,
        "secondaryValue": secondary_value,
        "delta": delta,
        "chartData": chart_data,
        "xAxisLabel": x_axis_label,
        "insights": insights,
        "tableData": table_data,
        "bars": bars,
        "marker": marker,
        "markerLabel": marker_label,
        "dotPlots": dot_plots,
        "colorScheme": color_scheme,
    }

    return _component_func(**data, key=key)
