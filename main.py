#Import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import csv

# Define scraping duration in seconds
scraping_duration = time.time() + 60 * 30 #minutes

# Define the frequency of scrapping in seconds
freq = 60

# Define the product you would like to get its price
product = "kindle"

# Write the output file headers
with open("amazon.csv", "a+", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Time", "Product", "Price"])

while time.time() < scraping_duration:  # Repeat the following process until the scraping_duration ends
    '''
    This loop will search for the requested product in amazon every (freq), and it will choose the first amazon's choice item

    from the search results, record its price, and the date and time of the record. This will be written to a CSV file in the 

    mentioned path
    '''
    now = datetime.now()
    dt_string = now.strftime("%H:%M")
    date_string = now.strftime("%m/%d/%Y")
    driver = webdriver.Chrome("C:\\Program Files (x86)\\chromedriver.exe")
    driver.get("http:\\amazon.ca")
    search = driver.find_element(By.ID, "twotabsearchtextbox")
    search.send_keys(product)
    search.send_keys(Keys.RETURN)
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Amazon's Choice")))
        element.click()
        title = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "productTitle")))
        Title = title.text
        price_whole = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole")))
        price_decimal = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-fraction")))
        Price = float(price_whole.text) + (float(price_decimal.text) / 100)
        Time = dt_string
        Date = date_string
        data = [Date, Time, product, Price]
        with open("amazon.csv", "a+", newline="") as f:  # append data into CSV file
            writer = csv.writer(f)
            writer.writerow(data)
    except:
        driver.quit()
    driver.quit()
    time.sleep(freq)  # sleep the process for the frequency duration before it repeats
