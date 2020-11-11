import logging
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
        zip = zipfile.ZipFile(self.file_name, 'r')
        try:
            self.metadata += zip.read('docProps/app.xml').decode('utf-8')
        except Exception as e:
            logging.debug("No app.xml file", exc_info=True)
        try:
            self.metadata += zip.read('docProps/core.xml').decode('utf-8')
        except:
            logging.debug("No core.xml file")
        zip.close()
        return self.metadata != ""

    def get_content(self):
        zip = zipfile.ZipFile(self.file_name, 'r')
        try:
            self.content += zip.read('word/document.xml').decode('utf-8')
        except Exception as e:
            logging.debug("No document.xml file")
        try:
            self.content += zip.read('word/comments.xml').decode('utf-8')
        except:
            logging.debug("No comments.xml file")
        zip.close()
        self.parser.set_content(self.content)
        return self.content != ""

    def get_users(self):
        p = re.compile('<dc:creator>(.*)</dc:creator>')
        res = p.findall(self.metadata, re.DOTALL)
        if res:
            self.users += res

        p = re.compile('w:author="(.*?)" w')
        res = p.findall(self.metadata, re.DOTALL)
        if res:
            self.users += res

        p = re.compile('<cp:lastModifiedBy>(.*)</cp:lastModifiedBy>')
        res = p.findall(self.metadata, re.DOTALL)
        if res:
            self.users += res

    def get_software(self):
        p = re.compile('<Application>(.*)</Application>')
        res = p.findall(self.metadata, re.DOTALL)
        if res:
            self.software += res

    def get_emails(self):
        self.emails = self.parser.emails()

    def get_shares(self):
        self.shares = self.parser.shares()
