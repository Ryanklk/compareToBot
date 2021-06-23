from flask import Flask, render_template
from flask import request
from bs4 import BeautifulSoup
import selenium
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(10)
driver.get('https://shopee.sg/?gclid=Cj0KCQjwhr2FBhDbARIsACjwLo1PDpFJlxLU7-NGwfghB_Nw5Xhfa8IuYgyMC1jviTu_CiwSNhIOcDEaAvW5EALw_wcB')
search = driver.find_element_by_class_name('shopee-searchbar-input__input')
html_text = requests.get('https://shopee.sg/search?keyword=nintendo%20switch').text
app = Flask(__name__)

@app.route('/')
def hello_world():
    #return render_template('asdf.html')
    return render_template('index.html')

@app.route('/destination.html')
def destination():
    searched = request.args.get('product')
    country = request.args.get('location')
    search.send_keys(searched)
    search.send_keys(Keys.RETURN)
    names = []
    links = []
    countries = []
    images = []
    prices = []
    items = driver.find_elements_by_class_name('col-xs-2-4.shopee-search-item-result__item')
    for _ in range(15):
        try:
            all_items = driver.find_elements_by_xpath('//div[@data-sqe="name"]')
            all_links = driver.find_elements_by_xpath('//a[@data-sqe="link"]')
            all_locations = driver.find_elements_by_xpath('//div[@class="_2CWevj"]')
            all_images = driver.find_elements_by_xpath('//img[@class="mxM4vG _2GchKS"]')
            all_prices = driver.find_elements_by_xpath('//span[@class="_29R_un"]')
            driver.execute_script("return arguments[0].scrollIntoView(true);",all_items[_])
            time.sleep(0.5)
        except:
            time.sleep(0.5)
    for i in range(len(all_items)):
        if country == all_locations[i].text or country == 'all':
            names += {all_items[i].find_element_by_xpath(".//*").text}
            links += {all_links[i].get_attribute("href")}
            countries += {all_locations[i].text}
            images += {all_images[i].get_attribute("src")}
            prices += {all_prices[i].text}

    driver.quit()
    #return render_template('result.html', names = names, links = links, length = len(names), countries=countries, images = images, prices = prices)
    return render_template('shop.html', names = names, links = links, length = len(names), countries=countries, images = images, prices = prices)
