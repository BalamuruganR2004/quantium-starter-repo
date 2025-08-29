"""
Integration tests for your Dash app using dash[testing] (dash_duo fixture).
Targets:
  1) Header is present (#header)
  2) Visualization is present (#sales-graph with Plotly SVG)
  3) Region picker is present (#region-picker) and interactive
Docs: https://dash.plotly.com/testing
"""

def test_header_is_present(dash_duo):
    # Import here so conftest has time to create data
    from app import app
    dash_duo.start_server(app)

    header = dash_duo.wait_for_element("#header")
    assert header is not None
    assert header.text.strip() != ""


def test_visualisation_is_present(dash_duo):
    from app import app
    dash_duo.start_server(app)

    graph = dash_duo.wait_for_element("#sales-graph")
    assert graph is not None

    # Plotly injects an <svg> with class .main-svg inside the graph container
    svg = dash_duo.wait_for_element("#sales-graph .main-svg")
    assert svg is not None
    assert svg.tag_name.lower() == "svg"


def test_region_picker_is_present_and_updates(dash_duo):
    from app import app
    dash_duo.start_server(app)

    picker = dash_duo.wait_for_element("#region-picker")
    assert picker is not None

    # Interact with dropdown to ensure callback runs without error
    # Try a couple of values that should exist from conftest data
    dash_duo.select_dcc_dropdown("#region-picker", "north")
    # Wait until the graph title updates (your app sets a layout title; Plotly uses .gtitle for the <text> node)
    dash_duo.wait_for_element("#sales-graph .gtitle")

    dash_duo.select_dcc_dropdown("#region-picker", "south")
    dash_duo.wait_for_element("#sales-graph .gtitle")
