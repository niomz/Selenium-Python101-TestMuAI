import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()
GRID_URL = os.getenv("TESTMU_GRID_URL", "https://hub.lambdatest.com/wd/hub")

BROWSER_MATRIX = [
    {"browserName": "Chrome", "browserVersion": "128.0", "platformName": "Windows 10", "label": "Chrome_128_Windows_10"},
    {"browserName": "MicrosoftEdge", "browserVersion": "127.0", "platformName": "macOS Ventura", "label": "Edge_127_macOS_Ventura"},
    {"browserName": "Firefox", "browserVersion": "130.0", "platformName": "Windows 11", "label": "Firefox_130_Windows_11"},
    {"browserName": "internet explorer", "browserVersion": "11.0", "platformName": "Windows 10", "label": "IE_11_Windows_10"},
]

def pytest_generate_tests(metafunc):
    if "browser_config" in metafunc.fixturenames:
        metafunc.parametrize("browser_config", BROWSER_MATRIX,
                             ids=[x["label"] for x in BROWSER_MATRIX])

@pytest.fixture
def remote_driver(browser_config, request):
    username, key = os.getenv("LT_USERNAME"), os.getenv("LT_ACCESS_KEY")
    if not username or not key:
        pytest.fail("Set LT_USERNAME and LT_ACCESS_KEY in your .env file.")

    options_class = {
        "Chrome": webdriver.ChromeOptions,
        "MicrosoftEdge": webdriver.EdgeOptions,
        "Firefox": webdriver.FirefoxOptions,
        "internet explorer": webdriver.IeOptions,
    }[browser_config["browserName"]]
    options = options_class()
    options.set_capability("browserName", browser_config["browserName"])
    options.set_capability("browserVersion", browser_config["browserVersion"])
    options.set_capability("platformName", browser_config["platformName"])
    options.set_capability("LT:Options", {
        "username": username,
        "accessKey": key,
        "build": "Selenium-Python-101-Assignment",
        "name": f"{request.node.name}-{browser_config['label']}",
        "video": True,
        "visual": True,
        "network": True,
        "console": True,
    })

    driver = webdriver.Remote(command_executor=GRID_URL, options=options)
    driver.set_page_load_timeout(20)
    print(f"TestMu session ID: {driver.session_id} | {browser_config['label']}")
    yield driver
    driver.quit()
