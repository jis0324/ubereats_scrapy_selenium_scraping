# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from ubereats.items import UbereatsItem
import time
import traceback
import re
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ubereats import selectors
from ubereats import cities
from ubereats import proxies
from selenium.webdriver.support.wait import WebDriverWait
class UbereatsspiderSpider(scrapy.Spider):
    name = 'ubereatsSpider'
    # allowed_domains = ['ubereats.com/']
    #start_urls = ['https://www.ubereats.com/portland/food-delivery/wow-bao-por02-1/HN5Uqz2FSOO8f_J7JoQaiA']
    def __init__(self,*args, **kwargs):
        self.result = dict()
        self.url = 'https://www.ubereats.com/'
        self.cities = cities.cities_list
        self.proxy_list = proxies.proxies_list

    def get_random_proxy(self):
        random_idx = random.randint(0, len(self.proxy_list)-1)
        proxy_ip = self.proxy_list[random_idx]
        return proxy_ip    
        
    def set_driver(self):
        # proxy_http = "http://"+ self.get_random_proxy()
        # webdriver.DesiredCapabilities.CHROME['proxy']={
        #     "httpProxy":proxy_http,
        #     "ftpProxy":proxy_http,
        #     "sslProxy":proxy_http,
        #     "proxyType":"MANUAL",
        # }
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/80.0.3987.132 Safari/537.36'
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_argument('--no-sandbox')
        chrome_option.add_argument('--disable-dev-shm-usage')
        chrome_option.add_argument('--ignore-certificate-errors')
        chrome_option.add_argument("--disable-blink-features=AutomationControlled")
        chrome_option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36')
        chrome_option.headless = True
     
        driver = webdriver.Chrome(options=chrome_option)
        return driver

    def start_requests(self):
        yield Request("https://www.ubereats.com/", callback=self.parse)
    
    def parse(self, response):
        self.cities = ['Anniston,AL']
        # /* Loop All United State Cities */
        for city in self.cities:

            # /* Create Driver */
            while True:
                try:
                    
                    self.driver = self.set_driver()
                    #wait = WebDriverWait(self.driver, 20)
                    self.driver.get("https://httpbin.org/ip")
                    print("###########################",self.driver.page_source)
                    #self.driver = self.set_driver()
                    wait = WebDriverWait(self.driver, 20)
                    self.driver.get(self.url)
                    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$",self.driver.page_source)
                    sleep(10)
                    el_search_input = self.driver.find_element_by_xpath(selectors.SELECTORS['search_input'])
                    el_search_input.send_keys(city)
                    sleep(10)

                    el_search_submit =self.driver.find_element_by_xpath(selectors.SELECTORS['search_button'])
                    el_search_submit.click()
                    sleep(20)
                    break
                except:
                    self.driver.quit()
                    #print(traceback.print_exc())
                    continue
            
            # /* Get Popular Foods */
            try:
                popular_food_nodes = self.driver.find_elements_by_xpath("/html[1]/body[1]/div[1]/div[1]/main[1]/div[2]/div[2]/div[2]/section[1]/div/ul/li")
                time.sleep(5)
                popular_food_lst = []
                for popular_food_node in popular_food_nodes:
                    food_name = popular_food_node.find_element_by_xpath(".//a").text
                    try:
                        delivery_cost = popular_food_node.find_element_by_xpath("./div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").text
                        if 'fee' not in delivery_cost or '$' not in delivery_cost:
                            delivery_cost = ''
                    except:
                        delivery_cost = ''
                    try:
                        delivery_time = popular_food_node.find_element_by_xpath("./div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/span[1]").text
                    except:
                        delivery_time = ''
                    try:
                        food_type = popular_food_node.find_element_by_xpath("./div[1]/div[1]/div[1]/div[1]/div[2]/div[1]").text
                    except:
                        food_type = ''
                    try:
                        pop_food_dict = {'food_name':food_name, 'delivery_cost':delivery_cost, 'delivery_time':delivery_time, 'food_type':food_type}
                    except:
                        pop_food_dict = ''
                        
                    popular_food_lst.append(pop_food_dict)
            except :
                pass

            # /* Find More View Button and Click */
            while True:
                try:
                    view_more_btn = self.driver.find_element_by_xpath(selectors.SELECTORS['show_more_button'])
                    if view_more_btn:
                        view_more_btn.click()
                        print('#################-- ', 'Cliced View More Btn', '--################')
                        time.sleep(10)
                    else:
                        break
                except:
                    break
            
            # /* Get All Restaurants Urls and Data */20200211 16:26:40
            restaurant_links = self.driver.find_elements_by_xpath(selectors.SELECTORS['restaurant_link'])
            rest_links = []
            for restaurant_link in restaurant_links:
                final_link = restaurant_link.get_attribute('href')
                if final_link:
                    rest_links.append(final_link)

            print('#################-- ', len(rest_links), '--################')
            for rest_link in rest_links:
                try:
                    print(rest_link)
                    self.driver.get(rest_link)
                    item = UbereatsItem()
                    try:
                        item['restaurant_name'] = ''.join(self.driver.find_element_by_xpath("//main/div[1]/div[1]/div[1]/div[2]/div/div[2]/h1").text).strip()
                    except:
                        continue

                    try:
                        res1 = self.driver.page_source
                        item['food_type'] =  res1[res1.index('"servesCuisine":[')+len('"servesCuisine":['):res1.index('],"priceRange"')].replace('"',"")
                    except:
                        item['food_type'] = ''

                    try:    
                        item['delivery_time'] = ''.join(self.driver.find_element_by_xpath("//tr[contains(.,'Every Day')]/following::tr/td").text).strip()
                    except:
                        item['delivery_time'] = ''

                    try:
                        rating = ''.join(self.driver.find_element_by_xpath("//h1//following::div[5]").text).strip()
                        if '$' in rating:
                            rating = ''
                    except:
                        rating = ''

                    try:
                        address = ''.join(self.driver.find_element_by_xpath("//p[@class][1]").text).strip()
                        item['address'] = ''.join(re.findall('[0-9A-Za-z,. ]',address.replace("More info",""))).strip()
                    except :
                        item['address'] = ''

                    try:
                        item['city'] = city.split(',')[0]
                        item['state'] = city.split(',')[1]
                    except:
                        pass

                    parent_nodes = self.driver.find_elements_by_xpath("//div/ul/li")
                    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@', len(parent_nodes), '@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                    food_lst = []
                    for parent_node in parent_nodes:
                        try:    
                            section = ''.join(parent_node.find_element_by_xpath("./h2").text).strip()
                            #print(section)
                            nodes = parent_node.find_elements_by_xpath(".//ul/li")
                            
                            for node in nodes:
                                if len(node.find_elements_by_xpath(".//h4"))==1:
                                    
                                    #print(cnt)
                                    food_name = ''.join(node.find_element_by_xpath(".//h4").text).strip()
                                    #print(food_name)
                                    food_desc = ''.join(node.find_element_by_xpath(".//div/div").text).strip()
                                    price = ''
                                    food_description = ''
                                    if "$" in food_desc:
                                        food_description = food_desc.split("$")[0]
                                        price = food_desc.split("$")[1]
                                    dict = {'food_name':food_name, 'food_desc':food_description, 'price':price,'section':section}
                                    food_lst.append(dict)
                        except :
                            continue
                    item['menu'] =  food_lst

                    item['rating'] = {'rating':rating, 'popular_food':popular_food_lst}

                    yield item
                except Exception as e:
                    print(e)
                    time.sleep(5) 
                    continue
                time.sleep(5)
            
            self.driver.quit()
            time.sleep(5)
