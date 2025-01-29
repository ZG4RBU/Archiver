import undetected_chromedriver as uc
from time import sleep
from random import uniform
import os
from typing import Callable



def get_window_size(driver):
    # Execute JavaScript to get screen width and height
    script = "return [window.screen.width, window.screen.height];"
    result = driver.execute_script(script)
    return result[0], result[1]



def kill_process(process_name:str):
    from psutil import process_iter

    if process_name in (p.name() for p in process_iter()):
        os.system(f"taskkill /f /im  {process_name}")


def chrome_setup(implicit_wait:int,profile:str,headless:bool=False,split_tabs:bool=False) -> uc.Chrome:
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    options.add_argument("--mute-audio")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    pc_user = os.getlogin()
    options.add_argument(rf'--user-data-dir=C:\Users\{pc_user}\AppData\Local\Google\Chrome\User Data')
    options.add_argument(f'--profile-directory={profile}')
    program_files = "Program Files" if "Google" in os.listdir("C:\\Program Files") else "Program Files (x86)"
    options.binary_location = f"C:\\{program_files}\\Google\\Chrome\\Application\\chrome.exe"

    if headless == True:
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920x1080")

    # Kill all chrome.exe processes to avoid chromedriver window already closed exception
    kill_process("chrome.exe")

    driver = uc.Chrome(options=options, headless=False)
    driver.implicitly_wait(implicit_wait)

    # Get window size
    width, height = get_window_size(driver)

    # Split windows size in half
    if split_tabs:
        width = width // 2

    # Set window size
    driver.set_window_size(width, height)

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
    sleep(delay+3)
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


async def slow_croll(tab,delay:Callable[[int],float]):
    for _ in range(3):
        scroll_amount = uniform(100,120)
        await tab.evaluate(f"window.scrollBy(0, {scroll_amount});")
        sleep(delay()+1)