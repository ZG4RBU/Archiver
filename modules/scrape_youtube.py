from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selectolax.parser import HTMLParser
from time import sleep
from modules.utilities.selenium_utils import slow_croll, page_scroll
import modules.htmls as htmls



def scrape_info(driver:webdriver.Chrome,yt_link:str,delay:int) -> str:

    driver.get(yt_link)
    slow_croll(driver,delay) #scroll to description section
    sleep(delay+2)

    html = HTMLParser(driver.page_source, detect_encoding=True)

    profile_image = html.css_first('yt-img-shadow#avatar img').attributes.get("src")
    profile_image = "".join(profile_image.replace("s88-c-k", "s48-c-k")) #make profile img size 48x48

    return profile_image


def parse_comment_text(driver:webdriver.Chrome,element:WebElement) -> str:
    """
    parse comments/replies text
    """

    #insert emojis in text
    emojis_imgs = element.find_elements(By.XPATH, './/yt-formatted-string[@id="content-text"]/img')
    for emoji_img in emojis_imgs:
        emoji = emoji_img.get_attribute('alt')
        driver.execute_script("arguments[0].innerHTML = arguments[1];", emoji_img, emoji)

    text = element.find_element(By.XPATH, './/yt-formatted-string[@id="content-text"]').text

    return text


def parse_comments(html:HTMLParser):

    like_count = html.css_first("[id='vote-count-middle']").text()

    channel_username = html.css_first("yt-img-shadow [id='img']").attributes.get("alt")

    comment_date = html.css_first("div[id='header-author'] yt-formatted-string a").text()

    channel_url = html.css_first("div[id='main'] div a").attributes.get("href")
    channel_url = "https://www.youtube.com" + channel_url

    channel_pfp = html.css_first("yt-img-shadow [id='img']").attributes.get("src")
    channel_pfp = channel_pfp.replace("s88-c-k", "s48-c-k")

    return (like_count,channel_username,comment_date,channel_url,channel_pfp)


def load_all_comments(driver:webdriver.Chrome,delay:float):
    """ Scroll to end of the page to load all comments. """

    # scroll to the bottom of the page
    page_end_count = 0
    while True:
        if page_scroll(driver,delay) == "page_end":
            page_end_count += 1
            if page_end_count > 3:
                break
        else:
            page_end_count = 0


def add_comments(driver:webdriver.Chrome,profile_image:str,output,delay:int):

    driver.implicitly_wait(delay+2) #reduce implicit wait to speed up parsing comments

    slow_croll(driver,delay) #scroll to description section and wait for comments to load
    load_all_comments(driver,delay)

    try:
        for element in driver.find_elements(By.XPATH, '//*[@id="contents"]//ytd-comment-thread-renderer'): #[:10]

            driver.execute_script("arguments[0].scrollIntoView();", element) #scroll to comment
            sleep(delay)

            if element.find_element(By.XPATH, './/*[@id="more"]').is_displayed(): #expand comment text
                element.find_element(By.XPATH, './/*[@id="more"]').click()

            text = parse_comment_text(driver,element)

            html = HTMLParser(element.get_attribute("innerHTML"))
            like_count,channel_username,comment_date,channel_url,channel_pfp = parse_comments(html)

            heart = element.find_element(By.XPATH, './/*[@id="creator-heart"]')
            if heart.is_displayed():
                heart = htmls.heart(profile_image)
            else: heart=""

            comment_box = htmls.comment_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart)
            divs = htmls.ending.divs

            if len(element.find_elements(By.XPATH, './/*[@id="more-replies"]')) == 0:
                #add comment HTML
                comment_box += divs
                output.write(comment_box)

            else:
                #add blue reply toggle
                reply_count = html.css_first("[id='more-replies'] button")

                try:
                    reply_count = reply_count.attributes.get("aria-label")
                except:
                    reply_count = reply_count.text()
                  
                more_replies_toggle = htmls.more_replies_toggle(reply_count)

                #add comment HTML
                comment_box += more_replies_toggle + divs
                output.write(comment_box)

                #add replies
                element.click() #fix element click intercepted
                element.find_element(By.XPATH, './/*[@id="more-replies"]').click()

                for reply in element.find_elements(By.XPATH, './/*[@id="replies"]//*[@id="expander-contents"]//ytd-comment-renderer'):

                    driver.execute_script("arguments[0].scrollIntoView();", reply) #slow scroll replies

                    text = parse_comment_text(driver,reply)

                    html = HTMLParser(reply.get_attribute("innerHTML"))
                    like_count,channel_username,comment_date,channel_url,channel_pfp = parse_comments(html)

                    heart = reply.find_element(By.XPATH, './/*[@id="creator-heart"]')
                    if heart.is_displayed():
                        heart = htmls.heart(profile_image)
                    else: heart=""

                    #add reply
                    reply_box = htmls.reply_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart)
                    output.write(reply_box) 

    except NoSuchElementException as e:
        print(f"No Such Element...{e}")
        pass