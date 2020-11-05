import zipfile
import random
import re
import zipfile
import os

import myparser


class metaInfoMS:
    def __init__(self):
        self.template = ""
        self.totalTime = ""
        self.pages = ""
        self.words = ""
        self.characters = ""
        self.application = ""
        self.docSecurity = ""
        self.lines = ""
        self.paragraphs = ""
        self.scaleCrop = ""
        self.company = ""
        self.linksUpToDate = ""
        self.charactersWithSpaces = ""
        self.shareDoc = ""
        self.hyperlinksChanged = ""
        self.appVersion = ""
        self.title = ""
        self.subject = ""
        self.creator = ""
        self.keywords = ""
        self.lastModifiedBy = ""
        self.revision = ""
        self.createdDate = ""
        self.modifiedDate = ""
        self.userscomments = ""
        self.thumbnailPath = ""
        self.comments = "ok"
        self.text = ""

    def __init__(self, filepath):
        self.template = ""
        self.totalTime = ""
        self.pages = ""
        self.words = ""
        self.characters = ""
        self.application = ""
        self.docSecurity = ""
        self.lines = ""
        self.paragraphs = ""
        self.scaleCrop = ""
        self.company = ""
        self.linksUpToDate = ""
        self.charactersWithSpaces = ""
        self.shareDoc = ""
        self.hyperlinksChanged = ""
        self.appVersion = ""
        self.title = ""
        self.subject = ""
        self.creator = ""
        self.keywords = ""
        self.lastModifiedBy = ""
        self.revision = ""
        self.createdDate = ""
        self.modifiedDate = ""
        self.thumbnailPath = ""
        self.text = ""
        rnd = str(random.randrange(0, 1001, 3))
        zip = zipfile.ZipFile(filepath, 'r')
        with open(f'app{rnd}.xml', 'wb') as f:
            if "docProps/app.xml" in zip.namelist():
                f.write(zip.read('docProps/app.xml'))
        with open(f'core{rnd}.xml', 'wb') as f:
            if "docProps/core.xml" in zip.namelist():
                f.write(zip.read('docProps/core.xml'))
        with open(f'docu{rnd}.xml', 'wb') as f:
            if "word/document.xml" in zip.namelist():
                f.write(zip.read('word/document.xml'))
        with open(f'comments{rnd}.xml', 'wb') as f:
            if "word/comments.xml" in zip.namelist():
                f.write(zip.read('word/comments.xml'))
        with open(f'xl{rnd}.xml', 'wb') as f:
            if "xl/sharedStrings.xml" in zip.namelist():
                f.write(zip.read('xl/sharedStrings.xml'))
        try:
            with open(f'comments{rnd}.xml', 'wb') as f:
                f.write(zip.read('word/comments.xml'))
            self.comments = "ok"
        except:
            self.comments = "error"
        thumbnailPath = ""

        zip.close()
        # primero algunas estadisticas del soft usado para la edicion y del documento
        with open(f'app{rnd}.xml', 'r') as f:
            app = f.read()
            self.cargaApp(app)

        with open(f'comments{rnd}.xml', 'r') as f:
            comm = f.read()
            self.cargaComm(comm)

        # document content
        with open(f'docu{rnd}.xml', 'r') as f:
            docu = f.read()
            self.text += docu

            # document content
        with open(f'xl{rnd}.xml', 'r') as f:
            xl = f.read()
            self.text += xl

        with open(f'core{rnd}.xml', 'r') as f:
            core = f.read()
            self.cargaCore(core)
            self.thumbnailPath = thumbnailPath

        # borramos todo menos el thumbnail

        os.remove(f'app{rnd}.xml')
        os.remove(f'core{rnd}.xml')
        os.remove(f'comments{rnd}.xml')
        os.remove(f'docu{rnd}.xml')
        os.remove(f'xl{rnd}.xml')

    def toString(self):
        print("--- Metadata app ---")
        print(" template: " + str(self.template))
        print(" totalTime: " + str(self.totalTime))
        print(" pages: " + str(self.pages))
        print(" words: " + str(self.words))
        print(" characters: " + str(self.characters))
        print(" application: " + str(self.application))
        print(" docSecurity: " + str(self.docSecurity))
        print(" lines: " + str(self.lines))
        print(" paragraphs: " + str(self.paragraphs))
        print(" scaleCrop: " + str(self.scaleCrop))
        print(" company: " + str(self.company))
        print(" linksUpToDate: " + str(self.linksUpToDate))
        print(" charactersWithSpaces: " + str(self.charactersWithSpaces))
        print(" shareDoc:" + str(self.shareDoc))
        print(" hyperlinksChanged:" + str(self.hyperlinksChanged))
        print(" appVersion:" + str(self.appVersion))

        print("\n --- Metadata core ---")
        print(" title:" + str(self.title))
        print(" subject:" + str(self.subject))
        print(" creator:" + str(self.creator))
        print(" keywords:" + str(self.keywords))
        print(" lastModifiedBy:" + str(self.lastModifiedBy))
        print(" revision:" + str(self.revision))
        print(" createdDate:" + str(self.createdDate))
        print(" modifiedDate:" + str(self.modifiedDate))

        print("\n thumbnailPath:" + str(self.thumbnailPath))

    def cargaComm(self, datos):
        try:
            p = re.compile('w:author="(.*?)" w')
            self.userscomments = p.findall(datos)
        except:
            pass

    def cargaApp(self, datos):
        try:
            p = re.compile('<Template>(.*)</Template>')
            self.template = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<TotalTime>(.*)</TotalTime>')
            self.totalTime = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<Pages>(.*)</Pages>')
            self.pages = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<Words>(.*)</Words>')
            self.words = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<Characters>(.*)</Characters>')
            self.characters = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<Application>(.*)</Application>')
            self.application = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<DocSecurity>(.*)</DocSecurity>')
            self.docSecurity = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<Lines>(.*)</Lines>')
            self.lines = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<Paragraphs>(.*)</Paragraphs>')
            self.paragraphs = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<ScaleCrop>(.*)</ScaleCrop>')
            self.scaleCrop = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<Company>(.*)</Company>')
            self.company = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<LinksUpToDate>(.*)</LinksUpToDate>')
            self.linksUpToDate = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<CharactersWithSpaces>(.*)</CharactersWithSpaces>')
            self.charactersWithSpaces = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<SharedDoc>(.*)</SharedDoc>')
            self.sharedDoc = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<HyperlinksChanged>(.*)</HyperlinksChanged>')
            self.hyperlinksChanged = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<AppVersion>(.*)</AppVersion>')
            self.appVersion = str(p.findall(datos)[0])
        except:
            pass

    def cargaCore(self, datos):
        try:
            p = re.compile('<dc:title>(.*)</dc:title>')
            self.title = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<dc:subject>(.*)</dc:subject>')
            self.subject = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<dc:creator>(.*)</dc:creator>')
            self.creator = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<cp:keywords>(.*)</cp:keywords>')
            self.keywords = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<cp:lastModifiedBy>(.*)</cp:lastModifiedBy>')
            self.lastModifiedBy = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<cp:revision>(.*)</cp:revision>')
            self.revision = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<dcterms:created xsi:type=".*">(.*)</dcterms:created>')
            self.createdDate = str(p.findall(datos)[0])
        except:
            pass

        try:
            p = re.compile('<dcterms:modified xsi:type=".*">(.*)</dcterms:modified>')
            self.modifiedDate = str(p.findall(datos)[0])
        except:
            pass

    def getData(self):
        return "ok"

    def getTexts(self):
        return "ok"

    def getRaw(self):
        raw = "Not implemented yet"
        return raw

    def getUsers(self):
        res = []
        temporal = []
        res.append(self.creator)
        res.append(self.lastModifiedBy)
        res.extend(self.userscomments)

        for x in res:
            if temporal.count(x) == 0:
                temporal.append(x)
            else:
                pass
        return temporal

    def getEmails(self):
        res = myparser.parser(self.text)
        return res.emails()

    def getPaths(self):
        res = []
        # res.append(self.revision)
        return res

    def getSoftware(self):
        res = []
        res.append(self.application)
        return res
