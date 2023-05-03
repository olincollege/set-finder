import pytest
import numpy as np
from Card import Card
from Image import Image

cases = [  # Valid sets
    (
        [
            ("green", "solid", "oval", 1),
            ("red", "liquid", "squiggle", 2),
            ("purple", "gas", "diamond", 3),
        ],
        True,
    ),
    (
        [
            ("red", "liquid", "oval", 2),
            ("green", "gas", "diamond", 2),
            ("purple", "solid", "squiggle", 2),
        ],
        True,
    ),
    (
        [
            ("purple", "liquid", "squiggle", 1),
            ("green", "solid", "diamond", 2),
            ("red", "gas", "oval", 3),
        ],
        True,
    ),
    (
        [
            ("green", "liquid", "diamond", 3),
            ("red", "gas", "oval", 1),
            ("purple", "solid", "squiggle", 2),
        ],
        True,
    ),
    (
        [
            ("red", "solid", "oval", 2),
            ("green", "solid", "diamond", 3),
            ("purple", "solid", "squiggle", 1),
        ],
        True,
    ),
    (
        [
            ("purple", "solid", "squiggle", 1),
            ("green", "gas", "diamond", 1),
            ("red", "liquid", "oval", 1),
        ],
        True,
    ),
    # Invalid sets
    (
        [
            ("green", "solid", "oval", 2),
            ("red", "solid", "squiggle", 3),
            ("green", "solid", "diamond", 1),
        ],
        False,
    ),
    (
        [
            ("purple", "solid", "oval", 3),
            ("red", "solid", "squiggle", 1),
            ("green", "liquid", "diamond", 2),
        ],
        False,
    ),
    (
        [
            ("green", "liquid", "oval", 1),
            ("purple", "gas", "squiggle", 2),
            ("red", "solid", "diamond", 2),
        ],
        False,
    ),
    (
        [
            ("red", "solid", "oval", 2),
            ("green", "liquid", "diamond", 3),
            ("purple", "solid", "squiggle", 3),
        ],
        False,
    ),
    # Edge cases
    (
        [
            ("green", "solid", "oval", 1),
            ("green", "solid", "oval", 2),
            ("green", "solid", "oval", 3),
        ],
        True,
    ),
    (
        [
            ("green", "solid", "oval", 1),
            ("green", "solid", "oval", 1),
            ("green", "solid", "oval", 2),
        ],
        False,
    ),
    (
        [
            ("green", "solid", "oval", 1),
            ("green", "solid", "oval", 2),
            ("green", "solid", "oval", 1),
        ],
        False,
    ),
    (
        [
            ("green", "solid", "oval", 1),
            ("green", "solid", "oval", 2),
            ("green", "solid", "diamond", 3),
        ],
        False,
    ),
]


img = Image(255 * np.ones((2, 2, 3)))


@pytest.mark.parametrize("attributes,result", cases)
def test_is_set(attributes, result):
    cards = []
    for color, fill, shape, number in attributes:
        card = Card(255 * np.ones((2, 2, 3)), 0)
        card._number = number
        card._color = color
        card._fill = fill
        card._shape = shape
        card._create_comparative()
        cards.append(card)
    img.cards = cards
    assert img._is_set(img.cards[0], img.cards[1], img.cards[2]) == result
