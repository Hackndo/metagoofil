from metagoofil.extractors.metadataDOC import MetadataExtractor as MetadataDOC


class MetadataExtractor(MetadataDOC):
    def __init__(self, file_name):
        super().__init__(file_name)
