# tests/test_basic.py
from app import app as dash_app


def start(dash_duo):
    """Start the Dash server for each test and assert no unexpected console errors."""
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_page(timeout=10)

    # Chrome reports React/Dash minified warnings as SEVERE. Ignore the usual benign ones.
    benign_substrings = (
        "dash_renderer",
        "react@18",
        "react-dom@18",
        "prop-types@15",
        "polyfill@7",
        "plotly.min.js",
        "favicon.ico",
        "Failed to load source map",
    )

    unexpected = [
        rec for rec in dash_duo.get_logs()
        if rec.get("level") == "SEVERE"
        and not any(s in rec.get("message", "") for s in benign_substrings)
    ]
    assert unexpected == [], f"Unexpected console errors: {unexpected}"


def test_header_is_present(dash_duo):
    start(dash_duo)
    # Be flexible: any <h1> is fine
    h1 = dash_duo.find_element("h1")
    assert h1 is not None
    assert h1.text.strip() != ""


def test_visualisation_is_present(dash_duo):
    start(dash_duo)
    # Wait for the Plotly SVG inside the graph to avoid stale element references
    svg = dash_duo.wait_for_element_by_css_selector("#sales-graph svg", timeout=10)
    assert svg is not None


def test_region_picker_is_present(dash_duo):
    start(dash_duo)
    region = dash_duo.find_element("#region-picker")
    assert region is not None
