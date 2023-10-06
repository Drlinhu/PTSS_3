import re

import pdfplumber

from PyQt5.QtCore import QSettings,QDate


def is_numeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def extract_nrc_subtask_from_pdf(pdf_file):
    # 读取.ini文件中的值
    settings = QSettings("config.ini", QSettings.IniFormat)
    p_run_date = settings.value("subtask_import/p_run_date")
    p_base_info = settings.value("subtask_import/p_base_info")
    p_subtask = settings.value("subtask_import/p_subtask")
    print(p_run_date)

    class_ = 'NRC'
    section_mark = ' '.join(['-'] * 14)

    register = None
    proj_id = None
    run_date = None

    items = []  # 记录每个NRC SUBTASK清单
    with pdfplumber.open(pdf_file) as pdf:
        collated = []
        # 获取register和proj_id信息
        first_page = pdf.pages[0]
        info_page = first_page.crop((0, 0, first_page.width, 145))
        for line in info_page.extract_text().splitlines():
            print(line)
            # PROJECT : XJ CUSTOMER : CX A/C TYPE : 777 A/C REGN : B-KPV CHECK TYPE : 2C
            r = re.match(p_base_info, line)
            if r:
                register = r.group('register')
                proj_id = r.group('proj_id')
            r = re.match(p_run_date, line)
            if r:
                temp = r.group('run_date').split('/')
                run_date = QDate(int(temp[2]), int(temp[0]), int(temp[1])).toString('yyyy-MM-dd')
        print(register, proj_id, run_date)
        if not register or not proj_id or not run_date:
            return

        for i, page in enumerate(pdf.pages):
            crop_page = page.crop((0, 145, page.width, page.height))
            for line in crop_page.extract_text().splitlines():
                if line == section_mark:
                    if is_numeric(collated[0]):
                        items.append(collated[1:])
                    else:
                        items.append(collated)
                    collated = []
                else:
                    collated.append(line)

    # register,proj_id,class,sheet,item_no,description,jsn,mhr,trade,report_date
    # front_page_mhr
    columns = ('register', 'proj_id', 'class', 'sheet', 'item_no', 'description', 'jsn', 'mhr', 'trade', 'report_date')
    subtasks = []

    for item in items:
        if len(item) > 3:
            # 1C 1 REMOVE BODY FAIRING 191SL &192SR 0.0
            for line in item:
                subtask = dict.fromkeys(columns)
                subtask['register'] = register
                subtask['trade'] = ''
                first_line = item[0].split()
                subtask['proj_id'] = first_line[0][:2]
                subtask['class'] = class_
                subtask['jsn'] = first_line[-3]
                temp = first_line[-1].split('/')
                subtask['report_date'] = '-'.join([temp[2], temp[0], temp[1]])
                r = re.match(p_subtask, line)
                if r:
                    subtask['sheet'] = r.group('sheet')
                    subtask['item_no'] = r.group('item_no')
                    subtask['description'] = r.group('description')
                    subtask['mhr'] = float(r.group('mhr'))
                    subtasks.append(subtask)

    for subtask in subtasks:
        print(subtask)


if __name__ == '__main__':
    # filename = "sample/NRC TALLY LIST WITH ESTIMATE MANHOUR.pdf"
    filename = "sample/NRC TALLY LIST WITH ESTIMATE MANHOUR - 1002.pdf"
    extract_nrc_subtask_from_pdf(filename)
