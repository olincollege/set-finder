from Image import Image
from View import View
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread("boards/1.jpg")
image = Image(img)
image.create_cards()
image.find_sets()
print(f"cards: {len(image.cards)},sets: {len(image.get_cards_set())}")
for set in image.get_cards_set():
    print(set)
view = View(img)
view.draw_set_cards(image.sets)
view.show()
