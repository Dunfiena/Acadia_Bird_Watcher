import cv2
import Bird
import imutils
import numpy as np
import time
from datetime import datetime


def run(source, min, max, k_value, sigma_value, fps, height_value):
    # Array of the birds found - ID is the id of the bird and increments

    birds = []
    birds_saved = []
    Id = 0
    high = 900
    wide = 1200
    frameArea = high * wide
    min_area = frameArea / 9000
    max_area = frameArea / 2500
    max_age = 15

    # VIDEO Source = ".mp4" or 0 for webcam
    # source = "bird vid.mp4"
    # source ="test.mp4"
    video = cv2.VideoCapture(source)

    f = video.get(cv2.CAP_PROP_FPS)  # OpenCV v2.x used "CV_CAP_PROP_FPS"
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / f
    time = 0

    # SOPHIE ADJUST AREA
    min_obj_width = min
    obj_width = max  # MOVEMENT BETWEEN FRAMES -> The higher the number = more movement
    MIN_SIZE_FOR_MOVEMENT = 100  # Low number = VERY SENSITVE  Keep it up above 100
    frametime = fps  # Play back rate of the video
    k = k_value
    sigma = sigma_value
    height_tol = height_value

    # First frame and next frame are used to compare the
    # differences between the two images
    first_frame = None
    next_frame = None
    delay_counter = 0

    ##################################################################################3
    # ret is return boolean   Frame is image array
    # movement flag true when detection true
    while True:
        time +=1
        success, frame = video.read()
        original_frame = frame.copy()
        frame = imutils.resize(frame, width=1000)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Adjusting this to larger numbers means a much lower senstivity
        gray = cv2.GaussianBlur(gray, (k, k), sigma)

        if first_frame is None: first_frame = gray
        next_frame = gray

        # compare 2 frames for differences - remove what is the same
        frame_delta = cv2.absdiff(first_frame, next_frame)

        # select the difference
        thresh = cv2.threshold(frame_delta, 5, 100, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)
        contours0, contours1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame = imutils.resize(frame, width=1000)
        (H, W) = frame.shape[:2]
        cv2.line(frame, [0, height_tol], [1000, height_tol], (0,0,255), 2)


        for cnt in contours0:
            if cv2.contourArea(cnt) < max_area:
                if cv2.contourArea(cnt) > min_area:
                    M = cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    x, y, w, h = cv2.boundingRect(cnt)
                    new = True
                    min_obj_width = min_obj_width/1000
                    if y < height_tol:
                        rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        for i in birds:
                            if (abs(x - i.getX())/obj_width <= w  and abs(y - i.getY())/obj_width <= h and
                                abs(x - i.getX())*min_obj_width <= w  and abs(y - i.getY())*min_obj_width <= h):
                                # the object is close to one that was detected before
                                new = False
                                i.updateCoords(cx, cy)
                            elif (abs(x + i.getX())*obj_width <= w and abs(y + i.getY())*obj_width <= h and
                                  abs(x - i.getX())*min_obj_width <= w  and abs(y - i.getY())*min_obj_width <= h):
                                new = False
                                i.updateCoords(cx, cy)
                            elif (abs(x + i.getX())*obj_width <= w and abs(y - i.getY())*obj_width <= h and
                                  abs(x - i.getX())*min_obj_width <= w  and abs(y - i.getY())*min_obj_width <= h):
                                new = False
                                i.updateCoords(cx, cy)
                            elif (abs(x - i.getX())*obj_width <= w and abs(y + i.getY())*obj_width <= h and
                                  abs(x - i.getX())*min_obj_width <= w  and abs(y - i.getY())*min_obj_width <= h):
                                new = False
                                i.updateCoords(cx, cy)
                            else:
                                i.age = i.age+1
                                if i.age == max_age:
                                    birds_saved.append(i)
                                    birds.remove(i)

                        if new == True:
                            current_Time = time / frametime
                            bird_pojo = Bird.Object(Id, x, y, w, h,0, current_Time)
                            birds.append(bird_pojo)
                            Id += 1

        for i in birds:
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), 0, 0.3, (0, 0, 124), 1, cv2.LINE_AA)

        frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)

        minutes = int(duration / 60)
        seconds = (int)(duration % 60)
        current_Time = time/frametime

        # cv2.imshow("frame", np.hstack((frame_delta, frame)))
        frame = cv2.putText(frame, (str)(current_Time) + " / "+(str)(minutes) + " " + (str)(seconds),
                            (50,50),0,1,(255,255,0), 2, cv2.LINE_AA)
        cv2.imshow("frame", frame)

        # waitkey sets the frame rate  ord('q') is the exit (press q to quit)
        if cv2.waitKey(frametime) & 0xFF == ord('q'):
            break

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    file = open("test.txt", "w")
    file.write("Video Name: " + source +
               "\nVideo Length: " + (str)(minutes) + ":" + (str)(seconds) +
               "\nRuntime (sec): " + (str)(current_Time) +
               "\nCurrent Date: " + dt_string + "\n\n" +
               "Total Birds Counted: " + str(len(birds)) + "\nBird based on timestamp: " + "\n")
    for bird in birds:
        birds_saved.append(bird)
    for bird in birds_saved:
        file.write(bird.toString())
    file.close()

    video.release()

def sample_Ground(source):
    sample = []
    video = cv2.VideoCapture(source)
    success, frame = video.read()
    for i in frame:
        colors = frame[i][-1]
        sample.append(colors)
        print(sample)
    exit(0)
    return sample

# run("bird vid.mp4", 6, 6, 21, 21, 10, 400)