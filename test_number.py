import os
import pytest
from cv2 import cv2 as cv
from Card import Card


@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_number(card):
    number = int(card[0])
    image = cv.imread(f"tests/{card}")
    card_obj = Card(image, 0)
    assert card_obj._number == number
