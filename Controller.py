"""
Module to read webcam input
"""
import cv2
import Image


class Controller:
    """
    Class for reading webcam input

    Attributes:
        cam: An OpenCV camera object representing the first camera connected to 
            the machine.
    """
    def __init__(self):
        pass

    def get_image(self):
        """
        Return a OpenCV array specifying an image at that time
        """
        cam = cv2.VideoCapture(0)
        _,frame = cam.read()
        cam.release()
        return frame 