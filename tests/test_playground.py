from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.testmuai.com/selenium-playground/"
WAIT = 12

def wait_for(driver, condition):
    return WebDriverWait(driver, WAIT).until(condition)

def open_demo(driver, link_text, url_part):
    driver.get(BASE_URL)
    wait_for(driver, EC.presence_of_element_located((By.LINK_TEXT, link_text))).click()
    wait_for(driver, lambda d: d.execute_script("return document.readyState") == "complete")
    assert url_part in driver.current_url

def test_scenario_1_simple_form_demo(browser_config, remote_driver):
    driver = remote_driver
    message = "Welcome to TestMu AI"
    open_demo(driver, "Simple Form Demo", "simple-form-demo")

    # Locator 1: ID
    box = wait_for(driver, EC.presence_of_element_located((By.ID, "user-message")))
    box.clear()
    box.send_keys(message)

    # Locator 2: CSS selector
    wait_for(driver, EC.presence_of_element_located((By.CSS_SELECTOR, "#showInput"))).click()

    # Locator 3: ID
    wait_for(driver, EC.text_to_be_present_in_element((By.ID, "message"), message))
    result = driver.find_element(By.ID, "message")
    assert result.text.strip() == message
    print("Scenario 1 passed:", result.text.strip())

def test_scenario_2_drag_drop_slider(browser_config, remote_driver):
    driver = remote_driver
    open_demo(driver, "Drag & Drop Sliders", "drag-drop-range-sliders-demo")

    slider = wait_for(driver, EC.visibility_of_element_located((By.XPATH, "//input[@type='range' and @value='15']")))
    min_v = float(slider.get_attribute("min") or 0)
    max_v = float(slider.get_attribute("max") or 100)
    current = float(driver.execute_script("return arguments[0].value", slider))
    target = 95.0
    rect = driver.execute_script(
        "return arguments[0].getBoundingClientRect().toJSON()", slider)
    width = rect["width"]
    start_x = ((current-min_v)/(max_v-min_v))*width - width/2
    delta_x = ((target-current)/(max_v-min_v))*width

    ActionChains(driver).move_to_element_with_offset(
        slider, int(start_x), 0).click_and_hold().move_by_offset(
        int(delta_x), 0).release().perform()

    wait_for(driver, lambda d: float(d.execute_script(
        "return arguments[0].value", slider)) == target)
    actual = float(driver.execute_script("return arguments[0].value", slider))
    output = driver.find_elements(By.ID, "range")
    if output:
        wait_for(driver, lambda d: d.find_element(By.ID, "range").text.strip() == "95")
    assert actual == target
    print("Scenario 2 passed: slider value =", actual)

def test_scenario_3_input_form_submit(browser_config, remote_driver):
    driver = remote_driver
    open_demo(driver, "Input Form Submit", "input-form-demo")

    # Empty submission: verify browser blocks the form and reports validation.
    wait_for(driver, EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()
    invalid = driver.execute_script("return document.querySelector('form :invalid')")
    assert invalid is not None, "Empty form was not blocked."
    validation_text = driver.execute_script(
        "return arguments[0].validationMessage", invalid)
    assert validation_text.strip() == "Please fill inthis field."
    print("Empty form validation:", validation_text)

    values = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "company": "TestMu Assignment",
        "website": "https://example.com",
        "city": "New York",
        "address1": "123 Test Street",
        "address2": "Suite 10",
        "state": "New York",
        "zip": "10001",
    }
    for field_name, value in values.items():
        field = wait_for(driver, EC.visibility_of_element_located(
            (By.NAME, field_name)))
        field.clear()
        field.send_keys(value)

    country = wait_for(driver, EC.visibility_of_element_located(
        (By.NAME, "country")))
    Select(country).select_by_visible_text("United States")

    wait_for(driver, EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()

    expected = "Thanks for contacting us, we will get back to you shortly."
    success = wait_for(driver, EC.visibility_of_element_located((
        By.XPATH, f"//*[contains(normalize-space(.), '{expected}')]")))
    assert expected in success.text
    print("Scenario 3 passed:", expected)
