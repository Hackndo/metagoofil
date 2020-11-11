import logging
import os
import random
import time

import requests


class Downloader:
    def __init__(self, url, working_directory, file_type):
        self.url = url
        self.dir = working_directory
        if url.endswith('/'):
            self.filename = str(url.split("/")[-2])
        else:
            self.filename = str(url.split("/")[-1])
        if not str(url.split("/")[-1]).lower().endswith("." + file_type):
            self.filename += "." + file_type

    def download(self, wait=1, jitter=0, force=False):
        if not force and os.path.exists(self.dir + "/" + self.filename):
            logging.info(f"File {self.filename} was already downloaded")
            return self.dir + "/" + self.filename
        else:
            logging.info(f"Downloading {self.url}")
            rnd = 0
            if jitter > 0:
                rnd = random.randrange(-jitter, jitter)
            time.sleep(wait + wait * rnd / 100)
            try:
                result = requests.get(self.url)
                if result.status_code != 200:
                    logging.debug(f"An error occurred while downloading {self.url}. Status code {result.status_code}")
                    self.filename = ""
                    return False
                with open(os.path.join(self.dir, self.filename), 'wb') as f:
                    f.write(result.content)
                    logging.debug(f"File saved: {os.path.join(self.dir, self.filename)}")
                    return os.path.join(self.dir, self.filename)
            except Exception as e:
                logging.debug("Failed to download file.")
        return False

    def get_filename(self):
        return self.filename
