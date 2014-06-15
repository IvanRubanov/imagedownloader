#!/usr/bin/python

import unittest
import logging
import config
import shutil
import urllib
import os.path

from urllib2 import URLError
from logging import Logger

from httphandler import HttpHandler
from imagedownloader import ImageDownloader

class TestImageDownloader(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(config.default_logger_tag)
        logging.basicConfig()
        self.http_handler = HttpHandler(self.logger)
        self.image_downloader = ImageDownloader(self.http_handler, self.logger)

    def test_normalize_url(self):
        with self.assertRaises(TypeError):
            self.image_downloader.normalize_url(None)

        url = self.image_downloader.normalize_url('b.com')
        self.assertEqual('http://b.com', url)
        
        url = self.image_downloader.normalize_url('/a.png', 'http://b.com')
        self.assertEqual('http://b.com/a.png', url)
        
        url = self.image_downloader.normalize_url('/a.png', 'http://b.com', 'q=1')
        self.assertEqual('http://b.com/a.png?q=1', url)
        
        url = self.image_downloader.normalize_url('//b.com/a.png')
        self.assertEqual('http://b.com/a.png', url)
        
        url = self.image_downloader.normalize_url('//b.com/a.png', None, 'q=1')
        self.assertEqual('http://b.com/a.png?q=1', url)

    def test_get_urls(self):
        with self.assertRaises(TypeError):
            self.image_downloader.get_urls(None)
            self.image_downloader.get_urls([])
        
        urls = self.image_downloader.get_urls(['a'])
        self.assertEqual(1, len(urls))

        urls = self.image_downloader.get_urls(['a', 'a'])
        self.assertEqual(2, len(urls))

        urls = self.image_downloader.get_urls(['a', 'b', 'c'])
        self.assertEqual(3, len(urls))


    def test_download_images(self):
        class TestHttpHandlerRaiseAlways():
            def get_request(self, url):
                raise URLError('Test url error in get_request')
            def __close_request(self, request):
                return
            def get_xhtml(self, url):
                raise URLError('Test url error in get_xhtml')
            def retrieve_image(self, url, filename):
                raise URLError('Test url error in retrieve_image')

        class TestImageDownloader(ImageDownloader):
             def get_formatted_date(self):
                return 'test_out'

        try:
            shutil.rmtree('test_out')
        except:
            pass
        test_http_handler = TestHttpHandlerRaiseAlways()
        test_image_downloader = TestImageDownloader(test_http_handler, self.logger)
        test_image_downloader.download_images(['http://beddit.com'])

        class TestHttpHandler():
            def get_request(self, url):
                return
            def __close_request(self, request):
                return
            def get_xhtml(self, url):
                xhtml_doc = '<html><img src="/static/img/beddit_logo.png" class="logo">"></img></html>'
                base_url = 'http://beddit.com'
                query = None
                return (xhtml_doc, base_url, query)
            def retrieve_image(self, url, filename):
                urllib.urlretrieve(url, 'beddit_logo.png')

        try:
            shutil.rmtree('test_out')
        except:
            pass

        test_http_handler = TestHttpHandler()
        test_image_downloader = TestImageDownloader(test_http_handler, self.logger)
        test_image_downloader.download_images(['http://beddit.com'])
        self.assertTrue(os.path.isfile('beddit_logo.png'))

        try:
            shutil.rmtree('test_out')
            os.remove('beddit_logo.png')
        except:
            pass

if __name__ == '__main__':
    unittest.main()