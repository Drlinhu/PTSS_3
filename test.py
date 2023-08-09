from utils.nrc_corpus import *
from utils.database import *
from PyQt5.QtSql import QSqlQuery

initialize_database()

desc = 'TOWING A/C FOR MAINTENANCE/OPERATIONAL NEEDS'
corpus = ManhourVectorCorpus()
# corpus.save()
sims = 0.9
results = corpus.get_similarity_by_latest(search_text=desc, threshold=sims)
db = DatabaseManager()
query = QSqlQuery(db.con)
for x in results:
    print(x)
    query.exec(f"SELECT mh_id,description FROM MhFinalized LIMIT 1 OFFSET {x[0]}")
# query.seek(x[0])
    query.first()
    print(query.value(0), query.value(1))


