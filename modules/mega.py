from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
from time import sleep



def mega_upload(driver:webdriver.Chrome,login:str,password:str,delay:int,files:list[str],embed:bool=True) -> list:

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

        for file in files:

            filepath = Path(file).resolve()

            longwait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='button link-button dropdown fm-uploads']")))
            driver.find_element(By.XPATH, "//div[@class='button link-button dropdown fm-uploads']").click()
            driver.find_element(By.ID, "fileselect1").send_keys(str(filepath)) #required full path

            sleep(delay+3)

            #check duplicate/wait until uploaded
            if driver.find_element(By.ID, "duplicate-conflict-title").is_displayed():
                #close tab
                driver.find_element(By.XPATH, "//div[@aria-labelledby='duplicate-conflict-title']/child::*").click()
            else:
                WebDriverWait(driver, 60**2*5, poll_frequency=20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='transfer-progress-txt' and text()='Completed']")))

            #click on get link
            column = driver.find_element(By.XPATH, f"//span[@class='tranfer-filetype-txt' and text()='{filepath.name}']/parent::*/ancestor::tr")
            act=ActionChains(driver)
            act.move_to_element(column).click().perform()
            driver.find_element(By.XPATH, "//button[@data-simpletip='Get link']").click()
            #click agree
            try:
                driver.find_element(By.XPATH, "//div[@aria-labelledby='copyrights-dialog-title']/footer/div/button[2]").click()
            except: 
                pass

            #copy link
            mega_link = longwait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@value,'https://mega.nz/file/')]"))).get_attribute("value")
            if any(x in file for x in [".mp4",".mov"]) and embed:
                mega_links_list.append(mega_link.replace('file', 'embed')+'!1a')
            else:
                mega_links_list.append(mega_link)
            #close tab
            driver.find_element(By.XPATH, "//div[@aria-labelledby='export-links-title']/child::*").click()

            
    except NoSuchElementException as e:
        print(f"No Such Element...{e}")
        pass

    return mega_links_list