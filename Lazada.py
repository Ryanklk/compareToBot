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

PATH = "/Users/ryankoh/Desktop/Me/Orbital/Selenium Test/chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(10)
driver.get('https://lazada.sg')

search = driver.find_element_by_id('q')

#x = input("What are you looking for?")
search.send_keys("Monitor")
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
        time.sleep(3)
    #print(x[i].find_element_by_tag_name("a").get_attribute("title"))
    #print(x[i].find_element_by_tag_name("a").get_attribute("href"))
    #print(b[i].get_attribute("src"))
    counter += 1
    print(items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("title"))
    print(items.find_element_by_class_name("GridItem__title___8JShU").find_element_by_tag_name("a").get_attribute("href"))
    print(items.find_element_by_class_name("index__image___1YObI ").get_attribute("src"))
    



#driver.quit()