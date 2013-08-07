#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import unittest


class Test(unittest.TestCase):
    _pump_js = 'return window.JSErrorCollector_errors ? window.JSErrorCollector_errors.pump() : []'
    _clear_js = 'if(!!window.JSErrorCollector_errors) window.JSErrorCollector_errors.clear();'
    _driver = None

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_extension('../extension.crx')
        cls._driver = webdriver.Chrome(chrome_options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls._driver.quit()

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
        self.assertEqual(expected_errors, actual_errors)

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
        self.assertEqual(expected_errors, actual_errors)

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
        self.assertEqual(expected_errors, actual_errors)

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
        self.assertEqual(expected_errors, actual_errors)

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
        self.assertEqual(expected_errors, actual_errors)

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
        self.assertEqual(expected_errors, actual_errors)

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


if __name__ == '__main__':
    unittest.main()
