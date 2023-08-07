from six import iteritems
from gensim import corpora, models, similarities
from PyQt5.QtSql import QSqlQuery

from utils.database import *
from .database import DatabaseManager

__all__ = ["ManhourVectorCorpus"]

STOP_LIST = set('zadd sadd for a b c d e f g h i j k l m n o p q r s t u v w x y z of the and to in total ea'.split())


class ManhourVectorCorpus(object):
    """
    Construct corpus through class, so that only one vector will be run in RAM.
    It's very friendly to RAM for large corpus.
    Then the corpus can be stored in disk, then return one vector one time.
    """

    def __init__(self):
        self.table_name = "MhFinalized"
        self.db = DatabaseManager()
        self.query = QSqlQuery(self.db.con)

        # 从数据库中读取文本作为训练用的文本
        self.read_corpus_from_database()
        # 对语料库进行降噪处理
        self.denoised_corpus = [self.remove_text_noise(line) for line in self.corpus_desc]
        # 创建语料库字典
        self.create_corpus_dictionary()

    def __iter__(self):
        for i, line in enumerate(self.corpus_desc):
            # assume there's one document per line, tokens separated by whitespace
            yield self.dictionary.doc2bow(line.lower().split())

    def get_similarity_by_latest(self, search_text, show_count=None, threshold=None):
        # create TfidfModel model and corresponding index here
        tfidf = models.TfidfModel(self)
        index = similarities.SparseMatrixSimilarity(tfidf[self], num_features=len(self.dictionary))
        # remove unwanted char from search text, then get the vector space by method `corpora.Dictionary.doc2bow`
        search_vec = self.dictionary.doc2bow(search_text.lower().split())
        # calculate similarity
        sims = index[tfidf[search_vec]]
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

    def get_similarity_by_local(self, search_text, show_count=None, threshold=None):
        corpusVector = corpora.MmCorpus(f'corpus/{self.table_name}_vector_corpus.mm')
        dictionary = corpora.Dictionary.load_from_text(f'corpus/{self.table_name}_tmp_corpus_dict.txt')
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

    def create_corpus_dictionary(self):
        # collect statistics about all tokens
        self.dictionary = corpora.Dictionary(line.lower().split() for line in self.denoised_corpus)
        # remove stop words and words that appear only once
        stopIds = [self.dictionary.token2id[stopWord] for stopWord in STOP_LIST
                   if stopWord in self.dictionary.token2id]
        onceIds = [tokenId for tokenId, docReq in iteritems(self.dictionary.dfs) if docReq == 1]
        self.dictionary.filter_tokens(stopIds + onceIds)
        self.dictionary.compactify()  # remove gaps in id sequence after words that were removed

    def read_corpus_from_database(self):
        """
        Read description from database to be used as trained corpus
        :return:
        """
        self.corpus_desc = []
        self.id = []
        self.query.exec(f"SELECT id, description FROM {self.table_name}")
        while self.query.next():
            self.corpus_desc.append(self.query.value('description'))
            self.id.append(self.query.value('id'))

    @classmethod
    def remove_text_noise(cls, x):
        noises = """#&'()*+%,-._/"”“0123456789:;~（），：。\\"""
        for noise in noises:
            x = x.replace(noise, ' ')
        return x

    def save(self):
        """
        1. save Corpus.Dictionary to disk, tha path is `corpus/tmpnrccorpusdict.txt`
        2. save Corpus.MmCorpus's serialized vector to disk, the path is `corpus/nrcvectorcorpus.mm`
        :return:
        """
        corpora.MmCorpus.serialize(f'corpus/{self.table_name}_vector_corpus.mm', self)  # store to disk, for later use
        self.dictionary.save_as_text(f'corpus/{self.table_name}_tmp_corpus_dict.txt')
