from selenium import webdriver
from selectolax.parser import HTMLParser
from time import sleep
from archiver_packages.utilities.selenium_utils import slow_croll



def scrape_info(driver:webdriver.Chrome,yt_link:str,delay:int) -> str:

    driver.get(yt_link)
    slow_croll(driver,delay) # Scroll to description section
    sleep(delay+2)

    html = HTMLParser(driver.page_source, detect_encoding=True)

    profile_image = html.css_first('yt-img-shadow#avatar img').attributes.get("src")
    profile_image = "".join(profile_image.replace("s88-c-k", "s48-c-k")) # Make profile img size 48x48

    return profile_image