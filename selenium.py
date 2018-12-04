import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
driver = webdriver.Chrome()
driver.get('http://localhost:8000')
# register
driver.find_element_by_xpath('/html/body/nav/div[3]/ul/li[3]/a').click()
driver.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('te')
driver.find_element_by_xpath('//*[@id="id_last_name"]').send_keys('st')
driver.find_element_by_xpath('//*[@id="id_email"]').send_keys('test@gmail.com')
driver.find_element_by_xpath('//*[@id="id_zip_code"]').send_keys('12345')
driver.find_element_by_xpath('//*[@id="id_email"]').send_keys('test@gmail.com')
driver.find_element_by_xpath(
    '//*[@id="id_password"]').send_keys('testpassword123')
driver.find_element_by_xpath(
    '/html/body/div[1]/div[1]/div/form/table/tbody/tr[7]/td[2]/button').click()

# driver.find_element_by_xpath('//*[@id="id_password"]').send_keys('testpassword123')
# driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form/table/tbody/tr[7]/td[2]/button').click()

# login
driver.find_element_by_xpath(
    '/html/body/nav/div[3]/ul/li[1]/a/button/span').click()
driver.find_element_by_xpath('//*[@id="id_email"]').send_keys('test@gmail.com')
driver.find_element_by_xpath(
    '//*[@id="id_password"]').send_keys('testpassword123')
driver.find_element_by_xpath(
    '/html/body/div[1]/div[1]/div/form/div/button').click()

# update profile
driver.find_element_by_xpath('/html/body/nav/div[3]/ul/li[1]/a').click()
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/a').click()
driver.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('tes')
driver.find_element_by_xpath('//*[@id="id_last_name"]').send_keys('t')
driver.find_element_by_xpath(
    '/html/body/div[1]/div[1]/div/form/table/tbody/tr[8]/td[2]/button').click()

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
