import time
import json
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement, EventFiringWebDriver
from selenium.webdriver.remote.webelement import WebElement

# user = os.environ.get('mongo_user')

chrome_driver_path = "/Users/arifrahman/Code/drivers/chromedriver"
url = 'https://www.jdsports.com.sg'
page_range = 9
path = Path.cwd()
data_folder = path / 'src/data'
brand = 'adidas,adidas-originals'


print(chrome_driver_path)


def save_data_to_file(data):
    # open file and write as json format
    with open(data_folder / f"{brand}_data.json", 'w') as json_file:
        json.dump(data, json_file)
        print('Succefully dump json')


def get_url(brand: str):
    return f'{url}/men/mens-footwear/brand/{brand}'


# declare and intialiase driver, change this as require
driver = webdriver.Chrome(chrome_driver_path)


def smooth_scrolling():
    '''
    a function that allow smooth scrolling to the bottom of the page,
    this help with page that lazy load data/element.
    '''

    total_height = int(driver.execute_script(
        "return document.body.scrollHeight"))

    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))


def remove_prefix(text: str, prefix: str):
    return text[text.startswith(prefix) and len(prefix):]


def main():
    try:
        print(f'[Start]: extraction from {get_url(brand)}')
        # browser should be loaded in maximized window, to ensure consistency on what to scrape
        driver.maximize_window()
        # open brower and control website
        driver.get(get_url(brand))

        mapped_items = []

        container: EventFiringWebDriver = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id = "productBrowse"]')))
        modal: EventFiringWebDriver = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="abandoned_email_img"]/img')))

        # modal open on new page, hence we get the close button and close the modal
        closeButton: EventFiringWebElement = modal.find_element(
            By.XPATH, '//*[@id="abandoned_email_section"]/span[4]/a')
        closeButton.click()

        for page in range(page_range):
            print(f'[PAGE]: {page}')

            # to ensure we loading lazy loading data before extraction
            smooth_scrolling()

            nextPageButton: EventFiringWebElement = driver.find_element(
                By.XPATH, '//*[@title = "Next Page"]')
            print(f'[NEXT BUTTON EXIST]:', bool(nextPageButton))

            # get all the list item
            products: EventFiringWebElement = driver.find_elements(
                By.CLASS_NAME, 'productListItem ')

            print(f'[PRODUCTS]: {products}')

            # traverse list of item and extract name, imgUrl & price and append in an array.
            for product in products:
                item: WebElement = product
                prefix = 'SGD '

                name = item.find_element(
                    By.CLASS_NAME, 'itemTitle').text
                imgUrl = item.find_element(
                    By.CLASS_NAME, 'thumbnail').get_attribute('src')
                price = remove_prefix(item.find_element(
                    By.CLASS_NAME, 'itemPrice').text, prefix)
                mapped_items.append({
                    "name": name,
                    "imgUrl": imgUrl,
                    "price": price
                })
            # navigate to next page when finished traversing all list of items.
            nextPageButton.click()
            # ensure page are loaded before extraction happens.
            time.sleep(1)

        print(mapped_items)
        # open file and write as json format
        save_data_to_file(mapped_items)
    except:
        print('Error: Something when wrong!')


main()
