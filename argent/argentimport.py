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


argenturl = f'chrome-extension://{argentidentifikator}/index.html'


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
    driver.get(argenturl)




    # Memorize the primary browser window.
    initial_window_handle = driver.current_window_handle
    time.sleep(1.337)  # Wait for a short while.

    # Close any additional browser tabs.
    for tab in driver.window_handles:
        if tab != initial_window_handle:
            driver.switch_to.window(tab)
            print("Cleaning extra tabs...")
            driver.close()

    # Go back to the primary browser window.
    driver.switch_to.window(initial_window_handle)
# ----------
    driver.get(argenturl)
    click_if_exists(driver,(By.XPATH,'//*[@id="root"]/div/div/div/div/div[1]/div/div[3]/button[2]'))
    pyperclip.copy(seed)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    click_if_exists(driver,(By.XPATH,'//*[@id="root"]/div/div/div/div/div[1]/div/form/div[3]/button'))
    click_if_exists(driver,(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div/form/input[1]'))
    pyperclip.copy(passwd)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    click_if_exists(driver,(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div/form/input[2]'))
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)
    #  -------
    # continue click
    click_if_exists(driver,(By.XPATH,'//*[@id="root"]/div/div/div/div/div[1]/div/form/div/button'))
    #  -------
    click_if_exists(driver,(By.XPATH,'//*[@id="root"]/div/div/div/div/div[1]/div/button'))
    driver.quit()
    requests.get(close_url)
    logger.info(f"profile {ads_id} done")

if __name__ == '__main__':
    if argentidentifikator == '':
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

