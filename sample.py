#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_extension('extension.crx')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('http://stuff-dharrya.rhcloud.com/get_js_error')
print(driver.execute_script('return window.JSErrorCollector_errors ? window.JSErrorCollector_errors.pump() : []')) 
driver.quit()