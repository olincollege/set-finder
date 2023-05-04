"""
Tests that duplicate cards are removed.
"""
import numpy as np
from card import Card
from image import Image

# pylint: disable=duplicate-code,protected-access
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

img = Image(255 * np.ones((2, 2, 3)))


def test_deduplicate():
    cards = []
    for color, fill, shape, number, comparative in attributes:
        card = Card(255 * np.ones((2, 2, 3)), 0)
        card._number = number
        card._color = color
        card._fill = fill
        card._shape = shape
        card._create_comparative()
        if card.comparative != comparative:
            raise ValueError
        cards.append(card)
    img.cards = cards
    img._deduplicate_cards()
    assert len(img.cards) == 11


def test_nothing_deduplicate():
    cards = []
    img.cards = cards
    img._deduplicate_cards()
    assert len(img.cards) == 0
