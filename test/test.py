#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import inspect


class Test(object):
    _pump_js = 'return window.JSErrorCollector_errors ? window.JSErrorCollector_errors.pump() : []'
    _clear_js = 'if(!!window.JSErrorCollector_errors) window.JSErrorCollector_errors.clear();'
    _close_driver = True

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--user-data-dir=.chrome_driver_data')
        self._driver = webdriver.Chrome(chrome_options=chrome_options)

    def run(self):
        if not self.test_extension_installed():
            self._close_driver = False
            print('Extension not installed, please install it at chrome://extensions page')
            return

        self.test_simple_event()
        self.test_simple()
        self.test_frame()
        self.test_external_js()
        self.test_external_js_cors()
        print('All done, you\'re rock!')

    def test_extension_installed(self):
        uri = self.get_resource('extension_installed.html')
        self._driver.get(uri)
        self.clear_errors()
        return self._driver.execute_script('return !!window.JSErrorCollector_errors')

    def test_simple_inline(self):
        uri = self.get_resource('simple.html')
        self._driver.get(uri)
        actual_errors = self.remove_path(self.get_errors())
        expected_errors = [
            {
                'errorMessage': "TypeError: Cannot read property 'inlineError' of null",
                'sourceName': 'simple.html',
                'pageUrl': 'simple.html',
                'lineNumber': 5
            }
        ]
        return self.equals(expected_errors, actual_errors)

    def test_simple_event(self):
        uri = self.get_resource('simple.html')
        self._driver.get(uri)
        self.clear_errors()
        self._driver.find_element_by_tag_name('button').click()
        actual_errors = self.remove_path(self.get_errors())
        expected_errors = [
            {
                'errorMessage': 'ReferenceError: eventError is not defined',
                'sourceName': 'simple.html',
                'pageUrl': 'simple.html',
                'lineNumber': 9
            }
        ]
        return self.equals(expected_errors, actual_errors)

    def test_simple(self):
        uri = self.get_resource('simple.html')
        self._driver.get(uri)
        self._driver.find_element_by_tag_name('button').click()
        actual_errors = self.remove_path(self.get_errors())
        expected_errors = [
            {
                'errorMessage': "TypeError: Cannot read property 'inlineError' of null",
                'sourceName': 'simple.html',
                'pageUrl': 'simple.html',
                'lineNumber': 5
            },
            {
                'errorMessage': 'ReferenceError: eventError is not defined',
                'sourceName': 'simple.html',
                'pageUrl': 'simple.html',
                'lineNumber': 9
            }
        ]
        return self.equals(expected_errors, actual_errors)

    def test_frame(self):
        uri = self.get_resource('frame.html')
        self._driver.get(uri)
        actual_errors = self.remove_path(self.get_errors())
        expected_errors = [
            {
                'errorMessage': "TypeError: Cannot read property 'inlineError' of null",
                'sourceName': 'simple.html',
                'pageUrl': 'simple.html',
                'lineNumber': 5
            }
        ]
        return self.equals(expected_errors, actual_errors)

    def test_external_js(self):
        uri = 'http://stuff-dharrya.rhcloud.com/static/js_error_collector/external_js.html'
        self._driver.get(uri)
        actual_errors = self.get_errors()
        expected_errors = [
            {
                'errorMessage': "ReferenceError: foo is not defined",
                'sourceName': 'http://stuff-dharrya.rhcloud.com/static/js_error_collector/external.js',
                'pageUrl': uri,
                'lineNumber': 1
            }
        ]
        return self.equals(expected_errors, actual_errors)

    def test_external_js_cors(self):
        uri = self.get_resource('external_js.html')
        self._driver.get(uri)
        actual_errors = self.remove_path(self.get_errors())
        #ErrorEvent{lineno: 0, filename: "", message: "Script error." ..} on cross-domain JS error by security policy
        expected_errors = [
            {
                'errorMessage': 'Script error.',
                'sourceName': '',
                'pageUrl': 'external_js.html',
                'lineNumber': 0
            }
        ]
        return self.equals(expected_errors, actual_errors)

    def get_resource(self, file_name):
        return 'file://{abs_path}'.format(
            abs_path=os.path.abspath('resources/' + file_name)
        )

    def get_errors(self):
        return self._driver.execute_script(self._pump_js)

    def clear_errors(self):
        return self._driver.execute_script(self._clear_js)

    def remove_path(self, errors):
        for item in errors:
            if 'sourceName' in item:
                item['sourceName'] = os.path.basename(item['sourceName'])
            if 'pageUrl' in item:
                item['pageUrl'] = os.path.basename(item['pageUrl'])
        return errors

    def equals(self, expected, actual):
        if expected != actual:
            test_name = inspect.stack()[1][3]
            delimiter = '-' * 10
            print('''
                {delimiter}\n
                {test_name} - Failed\n
                Expected: {expected}\n
                Actual: {actual}\n
                {delimiter}\n
                '''.format(
                delimiter=delimiter,
                test_name=test_name,
                expected=expected,
                actual=actual
                )
            )
            return False
        return True

    def __del__(self):
        if self._close_driver:
            self._driver.quit()

if __name__ == '__main__':
    tests = Test()
    tests.run()
