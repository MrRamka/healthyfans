import cv2 as cv
import numpy as np

CLOSE_KEY = 'q'
USER_CAMERA = 0
FACE_PATH = 'haarcascade/haarcascade_frontalface_default.xml'
FULL_BODY_PATH = 'haarcascade/haarcascade_fullbody.xml'
UPPER_BODY_PATH = 'haarcascade/haarcascade_upperbody.xml'


class Camera:
    def __init__(self, frame_title='Title'):
        self.frame_title = frame_title
        self.capture = cv.VideoCapture(USER_CAMERA)
        if not self.capture.isOpened():
            raise PermissionError('Cant open camera')
        self.running = True
        self.face_cascade = cv.CascadeClassifier(FACE_PATH)
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    def run(self):
        print('Exit - "q"')
        try:
            while self.running:
                # Capture frame-by-frame
                ret, frame = self.capture.read()
                # if frame is read correctly ret is True
                if not ret:
                    print("TODO: raise error")
                    break

                # self.draw_rectangle(frame)

                self.draw_body_rectangle(frame)

                # Display the resulting frame
                cv.imshow(self.frame_title, frame)

                # fix this - exit
                if cv.waitKey(1) & 0xFF == ord(CLOSE_KEY):
                    self.stop()
        except OSError:
            self.stop()

    def stop(self):
        self.capture.release()
        cv.destroyAllWindows()
        self.running = False

    def draw_rectangle(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    def draw_body_rectangle(self, frame):
        boxes, weights = self.hog.detectMultiScale(frame)

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
