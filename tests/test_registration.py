import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
	d = webdriver.Chrome()
	yield d
	d.quit()

def test_empty_username(driver):
	driver.get("http://127.0.0.1:5000/")
	driver.find_element(By.NAME, "pwd").send_keys("Gnit@2023")
	driver.find_element(By.NAME, "sb").click()
	time.sleep(3)
	WebDriverWait(driver, 10).until(EC.alert_is_present())
	a = Alert(driver)
	assert a.text == "Username cannot be empty."
	a.accept()

def test_empty_password(driver):
	driver.get("http://127.0.0.1:5000/")
	driver.find_element(By.NAME, "username").send_keys("yasan30")
	driver.find_element(By.NAME, "sb").click()
	time.sleep(3)
	WebDriverWait(driver, 10).until(EC.alert_is_present())
	a = Alert(driver)
	assert a.text == "Password cannot be empty."
	a.accept()

def test_short_password(driver):
	driver.get("http://127.0.0.1:5000/")
	driver.find_element(By.NAME, "username").send_keys("yasan30")
	driver.find_element(By.NAME, "pwd").send_keys("abc1")
	driver.find_element(By.NAME, "sb").click()
	time.sleep(3)
	WebDriverWait(driver, 10).until(EC.alert_is_present())
	a = Alert(driver)
	assert a.text == "Password must be at least 6 characters long."
	a.accept()

def test_valid_input(driver):
	driver.get("http://127.0.0.1:5000/")
	driver.find_element(By.NAME, "username").send_keys("yasan30")
	driver.find_element(By.NAME, "pwd").send_keys("Gnit@2023")
	driver.find_element(By.NAME, "sb").click()
	time.sleep(3)
	WebDriverWait(driver, 10).until(EC.url_contains("/submit"))
	assert "Hello, yasan30! Welcome to the website" in driver.find_element(By.TAG_NAME, "body").text