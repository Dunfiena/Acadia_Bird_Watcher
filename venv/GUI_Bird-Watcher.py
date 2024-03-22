import os
import shutil
import sys

import cv2
import matplotlib.pyplot as plt
import motion
import numpy as np
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, \
    QGroupBox, QWidget, QGridLayout, QRadioButton, QSlider, QTabWidget, QSpinBox, QMessageBox, QDialog
from imutils.video import fps

class MainWindow(QMainWindow):
    def set_filename(self, x):
        self._filename = x

    def get_filename(self):
        return self._filename

    def __init__(self):
        # region setup
        super().__init__()
        self._filename = None
        self.title = "Acadia Bird Watcher"
        self.setWindowIcon(QIcon("Assets/project_icon_2.png"))
        self.left = 0
        self.top = 0
        self.width = 1400
        self.height = 200

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        app.setStyleSheet('QLabel{font: 12pt; color:grey}'
                          'QRadioButton{font-size: 16pt;}'
                          'QComboBox{font-size: 12pt;}'
                          'QLineEdit{font-size: 16pt;}'
                          'QPushButton{font-size: 12pt;}'
                          'QSpinBox{font-size: 12pt;}'
                          'QDoubleSpinBox{font-size: 12pt;}'
                          'QCheckBox{font-size: 12pt;}'
                          'QGroupBox{border: 2px solid gray;border-radius: 5px;background: rgb(211, 218, 235);}'
                          'Selection-color: grey;')
        # endregion

        # region Widgets
        sub = QWidget(self)
        sub.setGeometry(self.left, self.top, self.width, self.height)
        layout = QGridLayout(self)

        File = QGroupBox(self)
        file_sel = QLabel(self)
        file_sel.setText('Select File: ')

        search = QPushButton('Select File', self)
        search.clicked.connect(self.select_file)
        search.setFixedSize(250, 50)

        height_border = QGroupBox(self)
        height_label = QLabel(self)
        height_label.setText('Select detection cutoff: ')

        self.height = QSpinBox()
        self.height.setFixedSize(250, 50)
        self.height.setMaximum(1000)
        self.height.setValue(550)

        threshold = QLabel(self)
        threshold.setText('Threshold')

        movement_max = QLabel(self)
        movement_max.setText('Maximum movement')

        speed = QLabel(self)
        speed.setText('Seconds per frame')

        self.threshold_value = QSpinBox()
        self.threshold_value.setFixedSize(100, 50)
        self.threshold_value.setValue(15)

        self.max_move = QSpinBox()
        self.max_move.setFixedSize(100, 50)
        self.max_move.setValue(7)

        self.fps = QSpinBox()
        self.fps.setFixedSize(100, 50)
        self.fps.setValue(10)

        k_label = QLabel(self)
        k_label.setText('K value')

        sigma_label = QLabel(self)
        sigma_label.setText('Sigma')

        self.k = QSpinBox()
        self.k.setFixedSize(100, 50)
        self.k.setValue(15)

        self.sigma = QSpinBox()
        self.sigma.setFixedSize(100, 50)
        self.sigma.setValue(3)

        run_button = QPushButton('Run', self)
        run_button.clicked.connect(self.run)
        run_button.setFixedSize(175,175)

        layout.addWidget(File, 0, 0, 2, 3)
        layout.addWidget(file_sel, 0,0,1,3)
        layout.addWidget(search, 1,0,1,3)

        layout.addWidget(height_border, 0, 6, 2, 3)
        layout.addWidget(height_label, 0,6,1,3)
        layout.addWidget(self.height, 1, 6, 1, 3)

        layout.addWidget(threshold, 0,11,1,3)
        layout.addWidget(movement_max, 1,11,1,3)
        layout.addWidget(self.threshold_value, 0,14,1,3)
        layout.addWidget(self.max_move, 1,14,1,3)

        layout.addWidget(k_label, 0,17,1,3)
        layout.addWidget(sigma_label, 1,17,1,3)
        layout.addWidget(speed, 2,17,1,3)

        layout.addWidget(self.k, 0,20,1,3)
        layout.addWidget(self.sigma, 1,20,1,3)
        layout.addWidget(self.fps, 2, 20, 1, 3)

        layout.addWidget(run_button, 0, 25, 3, 3)

        sub.setLayout(layout)
        self.show()

    def select_file(self):
        file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                    './Images_Input', "Image files (*.avi *.mp4 *.mov)")
        if file_dialog:
            image_path = file_dialog[0]
            window.set_filename(image_path)

    def run(self):
        if window.get_filename() == None or window.get_filename() == "":
            dlg = QMessageBox(self);
            dlg.setWindowTitle("Alert")
            dlg.setText("Please select file name and try again")
            dlg.exec_()
        else:
            k = self.k.value()
            if k%2 == 0:
                k +=1

            motion.run(window.get_filename(), self.threshold_value.value(), self.max_move.value(), k,
                            self.sigma.value(), self.fps.value(), self.height.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
