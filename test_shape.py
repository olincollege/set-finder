import os
import pytest
import cv2 as cv
from Card import Card


@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_shape(card):
    shape = ""
    if "diamond" in card:
        shape = "diamond"
    if "oval" in card:
        shape = "oval"
    if "squiggle" in card:
        shape = "squiggle"
    image = cv.imread(f"tests/{card}")
    card_obj = Card(image, 0)
    assert card_obj._shape == shape
