from selenium import webdriver
import undetected_chromedriver as uc
from time import sleep
from random import uniform



def chrome_setup(implicit_wait:int,headless:bool=False) -> uc.Chrome:
    options = uc.ChromeOptions()
    #options.add_argument("--window-size=1920x1080")
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    options.add_argument("--mute-audio")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    if headless == True:
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920x1080")

    driver = uc.Chrome(options=options)
    driver.implicitly_wait(implicit_wait)

    return driver


def page_scroll(driver,delay:int) -> str|None:
    ''' Scroll the webpage. return str if reached to the bottom. '''

    old_position = 0
    new_position = None

    # Get old scroll position
    old_position = driver.execute_script(
            ("return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"))
    # Wait and scroll
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

    if new_position == old_position: 
        return "page_end"


def slow_croll(driver:webdriver.Chrome,delay:int):
    for _ in range(3):
        driver.execute_script("window.scrollBy(0,100)","")
        sleep(delay)