# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import bs4
import pandas as pd
import chromedriver_binary
import configparser

import time
import random
import sys

#from logging import getLogger, StreamHandler, DEBUG
#logger = getLogger(__name__)
#handler = StreamHandler()
#handler.setLevel(DEBUG)
#logger.setLevel(DEBUG)
#logger.addHandler(handler)
#logger.propagate = False

def main():

    username = sys.argv[1]
    print("start crawling follower of " + username)

    options = Options()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    time.sleep(2)

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
    time.sleep(3)
    follower_button = driver.find_elements_by_css_selector("li.Y8-fY")[1]
    follower_button.click()
    time.sleep(3)

    dialog = driver.find_element_by_css_selector("div.isgrP")

    # scroll popup window
    height = driver.execute_script("return document.querySelectorAll('div.isgrP')[0].scrollHeight;")
    for i in range(0, height, 100):
        driver.execute_script("document.querySelectorAll('div.isgrP')[0].scrollTo(0, " + str(i) + ");")
        time.sleep(0.5)

    page_url = driver.page_source
    soup = bs4.BeautifulSoup(page_url,"lxml")
    elm = soup.find_all("a", {"class": "FPmhX notranslate _0imsa"})
    followers = []
    for e in elm:
        followers.append(e.text)
        print(e.text)

    df = pd.Series(followers)
    df.to_csv("insta_followers_of_" + username + ".csv")
    print("csv file is created.")
    driver.close()

if __name__ == '__main__':
    main()
