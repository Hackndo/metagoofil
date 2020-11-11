import string
import re


class Parser:
    def __init__(self, results, word="", inurl=False):
        self.results = results if isinstance(results, str) else results.decode('utf-8')
        self.domain_name = word
        self.temp = []
        self.inurl = inurl

    def generic_clean(self):
        results = self.results

        results = re.sub('<em>', '', results)
        results = re.sub('<b>', '', results)
        results = re.sub('</b>', '', results)
        results = re.sub('</em>', '', results)
        results = re.sub('%2f', ' ', results)
        results = re.sub('%3a', ' ', results)
        results = re.sub('<strong>', '', results)
        results = re.sub('</strong>', '', results)
        results = re.sub('<w:t>', ' ', results)

        for e in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
            results = results.replace(e, ' ')
        return results

    def url_clean(self):
        self.results = re.sub('<em>', '', self.results)
        self.results = re.sub('</em>', '', self.results)
        self.results = re.sub('%2f', ' ', self.results)
        self.results = re.sub('%3a', ' ', self.results)
        for e in ('<', '>', ':', '=', ';', '&', '%3A', '%3D', '%3C'):
            self.results = self.results.replace(e, ' ')

    def emails(self):
        results = self.generic_clean()
        reg_emails = re.compile('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
        return Parser.unique(reg_emails.findall(results))

    def file_urls(self):
        urls = []
        reg_urls = re.compile('<a href="(.*?)"')
        all_urls = Parser.unique(reg_urls.findall(self.results))
        for z in all_urls:
            y = z.replace('/url?q=', '')
            x = y.split('&')[0]
            if any(k in x for k in ['webcache', 'google.com']) or not x.startswith("http") \
                    or (self.domain_name not in x and not self.inurl):
                continue
            urls.append(x)
        return urls

    def shares(self):
        reg_shares = re.compile('(?:\\\\|smb:\/\/)((?:(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)+(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9]))(?![a-zA-Z0-9\-\.])')
        return [f"\\\\{share}" for share in Parser.unique(reg_shares.findall(self.results))]


    @staticmethod
    def unique(li):
        return list(set(li))
