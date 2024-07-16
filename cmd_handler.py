from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, \
    QGroupBox, QWidget, QGridLayout, QRadioButton, QSlider, QTabWidget, QSpinBox, QMessageBox, QDialog, QVBoxLayout, \
    QTableWidgetItem, QTableWidget, QProgressBar
import motion
from Bird import Object


class CmdHandler(QWidget):

    def __init__(self, source, threshold, max, k_value, sigma_value, pb_Rate, top, bottom, left, right):
        super().__init__()
        self.source = source
        self.threshold = threshold
        self.max = max
        self.k_value = k_value
        self.sigma_value = sigma_value
        self.PbRate = pb_Rate
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        self.title = "Pay Back Menu"
        self.setWindowIcon(QIcon("Assets/project_icon_2.png"))
        self.left_bound = 0
        self.top_bound = 0
        self.width = 500
        self.height = 800
        self.setGeometry(self.left_bound, self.top_bound, self.width, self.height)

        self.signalConnect = pyqtSignal(int)
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_program)

        pause_button = QPushButton("Pause", self)
        pause_button.clicked.connect(self.pause_program)

        quit_button = QPushButton("Exit", self)
        quit_button.clicked.connect(self.quit_program)

        self.savedBirdTable = QTableWidget(self)
        self.savedBirdTable.setColumnCount(3)
        self.savedBirdTable.setRowCount(1)

        self.savedBirdTable.setItem(0, 0, QTableWidgetItem("Bird ID"))
        self.savedBirdTable.setItem(0, 1, QTableWidgetItem("Coordinates"))
        self.savedBirdTable.setItem(0, 2, QTableWidgetItem("Time"))

        self.activeBirdTables = QTableWidget(self)
        self.activeBirdTables.setColumnCount(4)
        self.activeBirdTables.setRowCount(1)

        self.activeBirdTables.setItem(0, 0, QTableWidgetItem("Bird ID"))
        self.activeBirdTables.setItem(0, 1, QTableWidgetItem("Coordinates"))
        self.activeBirdTables.setItem(0, 2, QTableWidgetItem("Age"))
        self.activeBirdTables.setItem(0, 3, QTableWidgetItem("Time"))

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(30, 40, 200, 25)

        layout = QVBoxLayout()
        layout.addWidget(self.run_button)
        layout.addWidget(pause_button)
        layout.addWidget(quit_button)
        layout.addWidget(self.savedBirdTable)
        layout.addWidget(self.activeBirdTables)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

        self.worker = motion.MotionThread(self)
        self.worker.signal_1.connect(self.update)

    def run_program(self):
        if self.run_button.text() == "Run":
            for x in self.source:
                self.run_button.setText("Continue")
                self.worker.run(x, self.threshold, self.max, self.k_value,
                                self.sigma_value, self.PbRate, self.top, self.bottom, self.left, self.right)

    def pause_program(self):
        self.worker.pause()

    def quit_program(self):
        exit(0)

    def update(self, sig_DS):
        progress, birds, birds_saved = sig_DS.getStructData()
        self.progressBar.setValue(progress)

        j = 1
        if len(birds_saved) >= 0:
            self.savedBirdTable.setRowCount((len(birds_saved) + 1))
            for i in birds_saved:
                coord = str(i.getY()) + " , " + str(i.getX())
                self.savedBirdTable.setItem(j, 0, QTableWidgetItem(str(i.getId())))
                self.savedBirdTable.setItem(j, 1, QTableWidgetItem(str(coord)))
                self.savedBirdTable.setItem(j, 2, QTableWidgetItem(str(i.getTime())))
                j += 1

            j = 1
            self.activeBirdTables.setRowCount((len(birds) + 1))
            for i in birds:
                coord = str(i.getY()) + " , " + str(i.getX())
                self.activeBirdTables.setItem(j, 0, QTableWidgetItem(str(i.getId())))
                self.activeBirdTables.setItem(j, 1, QTableWidgetItem(str(str(coord))))
                self.activeBirdTables.setItem(j, 2, QTableWidgetItem(str(i.getAge())))
                self.activeBirdTables.setItem(j, 3, QTableWidgetItem(str(i.getTime())))
                j += 1
