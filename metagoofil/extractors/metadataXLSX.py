from metagoofil.extractors.metadataDOCX import MetadataExtractor as MetadataDOCX
import zipfile
import logging


class MetadataExtractor(MetadataDOCX):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_content(self):
        zip = zipfile.ZipFile(self.file_name, 'r')
        try:
            self.content += zip.read('xl/sharedStrings.xml').decode('utf-8')
        except Exception as e:
            logging.debug("No sharedStrings.xml file")
        zip.close()
        return self.content != ""
