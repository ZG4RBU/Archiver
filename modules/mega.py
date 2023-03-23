import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


def chrome_setup(implicit_wait:int,headless:str):
    options = Options()
    options.add_argument('--disable-notifications')
    options.add_argument("--start-maximized")
    options.add_argument("--mute-audio")

    if headless == "True":
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')

    s = Service('driver/chromedriver.exe')
    driver = webdriver.Chrome(options=options,service=s)
    driver.implicitly_wait(implicit_wait)

    return driver


def mega_upload(login:str,password:str,delay:int,headless:str) -> list:
    
    driver: webdriver.Chrome = chrome_setup(implicit_wait=delay+10,headless=headless)

    driver.get("https://mega.nz/login")

    longwait=WebDriverWait(driver, 60*2) #for long waits
    try:    

        longwait.until(EC.element_to_be_clickable((By.ID, "login-name2")))
        driver.find_element(By.ID, "login-name2").send_keys(login)
        driver.find_element(By.ID, "login-password2").send_keys(password)

        driver.find_element(By.XPATH, '//*[@id="login_form"]/button/child::span').click()

        #check if login is successful
        longwait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="transfer-bar-overlay"]')))

        mega_links_list = []

        os.chdir("upload") #NOTE: change dir to "upload" folder

        for file in sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime):
            
            longwait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='button link-button dropdown fm-uploads']")))
            driver.find_element(By.XPATH, "//div[@class='button link-button dropdown fm-uploads']").click()
            driver.find_element(By.ID, "fileselect1").send_keys(os.getcwd()+'/'+file) #needs full path
            
            sleep(delay+3)
            #check duplicate/wait until uploaded
            if driver.find_element(By.ID, "duplicate-conflict-title").is_displayed():
                #close tab
                driver.find_element(By.XPATH, "//div[@aria-labelledby='duplicate-conflict-title']/child::*").click()
            else:
                WebDriverWait(driver, 60**2*5, poll_frequency=20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='transfer-progress-txt' and text()='Completed']")))

            #click on get link
            COLUMN = driver.find_element(By.XPATH, f"//span[@class='tranfer-filetype-txt' and text()='{file}']/parent::*/ancestor::tr")
            act=ActionChains(driver)
            act.move_to_element(COLUMN).click().perform()
            driver.find_element(By.XPATH, "//button[@data-simpletip='Get link']").click()
            #click agree
            try:
                driver.find_element(By.XPATH, "//div[@aria-labelledby='copyrights-dialog-title']/footer/div/button[2]").click()
            except: 
                pass

            #copy link
            mega_link = longwait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@value,'https://mega.nz/file/')]"))).get_attribute("value")
            if any(x in file for x in [".mp4",".mov"]):
                mega_links_list.append(mega_link.replace('file', 'embed')+'!1a')
            else:
                mega_links_list.append(mega_link)
            #close tab
            driver.find_element(By.XPATH, "//div[@aria-labelledby='export-links-title']/child::*").click()

        os.chdir("../") #NOTE: back to main dir
        driver.quit()
            
    except NoSuchElementException as e:
        print(f"No Such Element...{e}")
        pass

    return mega_links_list