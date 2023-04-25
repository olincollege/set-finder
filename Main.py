from Image import Image
from View import View
import cv2 as cv
import matplotlib.pyplot as plt

if __name__ == "__main__":
    img = cv.imread("boards/1.jpg")
    image = Image(img)
    image.create_cards()
    for card in image.cards:
        fig = plt.figure()
        plt.imshow(card._im)
    # view=View(img)
    # view.draw_set_cards()
    # view.show()
