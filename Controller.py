"""
Module to read webcam input
"""
import cv2
import numpy as np
from v4l2py import Device
import matplotlib.pyplot as plt


class Controller:
    """
    Class for reading webcam input

    Attributes:
        cam: The index of the camera to read from. 
    """
    def __init__(self,index = 0):
        self.i = index

    def get_image(self):
        """
        Return a OpenCV array specifying an image at that time
        """
        with Device.from_id(self.i) as cam:
            #Iterator to generator to get single value
            frame = next(cam.__iter__())
        return cv2.imdecode(np.frombuffer(frame.data, dtype=np.uint8),cv2.IMREAD_COLOR)

if __name__ == "__main__":
    # Colors will be not correct because of BGR encoding in OpenCV
    control = Controller(4)
    image = control.get_image()
    plt.figure()
    plt.imshow(image)
    plt.show()