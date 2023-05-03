from cv2 import cv2 as cv
from View import View

if __name__ == "__main__":
    view = View(cv.imread("boards/1.jpg"))
    view.show()
