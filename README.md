ChromeJSErrorCollector
==============

## Introduction
JSErrorCollector for Chrome provide access to JavaScript errors while running tests with a ChromeDriver.

## Usage
Simple Python code:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_extension('extension.crx')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('http://stuff-dharrya.rhcloud.com/get_js_error')
print(driver.execute_script('return window.JSErrorCollector_errors ? window.JSErrorCollector_errors.pump() : []')) 
driver.quit()
```
Will output:

```
[{
	'sourceName': 'http://stuff-dharrya.rhcloud.com/get_js_error',
	'pageUrl': 'http://stuff-dharrya.rhcloud.com/get_js_error',
	'errorMessage': 'ReferenceError: someVariable is not defined',
	'lineNumber': 9
}]
```
## Thanks
I've been inspired to this by Oleg Strokatyy. He is a nice funny guy and great professional:-)