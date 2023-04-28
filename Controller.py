"""
Module to read webcam input
"""
import cv2
import Image


class Controller:
    """
    Class for reading webcam input

    Attributes:
        cam: The index of the camera to read from. 
    """
    def __init__(self,index):
        self.i = index

    def get_image(self):
        """
        Return a OpenCV array specifying an image at that time
        """
        cam = cv2.VideoCapture(self.i)
        _,frame = cam.read()
        cam.release()
        return frame 