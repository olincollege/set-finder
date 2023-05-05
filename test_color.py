"""
Test finding color on test cards.
"""
import os
import pytest
import cv2 as cv
from card import Card

# pylint: disable=duplicate-code,protected-access
@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_color(card):
    """
    Test card color detection on a sample card.

    Args:
        card: a string representing the path to the test card image file.
    """
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
