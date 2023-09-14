from PyQt5.QtCore import QSettings

__all__ = ['get_configuration', 'get_section_options','get_section_allKeys']


def get_section_allKeys(ini_file: str, section: str):
    settings = QSettings(ini_file, QSettings.IniFormat)  # 创建QSettings对象，指定.ini文件路径
    settings.beginGroup(section)
    all_keys = settings.allKeys()
    settings.endGroup()
    return all_keys


def get_section_options(ini_file: str, section: str, field: str):
    settings = QSettings(ini_file, QSettings.IniFormat)  # 创建QSettings对象，指定.ini文件路径
    settings.beginGroup(section)
    if field not in settings.allKeys():
        return [False, f'No {field} in {ini_file}']
    if not isinstance(settings.value(field), list):
        return [False, 'Value in mhr_import.ini must be end with `,`']
    values = settings.value(field)
    for _ in range(values.count('')):
        values.remove('')
    settings.endGroup()
    return True, values
