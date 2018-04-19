# _*_ encoding: utf-8 _*_
__author__ = 'Phantom3389'
__date__ = '2018/4/19 14:06'
import redis
import os
import time
import json
import random
from selenium import webdriver
from redisspider.settings import REDIS_URL

login_url = "http://www.jobbole.com/login/"

red = redis.Redis.from_url(REDIS_URL, db=2, decode_responses=True)


def get_cookies(account, password):
    # windows平台
    if os.name == 'nt':
        browser = webdriver.Chrome(executable_path="D://chromedriver.exe")
    # linux平台
    else:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800, 600))
        display.start()

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        browser = webdriver.Chrome(executable_path="/www/wwwroot/scrapy.detectivehao.cn/chromedriver", chrome_options=options)


    browser.get(login_url)
    time.sleep(10)
    browser.find_element_by_css_selector("#jb_user_login").send_keys(account)
    browser.find_element_by_css_selector("#jb_user_pass").send_keys(password)
    browser.find_element_by_css_selector("#jb_user_login_btn").click()

    Cookies = browser.get_cookies()
    Cookies_dict= {}
    for cookie in Cookies:
        Cookies_dict[cookie['name']] = cookie['value']
    #print(type(Cookies_dict))
    #print(Cookies_dict)
    browser.close()
    return json.dumps(Cookies_dict)


def init_cookie(red, spidername):
    raindex = random.randint(0, red.llen(spidername+":zhanghao")-1)
    user_dict = json.loads(red.lrange(spidername+":zhanghao", raindex, raindex)[0])
    user = user_dict["username"]
    password = user_dict["password"]
    if red.get("%s:Cookies" % spidername) is None:
        cookie = get_cookies(user, password)
        red.set("%s:Cookies" % spidername, cookie)


def update_cookie(red, accountText, spidername):
    #red = redis.Redis()
    pass


def remove_cookie(red, spidername, accountText):
    #red = redis.Redis()
    #red.delete("%s :Cookies: %s" % (spidername, accountText))
    pass

if __name__ == "__main__":
    init_cookie(red, "jobbole")
