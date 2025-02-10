import cv2
import numpy as np

RECT_MIN = 80
RECT_HEIGHT = 80

OFFSET = 6

CENTER_COORDINATES = []
VEHICLE_IN_COUNTER = 0
VEHICLE_OUT_COUNTER = 0

LINE_POSITION_Y = 550
LINE_IN_X_1 = 25
LINE_IN_X_2 = 600
LINE_OUT_X_1 = 600
LINE_OUT_X_2 = 1200


def getCenter(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


# Web camera
cap = cv2.VideoCapture('video.mp4')

# Initialize Substractor
algorithm = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame1 = cap.read()
    frame1 = cv2.resize(frame1, (1280, 720))

    # Blur each frame
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = algorithm.apply(blur)

    dilate = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilation = cv2.morphologyEx(dilate, cv2. MORPH_CLOSE, kernel)
    dilation = cv2.morphologyEx(dilation, cv2. MORPH_CLOSE, kernel)
    contours, h = cv2.findContours(
        dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw lane in line & offset
    cv2.line(frame1, (LINE_IN_X_1, LINE_POSITION_Y),
             (LINE_IN_X_2, LINE_POSITION_Y), (0, 0, 255), 2)
    cv2.line(frame1, (LINE_IN_X_1, LINE_POSITION_Y+OFFSET),
             (LINE_IN_X_2, LINE_POSITION_Y+OFFSET), (255, 255, 255), 1)
    cv2.line(frame1, (LINE_IN_X_1, LINE_POSITION_Y-OFFSET),
             (LINE_IN_X_2, LINE_POSITION_Y-OFFSET), (255, 255, 255), 1)

    # Draw lane out line & offset
    cv2.line(frame1, (LINE_OUT_X_1, LINE_POSITION_Y),
             (LINE_OUT_X_2, LINE_POSITION_Y), (0, 255, 0), 2)
    cv2.line(frame1, (LINE_OUT_X_1, LINE_POSITION_Y+OFFSET),
             (LINE_OUT_X_2, LINE_POSITION_Y+OFFSET), (255, 255, 255), 1)
    cv2.line(frame1, (LINE_OUT_X_1, LINE_POSITION_Y-OFFSET),
             (LINE_OUT_X_2, LINE_POSITION_Y-OFFSET), (255, 255, 255), 1)

    for(i, c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_contour = (w >= RECT_MIN) and (h >= RECT_HEIGHT)
        if not validate_contour:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (255, 255, 255), 2)
        center_coord = getCenter(x, y, w, h)
        CENTER_COORDINATES.append(center_coord)
        cv2.circle(frame1, center_coord, 4, (0, 0, 255), -1)

        for (x, y) in CENTER_COORDINATES:
            if y < (LINE_POSITION_Y+OFFSET) and y > (LINE_POSITION_Y-OFFSET) and x < (LINE_IN_X_2) and x > (LINE_IN_X_1):
                VEHICLE_IN_COUNTER += 1
                CENTER_COORDINATES.remove((x, y))

        for (x, y) in CENTER_COORDINATES:
            if y < (LINE_POSITION_Y+OFFSET) and y > (LINE_POSITION_Y-OFFSET) and x < (LINE_OUT_X_2) and x > (LINE_OUT_X_1):
                VEHICLE_OUT_COUNTER += 1
                CENTER_COORDINATES.remove((x, y))

    cv2.putText(frame1, "In : "+str(VEHICLE_IN_COUNTER), (400, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    cv2.putText(frame1, "Out : "+str(VEHICLE_OUT_COUNTER), (800, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    cv2.imshow("Contour CENTER_COORDINATESor", dilation)
    cv2.imshow("Counter", frame1)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()
