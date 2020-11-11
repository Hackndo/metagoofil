import logging
import importlib
import os


class Extractor:
    """
    Loader class to handle extractors.

    This class looks for provided extractor module name and returns an instance of this extractor method.
    Returns None if doesn't exist.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.extractor_module = self.file_name.split('.')[-1].upper()

    def load(self):
        """
        Load provided extractor module
        :param extractor_module: class name of extractor module
        :return: instance of extractor module
        """
        try:
            return importlib.import_module(
                "metagoofil.extractors.metadata{}".format(self.extractor_module), "MetadataExtractor"
            ).MetadataExtractor(self.file_name)
        except ModuleNotFoundError:
            logging.warning("Extractor module 'metadata{}' doesn't exist".format(self.extractor_module))
            return None
        except Exception:
            logging.warning("Unknown error while loading 'metadata{}'".format(self.extractor_module), exc_info=True)
            return None
