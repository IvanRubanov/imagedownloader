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
        else:
            self.__logger = logger

    def get_request(self, url):
        """ Get Request object from givven url """
        """ See https://docs.python.org/2/library/urllib.html """
        request = None
        try:
           request = urllib2.urlopen(url)
        except urllib2.URLError, e:
            self.__logger.error('couldnt-establish-connection reason = %s url = %s', e, url)
            raise e
        code = request.getcode()
        if code < 200 or code > 307:
            self.__logger.error('bad-http-response code = %d', code)
            raise URLError('bad http response')
        return request

    def __close_request(self, request):
        """ Close opened request """
        if request is None :
            self.__logger.warn('couldnt-close-request reason = request is None')
        else:
            request.close()

    def get_xhtml(self, url):
        """ Load and return xhtml for givven url """
        """ Return the tuple (xhtml_doc, base_url) """
        request = self.get_request(url)
        xhtml_doc = request.read()
        base_url = request.geturl()
        pbu = urlparse(base_url)
        base_url = pbu.scheme + '://' + pbu.netloc
        query = pbu.query
        
        self.__close_request(request)
        return (xhtml_doc, base_url, query)

    def retrieve_image(self, url, filename):
        """ Retrieve file from url and save it out directory """
        try:
            urllib.urlretrieve(url, filename)
        except URLError, e:
            self.__logger.warn('couldnt-download-and-save-file url = %s reason = %s filename = %s', url, e, filename)
            raise e