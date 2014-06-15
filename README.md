imagedownloader
===============

Parse the XHTML and download all images defined in <img> tag.

Application is following redirects. Saves images defined in relative and absolute pathes in output folder. The name of output folder is date and time of a moment when it was executed. Application accepts urls formats: http://hostname (for example, http://google.com) or hostname (for example, google.com). By default application uses http protocol. If image's file name longer then 255 symbols then stripes beginning and saves only last 255 symbols of file name. If error occures during the execution application ingnores it and continues execution with one exception if application can't create output folder then it stops.

Usage: ./imagedownloader.py <list of urls>
Example: ./imagedownloader.py google.com yahoo.com http://beddit.com