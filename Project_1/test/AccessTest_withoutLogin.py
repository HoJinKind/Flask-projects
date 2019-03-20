from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask , request, jsonify, render_template,redirect,url_for,session


driver = webdriver.Chrome("C:/chromedriver.exe")

driver.get('http://127.0.0.1:5000/home')#flaskapp running address
if not session['loggedIn']== True:
    raise AssertionError()

assert "home" in driver.title

driver.close()
