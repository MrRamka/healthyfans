import cv2 as cv

CLOSE_KEY = 'q'
USER_CAMERA = 0


class Camera:
    def __init__(self, frame_title='Title'):
        self.frame_title = frame_title
        self.capture = cv.VideoCapture(USER_CAMERA)
        if not self.capture.isOpened():
            raise PermissionError('Cant open camera')
        self.running = True

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
                # Display the resulting frame
                cv.imshow(self.frame_title, frame)

                # fix this
                if cv.waitKey(1) == ord(CLOSE_KEY):
                    self.stop()
        except OSError:
            self.stop()

    def stop(self):
        self.capture.release()
        cv.destroyAllWindows()
        self.running = False
