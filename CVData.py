from os.path import isfile
from pdfminer.high_level import extract_text
from docx import Document
from numpy import array
from numpy.linalg import norm


class CV(object):

    def __init__(self):
        self.contain = False
        self.data = set()

        self.engStopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
                     "you'd",
                     'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
                     'hers',
                     'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
                     'which',
                     'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
                     'been',
                     'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
                     'but',
                     'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                     'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
                     'down',
                     'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
                     'when',
                     'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
                     'such', 'no',
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                     'don',
                     "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
                     "aren't",
                     'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
                     'haven',
                     "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
                     'shan',
                     "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
                     "wouldn't"]

        self.frStopWords = ["au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle", "en", "et",
                         "eux", "il", "ils", "je", "la", "le", "leur", "lui", "ma", "mais", "me", "même",
                         "mes", "moi", "mon", "ne", "nos", "notre", "nous", "on", "ou", "par", "pas", "pour",
                         "qu", "que", "qui", "sa", "se", "ses", "son", "sur", "ta", "te", "tes", "toi", "ton",
                         "tu", "un", "une", "vos", "votre", "vous", "c", "d", "j", "l", "à", "m", "n", "s", "t",
                         "y", "été", "étée", "étées", "étés", "étant", "étante", "étants", "étantes", "suis",
                         "es", "est", "sommes", "êtes", "sont", "serai", "seras", "sera", "serons", "serez",
                         "seront", "serais", "serait", "serions", "seriez", "seraient", "étais", "était",
                         "étions", "étiez", "étaient", "fus", "fut", "fûmes", "fûtes", "furent", "sois", "soit",
                         "soyons", "soyez", "soient", "fusse", "fusses", "fût", "fussions", "fussiez", "fussent",
                         "ayant", "ayante", "ayantes", "ayants", "eu", "eue", "eues", "eus", "ai", "as", "avons",
                         "avez", "ont", "aurai", "auras", "aura", "aurons", "aurez", "auront", "aurais", "aurait",
                         "aurions", "auriez", "auraient", "avais", "avait", "avions", "aviez", "avaient", "eut",
                         "eûmes", "eûtes", "eurent", "aie", "aies", "ait", "ayons", "ayez", "aient", "eusse",
                         "eusses", "eût", "eussions", "eussiez", "eussent"]

    def loadCV(self, filePath: str, lang="en"):

        if not isfile(filePath):
            raise Exception("No such file")

        extention = filePath[filePath.rindex(".") + 1:]

        if extention == "pdf":
            pdfdata = extract_text(filePath).lower().replace(",", " ")

            self.data = [i for i in pdfdata.split(" ") if i]
        elif extention == "docx":
            req = Document(filePath)

            self.data = ""

            for par in req.paragraphs:
                self.data += par.text.replace(",", " ")

            self.data = [i for i in self.data.split(" ") if i]
        else:
            raise Exception("Un supported format")

        if "\n" in self.data:
            self.data.remove("\n")

        if lang == "fr":
            stopWords = [w for w in self.frStopWords]
        else:
            stopWords = [w for w in self.engStopWords]

        self.data = {i for i in self.data if not i in stopWords}

        self.contain = len(self.data) != 0

    def loadCVFromText(self, data: str, lang="en"):

        self.data += data.replace(",", " ")

        self.data = [i for i in data.split(" ") if i]

        if "\n" in self.data:
            self.data.remove("\n")

        if lang == "fr":
            stopWords = [w for w in self.frStopWords]
        else:
            stopWords = [w for w in self.engStopWords]

        self.data = {i for i in self.data if not i in stopWords}

        self.contain = len(self.data) != 0

    def isQualified(self, requirements: str, lang="en") -> str:

        required = [i for i in requirements.lower().replace("\n", " ").replace(",", " ").split(" ") if i]

        if lang == "fr":
            stopWords = [w for w in self.frStopWords]
        else:
            stopWords = [w for w in self.engStopWords]

        required = {i for i in required if not i in stopWords}

        v1 = []
        v2 = []

        for word in required:
            if word in self.data:
                v1.append(1)
            else:
                v1.append(0)

            v2.append(1)

        v1 = array(v1)
        v2 = array(v2)

        if sum(v1) == 0 or sum(v2) == 0:
            return "Not Qualified"

        sim = v1.dot(v2) / (norm(v1) * norm(v2))

        print(sim)

        if sim < 0.1:
            return "Not Qualified"
        elif sim < 0.3:
            return "Barely Qualified"
        elif sim < 0.5:
            return "May be Qualified"
        elif sim < 0.8:
            return "Almost Qualified"
        else:
            return "Qualified"

