import urllib2
import urllib
import logging
import os
from urlparse import urlparse
from urllib2 import URLError

class HttpHandler:
    def __init__(self, logger):
        if logger is None:
            self.__logger = logging.getLogger(config.default_logger_tag)
            formatter = logging.Formatter(config.default_logger_format)
            self.__logger.setFormatter(formatter)
        else:
            self.__logger = logger

    def __get_request(self, url):
        """ Get Request object from givven url """
        """ See https://docs.python.org/2/library/urllib.html """
        request = None
        try:
           request = urllib2.urlopen(url)
        except urllib2.URLError, e:
            self.__logger.error('couldn\'t establish connectio, reason: ' + e.reason + ' url: ' + url)
            raise e
        code = request.getcode()
        if code < 200 or code > 307:
            self.__logger.error('bad http response, code: ' + code)
            raise URLError
        return request

    def __close_request(self, request):
        """ Close opened request """
        if request is None :
            self.__logger.warn('couldn\'t close request, reason: request is None')
        else:
            request.close()

    def get_xhtml(self, url):
        """ Load and return xhtml for givven url """
        xhtml_doc = None
        base_url = None
        try:
            request = self.__get_request(url)
            xhtml_doc = request.read()
            base_url = request.geturl()
            pbu = urlparse(base_url)
            base_url = pbu.scheme + '://' + pbu.netloc
            self.__close_request(request)
        except urllib2.URLError, e:
            self.__logger.error('couldn\'t open givven url, reason: ' + e.reason + ' url: ' + url)
            raise e
        return (xhtml_doc, base_url)

    def retrieve_image(self, url, directory):
        """ Retrieve file from url and save it directory """
        filename=url.split('/')[-1]
        filename = os.path.join(directory, filename)
        try:
            urllib.urlretrieve(url, filename)
        except URLError, e:
            self.__logger.warn('couldn\'t download and save file url: ' + url + ', reson:'  + e + ', directory: ' + directory)