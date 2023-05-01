import os
import pytest
import cv2 as cv
from Card import Card

@pytest.mark.parametrize("card", os.listdir("tests/"))
def test_classify(card):
    errors=""
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
    image=cv.imread(f"tests/{card}")
    card_obj=Card(image,0)
    if card_obj._color!=color:
        errors+=f"color: {card_obj._color} "
    if card_obj._number!=number:
        errors+=f"number: {card_obj._number} "
    if card_obj._fill!=fill:
        errors+=f"fill: {card_obj._fill} "
    if card_obj._shape!=shape:
        errors+=f"shape: {card_obj._shape} "
    if errors:
        errors=f"res: {image.shape[0]*image.shape[1]} "+errors
    assert not errors


# def test_classify():
#     log = {}
#     sorted_log = ""
#     for card in os.listdir("tests/"):
#         errors = ""
#         number = int(card[0])
#         color = fill = shape = ""
#         if "red" in card:
#             color = "red"
#         if "green" in card:
#             color = "green"
#         if "purple" in card:
#             color = "purple"
#         if "gas" in card:
#             fill = "gas"
#         if "liquid" in card:
#             fill = "liquid"
#         if "solid" in card:
#             fill = "solid"
#         if "diamond" in card:
#             shape = "diamond"
#         if "oval" in card:
#             shape = "oval"
#         if "squiggle" in card:
#             shape = "squiggle"
#         image = cv.imread(f"tests/{card}")
#         card_obj = Card(image, 0)
#         if card_obj._color != color:
#             errors += f"color: {card_obj._color} "
#         if card_obj._number != number:
#             errors += f"number: {card_obj._number} "
#         if card_obj._fill != fill:
#             errors += f"fill: {card_obj._fill} "
#         if card_obj._shape != shape:
#             errors += f"shape: {card_obj._shape} "
#         if errors:
#             log[image.shape[0] * image.shape[1]] = card + " " + errors + "\n"
#     if log:
#         keys = list(log.keys())
#         keys.sort()
#         keys.reverse()
#         message = "".join((f"{i}: {log[i]}" for i in keys))
#         sorted_log = f"{len(keys)} errors\n{message}"
#     print(sorted_log)
#     assert not sorted_log
