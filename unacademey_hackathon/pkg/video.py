import cv2
import numpy as np


class RecordedVideo:
    def __init__(self, videopath,img_path=None):
        self.cap = cv2.VideoCapture(videopath)
        _, self.first_frame = self.cap.read()
        self.hsv = cv2.cvtColor(self.first_frame, cv2.COLOR_BGR2HSV)
        self.count = 0
        self.lower = np.array([0, 0, 0])
        self.upper = np.array([0, 0, 0])
        self.set_threshhold()
        if img_path:
            self.img = cv2.imread(img_path)
        else:
            self.img = None

    def __del__(self):
        self.cap.release()

    def set_threshhold(self):
        for i in range(0, 15):
            lower_green = np.array([(i * 10), 0, 0])
            upper_green = np.array([(i * 10) + 40, 255, 255])

            mask = cv2.inRange(self.hsv, lower_green, upper_green)
            mask_inv = cv2.bitwise_not(mask)
            _mask_inv = cv2.GaussianBlur(mask_inv, (5, 5), 0)
            fg = cv2.bitwise_and(self.first_frame, self.first_frame, mask=_mask_inv)

            tup = fg[20, 20]
            print(tup)
            if tup[0] in range(0, 30):
                if tup[1] in range(0, 30):
                    if tup[2] in range(0, 30):
                        self.count += 1
                        if self.count == 3:
                            self.lower += lower_green
                            self.upper += upper_green
                            break

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            blank_image = self.img
            #blank_image = np.full(frame.shape,255)
            #frame = self.rotate270(frame)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # lower_green = np.array([40, 0, 0])
            # upper_green = np.array([80, 255, 255])


            mask = cv2.inRange(hsv, self.lower, self.upper)
            mask_inv = cv2.bitwise_not(mask)

            # bg = cv2.bitwise_and(frame, frame, mask=mask)
            fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
            # _fg = cv2.GaussianBlur(fg,(5,5),0)
            fg1= cv2.resize(fg,(400,400))

            blank_image[0:fg1.shape[1], 0:fg1.shape[0]] = fg1

            ret, jpeg = cv2.imencode('.jpg', blank_image)
            #print(fg)
            return jpeg.tobytes()
        else:
            return None

    def rotate270(self,image, angle=270):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

