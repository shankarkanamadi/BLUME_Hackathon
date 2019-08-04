import cv2
class RecordedVideo(object):
    def __init__(self,path=None,img=None):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
        self.img = cv2.imread(img)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        blank_image = self.img
        frame = cv2.resize(frame, (340, 480))
        #print(frame.dtype)
        blank_image[0:frame.shape[0], 0:frame.shape[1]] = frame
        if ret:
            ret, jpeg = cv2.imencode('.jpg', blank_image)
            return jpeg.tobytes()
        else:
            return None
