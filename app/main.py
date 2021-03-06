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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing
import concurrent.futures
import os

app = Flask(__name__)
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--window-size=1920,1080");
# chrome_options.add_argument("--disable-extensions");
# chrome_options.add_argument("--proxy-server='direct://'");
# chrome_options.add_argument("--proxy-bypass-list=*");
# chrome_options.add_argument("--start-maximized");
# chrome_options.add_argument("--headless");
# chrome_options.add_argument("--disable-gpu");
# chrome_options.add_argument("--disable-dev-shm-usage");
# chrome_options.add_argument("--no-sandbox");
# chrome_options.add_argument("--ignore-certificate-errors");
# chrome_options.add_argument("--no-first-run");
# chrome_options.add_argument("--no-default-browser-check");
# chrome_options.add_argument('--allow-running-insecure-content')

# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

@app.route('/')
def hello_world():
    return render_template('asdd.html')

@app.route('/homepage.html')
def hello_world1():
    return render_template('asdd.html')

class Product:
    def __init__(self,name,link,country,image,price,platform):
        self.name = name
        self.link = link
        self.country = country
        self.image = image
        self.price = price
        self.platform = platform


def shopee(search_item,country,overseas):

    driver = webdriver.Chrome('./chromedriver')
    wait = WebDriverWait(driver,1)
    driver.get('https://shopee.sg/')
    search = driver.find_element_by_class_name('shopee-searchbar-input__input')
    search.send_keys(search_item)

    search.send_keys(Keys.RETURN)
    products = []

    try:
        driver.implicitly_wait(10)
        for _ in range(30):
            try:
                all_items = driver.find_elements_by_xpath('//div[@data-sqe="name"]')
                all_links = driver.find_elements_by_xpath('//a[@data-sqe="link"]')
                all_locations = driver.find_elements_by_xpath('//div[@class="_2CWevj"]')
                all_images = driver.find_elements_by_xpath('//img[@class="mxM4vG _2GchKS"]')
                all_prices =driver.find_elements_by_xpath('//div[@class="WTFwws _1k2Ulw _5W0f35"]')
                driver.execute_script("return arguments[0].scrollIntoView(true);",all_items[_])
                wait.until(EC.presence_of_element_located(By.XPATH,'//img[@class="mxM4vG _2GchKS"]'))
            except:
                time.sleep(0.5)
        for i in range(len(all_items)):
            if overseas == None:
                if country == all_locations[i].text:
                    names = all_items[i].find_element_by_xpath(".//*").text

                    links = all_links[i].get_attribute("href")
                    countries = all_locations[i].text
                    images = all_images[i].get_attribute("src")
                    prices = float(all_prices[i].find_element_by_class_name('_24JoLh').text.replace(',',''))
                    products += {Product(names,links,countries,images,prices,"Shopee")}
            elif overseas == 'all' and country == None:
                if all_locations[i].text != 'Singapore':
                    names = all_items[i].find_element_by_xpath(".//*").text

                    links = all_links[i].get_attribute("href")
                    countries = all_locations[i].text
                    images = all_images[i].get_attribute("src")
                    prices = float(all_prices[i].find_element_by_class_name('_24JoLh').text.replace(',',''))
                    products += {Product(names,links,countries,images,prices,"Shopee")}
            else:
                names = all_items[i].find_element_by_xpath(".//*").text

                links = all_links[i].get_attribute("href")
                countries = all_locations[i].text
                images = all_images[i].get_attribute("src")
                prices = float(all_prices[i].find_element_by_class_name('_24JoLh').text.replace(',',''))
                products += {Product(names,links,countries,images,prices,"Shopee")}
        print("try")
        print(products)
        return products
    except:
        print("EXCEPT")
        return products

def lazada(search_item,country,overseas):
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://lazada.sg')
    search = driver.find_element_by_id('q')

    products = []
    
    search.send_keys(search_item)
    search.send_keys(Keys.RETURN)
    
    try:

        for _ in range(30):
            try:
                x = driver.find_elements_by_class_name("index__gridItem___3VkVO")
                driver.execute_script("return arguments[0].scrollIntoView(true);",x[_])
                wait.until(EC.presence_of_element_located(By.XPATH,'//img[@name="index__image___1YObI "]'))
                time.sleep(0.6)
            except:
                time.sleep(0.6)

        for items in x:
            

            place = items.find_element_by_class_name("GridItem__location___1KUwM  ").text
            if overseas == None:
                if country == place:

                    name = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("title")

                    link = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("href")
                    price = float(items.find_element_by_class_name("index__currency___Q78Jz ").text[1:].replace(',',''))
                    countries = items.find_element_by_class_name("GridItem__location___1KUwM  ").text
                    image = items.find_element_by_class_name("index__image___1YObI ").get_attribute("src")
                    products += {Product(name,link,countries,image,price,"Lazada")}
            elif overseas == 'all' and country == None:
                if place != 'Singapore':

                    name = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("title")

                    link = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("href")
                    price = float(items.find_element_by_class_name("index__currency___Q78Jz ").text[1:].replace(',',''))
                    countries = items.find_element_by_class_name("GridItem__location___1KUwM  ").text
                    image = items.find_element_by_class_name("index__image___1YObI ").get_attribute("src")
                    products += {Product(name,link,countries,image,price,"Lazada")}
            else:

                name = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("title")

                link = items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("href")
                price = float(items.find_element_by_class_name("index__currency___Q78Jz ").text[1:].replace(',',''))
                countries = items.find_element_by_class_name("GridItem__location___1KUwM  ").text
                image = items.find_element_by_class_name("index__image___1YObI ").get_attribute("src")
                products += {Product(name,link,countries,image,price,"Lazada")}
        
        return products
    except:
        
        return products







@app.route('/destination.html')
def destination():
    search_item = request.args.get('product')
    country = request.args.get('location')
    la = request.args.get('l')
    sh = request.args.get('s')
    overseas = request.args.get('overseas')
    products = []

    if sh == None and la == None:
        text = "Please select at least one platform!"
        return render_template('Contact.html', text = text)
    if country == None and overseas == None:
        text = "Please select either local or overseas!"
        return render_template('Contact.html', text = text)


    with concurrent.futures.ProcessPoolExecutor() as executor:
        if sh:
            s = executor.submit(shopee,search_item,country,overseas)
        if la:
            l = executor.submit(lazada,search_item,country,overseas)

        try:
            products += s.result()
        except:
            pass

        try:
            products += l.result()
        except:
            pass
    

    text = f"Your search for '{search_item}' did not have any results. Please try searching with a different keyword!"
    if len(products) == 0:
        return render_template('Contact.html', text = text)


    for i in range(len(products)):
        sorted = True
        for j in range(len(products) - i - 1):
            if products[j].price > products[j+1].price:
                products[j],products[j+1] = products[j+1],products[j]

                sorted = False
        if sorted:
            break


    
    return render_template('shop.html', products = products, length = len(products))
