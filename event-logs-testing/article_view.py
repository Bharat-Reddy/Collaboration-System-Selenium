import unittest
from selenium import webdriver
import requests
from decouple import config

class test(unittest.TestCase):

    def setUp(self):
        self.user = config("EVENT_LOGS_USER")
        self.pwd = config("EVENT_LOGS_PASSWORD")
        self.url_basic = "http://" + config("IP_ADDRESS") + ":" + config("EVENT_LOGS_PORT") + "/"
        self.token = config("EVENT_API_TOKEN")  #This should be generated by tester
        self.headers={'Authorization': 'Token ' + str(self.token)}
        self.article_id = input("Enter article id: ")

    def test_article_view(self):
        url_api = self.url_basic + 'logapi/event/article/view/' + str(self.article_id) + '/'
        result = requests.get(url_api, headers = self.headers).json()
        new_result={}
        for key,value in result.iteritems():
            new_result[key.lower()] = value
        if (new_result["status code"] == 200):
            data = new_result["result"]
            total_hits = new_result["total hits"]
        driver = webdriver.Firefox()
        driver.maximize_window()  # For maximizing window
        driver.get(self.url_basic)
        driver.find_element_by_xpath('//a [@href="/login/?next=/"]').click()
        driver.get(self.url_basic + "login/?next=/")
        elem = driver.find_element_by_id("id_username")
        elem.send_keys(self.user)
        elem = driver.find_element_by_id("id_password")
        elem.send_keys(self.pwd)
        driver.find_element_by_class_name('btn-block').click()
        driver.find_element_by_xpath('//a [@href="/articles/"]').click()
        driver.find_element_by_xpath('//a [@href="/article-view/' + str(self.article_id) + '/"]').click()
        url_api = self.url_basic + 'logapi/event/article/view/' + str(self.article_id) + '/'
        result = requests.get(url_api, headers = self.headers).json()
        new_result={}
        for key,value in result.iteritems():
            new_result[key.lower()] = value
        if (new_result["status code"] == 200):
            data = new_result["result"]
            if (new_result["total hits"] == total_hits +1):
                self.assertEqual(data[0]["event_name"], "event.article.view")
                self.assertEqual(data[0]["event"]["article-id"], str(self.article_id))
            else:
                self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()
