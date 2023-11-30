from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selectolax.parser import HTMLParser
from time import sleep
from archiver_packages.utilities.selenium_utils import slow_croll, page_scroll
import archiver_packages.htmls as htmls



def scrape_info(driver:webdriver.Chrome,yt_link:str,delay:int) -> str:

    driver.get(yt_link)
    slow_croll(driver,delay) # Scroll to description section
    sleep(delay+2)

    html = HTMLParser(driver.page_source, detect_encoding=True)

    profile_image = html.css_first('yt-img-shadow#avatar img').attributes.get("src")
    profile_image = "".join(profile_image.replace("s88-c-k", "s48-c-k")) # Make profile img size 48x48

    return profile_image


def parse_comment_text(driver:webdriver.Chrome,element:WebElement) -> str:
    """
    Parse comments/replies text.
    """

    # Insert emojis in text
    emojis_imgs = element.find_elements(By.XPATH, './/yt-formatted-string[@id="content-text"]/img')
    for emoji_img in emojis_imgs:
        emoji = emoji_img.get_attribute('alt')
        driver.execute_script("arguments[0].innerHTML = arguments[1];", emoji_img, emoji)

    text = element.find_element(By.XPATH, './/yt-formatted-string[@id="content-text"]').text

    return text


def style_reply_mention(input_text:str) -> str:
    if input_text.strip().startswith('@'):

        # Extract the first word
        first_word, remaining_text = input_text.split(' ', 1)

        # Apply style to the mention
        input_text = f'<span style="color: #3EA6FF;">{first_word}</span> {remaining_text}'

    return input_text


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

    # Scroll to the bottom of the page
    page_end_count = 0
    while True:
        if page_scroll(driver,delay) == "page_end":
            page_end_count += 1
            if page_end_count > 2:
                break
        else:
            page_end_count = 0


def add_comments(driver:webdriver.Chrome,profile_image:str,output,delay:int):

    driver.implicitly_wait(delay+2) # Reduce implicit wait to speed up parsing comments

    slow_croll(driver,delay) # Scroll to description section and wait for comments to load
    print("Loading comments...")
    load_all_comments(driver,delay)

    print("Fetching comments...")
    comments = driver.find_elements(By.XPATH, '//*[@id="contents"]//ytd-comment-thread-renderer')
    comments_count = len(comments)
    comments_fetched = 0

    try:
        for comment in comments: #[:10]
            comments_fetched += 1
            print(f"Fetched {comments_fetched}/{comments_count} comments.", end='\r')

            # Scroll to comment
            driver.execute_script("arguments[0].scrollIntoView();", comment)
            sleep(delay)

            # Expand comment text
            if comment.find_element(By.XPATH, './/*[@id="more"]').is_displayed():
                comment.find_element(By.XPATH, './/*[@id="more"]').click()

            text = parse_comment_text(driver,comment)

            html_comment = HTMLParser(comment.get_attribute("innerHTML"))
            like_count,channel_username,comment_date,channel_url,channel_pfp = parse_comments(html_comment)

            # Add heart icon if present
            heart = html_comment.css_first('#creator-heart-button')
            if heart:
                heart = htmls.heart(profile_image)
            else: 
                heart = ""

            comment_box = htmls.comment_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart)
            divs = htmls.ending.divs

            if len(comment.find_elements(By.XPATH, './/*[@id="more-replies"]')) == 0:
                # Add comment HTML
                comment_box += divs
                output.write(comment_box)

            else:
                # Add blue reply toggle
                reply_count = html_comment.css_first("[id='more-replies'] button")

                try:
                    reply_count = reply_count.attributes.get("aria-label")
                except:
                    reply_count = reply_count.text()

                more_replies_toggle = htmls.more_replies_toggle(reply_count)

                # Add comment HTML
                comment_box += more_replies_toggle + divs
                output.write(comment_box)

                # Add replies
                comment.click() # Fix element click intercepted
                comment.find_element(By.XPATH, './/*[@id="more-replies"]').click()

                # Click Show more replies button
                while True:
                    sleep(3)
                    if len(comment.find_elements(By.XPATH, './/button[@aria-label="Show more replies"]')) > 0:
                        comment.click() # Fix element click intercepted
                        show_more_replies_btn = comment.find_element(By.XPATH, './/button[@aria-label="Show more replies"]')
                        driver.execute_script("arguments[0].scrollIntoView();", show_more_replies_btn)
                        driver.execute_script("window.scrollBy(0, -200)")
                        sleep(1)
                        show_more_replies_btn.click()
                    else:
                        break

                replies = comment.find_elements(By.XPATH, './/*[@id="replies"]//*[@id="expander-contents"]//ytd-comment-renderer')

                for reply in replies:

                    driver.execute_script("arguments[0].scrollIntoView();", reply) # Slow scroll replies

                    text = parse_comment_text(driver,reply)
                    text = style_reply_mention(text)

                    html_reply = HTMLParser(reply.get_attribute("innerHTML"))
                    like_count,channel_username,comment_date,channel_url,channel_pfp = parse_comments(html_reply)

                    # Add heart icon if present
                    heart = html_reply.css_first('#creator-heart-button')
                    if heart:
                        heart = htmls.heart(profile_image)
                    else:
                        heart = ""

                    # Add reply
                    reply_box = htmls.reply_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart)
                    output.write(reply_box) 

    except NoSuchElementException as e:
        print(f"No Such Element...{e}")
        pass