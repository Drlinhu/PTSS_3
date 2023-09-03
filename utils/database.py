from PyQt5.QtCore import QSettings
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

DATABASE = None
TABLE_SQL = ["""CREATE TABLE IF NOT EXISTS MhFinalized (
    mh_id       TEXT DEFAULT ""
                     PRIMARY KEY
                     NOT NULL,
    class       TEXT DEFAULT "",
    pkg_id      TEXT DEFAULT "",
    wo          TEXT DEFAULT "",
    ac_type     TEXT DEFAULT "",
    register    TEXT DEFAULT "",
    ref_task    TEXT DEFAULT "",
    description TEXT DEFAULT "",
    trade       TEXT DEFAULT "",
    ata         TEXT DEFAULT "",
    area        TEXT DEFAULT "",
    zone        TEXT DEFAULT "",
    category    TEXT DEFAULT "",
    skill       REAL DEFAULT (0.0),
    unskill     REAL DEFAULT (0.0),
    total       REAL DEFAULT (0.0),
    standard    TEXT DEFAULT (0),
    dskill      REAL DEFAULT (0.0),
    dunskill    REAL DEFAULT (0.0),
    dtotal      REAL DEFAULT (0.0),
    remark      TEXT DEFAULT ""
);
""",
             """CREATE TABLE IF NOT EXISTS MhCxRemark (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    mh_id           TEXT,
    remark          TEXT    DEFAULT "",
    create_user     TEXT,
    create_datetime TEXT    DEFAULT (datetime('now') ) 
                            NOT NULL,
    update_user     TEXT,
    update_datetime TEXT    DEFAULT (datetime('now') ) 
                            NOT NULL
);
""",
             """CREATE TABLE IF NOT EXISTS MhImage (
    id    INTEGER PRIMARY KEY,
    mh_id TEXT    NOT NULL,
    name  TEXT,
    image BLOB,
    sheet INTEGER DEFAULT (1) 
);
""",
             """CREATE TABLE IF NOT EXISTS MhNrcReport (
    nrc_id      TEXT DEFAULT "",
    register    TEXT DEFAULT "",
    ref_task    TEXT DEFAULT "",
    description TEXT DEFAULT "",
    area        TEXT DEFAULT "",
    trade       TEXT DEFAULT "",
    ata         TEXT DEFAULT "",
    status      TEXT DEFAULT "",
    standard    TEXT DEFAULT "",
    total       REAL DEFAULT (0.0),
    report_date TEXT,
    PRIMARY KEY (
        nrc_id,
        report_date
    )
);
""",
             """CREATE TABLE IF NOT EXISTS MhNrcReportTemp (
    nrc_id      TEXT PRIMARY KEY,
    register    TEXT DEFAULT "",
    ref_task    TEXT DEFAULT "",
    description TEXT DEFAULT "",
    area        TEXT DEFAULT "",
    trade       TEXT DEFAULT "",
    ata         TEXT,
    status      TEXT DEFAULT "",
    standard    TEXT,
    total       REAL DEFAULT (0.0),
    mh_changed  REAL DEFAULT (0.0)
);
""",
             """CREATE TABLE IF NOT EXISTS MhSubtask (
    register    TEXT    DEFAULT "",
    proj_id     TEXT    DEFAULT "",
    class       TEXT    DEFAULT "",
    sheet       TEXT    DEFAULT "",
    item_no     INTEGER DEFAULT (0),
    description TEXT    DEFAULT "",
    jsn         TEXT    DEFAULT "",
    mhr         REAL    DEFAULT (0.0),
    trade       TEXT    DEFAULT "",
    report_date TEXT,
    PRIMARY KEY (
        proj_id,
        item_no,
        jsn,
        report_date
    )
);
""",
             """CREATE TABLE IF NOT EXISTS MhSubtaskTemp (
    register    TEXT    DEFAULT "",
    proj_id     TEXT    DEFAULT "",
    class       TEXT    DEFAULT "",
    sheet       TEXT    DEFAULT "",
    item_no     INTEGER DEFAULT (0),
    description TEXT    DEFAULT "",
    jsn         TEXT    DEFAULT "",
    mhr         REAL    DEFAULT (0.0),
    trade       TEXT    DEFAULT "",
    PRIMARY KEY (
        proj_id,
        item_no,
        jsn
    )
);
""",
             """CREATE TABLE IF NOT EXISTS RegisterProjectId (
    register   TEXT DEFAULT "",
    proj_id    TEXT DEFAULT "",
    start_date TEXT DEFAULT "",
    end_date   TEXT DEFAULT "",
    status     TEXT DEFAULT "",
    PRIMARY KEY (
        register,
        proj_id
    )
);
""",
             """CREATE TABLE IF NOT EXISTS MhNrcStandardItem (
    item_no     TEXT PRIMARY KEY
                     NOT NULL,
    ac_type     TEXT DEFAULT "",
    description TEXT DEFAULT "",
    work_area   TEXT DEFAULT ""
);""",
             """CREATE TABLE IF NOT EXISTS MhNrcStandardImage (
    id      INTEGER PRIMARY KEY,
    item_no TEXT    REFERENCES MhNrcStandardItem (item_no) ON DELETE CASCADE
                                                           ON UPDATE CASCADE,
    name    TEXT    DEFAULT "",
    image   BLOB,
    sheet   INTEGER DEFAULT (1) 
);""",
             """CREATE TABLE IF NOT EXISTS MhNrcStandardMax (
    item_no TEXT PRIMARY KEY
                 REFERENCES MhNrcStandardItem (item_no) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
    ai      REAL DEFAULT (0.0),
    ae      REAL DEFAULT (0.0),
    av      REAL DEFAULT (0.0),
    ss      REAL DEFAULT (0.0),
    pt      REAL DEFAULT (0.0),
    sm      REAL DEFAULT (0.0),
    gw      REAL DEFAULT (0.0),
    cl      REAL DEFAULT (0.0) 
);""",
             """CREATE TABLE IF NOT EXISTS MhNrcStandardMin (
    item_no TEXT PRIMARY KEY
                 REFERENCES MhNrcStandardItem (item_no) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
    ai      REAL DEFAULT (0.0),
    ae      REAL DEFAULT (0.0),
    av      REAL DEFAULT (0.0),
    ss      REAL DEFAULT (0.0),
    pt      REAL DEFAULT (0.0),
    sm      REAL DEFAULT (0.0),
    gw      REAL DEFAULT (0.0),
    cl      REAL DEFAULT (0.0) 
);""",
             """CREATE TABLE IF NOT EXISTS MhNrcStandardRemark (
    item_no TEXT PRIMARY KEY
                 REFERENCES MhNrcStandardItem (item_no) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
    remark  TEXT DEFAULT ""
);""",
             """CREATE TABLE IF NOT EXISTS Procedure (
    proc_id     TEXT PRIMARY KEY,
    description TEXT DEFAULT ""
);
""",
             """CREATE TABLE IF NOT EXISTS ProcedureImage (
    id      INTEGER PRIMARY KEY,
    proc_id TEXT    REFERENCES Procedure (proc_id) ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
    name    TEXT,
    image   BLOB,
    sheet   INTEGER DEFAULT (1) 
);""",
             """CREATE TABLE IF NOT EXISTS ProcedureIcw (
    id      INTEGER PRIMARY KEY,
    proc_id TEXT    REFERENCES Procedure (proc_id) ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
    icw     TEXT,
    mhr     REAL    DEFAULT (0.0),
    remark  TEXT    DEFAULT ""
);
""",
             """CREATE TABLE IF NOT EXISTS ProcedurePanel (
    id      INTEGER PRIMARY KEY,
    proc_id TEXT    REFERENCES Procedure (proc_id) ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
    panel   TEXT
);
""",
             """CREATE TABLE IF NOT EXISTS ProcedureRef (
    id      INTEGER PRIMARY KEY,
    proc_id TEXT    REFERENCES Procedure (proc_id) ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
    ref     TEXT
);""",
             ]

TABLE_INDEX = ["""CREATE INDEX IF NOT EXISTS mh_history_desc ON MhFinalized (
    description
);""",
               ]

__all__ = ['initialize_database', 'DatabaseManager']


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

    # 创建表格
    for sql in TABLE_SQL:
        db_manager.query(sql)

    # 创建表格索引
    for sql in TABLE_INDEX:
        db_manager.query(sql)


class DatabaseManager(object):
    """ 该类为数据库管理单例类"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DatabaseManager, cls).__new__(cls)
            # 创建默认数据库连接对象并设置数据库名
            cls.__instance.con = QSqlDatabase.addDatabase('QSQLITE')
            cls.__instance.con.setDatabaseName(DATABASE)
            if not cls.__instance.con.open():
                print('Open database failed')
        return cls.__instance

    @classmethod
    def get_connection_by_name(cls, name='qt_sql_default_connection'):
        if QSqlDatabase.contains(name):
            con = QSqlDatabase.database(name)
        else:
            con = QSqlDatabase.addDatabase("QSQLITE", name)  # 添加SQL LITE数据库驱动
            con.setDatabaseName(DATABASE)
        if not con.open():
            raise ConnectionError('Failed to open database: ' + con.lastError().text())
        return con

    @classmethod
    def get_field_num(cls, table_model: QSqlTableModel):
        empty_rec = table_model.record()  # 获取空记录，只有字段名
        field_num = {}  # 字段名与序号的字典
        for i in range(empty_rec.count()):
            field_name = empty_rec.fieldName(i)  # 字段名
            field_num.setdefault(field_name)
            field_num[field_name] = i
        return field_num

    def query(self, query_string):
        query = QSqlQuery(self.__instance.con)  # 使用默认连接进行查询
        query.exec_(query_string)
        return query
