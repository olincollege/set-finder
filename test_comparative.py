"""
Test the creation of the binary representation of cards.
"""
import pytest
import numpy as np
from Card import Card


attributes = [
    ("green", "solid", "oval", 2, 594),
    ("green", "solid", "oval", 2, 594),
    ("green", "solid", "diamond", 1, 778),
    ("green", "solid", "diamond", 1, 778),
    ("red", "solid", "squiggle", 1, 649),
    ("red", "solid", "squiggle", 1, 649),
    ("purple", "liquid", "diamond", 3, 1316),
    ("purple", "liquid", "diamond", 3, 1316),
    ("red", "solid", "squiggle", 3, 673),
    ("red", "solid", "squiggle", 3, 673),
    ("green", "gas", "diamond", 3, 2338),
    ("green", "gas", "diamond", 3, 2338),
    ("purple", "solid", "oval", 2, 596),
    ("purple", "solid", "oval", 2, 596),
    ("green", "solid", "oval", 1, 586),
    ("green", "solid", "oval", 1, 586),
    ("red", "solid", "oval", 3, 609),
    ("red", "solid", "oval", 3, 609),
    ("purple", "liquid", "squiggle", 3, 1188),
    ("purple", "liquid", "squiggle", 3, 1188),
    ("purple", "gas", "squiggle", 1, 2188),
]
card = Card(255 * np.ones((2, 2, 3)), 0)


@pytest.mark.parametrize("color,fill,shape,number,comparative", attributes)
def test_comparative(number, color, fill, shape, comparative):
    card._number = number
    card._color = color
    card._fill = fill
    card._shape = shape
    card._create_comparative()
    assert comparative == card.comparative
