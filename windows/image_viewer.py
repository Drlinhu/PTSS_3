from typing import List, Dict

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QByteArray, pyqtSlot

from .ui.ui_imageviewer import Ui_ImageViewer


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, table_name: str, images: List[Dict[str, str]], parent=None):
        super(ImageViewer, self).__init__(parent)
        self.table_name = table_name
        self.ims = images
        self.im_index = 0
        self.im_count = len(images)
        self.zoom = 1
        self.rotate_angle = 0
        self.pixmap_item = None

        self.ui = Ui_ImageViewer()
        self.ui.setupUi(self)

        self.show_image()

    @pyqtSlot()
    def on_btnRadioLarger_clicked(self):
        factor = 1.2
        print(self.zoom)
        if self.zoom <= 3:
            self.ui.graphicsView.scale(factor, factor)
            self.zoom += 0.2

    @pyqtSlot()
    def on_btnRadioSmaller_clicked(self):
        factor = 0.8
        print(self.zoom)
        if self.zoom >= -1:
            self.ui.graphicsView.scale(factor, factor)
            self.zoom -= 0.2

    @pyqtSlot()
    def on_btnDelete_clicked(self):
        pass

    @pyqtSlot()
    def on_btnRotate_clicked(self):
        pass

    @pyqtSlot()
    def on_btnSave_clicked(self):
        pass

    @pyqtSlot()
    def on_btnPrint_clicked(self):
        pass

    @pyqtSlot()
    def on_btnLeft_clicked(self):
        self.ui.graphicsView.fitInView(self.pixmap_item, Qt.IgnoreAspectRatio)
        print(self.ui.graphicsView.scene().itemsBoundingRect())
        print(self.ui.graphicsView.rect())

    @pyqtSlot()
    def on_btnRight_clicked(self):
        self.ui.graphicsView.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        print(self.ui.graphicsView.scene().itemsBoundingRect())
        print(self.ui.graphicsView.rect())

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

        # self.fit_image()

    def fit_image(self):
        if self.pixmap_item is not None:
            self.ui.graphicsView.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        # self.ui.graphicsView.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

    # def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
    #     if self.pixmap_item is None:
    #         return
    #     if event.angleDelta().y() > 0:
    #         factor = 1.2
    #         self.zoom += 0.2
    #     else:
    #         factor = 0.8
    #         self.zoom -= 0.2
    #
    #     if self.zoom > -1:
    #         self.ui.graphicsView.scale(factor, factor)
    #     else:
    #         self.fit_image()
    #         self.zoom = 1
