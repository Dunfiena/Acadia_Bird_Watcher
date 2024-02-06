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
    QGroupBox, QWidget, QGridLayout, QRadioButton, QSlider, QTabWidget, QSpinBox, QMessageBox
from imutils.video import fps


class MainWindow(QMainWindow):
    def set_filename(self, x):
        self._filename = x

    def get_filename(self):
        return self._filename

    def set_output(self, x):
        self._output = x

    def get_output(self):
        return self._output
    def __init__(self):
        # region setup
        super().__init__()
        self._filename = None
        self._output = "./"
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
        self.height.setValue(600)

        movement_min = QLabel(self)
        movement_min.setText('Minimum movement')

        movement_max = QLabel(self)
        movement_max.setText('Maximum movement')

        speed = QLabel(self)
        speed.setText('Frames per second')

        self.min_move = QSpinBox()
        self.min_move.setFixedSize(100, 50)
        self.min_move.setValue(6)

        self.max_move = QSpinBox()
        self.max_move.setFixedSize(100, 50)
        self.max_move.setValue(6)

        self.fps = QSpinBox()
        self.fps.setFixedSize(100, 50)
        self.fps.setValue(10)

        k_label = QLabel(self)
        k_label.setText('K value')

        sigma_label = QLabel(self)
        sigma_label.setText('Sigma')

        self.k = QSpinBox()
        self.k.setFixedSize(100, 50)
        self.k.setValue(21)

        self.sigma = QSpinBox()
        self.sigma.setFixedSize(100, 50)
        self.sigma.setValue(51)

        out_label = QLabel(self)
        out_label.setText('Select output Location')

        out_button = QPushButton('Select output', self)
        out_button.clicked.connect(self.output)
        out_button.setFixedSize(250, 50)

        current_out = QLabel(self)
        current_out.setText(self._output)

        run_button = QPushButton('Run', self)
        run_button.clicked.connect(self.run)
        run_button.setFixedSize(175,175)

        layout.addWidget(File, 0, 0, 2, 3)
        layout.addWidget(file_sel, 0,0,1,3)
        layout.addWidget(search, 1,0,1,3)

        layout.addWidget(height_border, 0, 6, 2, 3)
        layout.addWidget(height_label, 0,6,1,3)
        layout.addWidget(self.height, 1, 6, 1, 3)

        layout.addWidget(movement_min, 0,11,1,3)
        layout.addWidget(movement_max, 1,11,1,3)
        layout.addWidget(self.min_move, 0,14,1,3)
        layout.addWidget(self.max_move, 1,14,1,3)

        layout.addWidget(k_label, 0,17,1,3)
        layout.addWidget(sigma_label, 1,17,1,3)
        layout.addWidget(speed, 2,17,1,3)

        layout.addWidget(self.k, 0,20,1,3)
        layout.addWidget(self.sigma, 1,20,1,3)
        layout.addWidget(self.fps, 2, 20, 1, 3)

        layout.addWidget(out_label, 2, 0, 1, 3)
        layout.addWidget(out_button, 2, 6, 1, 3)
        layout.addWidget(current_out, 2, 12, 1, 3)

        layout.addWidget(run_button, 0, 25, 3, 3)

        sub.setLayout(layout)
        self.show()

    def select_file(self):
        file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                    './Images_Input', "Image files (*.avi *.mp4)")
        if file_dialog:
            image_path = file_dialog[0]
            window.set_filename(image_path)

    def run(self):
        motion.run(window.get_filename(), self.min_move.value(), self.max_move.value(),
                   self.k.value(), self.sigma.value(), self.fps.value(), self.height.value())
    def output(self):
        output_path = QFileDialog().getExistingDirectory(self, None, "Select Folder")
        if output_path:
            window.set_output_dir(output_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
