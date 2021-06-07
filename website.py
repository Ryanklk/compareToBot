from flask import Flask, render_template
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
    return '<h1> compareToBot </h1>'

@app.route('/search/<searchresult>')
def search_page(searchresult):
    search.send_keys(searchresult)
    search.send_keys(Keys.RETURN)
    names = []
    links = []
    items = driver.find_elements_by_class_name('col-xs-2-4.shopee-search-item-result__item')
    all_items = driver.find_elements_by_xpath('//div[@data-sqe="name"]')
    all_links = driver.find_elements_by_xpath('//a[@data-sqe="link"]')
    for i in range(len(all_items)):
        names += {all_items[i].find_element_by_xpath(".//*").text}
        links += {all_links[i].get_attribute("href")}
    driver.quit()
    return render_template('result.html', names = names, links = links, length = len(names))
