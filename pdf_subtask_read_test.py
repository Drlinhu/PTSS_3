import re

import pdfplumber

from PyQt5.QtCore import QSettings, QDate

from utils import is_valid_date, is_numeric


def get_mode2_subtasks(item: list, p):
    subtasks = []
    collated = []  # 满足格式要求的单个subtask
    temp = []  # 记录属于同个subtask的行,待处理
    for i, line in enumerate(item):
        if re.match(p, line) and temp:
            collated.append(temp)
            temp = [line]
        else:
            temp.append(line)
        if i == len(item) - 1 and temp:
            collated.append(temp)
    for record in collated:
        r = re.match(p, record[0])
        sheet = ''
        item_no = r.group('item_no')
        desc = r.group('desc')
        mhr = r.group('mhr')
        if len(record) > 1:
            for x in record[1:]:
                desc += f' {x}'
        subtasks.append({'sheet': sheet, 'item_no': item_no, 'description': desc, 'mhr': mhr})
    return subtasks


def extract_nrc_subtask_from_pdf(pdf_file):
    mode = 1
    # 读取.ini文件中的值
    settings = QSettings("config.ini", QSettings.IniFormat)
    p_run_date = settings.value("subtask_import/p_run_date")
    p_base_info = settings.value("subtask_import/p_base_info")
    p_subtask = settings.value("subtask_import/p_subtask")
    print(p_run_date)

    class_ = 'NRC'

    short_line_qty = [int(x) for x in settings.value("read_pdf/short_line_qty")]
    section_mark = [' '.join(["-" for i in range(n)]) for n in short_line_qty]

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
            # PROJECT : XJ CUSTOMER : CX A/C TYPE : 777 A/C REGN : B-KPV CHECK TYPE : 2C
            r = re.match(p_base_info, line)
            if r:
                register = r.group('register')
                proj_id = r.group('proj_id')
            r = re.match(p_run_date, line)
            if r:
                run_date = is_valid_date(r.group('run_date'))
                if run_date:
                    run_date = run_date.toString('yyyy-MM-dd')
        print(register, proj_id, run_date)
        if not register or not proj_id or not run_date:
            return

        columns = (
            'register', 'proj_id', 'class', 'sheet', 'item_no', 'description', 'jsn', 'mhr', 'trade', 'report_date')
        subtasks = []
        # register,proj_id,class,sheet,item_no,description,jsn,mhr,trade,report_date
        # front_page_mhr

        # 收集subtask
        if mode == 1:
            top = None
            tops = [float(x) for x in settings.value("read_pdf/subtask_top")]
            for x in tops:
                crop_page = pdf.pages[0].crop((0, x, pdf.pages[0].width, pdf.pages[0].height))
                first_line = crop_page.extract_text().splitlines()[0]
                if re.match(r'[A-Z]{2}L\d{4}', first_line):
                    top = x
            if not top:
                print("无法识别开始行")
                return

            for i, page in enumerate(pdf.pages):
                crop_page = page.crop((0, top, page.width, page.height))
                for line in crop_page.extract_text().splitlines():
                    if line in section_mark:
                        if is_numeric(collated[0]):
                            items.append(collated[1:])
                        else:
                            items.append(collated)
                        collated = []
                    else:
                        collated.append(line)
            for item in items:
                if len(item) > 3:
                    print(item)
                    nrc_id = item[0].split()[0]
                    front_page_mhr = item[2]
                    total_mhr = 0
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
                            total_mhr += subtask['mhr']
                            subtasks.append(subtask)

        if mode == 2:
            new_start_pattern = r'[A-Z]{3}\d{4}'
            for i, page in enumerate(pdf.pages):
                crop_page = page.crop((0, 174, page.width, page.height))
                for line in crop_page.extract_text().splitlines():
                    if re.match(new_start_pattern, line) and collated and re.match(new_start_pattern, collated[0]):
                        items.append(collated)
                        collated = [line]
                    else:
                        collated.append(line)
            for item in items:
                temp = item[0].split()
                nrc_id, front_page_mhr = temp[0], temp[-2]
                p_subtask_2 = settings.value("subtask_import/p_subtask_2")
                for i, line in enumerate(item):
                    if i == 0:
                        jsn = re.match(r'.* (?P<jsn>L\d{3}) .*', line).group('jsn')
                    if re.match(p_subtask_2, line):
                        for subtask in get_mode2_subtasks(item[i:], p_subtask_2):
                            subtask['jsn'] = jsn
                            subtask['register'] = register
                            subtask['proj_id'] = proj_id
                            subtask['report_date'] = run_date
                            subtasks.append(subtask)
                        break
        if not subtasks:
            print("No subtasks")


if __name__ == '__main__':
    # filename = "sample/NRC TALLY LIST WITH ESTIMATE MANHOUR 1006.pdf"
    # filename = "sample/NRC TALLY LIST - 0929.pdf"
    filename = "sample/NRC TALLY LIST WITH ESTIMATE MANHOUR- 07 Jul.pdf"
    extract_nrc_subtask_from_pdf(filename)
