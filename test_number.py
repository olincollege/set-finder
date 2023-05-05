"""
Test detecting number of object on card.
"""
import os
import pytest
import cv2 as cv
from card import Card


# pylint: disable=duplicate-code,protected-access
@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_number(card):
    """
    Test card number detection on a sample card.

    Args:
        card: a string representing the path to the test card image file.
    """
    number = int(card[0])
    image = cv.imread(f"tests/{card}")
    card_obj = Card(image, 0)
    assert card_obj._number == number
