from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time


class Sites:

	@abstractmethod
	def start_process(self):
		pass

register_username = 'jttgitdfhiitrydfhfgjefvj'
register_password = 'Musqthcdjgd'
register_email = 'jttgitdfhiitrydfhfgjefvj@gmail.com'

username = register_username
password = register_password

class NeoBux(Sites):
	def __init__(self):
		chrome_options = uc.ChromeOptions()
		# chrome_options.add_argument('--user-data-dir=user_data')
		self.driver = uc.Chrome(driver_executable_path='/Applications/chromedriver', options=chrome_options)
		self.wait_driver = WebDriverWait(self.driver, 400)

	def register(self):
		self.driver.get('http://www.neobux.com')
		register_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Register')]")
		register_link.click()

		register_form = self.driver.find_element(By.TAG_NAME, 'tbody')
		register_form.find_element(By.ID, 'nomedeutilizador').send_keys(register_username)
		register_form.find_element(By.ID, 'palavrapasse').send_keys(register_password)
		register_form.find_element(By.ID, 'palavrapasseconfirmacao').send_keys(register_password)
		register_form.find_element(By.ID, 'emailprincipal').send_keys(register_email)
		register_form.find_element(By.ID, 'anonascimento').send_keys('1990')
		# TODO: add anti captcha
		register_form.find_element(By.ID, 'tosagree').click()
		register_form.find_element(By.ID, 'ppagree').click()

		self.driver.execute_script("window.open('about:blank','secondtab');")
		self.driver.switch_to.window(self.driver.window_handles[1])
		verification_code = self.get_verification_from_gmail()
		self.driver.close()
		self.driver.switch_to.window(self.driver.window_handles[0])

		verification_code_field = self.driver.find_element(By.XPATH, "//input[@type='text']")
		verification_code_field.send_keys(verification_code)
		#TODO: add anti captcha
		finish_registration_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'finish registration')]")
		finish_registration_link.click()

	def get_verification_from_gmail(self):
		self.driver.get('https://www.google.com/gmail/about/')
		sign_in_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")
		sign_in_link.click()

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Next')]")))
		email_field = self.driver.find_element(By.XPATH, "//input[@type='email']")
		email_field.send_keys(register_email)
		next_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Next')]")
		next_button[1].click()

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
		time.sleep(1)
		password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
		password_field.send_keys(register_password)
		next_button = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Next')]")
		next_button[1].click()

		self.wait_driver.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'NeoBux')]")))
		time.sleep(1)
		neo_email = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'NeoBux')]")
		neo_email[1].click()
		self.wait_driver.until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'copy-paste')]/following::div[1]")))
		verification_code = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'copy-paste')]/following::div[1]")[1].text
		return verification_code

	def start_process(self):
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


if __name__ == '__main__':
	web = NeoBux()
	web.start_process()