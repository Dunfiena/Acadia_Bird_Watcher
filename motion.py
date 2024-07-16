import os.path
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, \
    QGroupBox, QWidget, QGridLayout, QRadioButton, QSlider, QTabWidget, QSpinBox, QMessageBox, QDialog, QVBoxLayout, \
    QTableWidgetItem, QTableWidget, QProgressBar

import algo
import cmd_handler
import cv2
import Bird
import imutils
import numpy as np
import time
from datetime import datetime
from signal_DataStruct import signal_DataStruct


class MotionThread(QThread):
    signal_1 = pyqtSignal(signal_DataStruct)

    def run(self, source, threshold, max, k_value, sigma_value, PbRate, top, bottom, left, right):
        # Array of the birds found - ID is the id of the bird and increments
        birds = []
        birds_saved = []
        Id = 0
        max_age = 15

        # Adjustments for allowed size of bird
        frameArea = 1500 * 2000
        min_area = frameArea / 15000
        max_area = frameArea / 50

        # Video loading, getting time information of video
        video = cv2.VideoCapture(source)
        f = video.get(cv2.CAP_PROP_FPS)  # OpenCV v2.x used "CV_CAP_PROP_FPS"
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / f
        time = 0
        flag = True

        obj_width = max  # MOVEMENT BETWEEN FRAMES -> The higher the number = more movement
        frametime = PbRate  # Play back rate of the video
        k = k_value
        sigma = sigma_value

        # First frame and next frame are used to compare the
        # differences between the two images
        first_frame = None
        next_frame = None
        delay_counter = 0

        ##################################################################################3
        # ret is return boolean   Frame is image array
        # movement flag true when detection true
        while flag:
            ### if frames stil exist ###
            time += 1
            success, frame = video.read()
            if success:
                original_frame = frame.copy()
                # frame = imutils.resize(frame, width=1000)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Adjusting this to larger numbers means a much lower sensitivity
                gray = cv2.GaussianBlur(gray, (k, k), sigma)
                gray = cv2.equalizeHist(gray)

                if first_frame is None:
                    first_frame = gray
                else:
                    first_frame = next_frame

                next_frame = gray

                # compare 2 frames for differences - remove what is the same
                frame_delta = cv2.absdiff(first_frame, next_frame)

                # select the difference
                thresh = cv2.threshold(frame_delta, threshold, 255, cv2.THRESH_BINARY)[1]

                # thresh = cv2.adaptiveThreshold(frame_delta,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
                thresh = cv2.dilate(thresh, None, iterations=4)
                contours0, contours1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # frame = imutils.resize(frame, width=1000)
                (H, W) = frame.shape[:2]
                cv2.line(frame, [0, top], [1000, top], (0, 0, 255), 2)
                cv2.line(frame, [0, bottom], [1000, bottom], (0, 0, 255), 2)
                cv2.line(frame, [right, 0], [right, 1000], (0, 0, 255), 2)
                cv2.line(frame, [left, 0], [left, 1000], (0, 0, 255), 2)

                for cnt in contours0:
                    if max_area > cv2.contourArea(cnt):
                        M = cv2.moments(cnt)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        x, y, w, h = cv2.boundingRect(cnt)
                        new = True
                        if y > top and y + h < bottom and x > left and x + w < right:
                            rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            birds = algo.clean_slate(birds)
                            for i in birds:
                                if abs(x - i.getX()) / obj_width <= w and abs(y - i.getY()) / obj_width <= h:
                                    # the object is close to one that was detected before
                                    new = False
                                    i.updateCoords(cx, cy)
                                    i.setAge()
                                elif abs(x + i.getX()) * obj_width <= w and abs(y + i.getY()) * obj_width <= h:
                                    new = False
                                    i.updateCoords(cx, cy)
                                    i.setAge()
                                elif abs(x + i.getX()) * obj_width <= w and abs(y - i.getY()) / obj_width <= h:
                                    new = False
                                    i.updateCoords(cx, cy)
                                    i.setAge()
                                elif abs(x - i.getX()) / obj_width <= w and abs(y + i.getY()) * obj_width <= h:
                                    new = False
                                    i.updateCoords(cx, cy)
                                    i.setAge()
                                else:
                                    i.age = i.age + 1
                                    if i.age == max_age:
                                        birds_saved.append(i)
                                        birds.remove(i)

                            if new:
                                current_Time = time / f
                                bird_pojo = Bird.Object(Id, x, y, w, h, 0, current_Time)
                                birds.append(bird_pojo)
                                Id += 1

                birds = algo.clean_handler(birds, birds_saved)
                for i in birds:
                    cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), 0, 0.6, (0, 0, 124), 1, cv2.LINE_AA)

                frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)

                minutes = int(duration / 60)
                seconds = int(duration % 60)
                current_Time = time / f

                # This is the buffer branch
                cv2.imshow("Bird Watcher", frame)
                # cv2.imshow("Bird Watcher", frame_delta)

                progress_percent = (current_Time / duration) * 100

                sig_DS = signal_DataStruct(int(progress_percent), birds, birds_saved)
                self.signal_1.emit(sig_DS)

                # waitkey sets the frame rate  ord('q') is the exit (press q to quit)
                if (cv2.waitKey(int((f)/PbRate)) & 0xFF == ord('q')
                        or cv2.getWindowProperty('Bird Watcher', cv2.WND_PROP_VISIBLE) == 0):
                    flag = False
                    break
            else:
                break

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        file = open("test/" + os.path.basename(source) + ".txt", "w")
        file.write("Video Name: " + source +
                   "\nVideo Length: " + (str)(minutes) + ":" + (str)(seconds) +
                   "\nRuntime (sec): " + (str)(current_Time) +
                   "\nCurrent Date: " + dt_string + "\n\n" +
                   "Total Birds Counted: " + str(len(birds + birds_saved)) + "\nBird based on timestamp: " + "\n")
        for bird in birds:
            birds_saved.append(bird)

        birds_saved = algo.sort_index(birds_saved)
        birds_saved = algo.end_run_clean_index(birds_saved)

        for bird in birds_saved:
            file.write(bird.toString())
        file.close()
        video.release()
        cv2.destroyAllWindows()

        ### command handler check if the next video exists and run again

    def pause(self):
        cv2.waitKey(-1)  # wait until any key is pressed

    def continue_program(self, PbRate):
        cv2.destroyAllWindows()
