from View import View
import cv2 as cv

if __name__ == "__main__":
    view = View(cv.imread("boards/1.jpg"))
    view.show()
