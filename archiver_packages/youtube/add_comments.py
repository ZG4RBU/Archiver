from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selectolax.parser import HTMLParser
from time import sleep
import archiver_packages.youtube_html_elements as youtube_html_elements
from archiver_packages.utilities.selenium_utils import slow_croll, page_scroll
from archiver_packages.youtube.extract_comment_emoji import convert_youtube_emoji_url_to_emoji



def format_text_emoji(input_text:str) -> str:
    lines = input_text.split('\n')
    merged_lines = []

    for i in range(len(lines)):
        if i > 0 and len(lines[i]) == 1:
            merged_lines[-1] += ' ' + lines[i]
        else:
            merged_lines.append(lines[i])

    return '\n'.join(merged_lines)


def parse_comment_text(driver:webdriver.Chrome,element:WebElement) -> str:
    """
    Parse comments/replies text.
    """

    emojis_imgs = element.find_elements(By.XPATH, './/*[@id="content-text"]//img')

    for emoji_img in emojis_imgs:
        emoji_url = emoji_img.get_attribute('src')
        emoji = convert_youtube_emoji_url_to_emoji(emoji_url)

        # Execute JavaScript to set the inner text of the element
        driver.execute_script(f"arguments[0].innerText = '{emoji}';", emoji_img)

    text = element.find_element(By.XPATH, './/*[@id="content-text"]').text
    text = format_text_emoji(text)

    return text


def style_reply_mention(input_text:str) -> str:
    if input_text.strip().startswith('@'):

        # Extract the first word
        words = input_text.split(' ', 1)

        if len(words) > 1: #Check if there is more than one word to ensure that we have an actual mention instead of a one-word reply that starts with the '@' symbol
            first_word, remaining_text = words

            # Apply style to the mention
            input_text = f'<span style="color: #3EA6FF;">{first_word}</span> {remaining_text}'

    return input_text


def parse_comments(html:HTMLParser):

    like_count = html.css_first("[id='vote-count-middle']").text()

    channel_username = html.css_first("[id='author-text']").attributes.get("href")[1:]

    comment_date = html.css_first("div[id='header-author'] span[id='published-time-text'] a").text()

    channel_url = html.css_first("div[id='main'] div a").attributes.get("href")
    channel_url = "https://www.youtube.com" + channel_url

    channel_pfp = html.css_first("yt-img-shadow [id='img']").attributes.get("src")
    channel_pfp = channel_pfp.replace("s88-c-k", "s48-c-k")

    return (like_count,channel_username,comment_date,channel_url,channel_pfp)


def load_all_comments(driver:webdriver.Chrome,delay:float,max_comments:int):
    """ Scroll to end of the page to load all comments. """

    # Scroll to the bottom of the page
    page_end_count = 0
    while True:
        if page_scroll(driver,delay) == "page_end":
            page_end_count += 1
            if page_end_count > 3:
                break
        else:
            page_end_count = 0

        comments = driver.find_elements(By.XPATH, '//*[@id="contents"]//ytd-comment-thread-renderer')
        comments_count = len(comments)

        if comments_count > max_comments:
            break


def remove_video_recommendations(driver:webdriver.Chrome):
    items = driver.find_element(By.XPATH, '//ytd-watch-next-secondary-results-renderer')
    driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", items)


def add_comments(driver:webdriver.Chrome,profile_image:str,output,delay:int,max_comments:int):

    remove_video_recommendations(driver)

    driver.implicitly_wait(delay) # Reduce implicit wait to speed up parsing comments

    slow_croll(driver,delay) # Scroll to description section and wait for comments to load

    print("Loading comments...")
    load_all_comments(driver,delay,max_comments)

    print("Fetching comments...")
    comments = driver.find_elements(By.XPATH, '//*[@id="contents"]//ytd-comment-thread-renderer')[:max_comments]
    comments_count = len(comments)
    comments_fetched = 0

    try:
        for comment in comments:
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
                heart = youtube_html_elements.heart(profile_image)
            else:
                heart = ""

            comment_box = youtube_html_elements.comment_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart)
            divs = youtube_html_elements.ending.divs

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

                more_replies_toggle = youtube_html_elements.more_replies_toggle(reply_count)

                # Add comment HTML
                comment_box += more_replies_toggle + divs
                output.write(comment_box)

                # Add replies
                comment.click() # To fix element click intercepted
                comment.find_element(By.XPATH, './/*[@id="more-replies"]').click()

                # Click Show more replies button
                while True:
                    sleep(3)
                    if len(comment.find_elements(By.XPATH, './/button[@aria-label="Show more replies"]')) > 0:
                        comment.click() # To fix element click intercepted
                        show_more_replies_btn = comment.find_element(By.XPATH, './/button[@aria-label="Show more replies"]')
                        driver.execute_script("arguments[0].scrollIntoView();", show_more_replies_btn)
                        driver.execute_script("window.scrollBy(0, -200)")
                        sleep(1)
                        show_more_replies_btn.click()
                    else:
                        break

                replies = comment.find_elements(By.XPATH, './/*[@id="replies"]//*[@id="expander-contents"]//ytd-comment-view-model')

                for reply in replies:

                    driver.execute_script("arguments[0].scrollIntoView();", reply) # Slow scroll replies

                    text = parse_comment_text(driver,reply)
                    text = style_reply_mention(text)

                    html_reply = HTMLParser(reply.get_attribute("innerHTML"))
                    like_count,channel_username,comment_date,channel_url,channel_pfp = parse_comments(html_reply)

                    # Add heart icon if present
                    heart = html_reply.css_first('#creator-heart-button')
                    if heart:
                        heart = youtube_html_elements.heart(profile_image)
                    else:
                        heart = ""

                    # Add reply
                    reply_box = youtube_html_elements.reply_box(channel_url,channel_pfp,channel_username,comment_date,text,like_count,heart)
                    output.write(reply_box) 

    except NoSuchElementException as e:
        print(f"No Such Element...{e}")
        pass