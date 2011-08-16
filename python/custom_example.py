#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycherrypick import PyCherryPick
import re

class CustomExample(PyCherryPick):
    def __init__(self):
        CherryPick.__init__(self)


    def scrape(self):
        """
        Write new scraping, and returning urls process.
        This example shows scraping img tag's src.
        """
        reg = re.compile(self.regex)
        images = self.soup.findAll('img')
        results = []
        for img in images:
            try:
                url = dict(img.attrs)['src']
                url = self._make_url_path(url)
                if reg.match(url):
                    results.append(url)

            except:
                pass

        print 'Img tag scraping OK'
        return results


if __name__ == '__main__':
    f = CustomExample()
    f.main()
