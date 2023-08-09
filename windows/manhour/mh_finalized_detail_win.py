import os
from pathlib import Path
import pandas as pd
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime, QItemSelectionModel

from ..ui import Ui_MhFinalizedDetailForm
from .nrc_report_assistant_win import NrcReportAssistantWin
from utils.database import DatabaseManager
