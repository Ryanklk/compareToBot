#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gspread #import gspread package to allow functions that open and manipulate googlesheet
from oauth2client.service_account import ServiceAccountCredentials #import package that allows authentication of googlesheet 

import pandas as pd #import pandas to use dataframe
import re #import re to for trimming user entries in googlesheet
import time
from bs4 import BeautifulSoup
import lxml

from selenium import webdriver #import selenium so chrome can be used to access salesforce.
from selenium.webdriver.common.keys import Keys

import sys, os 
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))


time.sleep(3)



# In[2]:


sheet = client.open('Keyword Translation_ Automation').worksheet("Sample data") #open sheet containing info. Change sheet name according to name assigned to sheet
data = sheet.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
duplicates = int(sheet.acell('B1').value)
is_foreign= (sheet.acell('B2').value)
market= (sheet.acell('B3').value)
if( market== "TH"):
    market = "co.th"
if(market== "ID"):
    market= "co.id"
driver.get("https://shopee."+market) 
time.sleep(3)
try: 
    driver.find_element_by_xpath("//button[@class='shopee-button-outline shopee-button-outline--primary-reverse ']").click()
except:
    time.sleep(3)



time.sleep(3)
driver.find_element_by_xpath("//div[@class='shopee-popup__close-btn']").click()
keyword_counter=7
keyword_list =[]

if(df.iloc[keyword_counter-2,0]!=df.iloc[keyword_counter-1,0] and df.iloc[keyword_counter-1,0]!= df.iloc[keyword_counter,0]):
    while (df.iloc[keyword_counter-2,0]!=""):
        keyword_list.append(df.iloc[keyword_counter-2,0])
        sheet.update_cell(keyword_counter,1,"")
        keyword_counter+=1
    print(keyword_list)
    replace_counter=7
    for keyword in keyword_list:
        dummy_string=""
        for _ in range(0,duplicates):
            dummy_string+=keyword
            dummy_string+="*"
        sheet.update_cell(replace_counter,20,dummy_string)
        sheet.update_cell(7+int(duplicates)*(replace_counter-7),1,"=TRANSPOSE(split(T"+str(replace_counter)+",\"*\",TRUE,TRUE))")
        replace_counter+=1
    
    
data = sheet.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
    


# In[3]:


df.head(10)


# In[103]:


sheet = client.open('Keyword Translation_ Automation').worksheet("Sample data") #open sheet containing info. Change sheet name according to name assigned to sheet
data = sheet.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
counter=int(int(sheet.acell('Z1').value)/50) *50 +7
market= (sheet.acell('B3').value)
if( market== "TH"):
    market = "co.th"
if(market== "ID"):
    market= "co.id"


driver.get("https://shopee."+market) 
time.sleep(3)

try: 
    driver.find_element_by_xpath("//button[@class='shopee-button-outline shopee-button-outline--primary-reverse ']").click()
except:
    time.sleep(3)

try:
    driver.find_element_by_xpath("//div[@class='shopee-popup__close-btn']").click()
except: 
    time.sleep(1)
    
row_inspecting=counter
while (counter<3000):
    if(df.iloc[counter-2,1]==""):
        break

    driver.find_element_by_xpath("//input[@class='shopee-searchbar-input__input']").clear()
    driver.find_element_by_xpath("//input[@class='shopee-searchbar-input__input']").send_keys(df.iloc[counter-2,1]+Keys.ENTER)
    print(counter)
    time.sleep(2)
    try:
        driver.find_elements_by_xpath("//div[@class='shopee-filter-group__toggle-btn']")[1].click()
    except:
        time.sleep(0.5)
    time.sleep(2)
    if(market=="Foreign"):
        try:
            driver.find_element_by_xpath("//label[*[text()='Overseas']]").click()
        except:
            time.sleep(0.5)
            
    elif(market=="Local"):
        try:
            driver.find_element_by_xpath("//label[*[text()='Domestic']]").click()
        except:
            time.sleep(0.5)
    else:
        time.sleep(0.5)
        
        
    time.sleep(2)
    
    #### Scroll to load pages elements###
    for _ in range(10):
        try:
            element=driver.find_elements_by_xpath("//a[@data-sqe='link']")[10*_]
            driver.execute_script("return arguments[0].scrollIntoView(true);",element) #for searchs< 10 results
            time.sleep(3)
        except:
            time.sleep(0.5)
            
    #### Check how many rows use the same keyword######
    



    
    #### Gets links on the result page ###########
    time.sleep(1)
    soup_level1=BeautifulSoup(driver.page_source, features="lxml")#Helps to overcome the problem of selenium always encoding to ascii. Somehow lol    
    links=soup_level1.findAll('a',attrs={'data-sqe':'link'})
    links_list=[]
    for link in links: 
        links_list.append(link.get('href'))
    try:
        driver.find_elements_by_xpath("//div[@class='shopee-search-empty-result-section__title']")[0]
        links_list=[]
    except:
        time.sleep(0)

        
    

    value_list = range(0,50)
    
        

    

    for value in value_list:
        original_price=0
        discounted_price=0
        free_shipping=""
        sold=0
        sponsored=""
        favourite=""
        promotion=""
        
        
        
        print(value)
        if(value<len(links_list)):
            item =soup_level1.findAll('div',attrs={'data-sqe':'item'})[value]
            
            link="https://shopee."+market+links_list[value]
            
            try:
                original_price = item.findChildren("div",attrs={'class':'_1w9jLI QbH7Ig U90Nhh'} )[0].text
                discounted_price = item.findChildren("div",attrs={'class':'_1w9jLI _37ge-4 _2ZYSiu'} )[0].text

            except:
                original_price = item.findChildren("div",attrs={'class':'_1w9jLI _37ge-4 _2ZYSiu'} )[0].text
                discounted_price= "None"


            try:
                free_shipping= item.findChildren("svg",attrs={'class':'icon-free-shipping'} )[0]
                free_shipping = "True"
            except:
                free_shipping = "False"

            try: 
                promotion =item.findChildren("div",attrs={'class':'_1q6y2m'} )[0].findChildren("div")[0].text
                promotion +=","
                promotion +=item.findChildren("div",attrs={'class':'_1q6y2m'} )[0].findChildren("div")[1].text
                promotion +=","
                promotion +=item.findChildren("div",attrs={'class':'_1q6y2m'} )[0].findChildren("div")[2].text


            except:
                if(promotion==""):
                    promotion = "None"

            try: 
                sold =item.findChildren("div",attrs={'class':'_18SLBt'} )[0].text

            except:
                sold = "None"

            try:
                if(sold==""):
                    sold= "Not stated"
                else:
                    sold = re.split(" ", sold)[2]

            except:
                sold=sold


            try:
                sponsored = item.findChildren("div",attrs={'class':'_3ao649'} )[0].text
                sponsored="True"

            except:
                sponsored = "False"

            try:
                favourite= item.findChildren("div",attrs={'class':'_150RS_ bgXBUk'} )[0].text
                favourite="True"

            except:
                favourite = "False"

            string_data=""
            string_data+= link
            string_data+="*"
            string_data+= original_price
            string_data+="*"
            string_data+= discounted_price
            string_data+= "*"
            string_data+=free_shipping
            string_data+="*"
            string_data+=promotion
            string_data+="*"
            string_data+=sold
            string_data+="*"
            string_data+=sponsored
            string_data+="*"
            string_data+=favourite
            string_data+="*"
            string_data+=str(value)


            sheet.update_cell(counter,6,string_data)
        else:
            sheet.update_cell(counter,6,"Insufficient result")

        #try:
         #   discounted_price=soup_level1.find('div',attrs={'class':'_1w9jLI _37ge-4 _2ZYSiu'})
        time.sleep(1)
        counter+=1
    


# In[97]:


len(soup_level1.findAll('div',attrs={'data-sqe':'item'}))


# In[93]:





# In[ ]:




