# import requests
import datetime
import pandas as pd
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

from config import *


def initiate_driver(url, headless=None):
    """
    Initiate driver with the input url
    :param headless: used to have a chrome open or in headless
    :param url: input url to get page source
    :return:
    """
    if headless:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
    else:
        driver = webdriver.Chrome()
    driver.get(url)
    return driver


def preporcess_price(price):
    """
    Prepossess price and get clean price
    :param price: string price with currency
    :return:
    """
    price = price.replace("ab", "")
    price = price.replace("*", "")
    price = price.split("€")[0]
    return price


def get_currency(price):
    """
    Get currency from the price
    :param price:
    :return:
    """
    try:
        price = price.replace("*", "")
        currency = price.replace(" ", "").split(",")[-1][2:]
    except:
        currency = "€"
    return currency


def get_size(product_detail_url):
    """
    Get size from product detail page
    :param product_detail_url:
    :return:
    """
    sizes_list = []
    page_source = initiate_driver(product_detail_url, headless=True)
    product_sizes = page_source.find_elements_by_class_name('variation')
    print(product_detail_url)
    for size in product_sizes:
        sizes_dict = {}

        try:
            size = size.text
        except:
            size = size.strip(" ")

        if len(size) > 1:
            size = size.replace("bitte wählen", "")
            size = size.replace("Größe wählen:", "")
            size = size.replace("Weiß/Schwarz:", "")
            size = size.replace("Weiß/Schwarz", "")
            size = size.replace("Schwarz", "")

            try:
                size_price = size.split('+')[-1].strip(' ').split(" ")[0]
                size_price = size_price.replace(".", "")
                size_price = float(size_price.replace(",", "."))

                size = size.split('+')[0].strip(' ')
            except:
                size_price = 0.0

            sizes_dict["size"] = size
            sizes_dict["price"] = size_price
            sizes_list.append(sizes_dict)

    return sizes_list


def get_product_details():
    """
    Get product details
    :return:
    """
    items = []
    page_source = initiate_driver(INPUT_URL, headless=True)
    product_divs = page_source.find_elements_by_class_name('product-wrapper')
    date = datetime.datetime.today().strftime("%Y-%M-%d")
    for i in range(len(product_divs)):
        price = page_source.find_elements_by_class_name('price_wrapper')[i].text
        currency = get_currency(price)

        price = preporcess_price(price)
        price = price.replace(".", "")
        price = float(price.replace(",", "."))

        name = page_source.find_elements_by_class_name('title')[i].text
        url = page_source.find_elements_by_xpath("//div[@class='caption']//meta")[i].get_attribute('content')
        sizes = get_size(url)
        for size in sizes:
            size_price = size["price"]
            size = size["size"]
            final_price = round(price + size_price, 2)
            item = [date, INPUT_URL, name, size, final_price, currency]
            items.append(item)
    df = pd.DataFrame(items, columns=['date', 'website', 'productName', 'productSize', 'productPrice', 'currency'])
    return df


if __name__ == "__main__":
    product_df = get_product_details()
    print(product_df)
