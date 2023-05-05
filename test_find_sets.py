"""
Test detecting all sets in a board.
"""
import random
import pytest
import numpy as np
from card import Card
from image import Image

# pylint: disable=protected-access
cases = [  # Valid sets
    (
        {
            ("green", "solid", "oval", 1),
            ("red", "liquid", "squiggle", 2),
            ("purple", "gas", "diamond", 3),
        },
        True,
    ),
    (
        {
            ("red", "liquid", "oval", 2),
            ("green", "gas", "diamond", 2),
            ("purple", "solid", "squiggle", 2),
        },
        True,
    ),
    (
        {
            ("purple", "liquid", "squiggle", 1),
            ("green", "solid", "diamond", 2),
            ("red", "gas", "oval", 3),
        },
        True,
    ),
    (
        {
            ("green", "liquid", "diamond", 3),
            ("red", "gas", "oval", 1),
            ("purple", "solid", "squiggle", 2),
        },
        True,
    ),
    (
        {
            ("red", "solid", "oval", 2),
            ("green", "solid", "diamond", 3),
            ("purple", "solid", "squiggle", 1),
        },
        True,
    ),
    (
        {
            ("purple", "solid", "squiggle", 1),
            ("green", "gas", "diamond", 1),
            ("red", "liquid", "oval", 1),
        },
        True,
    ),
    (
        {
            ("green", "liquid", "diamond", 3),
            ("purple", "liquid", "squiggle", 1),
            ("red", "liquid", "oval", 2),
        },
        True,
    ),
    (
        {
            ("green", "solid", "oval", 1),
            ("purple", "solid", "oval", 3),
            ("red", "solid", "oval", 2),
        },
        True,
    ),
    (
        {
            ("green", "solid", "oval", 1),
            ("purple", "solid", "oval", 3),
            ("red", "solid", "oval", 2),
        },
        True,
    ),
    (
        {
            ("purple", "solid", "squiggle", 1),
            ("purple", "solid", "squiggle", 2),
            ("purple", "solid", "squiggle", 3),
        },
        True,
    ),
    (
        {
            ("green", "solid", "diamond", 1),
            ("purple", "solid", "squiggle", 3),
            ("red", "solid", "oval", 2),
        },
        True,
    ),
    (
        {
            ("green", "solid", "diamond", 3),
            ("purple", "solid", "oval", 3),
            ("red", "solid", "squiggle", 3),
        },
        True,
    ),
    (
        {
            ("green", "gas", "diamond", 2),
            ("green", "liquid", "diamond", 3),
            ("green", "solid", "diamond", 1),
        },
        True,
    ),
    (
        {
            ("green", "solid", "diamond", 2),
            ("purple", "solid", "oval", 3),
            ("red", "solid", "squiggle", 1),
        },
        True,
    ),
    (
        {
            ("green", "liquid", "diamond", 3),
            ("purple", "solid", "squiggle", 3),
            ("red", "gas", "oval", 3),
        },
        True,
    ),
    (
        {
            ("green", "solid", "diamond", 2),
            ("green", "liquid", "diamond", 3),
            ("green", "gas", "diamond", 1),
        },
        True,
    ),
    (
        {
            ("red", "solid", "oval", 2),
            ("red", "liquid", "oval", 1),
            ("red", "gas", "oval", 3),
        },
        True,
    ),
    (
        {
            ("green", "solid", "diamond", 2),
            ("purple", "solid", "squiggle", 2),
            ("red", "solid", "oval", 2),
        },
        True,
    ),
    (
        {
            ("green", "solid", "diamond", 1),
            ("green", "solid", "diamond", 2),
            ("green", "solid", "diamond", 3),
        },
        True,
    ),
    (
        {
            ("green", "solid", "diamond", 1),
            ("purple", "liquid", "squiggle", 1),
            ("red", "gas", "oval", 1),
        },
        True,
    ),
    (
        {
            ("green", "gas", "diamond", 1),
            ("purple", "solid", "squiggle", 3),
            ("red", "liquid", "oval", 2),
        },
        True,
    ),
    (
        {
            ("green", "gas", "diamond", 2),
            ("purple", "solid", "squiggle", 3),
            ("red", "liquid", "oval", 1),
        },
        True,
    ),
    (
        {
            ("green", "solid", "oval", 1),
            ("green", "solid", "oval", 2),
            ("green", "solid", "oval", 3),
        },
        True,
    ),
    (
        {
            ("green", "gas", "diamond", 1),
            ("purple", "solid", "oval", 3),
            ("red", "liquid", "squiggle", 2),
        },
        True,
    ),
]
rand_indices = [
    (random.randint(0, 23), random.randint(0, 23), random.randint(0, 23))
    for _ in range(1000)
]

img = Image(255 * np.ones((2, 2, 3)))


@pytest.mark.parametrize("indices", rand_indices)
def test_find_sets(indices):
    """
    Test that for 3 randomly selected SETs, a board made of those SETs returns
    all valid SETs in addition to those it was built from.

    Args:
        indices: a tuple integers of three SETs to extract card attributes from.
    """
    cards = []
    for index in indices:
        for entry in cases[index]:
            if not isinstance(entry, bool):
                for attributes in entry:
                    card = Card(255 * np.ones((2, 2, 3)), 0)
                    card._number = attributes[3]
                    card._color = attributes[0]
                    card._fill = attributes[1]
                    card._shape = attributes[2]
                    card._create_comparative()
                    cards.append(card)
    img.cards = cards
    img.find_sets()
    for card1, card2, card3 in img.sets:
        case = (
            {
                (card1._color, card1._fill, card1._shape, card1._number),
                (card2._color, card2._fill, card2._shape, card2._number),
                (card3._color, card3._fill, card3._shape, card3._number),
            },
            True,
        )
        if case not in cases:
            assert not case
    assert True
