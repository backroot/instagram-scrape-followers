# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import bs4
import pandas as pd
import chromedriver_binary
import configparser

import time
import random
import sys

def main():

    username = sys.argv[1]
    print("start crawling follower of " + username)

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.set_script_timeout(300)
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, 'username')))

    # login
    config = configparser.ConfigParser()
    config.read('config.ini')
    id = driver.find_element_by_name("username")
    u = config.get('account', 'username')
    id.send_keys(u)
    password = driver.find_element_by_name("password")
    p = config.get('account', 'password')
    password.send_keys(p)
    password.send_keys(Keys.RETURN)
    time.sleep(3)

    driver.get('https://www.instagram.com/' + username + '/')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "Y8-fY")))
    follower_button = driver.find_elements_by_css_selector("li.Y8-fY")[1]
    follower_button.click()
    time.sleep(10)

    # You can get followers by scrolling the follower popup window.
    height = driver.execute_script("return document.querySelectorAll('div.isgrP')[0].scrollHeight;")
    i = 0
    before_top = 0
    while True:
        i += 100
        try: 
            driver.execute_script("document.querySelectorAll('div.isgrP')[0].scrollTo(0, " + str(i) + ");")
            time.sleep(0.5)
            height = driver.execute_script("return document.querySelectorAll('div.isgrP')[0].scrollHeight;")
            top = driver.execute_script("return document.querySelectorAll('div.isgrP')[0].scrollTop;")
            print("\rfollowers window scrolling... {0}/{1}".format(top, height), end='', flush=True)
            if before_top == top:
                break
            before_top = top
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
            break

    print("")
    page_url = driver.page_source
    soup = bs4.BeautifulSoup(page_url,"lxml")
    elm = soup.find_all("a", {"class": "FPmhX notranslate _0imsa"})
    followers = []
    for e in elm:
        followers.append(e.text)
        print(e.text)

    df = pd.Series(followers)
    df.index = df.index + 1
    df.to_csv("insta_followers_of_" + username + ".csv", header=False)
    print("csv file is created.")
    driver.close()

if __name__ == '__main__':
    main()
