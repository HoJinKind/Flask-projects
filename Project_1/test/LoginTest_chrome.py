from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("C:/chromedriver.exe")

driver.get('http://127.0.0.1:5000/')#flaskapp running address
assert "login" in driver.title
if not "login" in driver.title:
    raise Exception("Unable to load eGenda page!")
user="tom"
pwd="sutd1234"
elem = driver.find_element_by_name("username")
elem.send_keys(user)
elem = driver.find_element_by_name("pd")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

driver.close()
