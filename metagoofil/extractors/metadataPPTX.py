from metagoofil.extractors.metadataDOCX import MetadataExtractor as MetadataDOCX
import zipfile
import logging


class MetadataExtractor(MetadataDOCX):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_content(self):
        zip = zipfile.ZipFile(self.file_name, 'r')
        try:
            for file in zip.namelist():
                if "ppt/slides/slide" in file:
                    self.content += zip.read(file).decode('utf-8')
        except Exception as e:
            logging.debug("No slideX.xml file")
        zip.close()
        self.parser.set_content(self.content)
        return self.content != ""
