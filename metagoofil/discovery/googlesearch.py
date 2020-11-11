import logging
import sys
import time
from urllib.parse import urlencode

import requests

from metagoofil.parser import Parser


class GoogleSearch:
    def __init__(self, domain_name, offset=0, results_limit=200, filetype="pdf",inurl=False):
        self.domain_name = domain_name
        self.offset = offset
        self.results = b""
        self.totalresults = b""
        self.filetype = filetype
        self.inurl = inurl
        self.server = "https://www.google.com"
        self.hostname = "www.google.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "100"
        self.results_limit = results_limit
        self.counter = 0

    def do_search_files(self, offset, quantity):
        headers = {
            'Host': self.hostname,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': '',
            'Upgrade-Insecure-Requests': '1'
        }
        params = {
            "num": quantity,
            "start": offset,
            "hl": "en",
            "meta": "",
            "q": f"filetype:{self.filetype} {'inurl' if self.inurl else 'site'}:{self.domain_name}"
        }

        logging.debug("Requested URL: " + self.server + "/search?" + urlencode(params))

        h = requests.get(self.server + "/search", params=params, headers=headers)
        if h.status_code == 429:
            logging.error("Google is blocking your requests. You should wait or validate captcha manually.")
            sys.exit()
        if h.status_code != 200:
            logging.debug(f"An error occurred while requesting Google (Error code {h.status_code})")
            return
        self.totalresults += h.content

    def search(self):
        while self.counter < self.results_limit:
            self.do_search_files(self.counter + self.offset, min(100, self.results_limit - self.counter))
            time.sleep(2)
            self.counter += 100
        parser = Parser(self.totalresults, self.domain_name, self.inurl)
        return parser.file_urls()
