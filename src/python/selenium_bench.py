from random import shuffle
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import string


def generate_random_ascii_string():
    random_ascii = list(string.ascii_letters + string.ascii_uppercase)
    random.shuffle(random_ascii)
    return "".join(random_ascii)


def delayed_typing(web_element, text):
    random_ascii = generate_random_ascii_string()
    for char in text:
        if random.randint(1, 10) == 5:
            web_element.send_keys(
                random_ascii[random.randint(0, len(random_ascii) - 1)]
            )
            sleep(random.randint(0, 5) / 5)
            web_element.send_keys(Keys.BACKSPACE)
        web_element.send_keys(char)
        sleep(
            round(random.randint(1, 5) / random.randint(25, 50), random.randint(0, 50))
        )
        if random.randint(1, 100) == 51:
            sleep(random.random() / random.randint(1, 25))


def create_driver(settings=[]):
    DRIVER_PATH = config("SELENIUM_DRIVER")
    if not DRIVER_PATH:
        print("Driver path not defined in .env file !")
        return None
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    if settings:
        for setting in settings:
            options.add_argument(setting)
    driver = webdriver.chrome.webdriver.WebDriver(
        options=options, executable_path=DRIVER_PATH
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
        },
    )
    return driver


def open_new_window(driver, url):
    driver.execute_script(f"window.open('{url}', 'new_window')")


def find_elements_by_aria_label(driver, label):
    return driver.find_elements_by_css_selector(f"[aria-label= '{label}']")
