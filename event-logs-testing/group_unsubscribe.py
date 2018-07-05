import unittest
from selenium import webdriver
import requests
from decouple import config

class test(unittest.TestCase):
	
	def setUp(self):
		print("Note that user should be a part of community and group belonging to this community: ")
		self.user = config("EVENT_LOGS_USER")
		self.pwd = config("EVENT_LOGS_PASSWORD")
		self.url_basic = "http://" + config("IP_ADDRESS") + ":" + config("EVENT_LOGS_PORT") + "/"
		self.token = config("EVENT_API_TOKEN")  #This should be generated by tester
		self.headers={'Authorization': 'Token ' + str(self.token)}
		self.comm_id = raw_input("Enter id of community whose group you wish to leave: ")
		self.grp_id = raw_input("Enter id of group you want to leave: ")
		
	def test_group_unsubscribe(self):
		url_api = self.url_basic + 'logapi/event/group/unsubscribe/'
		result = requests.get(url_api, headers=self.headers).json()
		new_result = {}
		for key, value in result.iteritems():
			new_result[key.lower()] = value
		if (new_result["status code"] == 200):
			data = new_result["result"]
			total_hits = new_result["total hits"]

		driver = webdriver.Firefox()
		driver.maximize_window() #For maximizing window
		driver.get(self.url_basic)
		driver.find_element_by_xpath('//a [@href="/login/?next=/"]').click()
		elem = driver.find_element_by_id("id_username")
		elem.send_keys(self.user)
		elem = driver.find_element_by_id("id_password")
		elem.send_keys(self.pwd)
		driver.find_element_by_class_name('btn-block').click()
		driver.find_element_by_xpath('//a [@href="/communities/"]').click()
		driver.find_element_by_xpath('//a [@href="/community-view/' + self.comm_id + '/"]').click()
		driver.find_element_by_xpath('//a [@href="/group-view/' + self.grp_id + '/"]').click()
		driver.find_element_by_xpath("//button [@type='button' and @data-target='#exampleModal']").click()
		driver.find_element_by_id("groupUnsubscribe").click()

		url_api = self.url_basic + 'logapi/event/group/unsubscribe/'
		result = requests.get(url_api, headers=self.headers).json()
		new_result = {}
		for key, value in result.iteritems():
			new_result[key.lower()] = value
		if (new_result["status code"] == 200):
			data = new_result["result"]
			if (new_result["total hits"] == total_hits + 1):
				self.assertEqual(data[0]["event_name"],"event.group.unsubscribe")
				self.assertEqual(data[0]["event"]["group-id"], self.grp_id)
			else:
				self.assertFalse(True)

		driver.quit()

if __name__ == '__main__':
	unittest.main()
