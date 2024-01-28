def run():
    import Bird
    import imutils
    import cv2
    import numpy as np
    import time

    # Array of the birds found - ID is the id of the bird and increments
    birds = []
    Id = 0
    h = 900
    w = 1200
    frameArea = h * w
    min_area = frameArea / 6000
    max_area = frameArea / 3000

    # VIDEO Source = ".mp4" or 0 for webcam
    source = "bird vid.mp4"
    video = cv2.VideoCapture(source)

    MIN_SIZE_FOR_MOVEMENT = 50  # Low number = VERY SENSITVE  Keep it up above 100
    frametime = 1  # Play back rate of the video

    # First frame and next frame are used to compare the
    # differences between the two images
    first_frame = None
    next_frame = None
    delay_counter = 0

    ##################################################################################3
    # ret is return boolean   Frame is image array
    # movement flag true when detection true
    while True:

        success, frame = video.read()
        original_frame = frame.copy()

        frame = imutils.resize(frame, width=750)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (25, 25), 0)

        if first_frame is None: first_frame = gray
        next_frame = gray

        # compare 2 frames for differences - remove what is the same
        frame_delta = cv2.absdiff(first_frame, next_frame)

        # select the difference
        thresh = cv2.threshold(frame_delta, 3, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=1)
        contours0, contours1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]

        for cnt in contours0:
            if cv2.contourArea(cnt) < max_area:
                if cv2.contourArea(cnt) > min_area:
                    M = cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    x, y, w, h = cv2.boundingRect(cnt)
                    new = True
                    rect = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    for i in birds:
                        if abs(x - i.getX()) <= w * 2 and abs(y - i.getY()) <= h * 2:
                            # the object is close to one that was detected before
                            new = False
                            i.updateCoords(cx, cy)
                    if new == True:
                        bird_pojo = Bird.Object(Id, x, y, w, h)
                        birds.append(bird_pojo)
                        Id += 1

        for i in birds:
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), 0, 0.3, (0, 0, 124), 1, cv2.LINE_AA)

        frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)
        # cv2.imshow("frame", np.hstack((frame_delta, frame)))
        cv2.imshow("frame", frame)

        # waitkey sets the frame rate  ord('q') is the exit (press q to quit)
        if cv2.waitKey(frametime) & 0xFF == ord('q'):
            break
    print(len(birds))
    video.release()


run()