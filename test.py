from PyQt5.QtCore import QDateTime
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from utils.database import *

initialize_database()
print(QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'))

db = DatabaseManager()
query = QSqlQuery(db.con)
query.prepare("INSERT INTO MhCxRemark VALUES (:id,:mh_id,:remark,:crt_user,:crt_dt,:upd_user,:upd_dt)")
query.bindValue(':id', None)
query.bindValue(':mh_id', 'test')
query.bindValue(':remark', 'test')
query.bindValue(':crt_user', '')
query.bindValue(':crt_dt', '')
query.bindValue(':upd_user', QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'))
query.bindValue(':upd_dt', QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'))
if not query.exec():
    print(query.lastError().text())

query = db.query("SELECT * FROM MhCxRemark")
while query.next():
    print([(query.value(i), type(query.value(i))) for i in range(query.record().count())])
