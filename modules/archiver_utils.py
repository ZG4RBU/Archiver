from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from random import uniform
from webdriver_manager.chrome import ChromeDriverManager


def chrome_setup(implicit_wait:int,headless:str):
    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument("--start-maximized")
    options.add_argument("--mute-audio")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    if headless == "True":
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920x1080")

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options,service=s)
    driver.implicitly_wait(implicit_wait)

    return driver


def scroll_to_bottom(driver:webdriver.Chrome,delay:str):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        sleep(delay+5)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        driver.execute_script(f"window.scrollBy(0,{uniform(5,100)})","")
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))


def slow_croll(driver:webdriver.Chrome,delay:int):
    for _ in range(3):
        driver.execute_script("window.scrollBy(0,100)","")
        sleep(delay)