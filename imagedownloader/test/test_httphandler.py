#!/usr/bin/python

import unittest
import logging
import config

from httphandler import HttpHandler

class TestHttpHandler(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(config.default_logger_tag)
        logging.basicConfig()
        self.http_handler = HttpHandler(self.logger)

    
    def test_get_xhtml(self):
        with self.assertRaises(AttributeError):
            self.http_handler.get_xhtml(None)
            self.http_handler.get_xhtml('google.com')
        
        result = self.http_handler.get_xhtml('http://google.com')
        self.assertTrue(len(result[0]) > 0)
        self.assertTrue(len(result[1]) > 0)
        self.assertTrue(len(result[2]) > 0)

        result = self.http_handler.get_xhtml('http://beddit.com')
        self.assertTrue(len(result[0]) > 0)
        self.assertTrue(len(result[1]) > 0)
        self.assertTrue(len(result[2]) == 0)

if __name__ == '__main__':
    unittest.main()