from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from django.test import TestCase
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import unittest


class SeleniumTest(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Chrome(
        #     "/Users/SJP/documents/personaldev/python/auto_selen/chromedriver")

        self.driver = webdriver.Remote(command_executor='http://selenium-chrome:4444/wd/hub',
                                       desired_capabilities=DesiredCapabilities.CHROME)
        # self.driver.get('http://localhost:8080')
        self.driver.get('http://web:8000')

    def register(self):
        # register
        self.driver.find_element_by_xpath(
            '/html/body/nav/div[3]/ul/li[3]/a').click()
        self.assertEqual(self.driver.current_url,
                         "http://localhost:8080/register/")

        self.driver.find_element_by_xpath(
            '//*[@id="id_first_name"]').send_keys('te')
        self.driver.find_element_by_xpath(
            '//*[@id="id_last_name"]').send_keys('st')
        self.driver.find_element_by_xpath(
            '//*[@id="id_email"]').send_keys('test@gmail.com')
        self.driver.find_element_by_xpath(
            '//*[@id="id_zip_code"]').send_keys('12345')
        self.driver.find_element_by_xpath(
            '//*[@id="id_password"]').send_keys('testpassword123')
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/form/table/tbody/tr[7]/td[2]/button').click()
        self.assertEqual(self.driver.current_url,
                         "http://localhost:8080/register/")

    def login(self):
        # login thru post item
        self.driver.find_element_by_xpath(
            '/html/body/nav/div[3]/ul/li[1]/a/button/span').click()
        self.assertEqual(self.driver.current_url,
                         "http://localhost:8080/login/?next=/post_item/")
        self.driver.find_element(
            By.XPATH, '//a[text()="Login"]').click()
        self.assertEqual(self.driver.current_url,
                         "http://localhost:8080/login/")

        self.driver.find_element_by_xpath(
            '//*[@id="id_email"]').send_keys('test@gmail.com')
        self.driver.find_element_by_xpath(
            '//*[@id="id_password"]').send_keys('testpassword123')
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/form/div/button').click()
        self.assertEqual(self.driver.current_url,
                         "http://localhost:8080/")

    def update_profile(self):
        # update profile
        # self.driver.find_element_by_xpath(
        #     '/html/body/nav/div[3]/ul/li[1]/a').click()
        self.driver.get('http://localhost:8080/profile')
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[2]/a').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_first_name"]').send_keys('tes')
        self.driver.find_element_by_xpath(
            '//*[@id="id_last_name"]').send_keys('t')

        self.assertEqual(self.driver.current_url,
                         "http://localhost:8080/update_profile/")

        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/form/table/tbody/tr[8]/td[2]/button').click()

    def post_item(self):
        # Post item
        post_item = self.driver.find_element_by_class_name('button_text')
        post_item.click()

        self.assertEqual(self.driver.current_url,
                         "http://localhost:8080/post_item/")

        title = self.driver.find_element_by_name('title')
        title.send_keys("brians biceps")

        price_per_day = self.driver.find_element_by_name('price_per_day')
        price_per_day.send_keys("5")

        condition = Select(self.driver.find_element_by_name('condition'))
        condition.select_by_value("G")

        max_borrow_days = self.driver.find_element_by_name('max_borrow_days')
        max_borrow_days.send_keys("5")

        description = self.driver.find_element_by_name('description')
        description.send_keys("high survival rate")

        post_item2 = self.driver.find_element_by_name(
            "submit")
        post_item2.click()

        # self.assertEqual(self.driver.text, "")

    def search(self):
        # search for and click the item
        searchbar = self.driver.find_element_by_class_name("uk-search-input")
        searchbar.send_keys("brians biceps")
        searchbar.send_keys(Keys.ENTER)

        assert "brians biceps" in self.driver.page_source

        item = self.driver.find_element(
            By.XPATH, '//a[text()="brians biceps"]')
        item.click()

        assert "brians biceps" in self.driver.page_source

    def misc(self):
        # all items, my profile, logout
        self.driver.get('http://localhost:8080/all_items')
        assert "brians biceps" in self.driver.page_source

        self.driver.get("http://localhost:8080/profile")
        assert "12345" in self.driver.page_source

    def logout(self):
        logout = self.driver.find_element(By.XPATH, '//a[text()="Logout"]')
        logout.click()
        # self.driver.quit()


if __name__ == "__main__":
    test = SeleniumTest()
    test.setUp()
    test.register()
    test.login()
    test.update_profile()
    test.post_item()
    test.search()
    test.misc()
    test.logout()
