from app import app as dash_app

DEFAULT_TIMEOUT = 45


def start(dash_duo):
    """Start Dash server and ensure no unexpected console errors."""
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_page(timeout=DEFAULT_TIMEOUT)
    dash_duo.driver.set_window_size(1400, 1000)

    benign = (
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
        and not any(s in rec.get("message", "") for s in benign)
    ]
    assert unexpected == [], f"Unexpected console errors: {unexpected}"


def test_header_is_present(dash_duo):
    start(dash_duo)
    h1 = dash_duo.find_element("h1")
    assert h1 is not None
    assert h1.text.strip() != ""


def test_visualisation_is_present(dash_duo):
    start(dash_duo)
    svg = dash_duo.wait_for_element_by_css_selector("#sales-graph svg", timeout=DEFAULT_TIMEOUT)
    assert svg is not None


def test_region_picker_is_present(dash_duo):
    start(dash_duo)
    picker = dash_duo.find_element("#region-picker")
    assert picker is not None
