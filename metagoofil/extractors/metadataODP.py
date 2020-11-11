from metagoofil.extractors.metadataODT import MetadataExtractor as MetadataODT


class MetadataExtractor(MetadataODT):
    def __init__(self, file_name):
        super().__init__(file_name)
