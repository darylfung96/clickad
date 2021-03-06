from abc import abstractmethod, abstractproperty
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc
import random
import seleniumwire.undetected_chromedriver as uc
import time
from seleniumwire import webdriver
from captcha import solve_captcha
from urllib.request import urlopen
import json
# timezone
from timezonefinder import TimezoneFinder
from datetime import datetime
from pytz import timezone


class Sites:

	@abstractproperty
	def driver(self):
		...

	@abstractmethod
	def start_process(self, username, password):
		pass

	@abstractmethod
	def quit(self):
		pass

	def get_ip(self):
		self.driver.get('https://api.ipify.org/')
		return self.driver.find_element(By.TAG_NAME, "body").text

# register_username = 'guteerdseamouertdea53'
# register_password = 'CHzaedxsww'
# register_email = 'guteerdseamouertdea53@gmail.com'

# username = register_username
# password = register_password

proxy_options = {
    'proxy': {
        'http': 'http://synthex1145:9cc8cb@167.160.89.19:10389',
        'https': 'https://synthex1145:9cc8cb@167.160.89.19:10389',
        'no_proxy': 'localhost,127.0.0.1'
    }
}


class NeoBux(Sites):
	def __init__(self):
		chrome_options = uc.ChromeOptions()
		# chrome_options.add_argument('--user-data-dir=user_data')
		chrome_options.add_argument("--disable-popup-blocking")
		self.driver = uc.Chrome(driver_executable_path='/Applications/chromedriver', options=chrome_options, proxy_options=proxy_options)
		self.wait_driver = WebDriverWait(self.driver, 400)

	def quit(self):
		self.driver.quit()

	def is_valid_time(self):
		# get location
		# if late then don't do this bot automation
		ip_address = self.get_ip()
		url = f'http://ipinfo.io/{ip_address}/json'
		response = urlopen(url)
		data = json.load(response)
		loc = data['loc']
		lat, lng = loc.split(",")
		lat = float(lat)
		lng = float(lng)
		timezone_finder = TimezoneFinder()
		location_timezone = timezone_finder.timezone_at(lat=lat, lng=lng)
		timezone_info = timezone(location_timezone)
		time = datetime.now(timezone_info)
		if time.hour < 21: # make sure in working hours (not too late or not too early)
			return True
		return False

	def register(self, register_username, register_password, register_email, backup_email):
		self.driver.get('http://www.neobux.com')
		register_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Register')]")
		register_link.click()

		self.wait_driver.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
		time.sleep(1)
		register_form = self.driver.find_element(By.TAG_NAME, 'tbody')
		register_form.find_element(By.ID, 'nomedeutilizador').send_keys(register_username)
		register_form.find_element(By.ID, 'palavrapasse').send_keys(register_password)
		register_form.find_element(By.ID, 'palavrapasseconfirmacao').send_keys(register_password)
		register_form.find_element(By.ID, 'emailprincipal').send_keys(register_email)
		register_form.find_element(By.ID, 'anonascimento').send_keys('1990')

		captcha_img = register_form.find_element(By.TAG_NAME, 'img').screenshot_as_base64
		captcha_text = solve_captcha(captcha_img)
		register_form.find_element(By.ID, 'codigo').send_keys(captcha_text)

		register_form.find_element(By.ID, 'tosagree').click()
		register_form.find_element(By.ID, 'ppagree').click()
		register_form.find_element(By.ID, 'botao_registo').click()
		# TODO get a check to stop registration if account has already been registered

		self.driver.execute_script("window.open('about:blank','secondtab');")
		time.sleep(1)
		self.driver.switch_to.window(self.driver.window_handles[1])
		verification_code = self.get_verification_from_gmail(register_email, register_password, backup_email)
		self.driver.close()
		self.driver.switch_to.window(self.driver.window_handles[0])

		verification_code_field = self.driver.find_element(By.XPATH, "//input[@type='text']")
		verification_code_field.send_keys(verification_code)
		captcha_img = self.driver.find_element(By.TAG_NAME, 'img').screenshot_as_base64
		captcha_text = solve_captcha(captcha_img)
		self.driver.find_element(By.ID, 'codigo').send_keys(captcha_text)

		finish_registration_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'finish registration')]")
		finish_registration_link.click()

	def get_verification_from_gmail(self, register_email, register_password, backup_email):
		self.driver.get('https://www.google.com/gmail/about/')
		sign_in_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")
		sign_in_link.click()

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Next')]")))
		email_field = self.driver.find_element(By.XPATH, "//input[@type='email']")
		email_field.send_keys(register_email)
		next_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Next')]")
		next_button[1].click()

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
		time.sleep(3)
		password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
		password_field.send_keys(register_password)
		next_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Next')]")
		next_button[1].click()
		time.sleep(3)

		confirm_recovery_email = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Confirm your recovery email')]")
		if len(confirm_recovery_email) != 0:
			confirm_recovery_email[0].click()
			self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
			backup_email_field = self.driver.find_element(By.XPATH, "//input[@type='email']")
			backup_email_field.send_keys(backup_email)
			next_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Next')]")
			next_button[1].click()

			time.sleep(2)
			notnow = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Not now')]")
			if len(notnow) != 0:
				notnow[0].click()

		time.sleep(3)
		smart_features = self.driver.find_elements(By.XPATH,
		                                           "//div[contains(@class, 'aiW aiK')]/div/label[@class='aho']/div[@class='ahq']")
		if len(smart_features) != 0:
			smart_features[0].click()
			time.sleep(1)
			self.wait_driver.until(EC.presence_of_element_located((By.NAME, "data_consent_dialog_next")))
			next_button = self.driver.find_elements(By.NAME, "data_consent_dialog_next")[0]
			next_button.click()

			self.wait_driver.until(EC.presence_of_element_located((By.XPATH,
			                                                       "//div[contains(@class, 'aiW aiM')]/div/label[@class='aho']/div[@class='ahq']")))
			limited_features = self.driver.find_elements(By.XPATH,
			                                                       "//div[contains(@class, 'aiW aiM')]/div/label[@class='aho']/div[@class='ahq']")
			limited_features[1].click()

			self.wait_driver.until(EC.presence_of_element_located((By.NAME, "data_consent_dialog_done")))
			done_button = self.driver.find_elements(By.NAME, 'data_consent_dialog_done')[0]
			done_button.click()

			self.wait_driver.until(EC.presence_of_element_located((By.NAME, "turn_off_cross_product")))
			off_features = self.driver.find_elements(By.NAME, "turn_off_cross_product")
			off_features[0].click()

			self.wait_driver.until(EC.presence_of_element_located((By.NAME, "r")))
			reload = self.driver.find_elements(By.NAME, "r")
			reload[0].click()

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'NeoBux')]")))
		time.sleep(3)
		neo_email = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'New registration: Email verification')]")
		neo_email[1].click()
		self.wait_driver.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'copy-paste')]/following::div[1]")))
		time.sleep(1)
		verification_code = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'copy-paste')]/following::div[1]")[-1].text
		return verification_code

	def __go_profile(self):
		profile_click = self.driver.find_elements(By.ID, 't_conta')
		profile_click[0].click()

	def __go_statistics(self):
		profile_click = self.driver.find_elements(By.ID, 't_conta')
		profile_click[0].click()

		self.wait_driver.until(
			EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Statistics')]")))
		self.driver.find_elements(By.XPATH, "//div/a[contains(text(), 'Statistics')]")[1].click()

	def __go_banners(self):
		profile_click = self.driver.find_elements(By.ID, 't_conta')
		profile_click[0].click()

		self.wait_driver.until(
			EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Banners')]")))
		self.driver.find_elements(By.XPATH, "//div/a[contains(text(), 'Banners')]")[1].click()

	def __go_coins(self):
		self.driver.find_elements(By.XPATH, "//*[contains(text(), 'View Advertisements')]")[0].click()
		self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Coins')]")[0].click()

	def get_random_process(self):
		random_times = random.randint(1, 10)

		random_funcs = [self.__go_banners, self.__go_statistics, self.__go_coins, self.__go_profile]

		for i in range(random_times):
			random.choice(random_funcs)()
			time.sleep(5)

	def start_process(self, username, password):
		if not self.is_valid_time():
			return

		self.driver.get('http://www.neobux.com')

		advertisements_link_list = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'View Advertisements')]")
		if len(advertisements_link_list) == 0:
			login_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Login')]")[0]
			login_button.click()

			login_form = self.driver.find_element(By.TAG_NAME, 'tbody')
			login_form.find_element(By.ID, 'Kf1').send_keys(username)
			login_form.find_element(By.ID, 'Kf2').send_keys(password)
			login_form.find_element(By.ID, 'Kf4').send_keys(password)
			login_form.find_element(By.ID, 'botao_login').click()

		# randomize
		self.wait_driver.until(
			EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'View Advertisements')]")))
		self.get_random_process()

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'View Advertisements')]")))
		view_ad_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'View Advertisements')]")[0]
		view_ad_button.click()

		self.wait_driver.until(EC.visibility_of_element_located((By.CLASS_NAME, 'cell')))
		time.sleep(1)
		all_clickable_ads = self.driver.find_elements(By.CLASS_NAME, 'cell')

		for ad in all_clickable_ads:
			# if ad has been clicked before then continue to the next one
			if len(ad.find_elements(By.CLASS_NAME, 'ad0')) > 0:
				continue

			ad.click()
			red_dot = ad.find_element(By.TAG_NAME, 'img')
			red_dot.click()

			self.driver.switch_to.window(self.driver.window_handles[1])
			self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'validated')]")))
			close_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Close')]")[0]
			close_button.click()

			self.driver.switch_to.window(self.driver.window_handles[0])
			# self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Fixed Advertisements')]")))
