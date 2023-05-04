"""
Test detecting shape on cards.
"""
import os
import pytest
import cv2 as cv
from card import Card

# pylint: disable=duplicate-code,protected-access
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
