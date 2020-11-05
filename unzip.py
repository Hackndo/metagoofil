""" unzip.py
    Version: 1.1

    Extract a zipfile to the directory provided
    It first creates the directory structure to house the files
    then it extracts the files to it.

    Sample usage:
    command line
    unzip.py -p 10 -z c:\testfile.zip -o c:\testoutput

    python class
    import unzip
    un = unzip.unzip()
    un.extract(r'c:\testfile.zip', 'c:\testoutput')
    

    By Doug Tolton
"""

import getopt
import os
import os.path
import sys
import zipfile


class Unzip:
    def __init__(self, verbose = False, percent = 10):
        self.verbose = False
        self.percent = percent

    def extract(self, file, directory):
        if not directory.endswith(':') and not os.path.exists(directory):
            os.mkdir(directory)

        zf = zipfile.ZipFile(file)

        # create directory structure to house files
        self._createstructure(file, directory)

        num_files = len(zf.namelist())
        percent = self.percent
        divisions = 100 / percent
        perc = int(num_files / divisions)

        # extract files to directory structure
        for i, name in enumerate(zf.namelist()):

            if self.verbose == True:
                print("Extracting %s" % name)
            elif perc > 0 and (i % perc) == 0 and i > 0:
                complete = int (i / perc) * percent
                #print "%s%% complete" % complete

            if not name.endswith('/'):
                outfile = open(os.path.join(directory, name), 'wb')
                outfile.write(zf.read(name))
                outfile.flush()
                outfile.close()


    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)


    def _makedirs(self, directories, basedir):
        """ Create any directories that don't currently exist """
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)
                #print("dir-->"+str(curdir))

    def _listdirs(self, file):
        """ Grabs all the directories in the zip structure
        This is necessary to create the structure before trying
        to extract the file to it. """
        zf = zipfile.ZipFile(file)

        dirs = []
        #print str(zf.namelist())

        for name in zf.namelist():
            dirsname = name.split("/")
            ant=""
            for dirname in dirsname[:-1]:
                dirs.append(ant+dirname)
                #print "anadiendo:"+(ant+dirname)
                ant=ant+dirname+"/"

        dirs.sort()
        return dirs

def usage():
    print("""usage: unzip.py -z <zipfile> -o <targetdir>
    <zipfile> is the source zipfile to extract
    <targetdir> is the target destination

    -z zipfile to extract
    -o target location
    -p sets the percentage notification
    -v sets the extraction to verbose (overrides -p)

    long options also work:
    --verbose
    --percent=10
    --zipfile=<zipfile>
    --outdir=<targetdir>""")