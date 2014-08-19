from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

class DjangoMeshTestAdmin(LiveServerTestCase):
	def setUp(self):
		
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_admin_login(self):
	
		user = User.objects.create_user(username='admin', 
										email='admin@admin.com',
										password= 'admin',
		)
		user.is_staff = True
		user.is_superuser = True
		user.save()

		
		self.browser.get(self.live_server_url + '/admin/')

		username = self.browser.find_element_by_name('username')
		username.send_keys('admin')

		password = self.browser.find_element_by_name('password')
		password.send_keys('admin')

		password.send_keys(Keys.RETURN)
	
		
		tryChannels = self.browser.find_element_by_link_text('Channels')
		tryChannels.click()

		self.browser.back()

		tryPosts = self.browser.find_element_by_link_text('Posts')
		tryPosts.click()

		self.browser.back()

		tryComments = self.browser.find_element_by_link_text('Comments')
		tryComments.click()

	





