import os
import random
import time

import requests


class downloader():
    def __init__(self, url, dir, ext):
        self.url = url
        self.dir = dir
        if url.endswith('/'):
            self.filename = str(url.split("/")[-2])
        else:
            self.filename = str(url.split("/")[-1])
        if not str(url.split("/")[-1]).lower().endswith("." + ext):
            self.filename += "." + ext

    def down(self, wait=1, jitter=0, force=False):
        if not force and os.path.exists(self.dir + "/" + self.filename):
            return True
        else:
            rnd = random.randrange(-jitter, jitter)
            time.sleep(wait + wait * rnd / 100)
            try:
                result = requests.get(self.url)
                if result.status_code != 200:
                    print(f"An error occurred while downloading {self.url}. Status code {result.status_code}")
                    self.filename = ""
                    return False
                with open(os.path.join(self.dir, self.filename), 'wb') as f:
                    f.write(result.content)
                    return True
            except:
                print("Failed to download file.")
        return False

    def name(self):
        return self.filename
