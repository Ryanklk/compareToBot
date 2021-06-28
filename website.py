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
from selenium.webdriver.common.action_chains import ActionChains
app = Flask(__name__)

@app.route('/')
def hello_world():
    #return render_template('asdf.html')
    return render_template('Abouty.html')

class Product:
    def __init__(self,name,link,country,image,price,platform):
        self.name = name
        self.link = link
        self.country = country
        self.image = image
        self.price = price
        self.platform = platform


@app.route('/destination.html')
def destination():
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    driver = webdriver.Chrome(PATH)
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    driver.implicitly_wait(10)
    driver.get('https://shopee.sg/')
    search = driver.find_element_by_class_name('shopee-searchbar-input__input')

    searched = request.args.get('product')
    country = request.args.get('location')
    overseas = request.args.get('overseas')
    search.send_keys(searched)
    search.send_keys(Keys.RETURN)
    products = []
    items = driver.find_elements_by_class_name('col-xs-2-4.shopee-search-item-result__item')
    for _ in range(15):
        try:
            all_items = driver.find_elements_by_xpath('//div[@data-sqe="name"]')
            all_links = driver.find_elements_by_xpath('//a[@data-sqe="link"]')
            all_locations = driver.find_elements_by_xpath('//div[@class="_2CWevj"]')
            all_images = driver.find_elements_by_xpath('//img[@class="mxM4vG _2GchKS"]')
            all_prices =driver.find_elements_by_xpath('//div[@class="WTFwws _1lK1eK _5W0f35"]')
            driver.execute_script("return arguments[0].scrollIntoView(true);",all_items[_])
            time.sleep(0.3)
        except:
            time.sleep(0.3)
    for i in range(len(all_items)):
        if country == all_locations[i].text or overseas == 'all':
            names = all_items[i].find_element_by_xpath(".//*").text
            links = all_links[i].get_attribute("href")
            countries = all_locations[i].text
            images = all_images[i].get_attribute("src")
            prices = float(all_prices[i].find_element_by_class_name('_29R_un').text.replace(',',''))
            products += {Product(names,links,countries,images,prices,"Shopee")}


    driver.get('https://lazada.sg')
    search = driver.find_element_by_id('q')

    #x = input("What are you looking for?")
    search.send_keys(searched)
    search.send_keys(Keys.RETURN)
    #driver.implicitly_wait(5)
    #driver.quit()

    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(5)
    #driver.execute_script("window.scrollTo(0, 1040)")


    x = driver.find_elements_by_class_name("index__gridItem___3VkVO")
    #x = driver.find_elements_by_class_name("GridItem__title___8JShU")
    #b = driver.find_elements_by_class_name("index__image___1YObI ")
    #/html/body/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/a

    counter = 0



    for items in x:
        if counter == 4:
            ActionChains(driver).move_to_element(items).perform()
            counter = 0
            time.sleep(0.3)
        #print(x[i].find_element_by_tag_name("a").get_attribute("title"))
        #print(x[i].find_element_by_tag_name("a").get_attribute("href"))
        #print(b[i].get_attribute("src"))
        counter += 1
        place = items.find_element_by_class_name("GridItem__location___1KUwM  ").text
        if country == place or country == None:
            name = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("title")
            link = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("href")
            price = float(items.find_element_by_class_name("index__currency___Q78Jz ").text[1:].replace(',',''))
            country = items.find_element_by_class_name("GridItem__location___1KUwM  ").text
            image = items.find_element_by_class_name("index__image___1YObI ").get_attribute("src")
            products += {Product(name,link,country,image,price,"Lazada")}

    for i in range(len(products)):
        sorted = True
        for j in range(len(products) - i - 1):
            if products[j].price > products[j+1].price:
                products[j],products[j+1] = products[j+1],products[j]

                sorted = False
        if sorted:
            break



    #return render_template('result.html', names = names, links = links, length = len(names), countries=countries, images = images, prices = prices)
    return render_template('shop.html', products = products, length = len(products))
