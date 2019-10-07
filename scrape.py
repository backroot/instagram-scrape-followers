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
import json
import re
import urllib.parse

def main():

    if len(sys.argv) <= 2:
        print("第１引数に username、第２引数に query_hash を指定してください。")
        sys.exit(1)

    username = sys.argv[1]
    query_hash = sys.argv[2]

    print("start crawling follower of " + username)
    print("query hash is " + query_hash)

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
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "isgrP")))

    user_id = driver.execute_script("return _sharedData['entry_data']['ProfilePage'][0]['graphql']['user']['id']")
    print("user id is " + user_id)

    source = driver.page_source

    source = source.rstrip()
    #js = re.findall(r'Consumer\.js', source)

    print(source)

    query = {
        "query_hash": query_hash,
        "variables": {
            "id": user_id,
            "include_reel": "true",
            "fetch_mutual": "false",
            "first": 12
        }
    }
    query = urllib.parse.quote(json.dumps(query))


    print(query)
    #driver.get('https://www.instagram.com/graphql/query/?' + query)

#    # You can get followers by scrolling the follower popup window.
#    height = driver.execute_script("return document.querySelectorAll('div.isgrP')[0].scrollHeight;")
#    i = 0
#    before_top = 0
#    while True:
#        i += 100
#        try: 
#            driver.execute_script("document.querySelectorAll('div.isgrP')[0].scrollTo(0, " + str(i) + ");")
#            time.sleep(0.5)
#            height = driver.execute_script("return document.querySelectorAll('div.isgrP')[0].scrollHeight;")
#            top = driver.execute_script("return document.querySelectorAll('div.isgrP')[0].scrollTop;")
#            print("\rfollowers window scrolling... {0}/{1}".format(top, height), end='', flush=True)
#            if before_top == top:
#                break
#            before_top = top
#        except TimeoutException as ex:
#            print("Exception has been thrown. " + str(ex))
#            break

    #print("")
    #page_url = driver.page_source
    #soup = bs4.BeautifulSoup(page_url,"lxml")
    #elm = soup.find_all("a", {"class": "FPmhX notranslate _0imsa"})
    #followers = []
    #for e in elm:
    #    followers.append(e.text)
    #    print(e.text)

    #df = pd.Series(followers)
    #df.index = df.index + 1
    #df.to_csv("insta_followers_of_" + username + ".csv", header=False)
    #print("csv file is created.")
    driver.close()

if __name__ == '__main__':
    main()
