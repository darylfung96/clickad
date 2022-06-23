from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Sites:

	@abstractmethod
	def start_process(self):
		pass


class NeoBux(Sites):
	def __init__(self):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--user-data-dir=user_data')
		self.driver = webdriver.Chrome('/Applications/chromedriver', options=chrome_options)
		self.wait_driver = WebDriverWait(self.driver, 400)

	def start_process(self):
		self.driver.get('http://www.neobux.com')

		advertisements_link_list = self.driver.find_elements_by_xpath("//*[contains(text(), 'View Advertisements')]")
		if len(advertisements_link_list) == 0:
			login_button = self.driver.find_elements_by_xpath("//*[contains(text(), 'Login')]")[0]
			login_button.click()

			login_form = self.driver.find_element_by_tag_name('tbody')
			login_form.find_element_by_id('Kf1').send_keys(username)
			login_form.find_element_by_id('Kf2').send_keys(password)
			login_form.find_element_by_id('Kf4').send_keys(password)

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'View Advertisements')]")))
		view_ad_button = self.driver.find_elements_by_xpath("//*[contains(text(), 'View Advertisements')]")[0]
		view_ad_button.click()

		self.wait_driver.until(EC.visibility_of_element_located((By.CLASS_NAME, 'cell')))
		all_clickable_ads = self.driver.find_elements_by_class_name('cell')

		for ad in all_clickable_ads:
			# if ad has been clicked before then continue to the next one
			if len(ad.find_elements_by_class_name('ad0')) > 0:
				continue

			ad.click()
			red_dot = ad.find_element_by_tag_name('img')
			red_dot.click()

			self.driver.switch_to.window(self.driver.window_handles[1])
			self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'validated')]")))
			close_button = self.driver.find_elements_by_xpath("//*[contains(text(), 'Close')]")[0]
			close_button.click()

			self.driver.switch_to.window(self.driver.window_handles[0])
			# self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Fixed Advertisements')]")))



web = NeoBux()
web.start_process()