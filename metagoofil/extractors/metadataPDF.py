import logging
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1

from metagoofil.parser import Parser
from metagoofil.extractors.imetadataextractor import IMetadataExtractor


class MetadataExtractor(IMetadataExtractor):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_content_extracts(self):
        self.get_emails()
        self.get_shares()

    def get_data_extracts(self):
        self.get_users()
        self.get_companies()
        self.get_software()

    def get_content(self):
        pdf_resource_manager = PDFResourceManager()
        layout_parameters = LAParams()
        content = StringIO()
        device = TextConverter(pdf_resource_manager, content, laparams=layout_parameters)
        try:
            with open(self.file_name, "rb") as fp:
                interpreter = PDFPageInterpreter(pdf_resource_manager, device)
                for page in PDFPage.get_pages(fp, check_extractable=False):
                    interpreter.process_page(page)
        except:
            logging.debug(f"Could not parse {self.file_name} content")
        self.content = content.getvalue()
        device.close()
        content.close()
        self.parser = Parser(self.content)
        return self.content

    def get_data(self):
        info = None
        with open(self.file_name, 'rb') as fp:
            doc = PDFDocument(parser=PDFParser(fp))
        try:
            for xref in doc.xrefs:
                info_ref = xref.trailer.get('Info')
                if info_ref:
                    info = resolve1(info_ref)
                self.metadata = info
            return self.metadata
        except Exception as e:
            logging.info("An error occurred while retrieving metadata", exc_info=True)
            return None

    """
    Requires self.content
    """

    def get_emails(self):
        self.emails = self.parser.emails()

    def get_shares(self):
        self.shares = self.parser.shares()

    """
    Requires self.metadata
    """

    def get_users(self):
        if 'Author' in self.metadata:
            self.users.append(self.metadata['Author'].decode('utf-8'))
        return self.users

    def get_companies(self):
        try:
            self.companies.append(self.metadata['Company'].decode('utf-8'))
        except Exception as e:
            logging.debug("No company")
        return self.companies

    def get_software(self):
        try:
            self.software.append(self.metadata['Producer'].decode('utf-8'))
        except Exception as e:
            logging.debug("No producer")
        try:
            self.software.append(self.metadata['Creator'].decode('utf-8'))
        except Exception as e:
            logging.debug("No creator")
        return self.software
