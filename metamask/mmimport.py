import requests,time,sys,pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    JavascriptException
)
from config import *
from loguru import logger


mmurl = f'chrome-extension://{mmidentifikator}/home.html'



def click_if_exists(driver, locator):
    """
    Tries to find and click an element on the web page using its XPATH locator.
    """
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except ElementClickInterceptedException:
            print("ElementClickInterceptedException")
            attempts += 1
            time.sleep(3)
        except TimeoutException:
            print("timeoutException")
            return False
        except StaleElementReferenceException:
            print("stale element")
            attempts += 1
            time.sleep(3)
        except JavascriptException:
            element = driver.find_element(*locator)
            driver.execute_script('arguments[0].click()', element)
            return True
    return False


def argimport(seed,passwd,ads_id):
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
    close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id
    resp = requests.get(open_url).json()
    if resp["code"] != 0:
        print(resp["msg"])
        print("please check ads_id")
        sys.exit()
    # setup
    chrome_driver = resp["data"]["webdriver"]
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
    driver.implicitly_wait(15)
    driver.maximize_window()
    driver.get(mmurl)

    # clicks
    click_if_exists(driver,(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div/div/button'))
    click_if_exists(driver,(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]'))
    click_if_exists(driver,(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button'))
    pyperclip.copy(seed)
    element = driver.find_element(By.CSS_SELECTOR,'#import-srp__srp-word-0') 
    element.send_keys(Keys.CONTROL, 'v')
    # PASSWORD
    pyperclip.copy(passwd)
    element = driver.find_element(By.CSS_SELECTOR,'#password')   
    element.send_keys(Keys.CONTROL, 'v')
    element = driver.find_element(By.CSS_SELECTOR,'#confirm-password')
    element.send_keys(Keys.CONTROL, 'v')
    click_if_exists(driver,(By.XPATH,'//*[@id="create-new-vault__terms-checkbox"]'))
    click_if_exists(driver,(By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button'))
    driver.quit()
    requests.get(close_url)
    logger.info(f"profile {ads_id} done")


if __name__ == '__main__':
    if mmidentifikator == '':
        logger.error("введи идентификатор!")
        sys.exit()

    if password == '':
        logger.error('введи пароль!')
        sys.exit()

    if len(ids) != len(seeds):
        logger.error("Колво сид-фраз и adspower ids не совпадает")
        sys.exit()
    
    for i,seed in enumerate(seeds):
        argimport(seeds[i],password,ids[i])

