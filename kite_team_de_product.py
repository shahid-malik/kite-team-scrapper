import requests
import pandas

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import *

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

driver.get(PRODUCT_URL)

print(driver.title)


# Variations driver.find_elements_by_class_name('variations')[0].text

