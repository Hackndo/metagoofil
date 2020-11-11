import logging

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from metagoofil.extractors.imetadataextractor import IMetadataExtractor


class MetadataExtractor(IMetadataExtractor):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_data_extracts(self):
        self.get_users()

    def get_content_extracts(self):
        pass

    def get_data(self):
        try:
            parser = createParser(self.file_name, self.file_name)
        except Exception as e:
            logging.warning(f"Could not create parser for {self.file_name}", exc_info=True)
            return False

        try:
            metadata = extractMetadata(parser)
            self.metadata = metadata.exportPlaintext()
        except Exception as e:
            logging.warning(f"Could not extract metadata for {self.file_name}", exc_info=True)
            return False
        return True

    def get_users(self):
        for line in self.metadata:
            res = line.split(":")
            if res[0] == "- Author":
                self.users.append(res[1])
            elif res[1] == " Author:":
                self.users.append(res[2])
            elif res[0] == "- Producer":
                self.software.append(res[1])
            elif res[1] == " LastSavedBy":
                self.users.append(res[2])

    def get_content(self):
        return False
