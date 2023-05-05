"""
Test finding fill on test cards.
"""
import os
import pytest
import cv2 as cv
from card import Card

# pylint: disable=duplicate-code,protected-access
@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_fill(card):
    """
    Test card fill detection on a sample card.

    Args:
        card: a string representing the path to the test card image file.
    """
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
