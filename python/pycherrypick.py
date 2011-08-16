#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (c) 2011, wg_koro <zeathwing@gmail.com> <http://zafiel.wingall.com/>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
import urllib2
import re
import time
import os.path
import traceback

class PyCherryPick:
    def __init__(self, page=''):
        self.version = '0.0.1'
        self.page = page
        self.ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
        self.interval = 2
        self.regex = 'http.+\.jpg'
        self.encode = 'utf-8'
        self.regex_url = re.compile('^https?:\/\/.+')
        self.html = ''

        realpath = os.path.realpath(os.path.dirname(__file__))
        self.download_dir = os.path.join(realpath, 'downloads/%s')


    def scrape(self):
        """
        Scrape HTML and return 'download URL' lists.
        """
        reg = re.compile(self.regex)
        links = self.soup.findAll('a')
        results = []
        for link in links:
            try:
                url = dict(link.attrs)['href']
                url = self._make_url_path(url)
                if reg.match(url):
                    results.append(url)

            except:
                pass

        print 'Scraping OK'
        return results


    def set_page(self, page):
        if page:
            self.page = page


    def set_encode(self, enc):
        if enc:
            self.encode = enc


    def set_interval(self, interval):
        if interval is 0:
            self.interval = 0
        elif interval:
            self.interval = interval


    def set_user_agent(self, ua):
        if ua:
            self.ua = ua


    def set_file_type(self, type):
        if type:
            reg = 'http.+\.(%s)'
            types = type.split(',')
            self.regex = reg % '|'.join(types)


    def set_regex(self, regex):
        if regex:
            self.regex = regex


    def set_html_file(self, html_file):
        if html_file:
            if os.path.isfile(html_file):
                filepath = html_file
            else:
                filepath = './html/%s' % html_file

            if os.path.isfile(filepath):
                for line in open(filepath, 'r'):
                    self.html += line
                
                return True
            else:
                return False


    def set_download_dir(self, path):
        if os.path.isdir(path):
            self.download_dir = path +'/%s'
            return True
        else:
            return False


    def _make_url_path(self, path):
        if not self.regex_url.match(path):
            return urljoin(self.page, path)
        else:
            return path


    def _get_url_lists(self):
        self._set_html_data()

        if not self.html:
            return []

        print 'Start Scraping'
        self.soup = BeautifulSoup(self.html)
        return self.scrape()


    def _set_html_data(self):
        """
        If Local HTML file name is not defined, fetch HTML data via HTTP.
        """
        if not self.html:
            if not self.page:
                print 'Target URL is not defined'
                self.html = ''
                return

            print 'Start fetching page: %s' % self.page
            html = unicode(self._download(self.page).read(), self.encode, 'ignore')
            if not html:
                self.html = ''
            else:
                self.html = html
                print 'Fetching OK'

        else:
            print 'Scrape Local HTML File'


    def _download(self, url):
        """Open URL with custom user-agent"""
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent', self.ua)]
            return opener.open(url)
        except:
            print 'URL Open Error: [ %s ]' % traceback.format_exc()
            return False


    def get_files(self):
        """Download files and store them"""
        print '* * * Start PyCherryPick * * *'

        url_list = self._get_url_lists()

        count = len(url_list)
        if count < 1:
            print 'URL list is empty'
        elif count == 1:
            self.interval = 0

        for i, url in enumerate(url_list):
            fname = os.path.basename(url)
            print 'Start download %s' % fname
            try:
                dw = self._download(url)
                if not dw:
                    raise

                localfile = open(self.download_dir % fname, 'wb')
                localfile.write(dw.read())
                dw.close()
                localfile.close()
                c = i + 1
                print '...OK (%d/%d)' % (c, count)
            except:
                print 'Download Error: %s\n' % url

            time.sleep(self.interval)

        print '----- End PyCherryPick -----'


    def main(self):
        """Parse command line"""
        from optparse import OptionParser
        usage = u'%prog [target page URL] [Options]\nDetailed options -h or --help'
        parser = OptionParser(usage=usage, version=self.version)
        parser.add_option(
                '-f', '--file',
                action = 'store',
                type = 'string',
                help = 'local HTML file path. example:"/Users/Foo/html/bar.html"'
                )

        parser.add_option(
                '-t', '--type',
                action = 'store',
                type = 'string',
                help = 'download file type. example:"jpg" "jpg,png,gif"'
                )

        parser.add_option(
                '-d', '--download',
                action = 'store',
                type = 'string',
                help = 'download directory path. example:"/User/foo/downloads"'
                )

        parser.add_option(
                '-e', '--encode',
                action = 'store',
                type = 'string',
                help = 'character encoding of target page. example:"utf-8"'
                )

        parser.add_option(
                '-i', '--interval',
                action = 'store',
                type = 'int',
                help = 'interval of downloading files (seconds)'
                )

        parser.add_option(
                '-u', '--ua',
                action = 'store',
                type = 'string',
                help = 'custom user-agent'
                )

        parser.add_option(
                '-r', '--regex',
                action = 'store',
                type = 'string',
                help = 'regexpression for dowload file\'s url'
                )

        parser.set_defaults(
                file = '',
                encode = '',
                interval = 2,
                ua = '',
                type = '',
                download = '',
                regex = ''
                )

        options, args = parser.parse_args()
        count = len(args)

        if count > 1:
            parser.error('Too many target')
        elif count == 1 and not re.match('^https?:\/\/.+', args[0]):
            parser.error('Invalid target')

        if not options.file and count is 0:
            parser.error('Target URL or Local file name must be defined')

        if options.file:
            if not self.set_html_file(options.file):
                print 'HTML file not found'
                sys.exit(2)

        else:
            self.set_page(args[0])

        if options.download and not self.set_download_dir(options.download):
            print 'Download directory not found'
            sys.exit(2)

        if options.regex:
            self.set_regex(options.regex)
        else:
            self.set_file_type(options.type)

        self.set_encode(options.encode)
        self.set_user_agent(options.ua)
        self.set_interval(options.interval)
        self.get_files()





if __name__ == '__main__':
    """
    import doctest
    doctest.testmod()
    """

    c = PyCherryPick()
    c.main()
