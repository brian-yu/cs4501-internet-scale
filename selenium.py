from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# driver = webdriver.Chrome()
driver = webdriver.Chrome(
    '/Users/SJP/documents/personaldev/python/auto_selen/chromedriver')
driver.get("http://localhost:8080/")
# assert "Python" in driver.title

# Login first
login = driver.find_element(By.XPATH, '//a[text()="Login"]')
login.click()

email = driver.find_element_by_name("email")
email.send_keys("sjp@hotmail.com")

password = driver.find_element_by_name("password")
password.send_keys("0o0o0o")

login_button = driver.find_element_by_name(
    "submit")
login_button.click()

# Post item
post_item = driver.find_element_by_class_name('button_text')
post_item.click()

title = driver.find_element_by_name('title')
title.send_keys("brians biceps")

price_per_day = driver.find_element_by_name('price_per_day')
price_per_day.send_keys("5")

condition = Select(driver.find_element_by_name('condition'))
condition.select_by_value("G")

max_borrow_days = driver.find_element_by_name('max_borrow_days')
max_borrow_days.send_keys("5")

description = driver.find_element_by_name('description')
description.send_keys("high survival rate")

post_item2 = driver.find_element_by_name(
    "submit")
post_item2.click()

# search for and click the item
searchbar = driver.find_element_by_class_name("uk-search-input")
searchbar.send_keys("brians biceps")
searchbar.send_keys(Keys.ENTER)

item = driver.find_element(By.XPATH, '//a[text()="brians biceps"]')
item.click()

# assert "No results found." not in driver.page_source
# driver.close()
