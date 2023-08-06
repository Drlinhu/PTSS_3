from typing import List, Dict

from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
from PyQt5.QtCore import Qt, QByteArray, pyqtSlot

from .ui.ui_imageviewer import Ui_ImageViewer
from utils.database import DatabaseManager


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, table_name: str, images: List[Dict[str, str]], parent=None):
        super(ImageViewer, self).__init__(parent)
        self.table_name = table_name
        self.db = DatabaseManager()
        self.query = QtSql.QSqlQuery(self.db.con)
        self.ims = images
        self.im_index = 0
        self.im_count = len(images)
        self.zoom = 1
        self.rotate_angle = -90
        self.pixmap_item = None

        self.ui = Ui_ImageViewer()
        self.ui.setupUi(self)
        self.ui.graphicsView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)  # 按压拉动滚动条进而移动试图

        self.show_image()

    @pyqtSlot()
    def on_btnRadioLarger_clicked(self):
        factor = 1.2
        if self.zoom <= 5:
            self.ui.graphicsView.scale(factor, factor)
            self.zoom += 0.2
            self.zoom = round(self.zoom, 2)

    @pyqtSlot()
    def on_btnRadioSmaller_clicked(self):
        factor = 0.8
        if self.zoom >= -1:
            self.ui.graphicsView.scale(factor, factor)
            self.zoom -= 0.2
            self.zoom = round(self.zoom, 2)

    @pyqtSlot()
    def on_btnDelete_clicked(self):
        choose = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choose == QtWidgets.QMessageBox.Yes:
            self.query.prepare(f"DELETE FROM {self.table_name} WHERE id=:id")
            self.query.bindValue(':id', self.ims[self.im_index]['id'])
            if self.query.exec():
                QtWidgets.QMessageBox.information(self, 'Information', 'Delete successfully!')
                self.ims.pop(self.im_index)
                self.im_count = len(self.ims)
                self.show_image()
            else:
                QtWidgets.QMessageBox.critical(self, 'Information', f'Delete failed!\n{self.query.lastError().text()}')

    @pyqtSlot()
    def on_btnRotate_clicked(self):
        self.ui.graphicsView.rotate(self.rotate_angle)
        self.fit_image()

    @pyqtSlot()
    def on_btnSave_clicked(self):
        pass

    @pyqtSlot()
    def on_btnPrint_clicked(self):
        pass

    @pyqtSlot()
    def on_btnLeft_clicked(self):
        self.im_index -= 1
        if self.im_index < 0:
            self.im_index = self.im_count - 1
        self.show_image()

    @pyqtSlot()
    def on_btnRight_clicked(self):
        self.im_index += 1
        if self.im_index > self.im_count - 1:
            self.im_index = 0
        self.show_image()

    def set_window_title(self):
        self.setWindowTitle(f"Image Viewer - {self.ims[self.im_index]['name']}")
        self.ui.labelPage.setText(f'{self.im_index + 1} / {self.im_count}')

    def show_image(self):
        self.set_window_title()

        scene = QtWidgets.QGraphicsScene()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.ims[self.im_index]['image'])
        self.pixmap_item = scene.addPixmap(pixmap)  # QGraphicsPixmapItem
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.setSceneRect(scene.itemsBoundingRect())
        self.fit_image()

    def fit_image(self):
        if self.pixmap_item is not None:
            self.ui.graphicsView.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

    def resizeEvent(self, event: QtCore.QSize) -> None:
        self.fit_image()
