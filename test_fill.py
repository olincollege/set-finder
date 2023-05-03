import os
import pytest
from cv2 import cv2 as cv
from Card import Card


@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_fill(card):
    fill = ""
    if "gas" in card:
        fill = "gas"
    if "liquid" in card:
        fill = "liquid"
    if "solid" in card:
        fill = "solid"
    image = cv.imread(f"tests/{card}")
    card_obj = Card(image, 0)
    assert card_obj._fill == fill
