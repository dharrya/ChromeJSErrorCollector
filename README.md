JSErrorCollector for Chrome provide access to JavaScript errors while running tests with a ChromeDriver.<br>
Usage in Python:<br>
<pre>
	<code>
#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pprint

chrome_options = Options()
chrome_options.add_argument('--user-data-dir=chrome_data')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('http://stuff-dharrya.rhcloud.com/get_js_error')
pprint.pprint(driver.execute_script('return window.JSErrorCollector_errors ? window.JSErrorCollector_errors.pump() : []')) 
driver.quit()
	</code>
</pre>
Note: When you first start you must install the extension from the extension folder.<br>
<p>
I've been inspired to this by Oleg Strokatyy. He is a nice funny guy and great professional:-)
</p>