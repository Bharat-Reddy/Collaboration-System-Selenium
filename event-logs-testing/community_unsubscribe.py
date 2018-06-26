import unittest
from selenium import webdriver
import requests


class test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.url_basic = "http://localhost:8000/"

    def test_community_unsubscribe(self):
        url_api = self.url_basic + 'logapi/event/community/unsubscribe/' + str(1) + '/'
        result = requests.get(url_api).json()
        if (result["status code"] == 200):
            data = result["result"]
            total_hits = result["total hits"]
        user = "root"
        pwd = "pass1234"
        driver = webdriver.Firefox()
        driver.maximize_window()  # For maximizing window
        driver.implicitly_wait(20)  # gives an implicit wait for 20 seconds
        driver.get("http://localhost:8000/")
        driver.find_element_by_xpath('//a [@href="/login/?next=/"]').click()
        driver.get("http://localhost:8000/login/?next=/")
        elem = driver.find_element_by_id("id_username")
        elem.send_keys(user)
        elem = driver.find_element_by_id("id_password")
        elem.send_keys(pwd)
        driver.find_element_by_class_name('btn-block').click()
        driver.find_element_by_xpath('//a [@href="/communities/"]').click()
        driver.find_element_by_xpath('//a [@href="/community-view/1/"]').click()
        driver.find_element_by_xpath("//button [@type='button' and @data-target='#exampleModal']").click()
        driver.find_element_by_id("communityUnsubscribe").click()

        url_api = self.url_basic + 'logapi/event/community/unsubscribe/' + str(1) + '/'
        result = requests.get(url_api).json()
        if (result["status code"] == 200):
            data = result["result"]
            if (result["total hits"] == total_hits + 1):
                self.assertEqual(data[0]["event_name"], "event.community.unsubscribe")
                self.assertEqual(data[0]["event"]["community-id"], '1')

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()