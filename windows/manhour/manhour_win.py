import os, re
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime, QItemSelectionModel, QSettings

from ..ui.ui_manhourform import Ui_ManHourForm
from ..ui import Ui_GeneralInputDialog
from ..image_viewer import ImageViewer
from .mh_finalized_detail_win import ManhourFinalizedWin
from .nrc_subtask_temp_win import NrcSubtaskTempWin
from .nrc_report_assistant_win import NrcReportAssistantWin
from .nrc_manhour_trend import NrcManhourTrendWin
from .nrc_standardItem_win import NrcStandardItemWin
from utils.database import DatabaseManager
from utils.nrc_corpus import *
from utils.setting import get_section_options, get_section_allKeys

TABLE_HEADER_MAPPING = {'mh_id': 'MH_Id',
                        'class': 'Class',
                        'pkg_id': 'Pkg_Id',
                        'wo': 'WO',
                        'ac_type': 'Ac_Type',
                        'register': 'Register',
                        'ref_task': 'Ref_Task',
                        'description': 'Description',
                        'trade': 'Trade',
                        'ata': 'ATA',
                        'area': 'Area',
                        'zone': 'Zone',
                        'category': 'Category',
                        'skill': 'Skill',
                        'unskill': 'Unskill',
                        'total': 'Total',
                        'standard': 'Standard',
                        'dskill': 'D_Skill',
                        'dunskill': 'D_Unskill',
                        'dtotal': 'D_Total',
                        'remark': 'Remark',
                        }

ini_file = "mhr_import.ini"


class ManhourWin(QtWidgets.QWidget):
    progress_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(ManhourWin, self).__init__(parent)
        self.ui = Ui_ManHourForm()
        self.ui.setupUi(self)

        self.table_name = "MhFinalized"
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)

        self.init_table()  # 初始化表格

        # 连接槽函数
        self.ui.lineEditSearchId.returnPressed.connect(self.on_pushButtonSearch_clicked)
        self.ui.lineEditSearchRefTask.returnPressed.connect(self.on_pushButtonSearch_clicked)
        self.ui.lineEditSearchRegister.returnPressed.connect(self.on_pushButtonSearch_clicked)
        self.ui.lineEditSearchDesc.returnPressed.connect(self.on_pushButtonSearch_clicked)
        self.ui.lineEditSearchAcType.returnPressed.connect(self.on_pushButtonSearch_clicked)
        self.ui.lineEditSearchPkgId.returnPressed.connect(self.on_pushButtonSearch_clicked)

    def init_table(self):

        # 创建表格模型(不可编辑, 默认可排序)
        self.table_model = QtSql.QSqlTableModel(self, self.db.get_connection_by_name())
        self.table_model.setTable(self.table_name)

        # 创建选择模型
        self.selection_model = QItemSelectionModel(self.table_model)

        # 设置表格数据模型和选择模型
        self.ui.tableView.setModel(self.table_model)
        self.ui.tableView.setSelectionModel(self.selection_model)

        # 设置表格标题
        self.field_num = self.db.get_field_num(self.table_model)  # 获取字段名和序号
        for field, column in self.field_num.items():  # 设置字段显示名
            self.table_model.setHeaderData(column, Qt.Horizontal, TABLE_HEADER_MAPPING[field])

        # 设置表格视图属性
        for field, column in self.field_num.items():  # 设置表格列宽度默认行为
            if field not in ['description', 'remark']:
                self.ui.tableView.horizontalHeader().setSectionResizeMode(column,
                                                                          QtWidgets.QHeaderView.ResizeToContents)
            else:
                self.ui.tableView.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)

        # 设置表格视图的水平标题右击弹出菜单
        self.ui.tableView.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.horizontalHeader().customContextMenuRequested.connect(self.show_table_header_menu)

    def on_tableView_doubleClicked(self, index):
        sel_model = self.ui.tableView.selectionModel()
        fields = list(TABLE_HEADER_MAPPING.keys())
        data = {fields[i]: idx.data(Qt.DisplayRole) for i, idx in enumerate(sel_model.selectedIndexes())}
        self.detail_win = ManhourFinalizedWin()
        self.detail_win.setData(**data)
        self.detail_win.show()

    @pyqtSlot()
    def on_toolButtonNrcReportAssistant_clicked(self):
        self.nrc_reportAssistant_win = NrcReportAssistantWin()
        self.nrc_reportAssistant_win.show()

    @pyqtSlot()
    def on_toolButtonNrcMhTrend_clicked(self):
        self.nrc_trend_win = NrcManhourTrendWin()
        self.nrc_trend_win.show()

    @pyqtSlot()
    def on_toolButtonNrcStandard_clicked(self):
        self.nrc_standardItem_win = NrcStandardItemWin()
        self.nrc_standardItem_win.show()

    @pyqtSlot()
    def on_toolButtonRtnQuotationAssistant_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_toolButtonRtnMhTrend_clicked(self):  # TODO
        pass

    @pyqtSlot()
    def on_pushButtonSearch_clicked(self):
        # self.table_name = "MhFinalized"
        has_nrc = self.ui.checkBoxNrc.isChecked()
        has_rtn = self.ui.checkBoxRtn.isChecked()
        filter_str = None
        if self.ui.radioButtonBySimi.isChecked():
            desc = self.ui.lineEditSearchDesc.text()
            corpus = ManhourVectorCorpus()
            sims = self.ui.doubleSpinBoxSims.value()
            results = corpus.get_similarity_by_latest(search_text=desc, threshold=sims)

            # 获得的结果是数据库记录的位置，而非mh_id，所以还要查询数据库以获得mh_id具体内容
            self.query.prepare(f"SELECT mh_id,description FROM {self.table_name} LIMIT 1 OFFSET :offset")
            coll_id = []
            for r in results:
                self.query.bindValue(":offset", r[0])
                if self.query.exec() and self.query.first():
                    coll_id.append(self.query.value('mh_id'))
            if coll_id:
                filter_str = ' OR '.join([f"mh_id='{x}'" for x in coll_id])
            else:
                filter_str = 'mh_id=-1'

        if self.ui.radioButtonByWord.isChecked():
            condition = {}
            if self.ui.lineEditSearchId.text():
                condition['mh_id'] = self.ui.lineEditSearchId.text()
            if self.ui.lineEditSearchAcType.text():
                condition['ac_type'] = self.ui.lineEditSearchAcType.text()
            if self.ui.lineEditSearchRegister.text():
                condition['register'] = self.ui.lineEditSearchRegister.text()
            if self.ui.lineEditSearchPkgId.text():
                condition['pkg_id'] = self.ui.lineEditSearchPkgId.text()
            if self.ui.lineEditSearchDesc.text():
                condition['description'] = self.ui.lineEditSearchDesc.text()
            if self.ui.lineEditSearchRefTask.text():
                condition['ref_task'] = self.ui.lineEditSearchRefTask.text()
            filter_str = ' AND '.join([f"{field} LIKE '%{value}%'" for field, value in condition.items()])

        if filter_str:
            if has_nrc and not has_rtn:
                filter_str += " AND class='NRC'"
            elif not has_nrc and has_rtn:
                filter_str += " AND class='RTN'"
            elif not has_nrc and not has_rtn:
                filter_str += " AND class!='NRC' AND class!='RTN'"
            else:
                pass
        else:
            if has_nrc and not has_rtn:
                filter_str = "class='NRC'"
            elif not has_nrc and has_rtn:
                filter_str = "class='RTN'"
            elif not has_nrc and not has_rtn:
                filter_str = "class!='NRC' AND class!='RTN'"
            else:
                filter_str = "class='NRC' OR class='RTN'"
        self.table_model.setFilter(filter_str)
        self.table_model.select()

    @pyqtSlot()
    def on_pushButtonImport_clicked(self):
        try:
            read_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx *.xls)")
            if not read_path:
                return

            # 启动数据库事务，执行保存
            self.db.con.transaction()

            """识别EXCEL页面"""
            sheet_names = {'summary': None,
                           'rtn': None,
                           'nrc': None, }
            xlsx = pd.ExcelFile(read_path)  # 读取整个页面
            for page, name in sheet_names.items():
                ok, options = get_section_options(ini_file, 'finalized_sheet_name', page)
                if not ok:
                    QtWidgets.QMessageBox.critical(self, 'Error', options)
                    return

                for option in options:
                    if option in xlsx.sheet_names:
                        sheet_names[page] = option
                        break

            """ 读取各表列名参数并识别excel各个表列名"""
            page_header = {'rtn': {},
                           'nrc': {}, }
            absence_header = {'rtn': [],
                              'nrc': []}
            for page, header in page_header.items():
                if sheet_names[page] is None:
                    continue
                df = pd.read_excel(xlsx, sheet_name=sheet_names[page], nrows=0)
                for field in get_section_allKeys(ini_file, 'finalized_header'):
                    # 读取配置
                    ok, options = get_section_options(ini_file, 'finalized_header', field)
                    if not ok:
                        QtWidgets.QMessageBox.critical(self, 'Error', options)
                        return
                    # 检查
                    for option in options:
                        if option in df.columns:
                            header[field] = option
                            break
                    else:
                        absence_header[page].append(field)
                        header[field] = ''

            # 提示确实的列名
            ab_headers_info = []
            for page, header in absence_header.items():
                if header:
                    ab_headers_info.append(f"Column {', '.join(header)} in {page} sheet")
            msg = ' and '.join(ab_headers_info) + ' not found.'
            if msg:
                QtWidgets.QMessageBox.warning(self, 'Warning', msg)

            """读取Summary页面"""
            ac_type = ''
            register = ''
            proj_id = ''
            if sheet_names['summary'] is not None:
                df = pd.read_excel(xlsx, sheet_name=sheet_names['summary'], keep_default_na=False, nrows=1)

                # 识别AC TYPE 和Register
                text = df.columns[0]
                r = re.search(r'.+(?P<ac_type>A|B\d{3}).+(?P<register>B-[A-Z]{3}).*', text, re.IGNORECASE)
                ac_type = r.group('ac_type')
                register = r.group('register')

                # 识别PROJECT ID
                text = ''.join(df.iloc[0, :])
                r = re.search(r'project ID:.*(?P<proj_id>[A-Z]{2})', text, re.IGNORECASE)
                proj_id = r.group('proj_id')

            if not ac_type or not register or not proj_id:
                dialog = GeneralRegisterInputDialog()
                dialog.exec()
                while dialog.is_ok and not dialog.register:
                    msg = "Register should not be empty"
                    QtWidgets.QMessageBox.warning(self, 'Warning', msg)
                    dialog.exec()
                ac_type = dialog.ac_type
                register = dialog.register.strip()
                proj_id = dialog.project_id.strip()

            """读取RTN页面"""
            main_pkgId = ''
            df_rtn_refPkg = None
            if sheet_names['rtn'] is not None:
                # 读取识别description语句标记
                ok, options = get_section_options(ini_file, 'default', 'desc_identification')
                if not ok:
                    QtWidgets.QMessageBox.critical(self, 'Error', options)
                    return
                desc_marks = options

                # 读取RTN表格
                df = pd.read_excel(xlsx, sheet_name=sheet_names['rtn'], keep_default_na=False)

                # 修改列名为格式列，方便导入数据库
                df.rename(columns={v: k for k, v in page_header['rtn'].items() if v}, inplace=True)

                # 添加缺失的列
                for ab_header in absence_header['rtn']:
                    if ab_header in ['D_Skill', 'D_Total', 'D_Unskill']:
                        default_value = 0.0
                    else:
                        default_value = ""
                    df[ab_header] = [default_value for _ in range(df.shape[0])]

                # 添加Class, Register和Standard列
                df['Class'] = ['RTN' for _ in range(df.shape[0])]
                df['Register'] = [register for _ in range(df.shape[0])]
                df['Ac_Type'] = [ac_type for _ in range(df.shape[0])]
                df['Standard'] = ['N' for _ in range(df.shape[0])]

                # 按数据库表列顺序修改dataframe列顺序
                df = df[TABLE_HEADER_MAPPING.values()]

                # 获取缺少MH ID的行待后续特殊处理
                df_no_mhId = df[~df['MH_Id'].str.contains(r'[A-Z]{2}\d{5}', case=False, regex=True)].reset_index(
                    drop=True)

                # 过滤掉缺少MH_Id的行并获取主package ID
                df = df[df['MH_Id'].str.contains(r'[A-Z]{2}\d{5}', case=False, regex=True)].reset_index(drop=True)
                pattern = r'(?P<pkg_id>[A-Z]{3}-BMP-\d{4}-(\d{3}[A-Z]|\d{2}[A-Z]{2}|GEAR))'
                df_pkg = df['Pkg_Id'].str.extractall(pattern)['pkg_id'].sort_values().drop_duplicates().tolist()
                if not df_pkg:
                    main_pkgId = df_pkg[0]
                else:
                    main_pkgId = df['Pkg_Id'].tolist()[0]

                # 给无MH_Id的行补充必要信息，如mh_id和pkg_id
                j = 0
                for i in range(df_no_mhId.shape[0]):
                    if j > 18:
                        QtWidgets.QMessageBox.critical(self, 'Error', 'Qty. of no MH_Id items is over limitation.')
                        return
                    for x in desc_marks:
                        if x.lower() in df_no_mhId.loc[i, 'Description'].lower():
                            df_no_mhId.loc[i, 'MH_Id'] = f'{proj_id}{j:0>5}'
                            df_no_mhId.loc[i, 'Pkg_Id'] = main_pkgId
                            j += 1

                # 合并df和df_no_mhId，并再次过滤缺少MH_Id的行
                df = pd.concat([df, df_no_mhId], ignore_index=True)
                df = df[df['MH_Id'].str.contains(r'[A-Z]{2}\d{5}', case=False, regex=True)].reset_index(drop=True)

                # 获取ref_pkg字典
                df_rtn_refPkg = df[['Ref_Task', 'Pkg_Id']]

                # 存入数据
                sql = f"""REPLACE INTO {self.table_name}
                          VALUES ({','.join([f':{k}' for k in TABLE_HEADER_MAPPING.keys()])})"""
                self.query.prepare(sql)
                for i in range(df.shape[0]):
                    for k, v in TABLE_HEADER_MAPPING.items():
                        self.query.bindValue(f":{k}", str(df.loc[i, v]))
                    if not self.query.exec():
                        QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                        self.db.con.rollback()
                        return

            """读取NRC页面"""
            if sheet_names['nrc'] is not None:
                # 读取识别standard语句标记
                ok, options = get_section_options(ini_file, 'standard', 'marks')
                if not ok:
                    QtWidgets.QMessageBox.critical(self, 'Error', options)
                    return
                standard_mark = options

                df = pd.read_excel(xlsx, sheet_name=sheet_names['nrc'])
                exclude_cols = [page_header['nrc']['MH_Id'], ]  # 指定要排除的列
                df = df.dropna(subset=exclude_cols)
                df.fillna('', inplace=True)

                # 修改列名为格式列，方便导入数据库
                df.rename(columns={v: k for k, v in page_header['nrc'].items() if v}, inplace=True)

                # 添加缺失的列
                for ab_header in absence_header['nrc']:
                    if ab_header in ['D_Skill', 'D_Total', 'D_Unskill']:
                        default_value = 0.0
                    else:
                        default_value = ""
                    df[ab_header] = [default_value for _ in range(df.shape[0])]

                # 添加Class, Register和Standard列
                df['Class'] = ['NRC' for _ in range(df.shape[0])]
                df['Register'] = [register for _ in range(df.shape[0])]
                df['Ac_Type'] = [ac_type for _ in range(df.shape[0])]

                standard_value = []
                for i in range(df.shape[0]):
                    for mark in standard_mark:
                        if mark.lower() in str(df.loc[i, 'Remark']).lower():
                            standard_value.append('Y')
                        else:
                            standard_value.append('N')
                df['Standard'] = standard_value

                # 按数据库表列顺序修改dataframe列顺序
                df = df[TABLE_HEADER_MAPPING.values()]

                # 更新Package ID 字段 TODO
                if df_rtn_refPkg is not None:
                    for i in range(df.shape[0]):
                        temp = df_rtn_refPkg[df_rtn_refPkg['Ref_Task'] == df.loc[i, 'Ref_Task']]['Pkg_Id'].tolist()
                        if temp:
                            df.loc[i, 'Pkg_Id'] = temp[0]
                        else:
                            df.loc[i, 'Pkg_Id'] = main_pkgId

                # 存入数据
                sql = f"""INSERT INTO {self.table_name}
                          VALUES ({','.join([f':{k}' for k in TABLE_HEADER_MAPPING.keys()])})
                          ON CONFLICT (mh_id) DO UPDATE SET
                          {','.join([f"{k}=CASE WHEN {k}>:{k} THEN {k} ELSE :{k} END"
                                     for k in TABLE_HEADER_MAPPING.keys()])}"""
                self.query.prepare(sql)
                for i in range(df.shape[0]):
                    for k, v in TABLE_HEADER_MAPPING.items():
                        self.query.bindValue(f":{k}", str(df.loc[i, v]))
                    if not self.query.exec():
                        QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                        self.db.con.rollback()
                        return

            # 以上存入过程正常，则提交数据库
            if self.db.con.commit():
                QtWidgets.QMessageBox.information(self, 'Information', 'Successfully')
            else:
                QtWidgets.QMessageBox.critical(self, 'Error', self.db.con.lastError().text())
                self.db.con.rollback()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', e)
            self.db.con.rollback()

    @pyqtSlot()
    def on_pushButtonExport_clicked(self):
        today = QDateTime.currentDateTime().toString('yyyy_MM_dd_hh_mm_ss')
        filename = f'MH_NRC_Finalized_{today}.xlsx'
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        save_path = Path(save_path).resolve()
        # 创建工时记录DataFrame对象
        data = []
        header = []
        for j in range(self.table_model.columnCount()):
            header.append(self.table_model.headerData(j, Qt.Horizontal, Qt.DisplayRole))

        for i in range(self.table_model.rowCount()):
            row_data = []
            for j in range(self.table_model.columnCount()):
                row_data.append(self.table_model.data(self.table_model.index(i, j), Qt.DisplayRole))
            data.append(row_data)
        df = pd.DataFrame(data, columns=header)
        df.to_excel(save_path, index=False)
        # 打开保存文件夹
        os.startfile(save_path.parent)

    @pyqtSlot()
    def on_pushButtonDelete_clicked(self):
        selected_indexes = self.selection_model.selectedRows(column=self.field_num['mh_id'])
        if not selected_indexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choose == QtWidgets.QMessageBox.Yes:
            self.query.prepare(f"DELETE FROM {self.table_name} WHERE mh_id=:mh_id")
            self.db.con.transaction()
            for index in selected_indexes:
                self.query.bindValue(':mh_id', index.data())
                self.query.exec()
            if self.db.con.commit():
                QtWidgets.QMessageBox.information(self, 'Information', 'Deleted!')
                self.table_model.select()
            else:
                QtWidgets.QMessageBox.critical(self, 'Error', self.db.con.lastError().text())

    @pyqtSlot()
    def on_pushButtonDetail_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        if len(sel_model.selectedRows(self.field_num['mh_id'])) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        fields = list(TABLE_HEADER_MAPPING.keys())
        data = {fields[i]: idx.data(Qt.DisplayRole) for i, idx in enumerate(sel_model.selectedIndexes())}
        self.detail_win = ManhourFinalizedWin()
        self.detail_win.setData(**data)
        self.detail_win.show()

    @pyqtSlot()
    def on_pushButtonSubtask_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        selected_rowIndexes = sel_model.selectedRows(column=self.field_num['mh_id'])
        if len(selected_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        mh_id = selected_rowIndexes[0].data()
        self.subtask_win = NrcSubtaskTempWin(mh_id)
        self.subtask_win.show()

    @pyqtSlot()
    def on_pushButtonAddImage_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=self.field_num['mh_id'])
        if not sel_rowIndexes:
            QtWidgets.QMessageBox.information(self, 'Information', 'No row(s) selected!')
            return

        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Image", "",
                                                               "Image Files (*.png *.jpg *.bmp)")
        if not file_paths:
            return
        sql = """INSERT INTO MhImage
                         VALUES (:id,:mh_id,:name,:image,(SELECT IFNULL(MAX(sheet)+1,1) FROM MhImage WHERE mh_id=:mh_id))"""
        self.db.con.transaction()  # 创建事务
        self.query.prepare(sql)
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                image_data = QtCore.QByteArray(f.read())  # 以二进制模式打开图片数据并转化为QByteArray对象
            path = Path(file_path)
            for index in sel_rowIndexes:
                self.query.bindValue(':id', None)
                self.query.bindValue(':mh_id', index.data())
                self.query.bindValue(':name', path.name)
                self.query.bindValue(':image', image_data)
                if not self.query.exec():
                    self.db.con.rollback()
                    QtWidgets.QMessageBox.critical(self, 'Error', self.query.lastError().text())
                    return
        self.db.con.commit()
        QtWidgets.QMessageBox.information(self, 'Information', 'Successfully')

    @pyqtSlot()
    def on_pushButtonImage_clicked(self):
        sel_model = self.ui.tableView.selectionModel()
        sel_rowIndexes = sel_model.selectedRows(column=self.field_num['mh_id'])
        if len(sel_rowIndexes) != 1:
            QtWidgets.QMessageBox.information(self, 'Information', 'One row should be selected!')
            return
        ims = []
        mh_id = sel_rowIndexes[0].data()
        self.query.prepare("SELECT id,sheet,name,image FROM MhImage WHERE mh_id=:mh_id ORDER BY sheet ASC")
        self.query.bindValue(':mh_id', mh_id)
        self.query.exec()
        while self.query.next():
            ims.append({field: self.query.value(field) for field in ['id', 'sheet', 'name', 'image']})
        if not ims:
            QtWidgets.QMessageBox.information(self, 'Information', 'No images')
            return

        self.image_viewer = ImageViewer('MhImage', ims)
        self.image_viewer.show()
        self.image_viewer.fit_image()

    def on_radioButtonBySimi_toggled(self, checked):
        if checked:
            self.ui.doubleSpinBoxSims.setEnabled(True)
            self.ui.lineEditSearchId.setEnabled(False)
            self.ui.lineEditSearchAcType.setEnabled(False)
            self.ui.lineEditSearchRegister.setEnabled(False)
            self.ui.lineEditSearchPkgId.setEnabled(False)
        else:
            self.ui.doubleSpinBoxSims.setEnabled(False)
            self.ui.lineEditSearchId.setEnabled(True)
            self.ui.lineEditSearchAcType.setEnabled(True)
            self.ui.lineEditSearchRegister.setEnabled(True)
            self.ui.lineEditSearchPkgId.setEnabled(False)
            self.ui.doubleSpinBoxSims.setValue(0.9)

    def show_table_header_menu(self, pos):
        # 创建右键菜单
        menu = QtWidgets.QMenu(self)
        # 获取右键点击处的列索引
        column = self.ui.tableView.horizontalHeader().logicalIndexAt(pos)
        # 添加菜单项
        if self.ui.tableView.horizontalHeader().sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            column_resizable_action = QtWidgets.QAction("Non-resizable", self)
        else:
            column_resizable_action = QtWidgets.QAction("Resizable", self)
        column_resizable_action.triggered.connect(lambda: self.set_column_resizable(pos))
        menu.addAction(column_resizable_action)

        # 显示右键菜单
        menu.exec_(self.ui.tableView.viewport().mapToGlobal(pos))

    def set_column_resizable(self, pos):
        # 获取右键点击处的列索引
        column = self.ui.tableView.horizontalHeader().logicalIndexAt(pos)

        if self.ui.tableView.horizontalHeader().sectionResizeMode(column) == QtWidgets.QHeaderView.Interactive:
            self.ui.tableView.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Stretch)
        else:
            self.ui.tableView.horizontalHeader().setSectionResizeMode(column, QtWidgets.QHeaderView.Interactive)


class GeneralRegisterInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.ui = Ui_GeneralInputDialog()
        self.ui.setupUi(self)
        self.ui.label_01.setText("Register:")
        self.ui.label_02.setText("Project ID:")
        self.is_ok = False

    @property
    def ac_type(self):
        return self.ui.cbbAcType.currentText()

    @property
    def register(self):
        return self.ui.lineEdit_01.text()

    @property
    def project_id(self):
        return self.ui.lineEdit_02.text()

    def on_buttonBox_accepted(self) -> None:
        self.is_ok = True
