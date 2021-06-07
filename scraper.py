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

#tried beautifulsoup & selenium; selenium works better 

#code to go to shopee website
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(10)
driver.get('https://shopee.sg/?gclid=Cj0KCQjwhr2FBhDbARIsACjwLo1PDpFJlxLU7-NGwfghB_Nw5Xhfa8IuYgyMC1jviTu_CiwSNhIOcDEaAvW5EALw_wcB')
search = driver.find_element_by_class_name('shopee-searchbar-input__input')
html_text = requests.get('https://shopee.sg/search?keyword=nintendo%20switch').text

#search for the item in the shopee searchbar
x = input("What are you looking for?")
search.send_keys(x)
search.send_keys(Keys.RETURN)

#outputs item name and item link
items = driver.find_elements_by_class_name('col-xs-2-4.shopee-search-item-result__item')
all_items = driver.find_elements_by_xpath('//div[@data-sqe="name"]')
all_links = driver.find_elements_by_xpath('//a[@data-sqe="link"]')
for i in range(len(all_items)):
    print(all_items[i].find_element_by_xpath(".//*").text)
    print(all_links[i].get_attribute("href"))
driver.quit()
