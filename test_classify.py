import os
import pytest
import cv2 as cv
from Card import Card

@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_classify(card):
    number=int(card[0])
    color=fill=shape=""
    if "red" in card:
        color="red"
    if "green" in card:
        color="green"
    if "purple" in card:
        color="purple"
    if "gas" in card:
        fill="gas"
    if "liquid" in card:
        fill="liquid"
    if "solid" in card:
        fill="solid"
    if "diamond" in card:
        shape="diamond"
    if "oval" in card:
        shape="oval"
    if "squiggle" in card:
        shape="squiggle"
    card_obj=Card(cv.imread(f"tests/{card}"),0)
    assert(card_obj._color==color and card_obj._fill==fill and card_obj._shape==shape and card_obj._number==number)
