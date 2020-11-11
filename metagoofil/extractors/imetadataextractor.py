import logging

from metagoofil.parser import Parser


class IMetadataExtractor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.content = ""
        self.metadata = ""
        self.users = []
        self.emails = []
        self.shares = []
        self.software = []
        self.companies = []
        self.parser = Parser()

    def get_results(self):
        return {
            "users": [o.strip(" \r\n\t") for o in self.users if o.strip(" \r\n\t") != ""],
            "emails": [o.strip(" \r\n\t") for o in self.emails if o.strip(" \r\n\t") != ""],
            "shares": [o.strip(" \r\n\t") for o in self.shares if o.strip(" \r\n\t") != ""],
            "software": [o.strip(" \r\n\t") for o in self.software if o.strip(" \r\n\t") != ""],
            "companies": [o.strip(" \r\n\t") for o in self.companies if o.strip(" \r\n\t") != ""]
        }

    def get_metadata(self):
        if not self.get_content():
            logging.debug("Unable to extract content")
        else:
            self.get_content_extracts()

        if not self.get_data():
            logging.debug("Unable to extract metadata")
        else:
            self.get_data_extracts()

    def get_content(self):
        raise NotImplementedError

    def get_content_extracts(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def get_data_extracts(self):
        raise NotImplementedError
