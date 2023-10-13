from PyQt5.QtCore import QDate, QSettings

__all__ = ["is_numeric", "is_valid_date"]


def is_numeric(string: str):
    try:
        float(string.split()[-1])
        return True
    except ValueError:
        return False


def is_valid_date(date_string):
    settings = QSettings("config.ini", QSettings.IniFormat)
    date_formatters = settings.value("date_format/nrc_report_date")[:-1]
    for fmt in date_formatters:
        dt = QDate.fromString(date_string, fmt)
        if dt:
            return dt
