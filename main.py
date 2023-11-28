from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import re 
import time
from selenium.webdriver.chrome.options import Options
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
options = Options()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')


class product:
    product = []
    def __init__(self, product_name = "", price = "", model ="" , SKU_Number = "", availability = ""):
        url = ""
        self.availability = availability
        self.model = model
        self.product_name = product_name
        self.price = price
        self.url = url
        self.SKU_Number = SKU_Number

    def get_name(self):
        return self.name
    def get_price(self):
        return self.price
    def get_url(self):
        return self.url
    def get_name(self):
        return self.name


class pageScraper(product):
    
    def __init__(self, url  ="", product = ""):
        product.__init__()
        self.url = url
        self.driver = webdriver.Chrome(options=options)
        self.product = product
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        
    def get_page(self):
        if(self.product == ""):
            print("No product name")
            return
        if(self.url == ""):
            print("No URL")
            return
        self.page =  requests.get(self.url, headers=self.headers)
        print(self.page.status_code)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        all = self.soup.find_all('li', class_='sku-item')
        for i in range(len(all)):
            self.make_product(all[i].text)
        return all
    
    def set_product_URL(self, product):
        self.product = product
        new = replace(self.product)
        self.url = "https://www.bestbuy.com/site/searchpage.jsp?st=" + new + "&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys"

    def getProduct(self):
        return self.product
    
    def getURL(self):
        return self.url
    
    def check_Inventory(self):
        url = 'https://www.bestbuy.com/site/product/5723319.p?skuId=5723319'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        stock_element = soup.find('div', {'class': 'fulfillment-fulfillment-summary'})
        print(stock_element)
    
    def make_product(self, line):
        line = line.replace("Not Yet ReviewedNot Yet ReviewedCompareSave", "") 
        line = line.replace("Your price for this item is", "") 
        sku_pos = re.search(r'SKU: ', line)
        SKU = line[sku_pos.end(): sku_pos.end()+7]
        Model_pos = re.search(r'Model: ', line)
        if(Model_pos == None):
            Model_pos = sku_pos
        product_name = line[ :Model_pos.start()]
        Model = "None"
        Model = line[Model_pos.end(): sku_pos.start()]
        price_pos = line.split('$')
        price = price_pos[1]
        New_product = product(product_name, price, Model, SKU)
        product.product.append(New_product)
    
    def find_pos_for_price(self, line):
        for i in range(len(line)):
            if(line[i] == '$' ):
                return i
    
    def print_list_long(self):
        for i in range(len(product.product)):
            print(f"[{i}]  Product: {product.product[i].product_name}           Model: {product.product[i].model}           Price: ${product.product[i].price}           SKU: {product.product[i].SKU_Number}      avaliable?: {product.product[i].availability} \n")
    
    def available(self, sku):
        url = 'https://www.bestbuy.com/site/{}.p?skuId={}'
        url = url.format(sku, sku)
        availability = requests.get(url, headers=self.headers)
        if(availability.status_code == 200):
            roup = BeautifulSoup(availability.text, 'html.parser')
            stock_element = roup.find('button', {'data-sku-id': f'{sku}'}) 
            return stock_element.text.strip()
    
    def wait_until(self, url):
        while  self.driver.current_url[ : len(url)] != url:
            time.sleep(1)
        return True
    
    def check_out(self,  email, password):
        if(len(product.product) == 0):
            print("No items in cart")
            return
        self.print_list_long()
        print("Which item would you like to add to cart? \n")
        choice = int(input()) 
        if(choice > len(product.product) - 1 or choice < 0):
            print("Sorry that is not a valid choice")
            self.check_out(email, password)
        product.product[choice].availability = self.available(product.product[choice].SKU_Number)
        if(product.product[choice].availability == "Sold Out" or product.product[choice].availability == "Coming Soon"):
            print("Sorry that item is sold out")
            return 
        try:
            self.driver.get("https://api.bestbuy.com/click/5592e2b895800000/"+ product.product[choice].SKU_Number + "/cart")
            self.wait_until("https://www.bestbuy.com/cart")
            self.driver.find_element(By.XPATH, '//*[@id="cartApp"]/div[2]/div/div[1]/div/div[1]/div[1]/section[2]/div/div/div[4]/div/div/button').click()
            self.wait_until("https://www.bestbuy.com/identity/signin")
            time.sleep(1)
            self.driver.find_element(By.XPATH, '/html/body/div[1]/div/section/main/div[2]/div[4]/div/div[2]/button').click()
            self.wait_until("https://www.bestbuy.com/checkout/r/fulfillment")
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="firstName"]').send_keys("John")
            self.driver.find_element(By.XPATH, '//*[@id="lastName"]').send_keys("Doe")
            self.driver.find_element(By.XPATH, '//*[@id="street"]').send_keys("1234 Main St")
        except:
            print("Something went wrong😒")
            return
   
     
def replace(string):
    for i in range(len(string)):
        string[i].replace(" ", "+")
    return string

def FixPrices(prices):
    for i in range(len(prices)):
        prices[i] = prices[i].text.replace("Your price for this item is $", "")
        length = len(prices[i])
        if(length%2 != 0):
            length = length - 1
        length = int(length/2)    
        prices[i] = prices[i][0:length+1]
    return prices

            

pageScraper1 =  pageScraper('https://www.bestbuy.com/site/searchpage.jsp?st=tears+of+kingdom&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys')

pageScraper2 = pageScraper()
pageScraper1.set_product_URL("pokemon cards")
pageScraper1.get_page()
pageScraper1.check_out("email", "password")
