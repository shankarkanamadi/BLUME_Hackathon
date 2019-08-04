import cv2
import numpy as np

class RecordedVideo:
    def __init__(self, videopath, img=None):
        self.cap = cv2.VideoCapture(videopath)
        _, self.first_frame = self.cap.read()
        self.hsv = cv2.cvtColor(self.first_frame, cv2.COLOR_BGR2HSV)
        self.count = 0
        self.lower = np.array([0, 0, 0])
        self.upper = np.array([0, 0, 0])
        self.set_threshold()
        if videopath == "small.mp4":
            self.rotate = True
        else:
            self.rotate = False
        if img:
            self.img = cv2.imread(img)
        else:
            self.img = None

    def __del__(self):
        self.cap.release()

    def set_threshold(self):

        for i in range(0, 15):
            lower_green = np.array([i * 10, 0, 0])
            upper_green = np.array([(i * 10) + 40, 255, 255])

            mask = cv2.inRange(self.hsv, lower_green, upper_green)
            mask_inv = cv2.bitwise_not(mask)
            _mask_inv = cv2.GaussianBlur(mask_inv, (5, 5), 0)

            bg = cv2.bitwise_and(self.first_frame, self.first_frame, mask=mask)
            fg = cv2.bitwise_and(self.first_frame, self.first_frame, mask=_mask_inv)

            tup = fg[20, self.first_frame.shape[0] - 20]
            print(lower_green)
            if tup[0] in range(0, 30):
                if tup[1] in range(0, 30):
                    if tup[2] in range(0, 30):
                        print(i)
                        print(lower_green)
                        print(upper_green)
                        self.count += 1
                        if self.count == 3:
                            self.lower += lower_green
                            self.upper += upper_green
                            break

    def get_frame(self):

        ret, _frame = self.cap.read()
        if ret:
            blank_image = self.img
            frame = cv2.resize(_frame, (340, 480))
            if self.rotate:
                frame = self.rotate270(frame)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # lower = np.array([40, 0, 0])
            # upper = np.array([70, 255, 255])

            mask = cv2.inRange(hsv, self.lower, self.upper)
            mask_inv = cv2.bitwise_not(mask)

            bg = cv2.bitwise_and(frame, frame, mask=mask)
            fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
            # _fg = cv2.GaussianBlur(fg,(5,5),0)
            blank_image[0:fg.shape[0], 0:fg.shape[1]] = fg

            ret, jpeg = cv2.imencode('.jpg', blank_image)
            return jpeg.tobytes()

        else:
            return None

    def rotate270(self, image, angle=270):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result
