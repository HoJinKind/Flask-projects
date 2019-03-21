from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("C:/chromedriver.exe")

driver.get('http://127.0.0.1:5000/')#flaskapp running address
assert "login" in driver.title
if not "login" in driver.title:
    raise Exception("Unable to load eGenda page!")

user = "tomwdsf"
pwd = "sutd1234wwdscfg"

driver.find_element_by_name("username").click()
driver.find_element_by_name("username").clear()
driver.find_element_by_name("username").send_keys(user)
assert "tom" == user
driver.find_element_by_name("pd").click()
driver.find_element_by_name("pd").clear()
driver.find_element_by_name("pd").send_keys(pwd)
assert "sutd1234" == pwd
driver.find_element_by_name("pd").send_keys(Keys.ENTER)
driver.close()
