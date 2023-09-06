import pandas as pd
from PyQt5.QtCore import QSettings

filename = 'sample/B-KQX NRC LIST - 0904.xlsx'


def import_report(read_path):
    sheet_name_nrc = None
    sheet_name_subtask = None
    settings = QSettings("nrc_daily_report.ini", QSettings.IniFormat)  # 创建QSettings对象，指定.ini文件路径
    """ 识别文件 """
    xlsx = pd.ExcelFile(read_path)  # 读取整个页面
    # 识别NRC页面名称
    if not isinstance(settings.value("sheet_name/nrc"), list):
        return '配置参数有错'
    values = [x.lower() for x in settings.value("sheet_name/nrc")]
    for _ in range(values.count('')):
        values.remove('')
    for sheet_name in xlsx.sheet_names:
        if sheet_name.lower() in values:
            sheet_name_nrc = sheet_name
            break

    # 识别SUBTASK页面名称
    if not isinstance(settings.value("sheet_name/subtask"), list):
        return '配置参数有错'
    values = [x.lower() for x in settings.value("sheet_name/subtask")]
    for _ in range(values.count('')):
        values.remove('')
    for sheet_name in xlsx.sheet_names:
        if sheet_name.lower() in values:
            sheet_name_subtask = sheet_name
            break

    if sheet_name_nrc is None:
        return 'NO NRC PAGE'  # TODO 改为MESSAGE...

    df_nrc = pd.read_excel(xlsx, sheet_name=sheet_name_nrc, nrows=0)
    settings.beginGroup('header_nrc')
    for field in settings.allKeys():
        options: list = settings.value(field)
        for _ in range(options.count('')):
            options.remove('')
        for option in options:
            if option in df_nrc.columns:
                # 修改指定列的列名
                df_nrc.rename(columns={option: field}, inplace=True)
            else:
                return f'没有列{field}' # TODO
    print(df_nrc.columns.tolist())

    settings.endGroup()

    if sheet_name_subtask is None:  # 若没有subtask页则不执行后续代码
        return


if __name__ == '__main__':
    print(import_report(read_path=filename))
