import os
import pytest
import cv2 as cv
from Card import Card


@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_color(card):
    color = ""
    if "red" in card:
        color = "red"
    if "green" in card:
        color = "green"
    if "purple" in card:
        color = "purple"
    image = cv.imread(f"tests/{card}")
    card_obj = Card(image, 0)
    assert card_obj._color == color
