import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1

import myparser


class metapdf:
    def __init__(self, fname, password=''):
        self.fname = fname
        self.password = password
        self.metadata = None
        self.users = []
        self.software = []
        self.paths = []
        self.raw = ""
        self.company = []
        self.text = ""

    def getTexts(self):
        rsrcmgr = PDFResourceManager()

        laparams = LAParams()

        with open("/tmp/.metagoofil_rnd", 'w', encoding='utf-8', errors="ignore") as retstr:
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)
            with open(self.fname, "rb") as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)

                for page in PDFPage.get_pages(fp, check_extractable=False):
                    interpreter.process_page(page)
        with open("/tmp/.metagoofil_rnd", 'r', encoding='utf-8', errors="ignore") as retstr:
            self.text = retstr.read()

        os.remove('/tmp/.metagoofil_rnd')

        device.close()
        retstr.close()
        return True

    def getData(self):
        info = None
        with open(self.fname, 'rb') as fp:
            doc = PDFDocument(parser=PDFParser(fp))
        try:
            for xref in doc.xrefs:
                info_ref = xref.trailer.get('Info')
                if info_ref:
                    info = resolve1(info_ref)
                self.metadata = info
                self.raw = info

            return self.raw is not None
        except Exception as e:
            print(str(e))
            return e

    def getEmails(self):
        em = myparser.parser(self.text)
        return em.emails()

    def getHosts(self, domain):
        em = myparser.parser(self.text, domain)
        return em.hostnames()

    def getUsers(self):
        if 'Author' in self.metadata:
            self.users.append(self.metadata['Author'])
        return self.users

    def getCompany(self):
        try:
            self.users.append(self.metadata['Company'])
        except:
            print("\t [x] Error in PDF metadata Company")
        return self.company

    def getSoftware(self):
        try:
            self.software.append(self.metadata['Producer'])
        except:
            print("\t [x] Error in PDF metadata Software")
        try:
            self.software.append(self.metadata['Creator'])
        except:
            print("\t [x] Error in PDF metadata Creator")
        return self.software

    def getPaths(self):
        return self.paths

    def getRaw(self):
        return self.raw
