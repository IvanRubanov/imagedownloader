#!/usr/bin/python

import sys
import os
import config
import logging
import urllib2
import datetime
from bs4 import BeautifulSoup

from httphandler import HttpHandler

class ImageDownloader:
    def __init__(self, http_handler, logger):
        if http_handler is None:
            raise ValueError('http_handler must not be None')
        else:
            self.__http_handler = http_handler
        if logger is None:
            self.__logger = logging.getLogger(config.default_logger_tag)
        else:
            self.__logger = logger

    def __print_usage_instructions(self):
        print "Usage: ./imagedownloader.py <list of urls>"
        print "Example: ./imagedownloader.py google.com yahoo.com http://beddit.com"

    def get_formatted_date(self):
        return str(datetime.datetime.now().strftime(config.default_date_format))

    def __create_out_directory(self):
        """ Create output directory """ 
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), str(self.get_formatted_date()))
        try:
            os.makedirs(directory)
        except os.error, e:
            self.__logger.error('couldnt-create-output-directory reason = %s', e)
            raise e 
        return directory

    def normalize_url(self, url, base_url=None, query=None):
        """ Normalize url for further ugage """
        """ Supports following rules: """ 
        """ if url starts with default protocol (http) then return url without modifications """ 
        """ if url starts with '//' then return url  = http:+url """ 
        """ in any othe case adding 'http://' in front """
        if url is None or not url:
            self.__logger.error('couldnt-normalize-url reason = url is None or empty string')
            raise TypeError('url must not be None or empty')
        if not url.startswith(config.default_protocol):
            if url.startswith('//'):
                url = config.default_protocol + ':' + url
            else:
                if base_url  is not None:
                    url = base_url + url
                else:
                    url = config.default_protocol + '://' + url
        if query is not None and query:
            url = url + '?' + query
        return url

    def get_urls(self, args):
        """ Parse command line arguments and return the list of url """
        if args is None or not args:
            self.__logger.error('couldnt-get-urls-from-args  reason = args is None or empty list')
            raise TypeError('args must not be None or empty')
        result = []
        if len(args) < 1:
            self.__print_usage_instructions()
        else:
            for arg in args:
                if(arg):
                    result.append(self.normalize_url(arg))
        return result

    def __get_src_urls(self, xhtmlDoc, base_url):
        """ Parse xhtml doc and get the list of src urls """
        soup = BeautifulSoup(xhtmlDoc)
        img_tags = soup.findAll('img')
        result = []
        for img in img_tags:
            img_url = img['src']
            try:
                img_url = self.normalize_url(img_url, base_url)
                result.append(img_url)
            except TypeError, e:
                self.__logger.error('couldnt-normalize-src-url reson = %s', e)
        return result

    def download_images(self, args):
        try:
            urls = self.get_urls(args)
        except TypeError, e:
            self.__logger.error('fatal-error-occured-during-downloading-images  error = %s', e)
            raise e
        else:
            if len(urls) > 0:
                try:
                    out_dir = self.__create_out_directory()
                except os.error, e:
                    self.__logger.error('error-occured-during-mk-out-dir error = %s', e)
                    raise e
                else:
                    for url in urls:
                        try:
                            doc = self.__http_handler.get_xhtml(url)
                            xhtml_doc = doc[0]
                            base_url = doc[1]
                            query = doc[2]
                            img_urls = self.__get_src_urls(xhtml_doc, base_url)
                            for img_url in img_urls:
                                filename = img_url.split('/')[-1]
                                if len(filename) >= 255:
                                    filename = filename[-254:]
                                filename = os.path.join(out_dir, filename)
                                img_url = self.normalize_url(img_url, base_url, query)
                                try:
                                    self.__http_handler.retrieve_image(img_url, filename)
                                except:
                                    pass
                        except:
                            pass


if __name__ == "__main__":
    logger = logging.getLogger(config.default_logger_tag)
    logging.basicConfig()
    http_handler = HttpHandler(logger)
    image_downloader = ImageDownloader(http_handler, logger)
    image_downloader.download_images(sys.argv[1:])