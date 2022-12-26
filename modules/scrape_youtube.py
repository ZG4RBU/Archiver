from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import modules.htmls as htmls



def chrome_setup(implicit_wait:int,headless:str):
    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument("--start-maximized")
    options.add_argument("--mute-audio")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    
    if headless == "True":
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')

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
        sleep(delay+5)
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
    for _ in range(5):
        driver.execute_script("window.scrollBy(0,100)","")
        sleep(delay)



def scrape(link:str,delay:int,headless:str):

    driver = chrome_setup(implicit_wait=delay+5,headless=headless)

    driver.get(link)
    slow_croll(driver,delay) #scroll to description section 
    sleep(delay+2)

    subscribers = driver.find_element(By.XPATH, '//*[@id="owner-sub-count"]').text

    like_count = driver.find_element(By.XPATH, '//div[@id="segmented-like-button"]').text

    profile_image = driver.find_element(By.XPATH, '//yt-img-shadow[@id="avatar"]/img').get_attribute("src")
    profile_image = "".join(profile_image.replace("s88-c-k", "s48-c-k")) #make profile img size 48x48
    
    try:
        comments_count = driver.find_element(By.XPATH, '//h2[@id="count"]//span[1]').text
        comments_count += ' Comments'
    except:
        comments_count = "Comments are turned off."
    
    driver.quit()
    
    return subscribers,like_count,profile_image,comments_count;  


def add_comments(link:str,profile_image:str,output,delay:int,headless:str):

    driver = chrome_setup(implicit_wait=delay+2,headless=headless)
    
    driver.get(link)
    slow_croll(driver,delay) #scroll to description section 
    scroll_to_bottom(driver,delay)

    try:
        for element in driver.find_elements(By.XPATH, '//*[@id="contents"]//ytd-comment-thread-renderer'): #[:10]

            driver.execute_script("arguments[0].scrollIntoView();", element) #slow scroll comments
            sleep(delay)

            if element.find_element(By.XPATH, './/*[@id="more"]').is_displayed():
                element.find_element(By.XPATH, './/*[@id="more"]').click()
            
            #insert emojis in text
            emojis_imgs = element.find_elements(By.XPATH, './/yt-formatted-string[@id="content-text"]/img')
            for emoji_img in emojis_imgs:
                emoji = emoji_img.get_attribute('alt')
                driver.execute_script("arguments[0].innerHTML = arguments[1];", emoji_img, emoji)
            
            text = element.find_element(By.XPATH, './/yt-formatted-string[@id="content-text"]').text
            
            like_count = element.find_element(By.XPATH, './/*[@id="vote-count-middle"]').text
            
            #split comment header to username/date
            header = element.find_element(By.XPATH, './/div[@id="main"]//div[1]').text
            channel_username = header.split("\n")[0]
            comment_date = header.split("\n")[1]
            
            channel_url = element.find_element(By.XPATH, './/div[@id="main"]//div[1]//a').get_attribute('href')
            
            channel_pfp = str(element.find_element(By.XPATH, './/yt-img-shadow//*[@id="img"]').get_attribute('src'))
            channel_pfp = channel_pfp.replace("s88-c-k", "s48-c-k")
            
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
                reply_count = element.find_element(By.XPATH, './/*[@id="more-replies"]//button')
                try:
                    reply_count = reply_count.get_attribute('aria-label')
                except:
                    reply_count = reply_count.text
                  
                more_replies_toggle = htmls.more_replies_toggle(reply_count)
                
                #add comment
                comment_box += more_replies_toggle + divs
                output.write(comment_box)

                #add replies
                element.click() #fix element click intercepted
                element.find_element(By.XPATH, './/*[@id="more-replies"]').click()

                for reply in element.find_elements(By.XPATH, './/*[@id="replies"]//*[@id="expander-contents"]//ytd-comment-renderer'):
                    
                    driver.execute_script("arguments[0].scrollIntoView();", reply) #slow scroll replies

                    #get text
                    emojis_imgs = reply.find_elements(By.XPATH, './/yt-formatted-string[@id="content-text"]/img')
                    for emoji_img in emojis_imgs:
                        emoji = emoji_img.get_attribute('alt')
                        driver.execute_script("arguments[0].innerHTML = arguments[1];", emoji_img, emoji)
                    text = reply.find_element(By.XPATH, './/yt-formatted-string[@id="content-text"]').text
                    
                    like_count = reply.find_element(By.XPATH, './/*[@id="vote-count-middle"]').text
                    
                    #split comment head to username/date
                    header = reply.find_element(By.XPATH, './/div[@id="main"]//div[1]').text
                    channel_username = header.split("\n")[0]
                    comment_date = header.split("\n")[1]
                    
                    channel_url = reply.find_element(By.XPATH, './/div[@id="main"]//div[1]//a').get_attribute('href')
                    
                    channel_pfp = reply.find_element(By.XPATH, './/yt-img-shadow//*[@id="img"]').get_attribute('src')
                    channel_pfp = channel_pfp.replace("s88-c-k", "s48-c-k")
                    
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


