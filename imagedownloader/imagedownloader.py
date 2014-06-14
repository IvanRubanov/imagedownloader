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
            raise ValueError
        else:
            self.__http_handler = http_handler
        if logger is None:
            self.__logger = logging.getLogger(config.default_logger_tag)
            formatter = logging.Formatter(config.default_logger_format)
            self.__logger.setFormatter(formatter)
        else:
            self.__logger = logger

    def print_usage_instructions(self):
        # TODO: Write usage instructions
        print "Usage:!!!"

    def __get_formatted_date(self):
        return str(datetime.datetime.now().strftime(config.default_date_format))

    def __create_out_directory(self):
        """ Create output directory """ 
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), str(self.__get_formatted_date()))
        try:
            os.makedirs(directory)
        except os.error, e:
            self.__logger.error('couldn\'t create output directory, reason: ' + e)
            raise e 
        return directory

    def __normalize_url(self, url, base_url=None):
        """ Normalize url for further ugage """
        """ Supports following rules: """ 
        """ if url starts with default protocol (http) then return url without modifications """ 
        """ if url starts with '//' then return url  = http:+url """ 
        """ in any othe case adding 'http://' in front """
        if url is None or not url:
            self.__logger.error('couldn\'t normalize url, reason: url is None or empty string')
            raise TypeError
        if not url.startswith(config.default_protocol):
            if url.startswith('//'):
                url = config.default_protocol + ':' + url
            else:
                if base_url  is not None:
                    url = base_url + url
                else:
                    url = config.default_protocol + '://' + url
        return url

    def __get_urls(self, args):
        """ Parse command line arguments and return the list of url """
        if args is None or not args:
            self.__logger.error('couldn\'t get urls from args, reason: args is None or empty list')
            raise TypeError
        result = []
        if len(args) < 2:
            self.print_usage_instructions()
        else:
            args_len = len(args)
            for i in range(1,args_len):
                arg = args[i]
                result.append(self.__normalize_url(arg))
        return result

    def __get_src_urls(self, xhtmlDoc, base_url):
        """ Parse xhtml doc and get the list of src urls """
        soup = BeautifulSoup(''.join(xhtmlDoc))
        img_tags = soup.findAll('img')
        result = []
        for img in img_tags:
            img_url = img['src']
            try:
                img_url = self.__normalize_url(img_url, base_url)
                result.append(img_url)
            except TypeError, e:
                self.__logger.error('couldn\'t normalize src url, reson: ' + e)
        return result

    def download_images(self):
        urls = self.__get_urls(sys.argv)
        try:
            out_dir = self.__create_out_directory()
            for url in urls:
                try:
                    doc = self.__http_handler.get_xhtml(url)
                    xhtml_doc = doc[0]
                    base_url = doc[1]
                    img_urls = self.__get_src_urls(xhtml_doc, base_url)
                    for img_url in img_urls:
                        img_url = self.__normalize_url(img_url, base_url)
                        print img_url
                        self.__http_handler.retrieve_image(img_url, out_dir)
                except Exception, e:
                    self.__logger.warn('warning here ' + str(e))
        except Exception, e:
            self.__logger.error('FATAL ERROR:' + str(e))

if __name__ == "__main__":
    logger = logging.getLogger(config.default_logger_tag)
    logging.basicConfig()
    formatter = logging.Formatter(config.default_logger_format)
    http_handler = HttpHandler(logger)
    image_downloader = ImageDownloader(http_handler, logger)
    image_downloader.download_images()

