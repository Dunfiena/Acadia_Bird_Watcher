import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, \
    QGroupBox, QWidget, QGridLayout, QSpinBox, QMessageBox

from cmd_handler import CmdHandler


class MainWindow(QMainWindow):
    def set_filename(self, x):
        self._filename = x

    def get_filename(self):
        return self._filename

    def __init__(self):
        # region setup
        super().__init__()
        self.play = None
        self._filename = []
        self.title = "Acadia Bird Watcher"
        self.setWindowIcon(QIcon("Assets/project_icon_2.png"))
        self.left_bound = 0
        self.top_bound = 0
        self.width = 1400
        self.height = 200

        self.setWindowTitle(self.title)
        self.setGeometry(self.left_bound, self.top_bound, self.width, self.height)
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
        sub.setGeometry(self.left_bound, self.top_bound, self.width, self.height)
        layout = QGridLayout(self)

        File = QGroupBox(self)
        file_sel = QLabel(self)
        file_sel.setText('Select File: ')

        search = QPushButton('Select File', self)
        search.clicked.connect(self.select_file)
        search.setFixedSize(250, 50)

        top_label = QLabel(self)
        top_label.setText("Top cutoff")

        bottom_label = QLabel(self)
        bottom_label.setText("Bottom cutoff")

        left_label = QLabel(self)
        left_label.setText("Left cutoff")

        right_label = QLabel(self)
        right_label.setText("Right cutoff")

        self.top = QSpinBox()
        self.top.setFixedSize(100, 50)
        self.top.setMaximum(1000)
        self.top.setValue(0)

        self.right = QSpinBox()
        self.right.setFixedSize(100, 50)
        self.right.setMaximum(1000)
        self.right.setValue(1000)

        self.bottom = QSpinBox()
        self.bottom.setFixedSize(100, 50)
        self.bottom.setMaximum(1000)
        self.bottom.setValue(1000)

        self.left = QSpinBox()
        self.left.setFixedSize(100, 50)
        self.left.setMaximum(1000)
        self.left.setValue(0)

        threshold = QLabel(self)
        threshold.setText('Threshold')

        movement_max = QLabel(self)
        movement_max.setText('Maximum movement')

        speed = QLabel(self)
        speed.setText('Playback rate')

        self.threshold_value = QSpinBox()
        self.threshold_value.setFixedSize(100, 50)
        self.threshold_value.setValue(15)

        self.max_move = QSpinBox()
        self.max_move.setFixedSize(100, 50)
        self.max_move.setValue(10)

        self.PbRate = QSpinBox()
        self.PbRate.setFixedSize(100, 50)
        self.PbRate.setValue(1)

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
        run_button.setFixedSize(175, 175)

        layout.addWidget(File, 0, 0, 2, 3)
        layout.addWidget(file_sel, 0, 0, 1, 3)
        layout.addWidget(search, 1, 0, 1, 3)

        layout.addWidget(top_label, 0, 4, 1, 3)
        layout.addWidget(left_label, 1, 4, 1, 3)
        layout.addWidget(right_label, 2, 4, 1, 3)
        layout.addWidget(bottom_label, 3, 4, 1, 3)

        layout.addWidget(self.top, 0, 7, 1, 3)
        layout.addWidget(self.left, 1, 7, 1, 3)
        layout.addWidget(self.right, 2, 7, 1, 3)
        layout.addWidget(self.bottom, 3, 7, 1, 3)

        layout.addWidget(threshold, 0, 11, 1, 3)
        layout.addWidget(movement_max, 1, 11, 1, 3)
        layout.addWidget(self.threshold_value, 0, 14, 1, 3)
        layout.addWidget(self.max_move, 1, 14, 1, 3)

        layout.addWidget(k_label, 0, 17, 1, 3)
        layout.addWidget(sigma_label, 1, 17, 1, 3)
        layout.addWidget(speed, 2, 17, 1, 3)

        layout.addWidget(self.k, 0, 20, 1, 3)
        layout.addWidget(self.sigma, 1, 20, 1, 3)
        layout.addWidget(self.PbRate, 2, 20, 1, 3)

        layout.addWidget(run_button, 0, 25, 3, 3)

        sub.setLayout(layout)
        self.show()

    def select_file(self):
        file_dialog = QFileDialog().getOpenFileNames(self, 'Open file',
                                                     './Images_Input', "Image files (*.avi *.mp4 *.mov)")

        if file_dialog:
            image_path = file_dialog[0]
            print(image_path)
            window.set_filename(image_path)
            self.checkSettings(file_dialog[0][0])

    def run(self):
        if len(window.get_filename()) == 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Alert")
            dlg.setText("Please select file name and try again")
            dlg.exec_()
        else:
            # self.write_settings()
            k = self.k.value()
            if k % 2 == 0:
                k += 1
            self.play = CmdHandler(window.get_filename(), self.threshold_value.value(), self.max_move.value(), k,
                                   self.sigma.value(), self.PbRate.value(), self.top.value(), self.bottom.value(),
                                   self.left.value(), self.right.value())
            self.play.show()

    def checkSettings(self, image_path):
        if os.path.isfile("database.txt"):
            with open("database.txt", 'a+') as f:
                f.seek(0)
                lines = f.readlines()
                line_num = 0
                values = []
                for line in lines:
                    line_num += 1
                    if image_path[0] in line:
                        for i in range(9):
                            val = lines[line_num + i].split(":")
                            values.append(val[-1])
                        self.setValues(values)
                        print("found")
                        f.close()
                        break

                    elif line == lines[-1]:
                        f.write("\n\n")
                        f.write(image_path[0])
                        f.write("\ntop: 1")
                        f.write("\nleft: 1")
                        f.write("\nright: 1")
                        f.write("\nbottom: 1")
                        f.write("\nthreshold: 15")
                        f.write("\nMaximum: 10")
                        f.write("\nK-value: 15")
                        f.write("\nSigma: 3")
                        f.write("\nPbRate: 1")
                        self.setValues(values=[1, 1, 1, 1, 15, 10, 15, 3, 1])
                        f.close()

        else:
            f = open("database.txt", "w")
            f.write("Database file created\n----------------------------------------------")
            f.write("\n\n")
            f.write(image_path[0])
            f.write("\ntop: 1")
            f.write("\nleft: 1")
            f.write("\nright: 1")
            f.write("\nbottom: 1")
            f.write("\nthreshold: 15")
            f.write("\nMaximum: 10")
            f.write("\nK-value: 15")
            f.write("\nSigma: 3")
            f.write("\nPbRate: 1")
            self.setValues(values=[1, 1, 1, 1, 15, 10, 15, 3, 1])
            f.close()

    def write_settings(self):
        f = open("database.txt", "r")
        lines = f.readlines()
        line_num = 0

        for line in lines:
            line_num += 1
            if window.get_filename() in line:
                lines[line_num] = "top: " + str(self.top.value()) + "\n"
                lines[line_num + 1] = "left: " + str(self.left.value()) + "\n"
                lines[line_num + 2] = "right: " + str(self.right.value()) + "\n"
                lines[line_num + 3] = "bottom: " + str(self.bottom.value()) + "\n"
                lines[line_num + 4] = "threshold: " + str(self.threshold_value.value()) + "\n"
                lines[line_num + 5] = "Maximum: " + str(self.max_move.value()) + "\n"
                lines[line_num + 6] = "K-value: " + str(self.k.value()) + "\n"
                lines[line_num + 7] = "Sigma: " + str(self.sigma.value()) + "\n"
                lines[line_num + 8] = "PbRate: " + str(self.PbRate.value()) + "\n"
                break

        f.close()
        f = open("database.txt", "w")
        f.writelines(lines)
        f.close()

    # Set values
    def setValues(self, values):
        self.top.setValue(int(values[0]))
        self.left.setValue(int(values[1]))
        self.right.setValue(int(values[2]))
        self.bottom.setValue(int(values[3]))

        self.threshold_value.setValue(int(values[4]))
        self.max_move.setValue(int(values[5]))
        self.k.setValue(int(values[6]))
        self.sigma.setValue(int(values[7]))
        self.PbRate.setValue(int(values[8]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
