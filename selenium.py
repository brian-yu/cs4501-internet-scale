import time
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
driver = webdriver.Chrome()
driver.get('http://localhost:8000')
# register
driver.find_element_by_xpath('/html/body/nav/div[3]/ul/li[3]/a').click()
driver.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('te')
driver.find_element_by_xpath('//*[@id="id_last_name"]').send_keys('st')
driver.find_element_by_xpath('//*[@id="id_email"]').send_keys('test@gmail.com')
driver.find_element_by_xpath('//*[@id="id_zip_code"]').send_keys('12345')
driver.find_element_by_xpath('//*[@id="id_password"]').send_keys('testpassword123')
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form/table/tbody/tr[7]/td[2]/button').click()

# login
driver.find_element_by_xpath('/html/body/nav/div[3]/ul/li[1]/a/button/span').click()
driver.find_element_by_xpath('//*[@id="id_email"]').send_keys('test@gmail.com')
driver.find_element_by_xpath('//*[@id="id_password"]').send_keys('testpassword123')
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form/div/button').click()

# update profile
driver.find_element_by_xpath('/html/body/nav/div[3]/ul/li[1]/a').click()
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/a').click()
driver.find_element_by_xpath('//*[@id="id_first_name"]').send_keys('tes')
driver.find_element_by_xpath('//*[@id="id_last_name"]').send_keys('t')
driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form/table/tbody/tr[8]/td[2]/button').click()