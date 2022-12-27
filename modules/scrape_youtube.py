from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import modules.htmls as htmls
from selectolax.parser import HTMLParser


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

    s = Service('driver/chromedriver.exe')
    driver = webdriver.Chrome(options=options,service=s)
    driver.implicitly_wait(implicit_wait)

    return driver


def scroll_to_bottom(driver:webdriver.Chrome,delay:int):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        sleep(delay+3)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))


def slow_croll(driver:webdriver.Chrome,delay:int):
    for _ in range(3):
        driver.execute_script("window.scrollBy(0,100)","")
        sleep(delay)



def scrape(link:str,delay:int,headless:str):

    driver = chrome_setup(implicit_wait=delay+5,headless=headless)

    driver.get(link)
    slow_croll(driver,delay) #scroll to description section
    sleep(delay+2)

    html = HTMLParser(driver.page_source)

    subscribers = html.css_first('#owner-sub-count').text()

    like_count = html.css_first('div#segmented-like-button').css_first("span[role='text']").text()

    profile_image = html.css_first('yt-img-shadow#avatar img').attributes.get("src")
    profile_image = "".join(profile_image.replace("s88-c-k", "s48-c-k")) #make profile img size 48x48

    try:
        comments_count = html.css_first("h2[id='count'] span").text()
        comments_count += ' Comments'
    except:
        comments_count = "Comments are turned off."

    driver.quit()

    return subscribers,like_count,profile_image,comments_count;


def comment_elements(html:HTMLParser):

    text = html.css_first('yt-formatted-string[id="content-text"]').text()

    like_count = html.css_first("[id='vote-count-middle']").text()

    channel_username = html.css_first("yt-img-shadow [id='img']").attributes.get("alt")

    comment_date = html.css_first("div[id='header-author'] yt-formatted-string a").text()

    channel_url = html.css_first("div[id='main'] div a").attributes.get("href")

    channel_pfp = html.css_first("yt-img-shadow [id='img']").attributes.get("src")
    channel_pfp = channel_pfp.replace("s88-c-k", "s48-c-k")

    return text,like_count,channel_username,comment_date,channel_url,channel_pfp


def add_comments(link:str,profile_image:str,output,delay:int,headless:str):

    driver = chrome_setup(implicit_wait=delay+2,headless=headless)

    driver.get(link)
    slow_croll(driver,delay) #scroll to description section and wait for comments to load
    scroll_to_bottom(driver,delay) #scroll to end of the page to load all comments

    try:
        for element in driver.find_elements(By.XPATH, '//*[@id="contents"]//ytd-comment-thread-renderer'): #[:10]

            driver.execute_script("arguments[0].scrollIntoView();", element) #slow scroll comments
            sleep(delay)

            if element.find_element(By.XPATH, './/*[@id="more"]').is_displayed(): #expand comment text
                element.find_element(By.XPATH, './/*[@id="more"]').click()

            #insert emojis in text
            emojis_imgs = element.find_elements(By.XPATH, './/yt-formatted-string[@id="content-text"]/img')
            for emoji_img in emojis_imgs:
                emoji = emoji_img.get_attribute('alt')
                driver.execute_script("arguments[0].innerHTML = arguments[1];", emoji_img, emoji)

            html = HTMLParser(element.get_attribute("innerHTML"))
            text,like_count,channel_username,comment_date,channel_url,channel_pfp = comment_elements(html)

            heart = element.find_element(By.XPATH, './/*[@id="creator-heart"]')
            if heart.is_displayed():
                heart = htmls.heart(profile_image)
            else: heart=""

            comment_box = htmls.comment_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart)
            divs = htmls.ending.divs

            if len(element.find_elements(By.XPATH, './/*[@id="more-replies"]')) == 0:
                #add comment
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

                #add comment
                comment_box += more_replies_toggle + divs
                output.write(comment_box)

                #add replies
                element.click() #fix element click intercepted
                element.find_element(By.XPATH, './/*[@id="more-replies"]').click()

                for reply in element.find_elements(By.XPATH, './/*[@id="replies"]//*[@id="expander-contents"]//ytd-comment-renderer'):

                    driver.execute_script("arguments[0].scrollIntoView();", reply) #slow scroll replies

                    html = HTMLParser(reply.get_attribute("innerHTML"))
                    text,like_count,channel_username,comment_date,channel_url,channel_pfp = comment_elements(html)

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

    driver.quit()
