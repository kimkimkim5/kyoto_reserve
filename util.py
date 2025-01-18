from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logger
import csv

SLEEP_TIME = 3

KYOTO_FACILITY_USERNAME = os.environ.get('KYOTO_FACILITY_USERNAME')
KYOTO_FACILITY_PASSWORD = os.environ.get('KYOTO_FACILITY_PASSWORD')

SELECT_MONTH = 0
SELECT_DAY = []

POPUP_ACCEPT = 1
POPUP_DISMISS = 2

file_path = 'input.csv'

# CSVファイルを読み込む
def read_csvfile():
    global SELECT_MONTH, SELECT_DAY
    file = open(file_path, mode='r', encoding='utf-8')
    index = 0
    reader = csv.reader(file)
    for row in reader:
        if index == 0:
            SELECT_MONTH = row[0]
        else:
            SELECT_DAY = row
        index = index + 1


def link_click(driver, link_text, index):
    logger.debug(f'link_text START {link_text}')
    # エレメント取得
    basketball_element = driver.find_elements(By.LINK_TEXT, link_text)
    # クリック
    basketball_element[index].click()
    logger.debug(f'link_text END {link_text}')
    time.sleep(SLEEP_TIME)


def xpath_click(driver, xpath_text, index):
    logger.debug(f'xpath_click START {xpath_text}')
    # エレメント取得
    element = driver.find_elements(By.XPATH, xpath_text)
    # クリック
    element[index].click()
    logger.debug(f'xpath_click END {xpath_text}')
    time.sleep(SLEEP_TIME)


def get_elements_xpath(driver, xpath_text):
    logger.debug(f'get_element_xpath START {xpath_text}')
    # エレメント取得
    elements = driver.find_elements(By.XPATH, xpath_text)
    logger.debug(f'get_element_xpath END {xpath_text}')
    return elements


def popup_click(driver, f):
    logger.debug(f'popup_click START {f}')
    alert = driver.switch_to.alert
    if f == POPUP_ACCEPT:
        alert.accept()
    else:
        alert.dismiss()
    logger.debug(f'popup_click END {f}')
    time.sleep(SLEEP_TIME)


def switch_window(driver, all_windows, original_window):
    logger.debug(f'switch_window START')
    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            break
    time.sleep(SLEEP_TIME)
    logger.debug(f'switch_window END')


def set_textbox(driver, xpath_text, value, index):
    logger.debug(f'set_textbox START {value}')
    # エレメント取得
    textbox = driver.find_elements(By.XPATH, xpath_text)
    textbox[index].clear()
    textbox[index].send_keys(value)
    logger.debug(f'set_textbox END {value}')
    time.sleep(SLEEP_TIME)



