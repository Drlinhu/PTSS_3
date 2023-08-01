from PyQt5.QtCore import QSettings
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

DATABASE = None
TABLE_SQL = ["""CREATE TABLE IF NOT EXISTS test (
    a TEXT,
    b TEXT
);
"""]


def initialize_database():
    global DATABASE
    # 创建QSettings对象，并指定.ini文件的路径
    settings = QSettings("config.ini", QSettings.IniFormat)

    # 读取.ini文件中的值
    db_default = settings.value("db_name/default")
    db_main = settings.value("db_name/main")

    if db_main:
        DATABASE = db_main
    else:
        DATABASE = db_default

    # 初始化数据库
    db_manager = DatabaseManager()
    for sql in TABLE_SQL:
        db_manager.query(sql)


class DatabaseManager(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db = QSqlDatabase.addDatabase('QSQLITE')
            cls._instance.db.setDatabaseName(DATABASE)  # 数据库文件名
            if not cls._instance.db.open():
                print('无法打开数据库')
        return cls._instance

    @classmethod
    def query(cls, query_string):
        query = QSqlQuery()
        query.exec_(query_string)
        return query
