import re
import zipfile

from metagoofil.extractors.imetadataextractor import IMetadataExtractor


class MetadataExtractor(IMetadataExtractor):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_data_extracts(self):
        self.get_users()
        self.get_software()

    def get_content_extracts(self):
        self.get_emails()
        self.get_shares()

    def get_data(self):
        zipf = zipfile.ZipFile(self.file_name, 'r')
        self.metadata = zipf.read('meta.xml').decode('utf-8')
        zipf.close()
        return self.metadata

    def get_content(self):
        zip = zipfile.ZipFile(self.file_name, 'r')
        self.content = zip.read('content.xml').decode('utf-8')
        zip.close()
        self.parser.set_content(self.content)
        return self.content

    def get_emails(self):
        self.emails = self.parser.emails()

    def get_shares(self):
        self.shares = self.parser.shares()

    def get_users(self):
        p = re.compile('<dc:creator>(.*)</dc:creator>')
        res = p.findall(self.metadata, re.DOTALL)
        if res:
            self.users = res

    def get_software(self):
        p = re.compile('<meta:generator>(.*)</meta:generator>')
        res = p.findall(self.metadata, re.DOTALL)
        if res:
            self.software = res
