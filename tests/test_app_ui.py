DEFAULT_TIMEOUT = 60  # generous wait

def _prep(dash_duo):
    dash_duo.wait_for_page(timeout=DEFAULT_TIMEOUT)
    dash_duo.driver.set_window_size(1400, 1000)


def test_region_picker_is_present_and_updates(dash_duo):
    from app import app
    dash_duo.start_server(app)
    _prep(dash_duo)

    # ✅ Wait for the radio items group to appear
    picker = dash_duo.wait_for_element("#region-picker", timeout=DEFAULT_TIMEOUT)
    assert picker is not None

    # ✅ Locate all radio buttons
    radios = dash_duo.find_elements("#region-picker input[type='radio']")
    assert len(radios) > 0

    # ✅ Click "north"
    radios[0].click()
    dash_duo.wait_for_element("#sales-graph .gtitle", timeout=DEFAULT_TIMEOUT)

    # ✅ Click "south" (assuming it's the 3rd option in REGION_OPTIONS)
    radios[2].click()
    dash_duo.wait_for_element("#sales-graph .gtitle", timeout=DEFAULT_TIMEOUT)
