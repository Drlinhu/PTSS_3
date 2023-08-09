from six import iteritems
from gensim import corpora, models, similarities
from PyQt5.QtSql import QSqlQuery,QSqlDatabase

from utils.database import *

__all__ = ["NrcVectorCorpus"]

NRC_HISTORY_TABLE_NAME = "NrcHistory"
STOP_LIST = set('zadd sadd for a b c d e f g h i j k l m n o p q r s t u v w x y z of the and to in total ea'.split())


class NrcVectorCorpus(object):
    """
    Construct corpus through class, so that only one vector will be run in RAM.
    It's very friendly to RAM for large corpus.
    Then the corpus can be stored in disk, then return one vector one time.
    """

    def __init__(self):
        """
        file of tmpnrccorpusdict.txt is that that saved through meth: corpora.Dictionary.save_as_text
        """
        self.db = QSqlDatabase.addDatabase("QSQLITE", )
        self.db.setDatabaseName("default.db")
        self.db.open()
        self.query = QSqlQuery(self.db)
        self._corpus_mapp_dict = 'tmpnrccorpusdict.txt'

        self.readCorpus()
        self._denoiseCorpus = [self.removeNoise(line) for line in self._descCorpus]
        self.createCorpusDictionary()

    def __iter__(self):
        for i, line in enumerate(self._descCorpus):
            # assume there's one document per line, tokens separated by whitespace
            yield self._dictionary.doc2bow(line.lower().split())

    def calculateSimilarityByLatestModel(self, search_text, show_count=None, threshold=None):
        # create TfidfModel model and corresponding index here
        tfidf = models.TfidfModel(self)
        index = similarities.SparseMatrixSimilarity(tfidf[self], num_features=len(self.dictionary))
        # remove unwanted char from search text, then get the vector space by method `corpora.Dictionary.doc2bow`
        searchVec = self.dictionary.doc2bow(search_text.lower().split())
        # calculate similarity
        sims = index[tfidf[searchVec]]
        sims = list(enumerate(sims))
        sims.sort(key=lambda x: x[1], reverse=True)
        if show_count is not None and threshold is None:
            results = (sims[i] for i in range(len(sims)) if i < show_count)
        elif show_count is not None and threshold is not None:
            results = (sims[i] for i in range(len(sims)) if i < show_count and sims[i][1] > threshold)
        elif show_count is None and threshold is not None:
            results = (sims[i] for i in range(len(sims)) if sims[i][1] > threshold)
        else:
            results = (sims[i] for i in range(len(sims)) if i < 1 and sims[i][1] > 0.9)
        return results

    @classmethod
    def calculateSimilarityByLocalModel(cls, search_text, show_count=None, threshold=None):
        corpusVector = corpora.MmCorpus('corpus/nrcvectorcorpus.mm')
        dictionary = corpora.Dictionary.load_from_text('corpus/tmpnrccorpusdict.txt')
        # create TfidfModel model and corresponding index here
        tfidf = models.TfidfModel(corpusVector)
        index = similarities.SparseMatrixSimilarity(tfidf[corpusVector], num_features=len(dictionary))
        # remove unwanted char from search text, then get the vector space by method `corpora.Dictionary.doc2bow`
        searchVec = dictionary.doc2bow(search_text.lower().split())
        # calculate similarity
        sims = index[tfidf[searchVec]]
        sims = list(enumerate(sims))
        sims.sort(key=lambda x: x[1], reverse=True)

        if show_count is not None and threshold is None:
            results = (sims[i] for i in range(len(sims)) if i < show_count)
        elif show_count is not None and threshold is not None:
            results = (sims[i] for i in range(len(sims)) if i < show_count and sims[i][1] > threshold)
        elif show_count is None and threshold is not None:
            results = (sims[i] for i in range(len(sims)) if sims[i][1] > threshold)
        else:
            results = (sims[i] for i in range(len(sims)) if i < 1 and sims[i][1] > 0.9)
        return results

    @property
    def docCorpus(self):
        return self._descCorpus

    @property
    def dictionary(self):
        return self._dictionary

    def createCorpusDictionary(self):

        # collect statistics about all tokens
        self._dictionary = corpora.Dictionary(line.lower().split() for line in self._denoiseCorpus)
        # remove stop words and words that appear only once
        stopIds = [self._dictionary.token2id[stopWord] for stopWord in STOP_LIST
                   if stopWord in self._dictionary.token2id]
        onceIds = [tokenId for tokenId, docReq in iteritems(self._dictionary.dfs) if docReq == 1]
        self._dictionary.filter_tokens(stopIds + onceIds)
        self._dictionary.compactify()  # remove gaps in id sequence after words that were removed

    def readCorpus(self):
        """
        Read description from database
        :return:
        """
        self.query.exec("SELECT mh_id, description FROM MhFinalized")
        self._descCorpus = []
        self._nrcId = []
        while self.query.next():
            print(self.query.value('description'))
            self._descCorpus.append(self.query.value('description'))
            self._nrcId.append(self.query.value('mh_id'))

    @classmethod
    def removeNoise(cls, x):
        noises = """#&'()*+%,-._/"”“0123456789:;~（），：。\\"""
        for noise in noises:
            x = x.replace(noise, ' ')
        print(x)
        return x

    def save(self):
        """
        1. save Corpus.Dictionary to disk, tha path is `corpus/tmpnrccorpusdict.txt`
        2. save Corpus.MmCorpus's serialized vector to disk, the path is `corpus/nrcvectorcorpus.mm`
        :return:
        """
        corpora.MmCorpus.serialize('corpus/nrcvectorcorpus.mm', self)  # store to disk, for later use
        self._dictionary.save_as_text('corpus/tmpnrccorpusdict.txt')
